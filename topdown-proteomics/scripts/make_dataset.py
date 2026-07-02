#!/usr/bin/env python3
"""把 sandbox 里的大输入(GB 级 .raw)创建为 Bohrium Dataset,返回挂载路径。

大文件走 dataset 挂载,不进 -p 上传包 / LLM 上下文。
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import requests

DS_API = "https://open.bohrium.com/openapi"


def _iter_leaves(host, token, prefix, depth=0):
    """递归列出 prefix 下所有叶子文件 -> [(path, size)](tiefblue iterate 单层,须下钻 upload/ 等层)。"""
    out, nxt = [], ""
    while True:
        try:
            data = requests.post(
                f"{host}/api/iterate",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"maxObjects": 200, "prefix": prefix, "nextToken": nxt}, timeout=20,
            ).json().get("data", {})
        except Exception:
            return out
        for o in (data.get("objects") or []):
            p = o.get("path", "")
            if p.rstrip("/") == prefix.rstrip("/"):
                continue
            if o.get("isDir") or p.endswith("/"):
                if depth < 20:
                    out += _iter_leaves(host, token, p if p.endswith("/") else p + "/", depth + 1)
            else:
                out.append((p, o.get("size", 0)))
        nxt = data.get("nextToken", "")
        if not data.get("hasNext") or not nxt:
            break
    return out


def _find_existing(project, ak, basename, size):
    """扫项目已有数据集,若某个含 basename 且 size 一致的文件,返回 (mount, 内部挂载路径);否则 None。"""
    H = {"Authorization": f"Bearer {ak}"}
    try:
        items = requests.get(f"{DS_API}/v2/ds/?projectId={project}&page=1&pageSize=50",
                             headers=H, timeout=20).json().get("data", {}).get("items", [])
    except Exception:
        return None
    for it in items:
        did, mount = it.get("id"), it.get("path", "")
        try:
            vr = requests.get(f"{DS_API}/v2/ds/{did}/version", headers=H, timeout=20).json().get("data", [])
        except Exception:
            continue
        vers = vr if isinstance(vr, list) else vr.get("items", [])
        if not vers:
            continue
        tb = (vers[0].get("tiefbluePath") or "").rstrip("/")
        if not tb:
            continue
        try:
            tk = requests.get(f"{DS_API}/v2/ds/input/token", headers=H,
                             params={"projectId": project, "path": tb}, timeout=20).json().get("data", {})
        except Exception:
            continue
        token, host = tk.get("token"), tk.get("host") or "https://tiefblue.dp.tech"
        if not token:
            continue
        for p, sz in _iter_leaves(host, token, tb + "/"):
            if p.rsplit("/", 1)[-1] == basename and sz == size:
                return mount, f"{mount}/{p[len(tb) + 1:]}"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="sandbox 里的大文件路径")
    ap.add_argument("--name", required=True, help="数据集名(也作 -p 前缀)")
    ap.add_argument("--force", action="store_true", help="跳过查重,强制新建(默认先查重复用)")
    a = ap.parse_args()
    project = os.environ.get("PROJECT_ID")
    if not project:
        sys.exit("missing env: PROJECT_ID")

    src = Path(a.file)
    if not src.exists():
        sys.exit(f"file not found: {src}")
    # fasta 绝不做成 dataset:dataset 是只读挂载,toppic/mspathfindert 要在 fasta 旁建
    # .fasta_idx 索引,只读会失败(LOG ERROR: ...fasta_idx could not be created)。
    # fasta 小,走本地路径随 -p 上传(可写)。dataset 只给大谱图(.raw/.mzML)。
    if src.suffix.lower() in (".fasta", ".fa", ".faa"):
        sys.exit("fasta 不要做成 dataset(只读挂载,搜索工具建索引会失败)。"
                 "fasta 直接在 pipeline.json 用本地路径(submit 自动拷进 -p 可写区);"
                 "dataset 只给大谱图 .raw/.mzML。")

    # ★ 查重(硬要求):建前扫项目已有数据集,若已有同名+同大小文件,直接复用,绝不重复创建。
    _ak = os.environ.get("ACCESS_KEY") or os.environ.get("BOHR_ACCESS_KEY", "")
    if not a.force and _ak:
        hit = _find_existing(project, _ak, src.name, src.stat().st_size)
        if hit:
            mount, spectrum_mount = hit
            print(json.dumps({
                "ok": True, "reused": True, "mount": mount, "spectrum_mount": spectrum_mount,
                "hint": "已存在含相同文件(名+大小)的数据集,直接复用,未重复创建。"
                        "inputs.spectrum 填 %s;submit 带 --dataset-path %s(如确需新建用 --force)"
                        % (spectrum_mount, mount),
            }, ensure_ascii=False))
            return

    # bohr dataset create -n <name> ... -l <目录>(目录级上传,支持断点续传)
    # 直接调 bohr(ACCESS_KEY 经 env 继承——调用前须 source .bohr_env)
    # 喂 stdin:bohr 可能弹 "Detected cached files, resume? (y/n)",无 stdin 会 panic
    p = subprocess.run(
        ["bohr", "dataset", "create", "-n", a.name, "-p", a.name, "-i", project, "-l", str(src.parent)],
        input="y\n", capture_output=True, text=True,
    )
    raw = p.stdout + p.stderr

    # bohr CLI 上传失败/超时会 panic(非优雅报错);明确提示而非后面查不到时困惑
    if "Upload Failed" in raw or "panic:" in raw or p.returncode != 0:
        tail = raw[-400:]
        sys.exit("dataset 上传失败(网络慢/文件过大致 tiefblue 超时,bohr CLI 会 panic)。"
                 "Shrimp 内网通常正常;或重试(支持断点续传)。原始: " + tail)

    # ★ 关键:Bohrium 给数据集名加随机后缀(如 -hvx3),真实挂载路径必须从 API 查;
    #   不能假设 /bohr/<name>/v1,否则 job 报 "Dataset ... has been deleted"。
    ak = os.environ.get("ACCESS_KEY") or os.environ.get("BOHR_ACCESS_KEY", "")
    url = f"https://openapi.dp.tech/openapi/v1/ds/?projectId={project}&page=1&pageSize=50"
    req = urllib.request.Request(url, headers={"accessKey": ak})
    items = json.load(urllib.request.urlopen(req, timeout=20)).get("data", {}).get("items", [])
    match = next((i for i in items if i.get("title") == a.name), None)
    if not match:
        sys.exit(f"dataset '{a.name}' 创建后未在列表中找到(create 输出: {raw[-200:]})")
    mount = match["path"]          # /bohr/<name>-<随机>/v1
    # ★ bohr dataset create -l <dir> 会把 <dir> 的 basename 作为一层嵌进挂载路径
    #   (实测: -l /x/upload → 文件在 v1/upload/file,不在 v1/file)。故返回路径必须带这层。
    spectrum_mount = f"{mount}/{src.parent.name}/{src.name}"
    print(json.dumps({
        "ok": True, "dataset": a.name, "dataset_id": match.get("id"), "mount": mount,
        "spectrum_mount": spectrum_mount,
        "hint": "pipeline.json 的 inputs.spectrum 填 %s;submit 带 --dataset-path %s" % (spectrum_mount, mount),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
