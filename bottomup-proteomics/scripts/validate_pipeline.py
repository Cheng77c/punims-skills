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
    try:
        with open(os.path.join(_HERE, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


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


def validate_config(cfg: dict) -> list[str]:
    errs: list[str] = []
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
    _check_overrides(cfg, steps, errs)
    _check_required(cfg, steps, errs)
    return errs


def _check_params(step: dict, errs: list) -> None:
    _check_param_dict(step.get("tool"), step.get("params"), errs,
                      f"步 {step.get('step_id')}({step.get('tool')})")


def validate_with_fs(cfg: dict) -> dict:
    """validate_config(纯规则) + 本地大文件硬拦(>100MB 逼 make_dataset)。
    submit_pipeline 调用此接口;返回 {"ok": bool, "errors": list[str]}。"""
    errs = validate_config(cfg)
    for p in (cfg.get("raw_files") or []):
        if isinstance(p, str) and not p.startswith("/bohr/") and os.path.exists(p):
            mb = os.path.getsize(p) / (1024 * 1024)
            if mb > _MAX_LOCAL_MB:
                errs.append(f"本地输入 {p} = {mb:.0f}MB > {_MAX_LOCAL_MB}MB,须 make_dataset 注册")
    return {"ok": not errs, "errors": errs}


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: validate_pipeline.py pipeline.json", file=sys.stderr)
        return 2
    cfg = json.loads(open(args[0]).read())
    vres = validate_with_fs(cfg)
    for e in vres["errors"]:
        print(f"ERROR: {e}", file=sys.stderr)
    print(json.dumps(vres, ensure_ascii=False))
    return 0 if vres["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
