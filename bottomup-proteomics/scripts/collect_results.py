#!/usr/bin/env python3
"""bohr job download 拉回 job 的 out/,解析 summary.json,报指标 + 本地交付物路径。输出 JSON。

job 节点隔离、写不回共享盘,故结果只能 download。小 summary + 终端产物默认下载;
大中间产物(mzML)须 pipeline.json `collect` 指定后才在 out/ 里、随之下载。
"""
import argparse
import json
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path

EXPECTED_CONTRACT_VERSION = 2   # 与 bu_cli.CONTRACT_VERSION 对齐

# ── 交付层白名单 ─────────────────────────────────────────────
# 只有结果表格是交付物。中间产物(.pin/.pepXML/.prot.xml)、参数文件、各步日志
# 一律不外发:对用户没用,且带后端实现信息。它们仍留在 out/ 供内部诊断。
USER_FACING_EXACT = {
    "psm.tsv", "peptide.tsv", "protein.tsv", "ion.tsv", "modified_peptide.tsv",
    "report.tsv", "report.pr_matrix.tsv", "report.pg_matrix.tsv", "report.stats.tsv",
}
USER_FACING_PREFIX = ("combined_", "abundance_", "ratio_")
# 文件名里带后端工具名的一律排除(如 modmasses_ionquant.txt、*_stdout.log、fragger.params)
DENY_SUBSTR = ("fragger", "ionquant", "philosopher", "diann", "dia-nn", "percolator",
               "peptideprophet", "ptmprophet", "ptmshepherd", "tmtintegrator",
               "crystalc", "msbooster", "stdout", "stderr")


def _is_user_facing(f: Path) -> bool:
    low = f.name.lower()
    if any(t in low for t in DENY_SUBSTR):
        return False
    if f.suffix.lower() != ".tsv":
        return False
    return f.name in USER_FACING_EXACT or low.startswith(USER_FACING_PREFIX)


def _n_cols(f: Path) -> int:
    try:
        with open(f, errors="replace") as fh:
            return len(fh.readline().rstrip("\n").split("\t"))
    except Exception:
        return 0


def _curate(out_dir: Path, dest: Path) -> list:
    """把面向用户的结果表拷进 dest/,返回其路径。out_dir 原样保留(内部诊断用)。

    同名表可能在多个步目录里各有一份(如 report/psm.tsv 37 列,定量步又补出 42 列的超集)。
    只交付信息最全的那一份 —— 交两份内容不同的 psm.tsv 给用户,纯属制造困惑。
    """
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    best: dict = {}
    for f in sorted(out_dir.rglob("*")):
        if not (f.is_file() and _is_user_facing(f)):
            continue
        cur = best.get(f.name)
        if cur is None or _n_cols(f) > _n_cols(cur):
            best[f.name] = f
    kept = []
    for name, f in sorted(best.items()):
        shutil.copy2(f, dest / name)
        kept.append(str(dest / name))
    return kept


def _zip_dir(src: Path, zpath: Path) -> None:
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(src))


def _count_data_rows(f: Path) -> int:
    try:
        with open(f, errors="replace") as fh:
            n = sum(1 for _ in fh)
        return max(0, n - 1)   # 减表头
    except Exception:
        return 0


def _metrics_from_out(out_dir: Path) -> dict:
    """从下载产物实算 BU 指标(psm/peptide/protein 行数 + diann report),与 bu_cli._bu_metrics 一致;
    放 collect 兜底,旧镜像 summary 的 metrics 偏薄时也能得指标。"""
    m: dict = {}
    for name, key in (("psm.tsv", "psm_rows"), ("peptide.tsv", "peptide_rows"),
                      ("protein.tsv", "protein_rows")):
        f = next(iter(out_dir.rglob(name)), None)
        if f:
            m[key] = _count_data_rows(f)
    rep = next(iter(out_dir.rglob("report.tsv")), None)
    if rep:
        m["diann_precursor_rows"] = _count_data_rows(rep)
    return m


def _bohr_download(job_id: str, dl_dir: str) -> str:
    Path(dl_dir).mkdir(parents=True, exist_ok=True)
    # bohr 直接跑(ACCESS_KEY 经 env 继承——调用前须 source .bohr_env);返回输出供出错时诊断
    p = subprocess.run(["bohr", "job", "download", "-j", job_id, "-o", dl_dir],
                       capture_output=True, text=True)
    return (p.stdout or "") + (p.stderr or "")


def _has_result(dl: Path) -> bool:
    return any(dl.rglob("*.zip")) or any(dl.rglob("summary.json"))


def collect(job_id: str, dl_dir: str, expected_version: int = EXPECTED_CONTRACT_VERSION,
            downloader=_bohr_download) -> dict:
    dl = Path(dl_dir)
    # 幂等关键:download 前清空目录。否则重复 collect 时,rglob 会把上次保留的 <jobId>.zip
    # 重新解压污染顶层、或锚到上次 out/summary.json 跳过扁平化 → 结构错乱(非幂等)。
    # 结果在 Bohrium 结果库,清掉本地副本可随时重下,安全。
    if dl.exists():
        shutil.rmtree(dl)
    dl.mkdir(parents=True, exist_ok=True)
    # 下载 + 校验产出:bohr download 偶发空产出(只建空 jobId 目录,无 out.zip)。
    # 校验没拿到结果就重试一次;仍失败则报 bohr 真实输出,而非笼统"没找到 summary"——
    # 否则 agent 会被迫手动 download/解压,搞出 dl/、out/out/ 等混乱。
    log = downloader(job_id, dl_dir) or ""
    if not _has_result(dl):
        log += "\n--- 重试 download ---\n" + (downloader(job_id, dl_dir) or "")
    if not _has_result(dl):
        return {"ok": False, "jobId": job_id,
                "error": f"bohr job download 未产出结果(out.zip/summary.json),重试仍失败。"
                         f"bohr 输出: {log[-500:]}"}
    # bohr job download 把结果打成 out.zip:解压用于读取/扁平化(此刻 dl 只有本次产物,rglob 安全)。
    for z in dl.rglob("*.zip"):
        try:
            zipfile.ZipFile(z).extractall(z.parent)
        except Exception:
            pass
    summ = next(iter(dl.rglob("summary.json")), None)
    if not summ:
        return {"ok": False, "jobId": job_id, "error": f"download 后未找到 summary.json: {dl_dir}"}
    # 扁平化:bohr download 多套一层 <jobId>/。把 out/ 提到 dl/out;再无条件把 zip 归位到
    # dl/<jobId>.zip 保留(供下载)、清掉残留中间层。最终:dl/out/(可读)+ dl/<jobId>.zip。
    src_out = summ.parent                    # 形如 dl/<jobId>/out
    final_out = dl / "out"
    if src_out.resolve() != final_out.resolve():
        if final_out.exists():
            shutil.rmtree(final_out)
        shutil.move(str(src_out), str(final_out))
        summ = final_out / "summary.json"
    # 清场:down 下来的整包 zip 与中间层目录一律删除。那个 zip 是**整个作业目录**
    # (各步日志、参数文件、引擎中间格式),交给用户等于把后端实现全抖出去;
    # 结果表另行裁剪成 results/ 交付,out/ 留本地供失败诊断。
    for z in list(dl.rglob("*.zip")):
        z.unlink()
    for child in dl.iterdir():
        if child.is_dir() and child.name != "out":
            shutil.rmtree(child, ignore_errors=True)
    summary = json.loads(summ.read_text())
    out_dir = summ.parent
    # 交付层裁剪:只有结果表进 results/,再打成 <jobId>-results.zip 供用户下载。
    results_dir = dl / "results"
    paths = _curate(out_dir, results_dir)
    archive = None
    if paths:
        archive = dl / f"{job_id}-results.zip"
        _zip_dir(results_dir, archive)
    warn = ""
    if summary.get("contract_version", 0) < expected_version:
        warn = "镜像执行器版本偏旧(contract_version < 期望),建议重建镜像 v2"
    # 指标:以下载产物实算为准(覆盖镜像 summary 里可能偏薄的 metrics),旧镜像也得富指标
    metrics = dict(summary.get("metrics") or {})
    metrics.update(_metrics_from_out(out_dir))
    res = {
        "ok": True, "jobId": job_id, "status": summary.get("status"),
        "steps": summary.get("steps"), "failed_step": summary.get("failed_step"),
        "metrics": metrics, "pipeline": summary.get("pipeline"),
        "deliverable_paths": paths,                     # 已裁剪:只含结果表,可交付
        "results_dir": str(results_dir),                # 可交付
        "archive": str(archive) if archive else None,   # 已裁剪的结果 zip,可交付
        "result_dir": str(out_dir),                     # ⚠️ 内部诊断用
        "internal_only": "result_dir 与 pipeline 含中间产物/日志/后端工具名,仅供内部诊断:"
                         "不要把该目录、其中文件路径或工具名交给用户。交付只用 "
                         "deliverable_paths / results_dir / archive。",
        "version_warning": warn,
    }
    # 失败时直接surface真错:summary.error(执行器已含日志尾)+ failed_logs 尾部,
    # 免得 agent 还得手动下日志找原因。
    if summary.get("status") == "failed":
        res["error"] = summary.get("error")
        if summary.get("missing_inputs"):
            res["missing_inputs"] = summary["missing_inputs"]
        logs = sorted((out_dir / "failed_logs").glob("*.log")) if (out_dir / "failed_logs").is_dir() else []
        if logs:
            tail = "\n".join(logs[-1].read_text(errors="replace").splitlines()[-15:]).strip()
            res["failed_log_tail"] = tail
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job-id", required=True)
    ap.add_argument("--out", "--outdir", "--output-dir", dest="out", default=None,
                    help="下载目录(默认 /bohr-workspace/bu-result/<jobId>;--outdir/--output-dir 同义)")
    a = ap.parse_args()
    dl = a.out or f"/bohr-workspace/bu-result/{a.job_id}"
    res = collect(a.job_id, dl)

    # 失败必须体现在退出码上。以前无论收没收到结果都 exit 0,agent 用
    # `collect_results.py && echo ok` 会看到 ok,把"什么都没拿到"当成功。
    if not res.get("ok"):
        res.setdefault("next", "先 `poll_job.py --job-id %s` 确认作业是否真的到了终态;"
                               "done=false 就结束本轮、等作业跑完再收。" % a.job_id)
        res.setdefault("forbidden", "不要手动 `bohr job download` 再自己解压 —— 会产生 dl/、"
                                    "out/out/ 之类的错乱目录,后续 collect 全部失灵。")
        print(json.dumps(res, ensure_ascii=False))
        sys.exit(3)

    # 作业本身失败 ≠ 收集失败。给一个显式判决字段,免得 agent 把 ok:true 读成"跑成功了"。
    if (res.get("summary") or {}).get("status") == "failed":
        res["verdict"] = "JOB_FAILED"
        res["next"] = "作业是失败终态。读上面的失败日志、如实向用户说明真实报错原因。"
        res["forbidden"] = "不要下结论说'不支持/架构限制';失败原因以真实报错为准。"
        print(json.dumps(res, ensure_ascii=False))
        sys.exit(4)

    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
