#!/usr/bin/env python3
"""编译 v4 plan，装配本地输入并提交 Bohrium job。

用法:agent 先按 schema 写好 pipeline.json(inputs + steps),再:
    python3 submit_pipeline.py --pipeline pipeline.json [--dataset-path /bohr/<ds>/v1]
本脚本会:校验 authoring JSON、暂存本地输入、写 execution_plan.json/job.json、bohr 提交。
contract-v4 执行器(td_cli/execution_plan/run.sh)已烤在镜像 /opt/topdown,不随包上传。

env(由 openclaw 注入,先 source /bohr-workspace/.bohr_env):
  BOHR_ACCESS_KEY、PROJECT_ID(无默认,必须由当前用户/平台提供)、IMAGE_ADDRESS、MACHINE_TYPE
输出: JSON {ok, jobId, status, pollAfterMs, nextTool}
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import validate_pipeline
import compile_execution_plan

# 镜像地址单一源:skill 根的 image.txt(版本迭代只改这一处)。env IMAGE_ADDRESS 可覆盖。
_IMAGE_FILE = Path(__file__).resolve().parent.parent / "image.txt"
DEFAULT_IMAGE = _IMAGE_FILE.read_text().strip() if _IMAGE_FILE.exists() else ""
# PROJECT_ID 无默认:项目相关,必须由 env/configField 注入(同 ACCESS_KEY),否则误投错项目。

# 数据集挂载根:/bohr/<数据集名>/v<版本>。
_BOHR_MOUNT_RE = re.compile(r"^(/bohr/[^/]+/v[0-9]+)(?:/.*)?$")


def _derive_dataset_paths(inputs: dict, explicit: list):
    """从 inputs 里的 /bohr 文件路径自动推导 dataset_path 挂载根。"""
    mounts = list(dict.fromkeys(explicit))
    errors = []
    for key, value in (inputs or {}).items():
        if not value or not str(value).startswith("/bohr/"):
            continue
        match = _BOHR_MOUNT_RE.match(str(value))
        if not match:
            errors.append({
                "field": f"inputs.{key}",
                "value": value,
                "problem": "这是 /bohr 路径但推不出数据集挂载根"
                           "(应形如 /bohr/<数据集名>/v1/<文件>)",
                "fix": "用 dataset_manager.py files --id <ID> 获取确切 mount_path,"
                       "不要猜路径。",
            })
            continue
        root = match.group(1)
        if root not in mounts:
            mounts.append(root)
    return mounts, errors


# bohr CLI 只认 ACCESS_KEY，平台只保证注入 BOHR_ACCESS_KEY。
_AUTH_MARKERS = (
    "cannot unmarshal object into Go struct field RespErr.error",
    "AccessKey Invalid",
    "Invalid AccessKey",
    "AccessKey is required",
    "code:2000",
    "Unauthorized",
)


def _child_env() -> dict:
    env = os.environ.copy()
    ak = env.get("BOHR_ACCESS_KEY") or env.get("ACCESS_KEY")
    if ak:
        env["ACCESS_KEY"] = ak
        env["BOHR_ACCESS_KEY"] = ak
    return env


def _looks_unauthenticated(text: str) -> bool:
    return any(marker in (text or "") for marker in _AUTH_MARKERS)


def _submit(workdir: str) -> str:
    # 显式桥接 key，不依赖调用方是否 source .bohr_env。
    p = subprocess.run(["bohr", "job", "submit", "-i", "job.json", "-p", "./"],
                       cwd=workdir, capture_output=True, text=True, env=_child_env())
    out = p.stdout + p.stderr
    m = re.search(r"JobId:\s*(\d+)", out)
    if not m:
        if _looks_unauthenticated(out):
            sys.exit(
                "submit 失败:平台注入的密钥已失效(终局错误,重试没用)。"
                "这是平台侧的密钥注入问题;如实告知用户后停止本轮。"
                "不要向用户索取 key,不要运行 bohr auth login。\n原始输出:\n"
                + out[-800:]
            )
        sys.exit("submit 失败:\n" + out[-800:])
    return m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pipeline", required=True, help="agent 写好的 pipeline.json(inputs+steps)")
    ap.add_argument("--dataset-path", action="append", default=[], help="/bohr/<ds>/v1,可多次")
    ap.add_argument("--job-name", default="topdown")
    ap.add_argument("--workdir", default=None,
                    help="打包目录(默认=pipeline.json 所在目录;每任务用独立子目录如 "
                         "td-runs/<名>/,勿直接放 /bohr-workspace 根)")
    a = ap.parse_args()

    pipeline = json.loads(Path(a.pipeline).read_text())

    # 先本地校验 pipeline(错则停,不浪费 job;错误带 step/tool/field/fix 供 agent 自纠),
    # 再查提交所需 env(PROJECT_ID 无默认,须注入)。
    vres = validate_pipeline.validate_with_fs(
        pipeline, base=str(Path(a.pipeline).resolve().parent))
    if not vres["ok"]:
        print(json.dumps({"ok": False, "stage": "validate", "errors": vres["errors"]},
                         ensure_ascii=False))
        return 1

    project = os.environ.get("PROJECT_ID")
    if not project:
        sys.exit("missing env: PROJECT_ID(须经 .bohr_env/configField 注入,无默认值)")
    image = os.environ.get("IMAGE_ADDRESS", DEFAULT_IMAGE)
    if not image:
        sys.exit(
            "image_address 为空:skill 根目录的 image.txt 找不到,env IMAGE_ADDRESS 也没设。"
            "不要凭记忆编造 registry 地址或镜像 tag。"
        )
    machine = os.environ.get("MACHINE_TYPE", "c16_m32_cpu")

    # 就地打包:默认用 pipeline.json 所在目录(per-task 自包含、并发安全、不散落根目录)。
    # 不 rmtree(会删掉 pipeline.json 自己);约定每任务一个独立子目录,重提则覆盖同名打包物。
    wd = Path(a.workdir).resolve() if a.workdir else Path(a.pipeline).resolve().parent
    if wd == Path("/bohr-workspace"):
        sys.exit("pipeline.json 须放进专属子目录(如 /bohr-workspace/td-runs/<任务名>/pipeline.json),"
                 "勿直接放 /bohr-workspace 根——否则打包会把整个工作空间上传。")
    wd.mkdir(parents=True, exist_ok=True)

    # 本地输入拷进上传包并改为包内相对名;/bohr 挂载路径保留
    pdir = Path(a.pipeline).resolve().parent
    inputs = pipeline.get("inputs") or {}
    for k, v in list(inputs.items()):
        if v and not str(v).startswith("/bohr/"):
            src = Path(v)
            if not src.is_absolute():
                src = pdir / src
            src = src.resolve()
            dst = wd / src.name
            if src != dst.resolve():   # 就地打包时输入可能已在 wd,避免 copy 自己到自己
                shutil.copy(src, dst)
            inputs[k] = src.name
    pipeline["inputs"] = inputs

    mounts, dataset_errors = _derive_dataset_paths(inputs, a.dataset_path)
    if dataset_errors:
        print(json.dumps({
            "ok": False,
            "stage": "dataset_path",
            "errors": dataset_errors,
        }, ensure_ascii=False))
        return 1

    (wd / "pipeline.json").write_text(json.dumps(pipeline, ensure_ascii=False, indent=2))
    execution_plan = compile_execution_plan.compile_topdown(pipeline)
    (wd / "execution_plan.json").write_text(
        json.dumps(execution_plan, ensure_ascii=False, indent=2)
    )

    job = {
        "job_name": a.job_name,
        # 执行器在镜像 /opt/topdown;run.sh 已设 PYTHONDONTWRITEBYTECODE+ -B,不积陈旧 .pyc。
        "command": "bash /opt/topdown/run.sh --config execution_plan.json",
        "log_file": "out/run.log",
        "backward_files": ["out/"],
        "project_id": int(project),
        "machine_type": machine,
        "job_type": "container",
        "disk_size": 100,
        "max_run_time": 120,
        "image_address": image,
    }
    if mounts:
        job["dataset_path"] = mounts
    (wd / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=2))

    jid = _submit(str(wd))
    # per-task 自包含:wd 即任务目录(含 pipeline.json + 输入 + 待 collect 回收的 result/),不清理。
    print(json.dumps({
        "ok": True, "jobId": jid, "status": "scheduling",
        "pollAfterMs": 20000, "nextTool": "poll_job.py",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
