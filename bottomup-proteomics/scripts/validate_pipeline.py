#!/usr/bin/env python3
"""BU pipeline.json 本地校验(纯 stdlib;submit 内部也会再校验=闸门)。

校验:结构(工具/边/fasta位置/文件大小)+ 顶层字段名 + 参数(名/类型/范围/枚举/必填)。
参数 schema 从 specs.py 的 ParamDef 导出(param_schema.json);模板步骤映射(template_tools.json)
让模板入口的 overrides/必填检查也能精确到工具。改 specs/templates 后重新导出这两个 json。
"""
from __future__ import annotations
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tool_names          # noqa: E402  公开名 ⇄ 内部名(与镜像同一套映射)

_BU_TOOLS = {
    "msconvert", "msfragger-closed", "crystalc", "percolator",
    "percolator-to-pepxml", "philosopher-database", "peptideprophet",
    "ptmprophet", "philosopher-report", "ionquant", "ptmshepherd",
    "tmtintegrator", "diann", "diaumpire", "diatracer", "easypqp",
    "opair", "msbooster", "iprophet", "proteinprophet",
}
_FASTA_EXTS = (".fas", ".fasta", ".fa")
_MAX_LOCAL_MB = 100
_TOP_KEYS = {"steps", "edges", "raw_files", "fasta_path", "annotation_path",
             "template_id", "overrides", "output_dir", "collect", "dataset_path"}
# 执行器自动注入的必填参数:注入源存在则豁免必填检查
_INJECTED_REQUIRED = {"database_path", "annotation_file"}

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    """校验用的 schema。读不到就必须硬失败 —— 绝不能返回 {} 静默放行。

    返回 {} 会让 _check_param_dict / _check_required / template_id 检查全部退化成 no-op,
    validate 报 ok:true,submit 照常提交一个参数全错的作业,烧完整个 job 才暴露。
    闸门失效时必须有声音。
    """
    try:
        with open(os.path.join(_HERE, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        sys.exit(json.dumps({"ok": False, "stage": "validate",
            "error": f"校验 schema 缺失或损坏: scripts/{name} ({e})",
            "next": "skill 安装不完整。重新拉取 skill 目录,确认 scripts/param_schema.json "
                    "与 scripts/template_tools.json 都在。",
            "forbidden": "不要跳过校验直接 submit_pipeline.py(会花钱跑一个参数没校验过的作业);"
                         "也不要凭记忆手写一个 schema 文件顶替。"}, ensure_ascii=False))


_PARAM_SCHEMA = _load("param_schema.json")     # {tool: {param: {type,required?,enum?,min?,max?,xmin?}}}
_TPL_TOOLS = _load("template_tools.json")       # {template_id: {step_id: tool}}
_ALL_PARAMS = (set().union(*[set(v) for v in _PARAM_SCHEMA.values()])
               if _PARAM_SCHEMA else set())


def _type_ok(val, t) -> bool:
    if t == "bool":
        return isinstance(val, bool)
    if t == "int":
        return isinstance(val, int) and not isinstance(val, bool)
    if t == "float":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if t in ("str", "enum"):
        return isinstance(val, str)
    if t == "str_list":
        return isinstance(val, list)
    return True


def _check_value(where: str, name: str, val, spec: dict, errs: list) -> None:
    t = spec.get("type")
    if not _type_ok(val, t):
        errs.append(f"{where} 参数 '{name}' 类型应为 {t},实际 {type(val).__name__} {val!r}")
        return
    if spec.get("enum") and val not in spec["enum"]:
        errs.append(f"{where} 参数 '{name}'={val!r} 不在允许值 {spec['enum']}")
    if t in ("int", "float") and isinstance(val, (int, float)) and not isinstance(val, bool):
        mn, mx = spec.get("min"), spec.get("max")
        if mn is not None and (val <= mn if spec.get("xmin") else val < mn):
            errs.append(f"{where} 参数 '{name}'={val} {'≤' if spec.get('xmin') else '<'} 下限 {mn}")
        if mx is not None and val > mx:
            errs.append(f"{where} 参数 '{name}'={val} > 上限 {mx}")


def _check_param_dict(tool: str, params: dict, errs: list, where: str) -> None:
    """校验一组参数:名(+建议)/ 类型 / 范围 / 枚举。"""
    schema = _PARAM_SCHEMA.get(tool)
    if not schema:
        return
    for name, val in (params or {}).items():
        spec = schema.get(name)
        if spec is None:
            sug = difflib.get_close_matches(name, list(schema), n=2, cutoff=0.4)
            hint = (f"(应为 {' / '.join(sug)} ?)" if sug
                    else f"(合法参数:{', '.join(list(schema)[:10])}…)")
            errs.append(f"{where} 未知参数名 '{name}' {hint}")
        else:
            _check_value(where, name, val, spec, errs)


def _check_overrides(cfg: dict, steps: list, errs: list) -> None:
    """overrides 参数名/值校验。显式 DAG 用 step→tool;模板入口用 template_tools 映射精确到工具;
    都拿不到则对全工具并集只查名(拦完全不存在的)。"""
    tool_by_step = {s.get("step_id"): s.get("tool") for s in steps}
    tpl_map = _TPL_TOOLS.get(cfg.get("template_id"), {})
    for sid, ov in (cfg.get("overrides") or {}).items():
        tool = tool_by_step.get(sid) or tpl_map.get(sid)
        if tool:
            _check_param_dict(tool, ov, errs, f"overrides[{sid}]({tool})")
        else:
            for name in (ov or {}):
                if name not in _ALL_PARAMS:
                    sug = difflib.get_close_matches(name, sorted(_ALL_PARAMS), n=2, cutoff=0.4)
                    errs.append(f"overrides[{sid}] 未知参数名 '{name}'"
                                + (f" (应为 {' / '.join(sug)} ?)" if sug else ""))


def _check_required(cfg: dict, steps: list, errs: list) -> None:
    """必填参数缺失;执行器可注入的(database_path←db步/fasta_path、annotation_file←annotation_path)豁免。"""
    has_db = any(s.get("tool") == "philosopher-database" for s in steps)
    has_fasta = bool(cfg.get("fasta_path"))
    has_annot = bool(cfg.get("annotation_path"))
    overrides = cfg.get("overrides") or {}
    for s in steps:
        tool = s.get("tool")
        schema = _PARAM_SCHEMA.get(tool)
        if not schema:
            continue
        given = set((s.get("params") or {})) | set(overrides.get(s.get("step_id"), {}))
        for name, spec in schema.items():
            if not spec.get("required") or name in given:
                continue
            if name == "database_path" and (has_db or has_fasta):
                continue
            if name == "annotation_file" and has_annot:
                continue
            errs.append(f"步 {s.get('step_id')}({tool}) 缺必填参数 '{name}'")


_SPECTRA_PRODUCERS = {"msconvert", "diaumpire", "diatracer"}   # 产 mzML 的步
# 硬要求 mzML 输入的工具(缺谱图会在运行时 raise InputError)。谱图(raw_files)只送达
# 无入边的根节点;非根的这些工具必须有一个产 mzML 的父(msconvert 等),否则被饿死。
_SPECTRA_CONSUMERS = {"msfragger-closed", "crystalc", "ionquant",
                      "ptmshepherd", "msbooster", "opair", "easypqp"}


def _check_spectra_consumers(steps: list, edges: list, errs: list) -> None:
    """吃 mzML 的工具:谱图来自 raw_files,只喂无入边的根节点。
    - msfragger 通常作谱图根节点(别画 db→msfragger 边——库经 database_path 自动注入)。
    - crystalc/ionquant/ptmshepherd/msbooster/opair/easypqp 既要谱图又要上游产物(非根),
      必须有一个产 mzML 的父(msconvert/diaumpire/diatracer),否则运行时 'requires mzML'。
    这是手写 DAG 最常见的坑;能用官方 template_id 就别手写。"""
    tool_by_id = {s.get("step_id"): s.get("tool") for s in steps}
    for s in steps:
        tool = s.get("tool") or ""
        if tool not in _SPECTRA_CONSUMERS:
            continue
        sid = s.get("step_id")
        parents = [e.get("src") for e in (edges or []) if e.get("dst") == sid]
        if parents and not any(tool_by_id.get(p) in _SPECTRA_PRODUCERS for p in parents):
            pt = ", ".join(f"{p}({tool_by_id.get(p)})" for p in parents)
            fix = (f"去掉指向 {sid} 的边让它成为谱图根节点(仅 msfragger 可这样),"
                   if tool == "msfragger-closed"
                   else "加一条 msconvert→本步 的边供谱图,")
            errs.append(
                f"步 {sid}({tool})有入边但没有谱图来源(父节点:{pt});它硬要求 mzML 输入,"
                f"而 raw_files 只送达无入边的根节点。修复:{fix}或改用官方 template_id。")


def _normalize_names(cfg: dict) -> None:
    """把公开名/公开模板 id 归一成内部名 —— 与镜像执行器入口同一套映射。

    param_schema.json / template_tools.json 是从镜像 specs.py 导出的,键是内部名;
    归一之后,下面所有校验(参数名、必填、overrides)照旧生效,不必重新导出这两张表。
    """
    for s in (cfg.get("steps") or []):
        if s.get("tool"):
            s["tool"] = tool_names.to_internal(s["tool"])
    tid = cfg.get("template_id")
    if tid and tid not in _TPL_TOOLS and f"fp-{tid}" in _TPL_TOOLS:
        cfg["template_id"] = f"fp-{tid}"


def validate_config(cfg: dict) -> list[str]:
    errs: list[str] = []
    _normalize_names(cfg)
    # 顶层字段名(raw_file/fastapath 拼错会被静默忽略 → 作业找不到输入才失败)
    for k in cfg:
        if k not in _TOP_KEYS:
            sug = difflib.get_close_matches(k, _TOP_KEYS, n=1, cutoff=0.5)
            errs.append(f"未知顶层字段 '{k}'" + (f"(应为 {sug[0]} ?)" if sug else ""))
    fp = cfg.get("fasta_path")
    if isinstance(fp, str) and fp.startswith("/bohr/"):
        errs.append(f"fasta_path 不能放只读 dataset(/bohr…),须走 -p 上传:{fp}")

    if cfg.get("template_id"):     # 模板入口:steps/edges 镜像展开;用 template_tools 映射查 overrides/必填
        tid = cfg["template_id"]
        tpl_steps = [{"step_id": sid, "tool": tool}
                     for sid, tool in _TPL_TOOLS.get(tid, {}).items()]
        if tid not in _TPL_TOOLS and _TPL_TOOLS:
            errs.append(f"未知 template_id '{tid}'(不在已知模板列表)")
        _check_overrides(cfg, [], errs)
        _check_required(cfg, tpl_steps, errs)
        return errs

    steps = cfg.get("steps") or []
    if not steps:
        errs.append("steps 为空")
    ids = {s.get("step_id") for s in steps}
    for s in steps:
        if s.get("tool") not in _BU_TOOLS:
            errs.append(f"未知工具:{s.get('tool')}")
        else:
            _check_params(s, errs)
    for e in cfg.get("edges") or []:
        for end in ("src", "dst"):
            if e.get(end) not in ids:
                errs.append(f"边引用了不存在的步:{e.get(end)}")
    _check_spectra_consumers(steps, cfg.get("edges") or [], errs)
    _check_overrides(cfg, steps, errs)
    _check_required(cfg, steps, errs)
    return errs


def _check_params(step: dict, errs: list) -> None:
    _check_param_dict(step.get("tool"), step.get("params"), errs,
                      f"步 {step.get('step_id')}({step.get('tool')})")


def _check_local_input(v, base, field, errs):
    """本地输入:存在性 + >100MB 硬拦。相对路径按 pipeline.json 所在目录解析。

    base 必须与 submit 的 _stage 用同一个基准目录。以前这里按 CWD 解析、且"文件不存在"
    是直接跳过(不是报错):相对路径写的 GB 级 raw 在校验端 exists()=False → 静默绕过
    100MB 硬拦,submit 端却按 pipeline 目录解析成功、把它拷进 -p 上传包。校验器自己放的水。
    """
    if not isinstance(v, str) or v.startswith("/bohr/"):
        return                      # /bohr 是只读挂载路径,不做本地存在性检查
    path = v if os.path.isabs(v) else os.path.join(base or ".", v)
    if not os.path.exists(path):
        errs.append(
            f"{field} 的本地文件不存在: {v}(按 pipeline.json 所在目录解析为 {path})。"
            f"修复:ls 确认真实文件名后改 pipeline.json。"
            f"禁止:不要拿名字相近的另一个文件顶替;不要随手填一个 /bohr/... 路径——"
            f"/bohr 开头的路径本校验器不做存在性检查,猜的路径必定通过校验、到作业里才炸,"
            f"/bohr 路径只能来自 make_dataset.py 的返回值。")
        return
    mb = os.path.getsize(path) / (1024 * 1024)
    if field == "raw_files" and mb > _MAX_LOCAL_MB:
        errs.append(
            f"本地输入 {v} = {mb:.0f}MB > {_MAX_LOCAL_MB}MB,不能随作业打包上传。"
            f"修复:python3 make_dataset.py --file {path} --name <稳定的英文名>,"
            f"然后把它返回的 spectrum_mount 原样填进 raw_files。"
            f"禁止:不要压缩/切分后硬塞进上传包,不要把它下载到别处再传。")


def validate_with_fs(cfg: dict, base: str | None = None) -> dict:
    """validate_config(纯规则) + 本地输入存在性 + 大文件硬拦(>100MB 逼 make_dataset)。

    base = pipeline.json 所在目录,必须与 submit 的 _stage 同基准,否则相对路径两边解析
    不一致,硬拦会被静默绕过。submit_pipeline 调用此接口;返回 {"ok","errors"}。
    """
    errs = validate_config(cfg)
    for p in (cfg.get("raw_files") or []):
        _check_local_input(p, base, "raw_files", errs)
    for key in ("fasta_path", "annotation_path"):   # 以前完全没检查 → submit 里裸 FileNotFoundError
        if cfg.get(key):
            _check_local_input(cfg[key], base, key, errs)
    return {"ok": not errs, "errors": errs}


def main(argv=None) -> int:
    # TD 版用 --pipeline,BU 版历史上只吃位置参数。agent 在两个 skill 间迁移经验时
    # `validate_pipeline.py --pipeline p.json` 会变成 open("--pipeline") → 一个看不懂的
    # "文件 --pipeline 不存在"。两种写法都接受。
    args = list(argv if argv is not None else sys.argv[1:])
    path = None
    if "--pipeline" in args:
        i = args.index("--pipeline")
        if i + 1 < len(args):
            path = args[i + 1]
    elif args and not args[0].startswith("-"):
        path = args[0]
    if not path:
        print("usage: validate_pipeline.py <pipeline.json>   (--pipeline <path> 亦可)",
              file=sys.stderr)
        return 2
    args = [path]
    try:
        cfg = json.loads(open(args[0]).read())
    except FileNotFoundError:
        print(f"ERROR: pipeline file not found: {args[0]}", file=sys.stderr)
        print("FIX:   Write the pipeline.json first, then validate it. Check the path you "
              "passed against the file you actually wrote.", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"ERROR: {args[0]} is not valid JSON: {e}", file=sys.stderr)
        print(f"FIX:   Fix the syntax at line {e.lineno}, column {e.colno}, then re-run. "
              "A trailing comma or an unquoted key is the usual cause.", file=sys.stderr)
        return 2
    vres = validate_with_fs(cfg, base=os.path.dirname(os.path.abspath(args[0])))
    for e in vres["errors"]:
        print(f"ERROR: {e}", file=sys.stderr)
    print(json.dumps(vres, ensure_ascii=False))
    return 0 if vres["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
