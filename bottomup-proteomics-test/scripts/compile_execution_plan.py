#!/usr/bin/env python3
"""Compile TD/BU authoring JSON into the image's explicit contract-v4 plan.

This file is intentionally stdlib-only.  It belongs to the skill: template
selection and workflow semantics are resolved before submission.  The image
receives only the resulting execution_plan.json and mechanically executes its
bindings, parameter injections, transforms, edges, and map_over directives.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CONTRACT_VERSION = 4
CATALOG_VERSION = 1
_HERE = Path(__file__).resolve().parent

_FASTA_SUFFIXES = (".fas", ".fasta", ".fa")
_SPECTRA_PRODUCERS = {"msconvert", "diaumpire", "diatracer"}

# Used only when a generated tool_contracts.json is absent (for example while
# editing the skill source). Production assets always include that file.
_FALLBACK_INPUT_SUFFIXES: dict[str, tuple[str, ...]] = {
    "msconvert": (".raw", ".mzml", ".mzxml", ".mgf", ".wiff", ".d"),
    "msfragger-closed": (".mzml", ".mzxml"),
    "philosopher-database": _FASTA_SUFFIXES,
    "philosopher-report": (".pepxml", ".pep.xml", *_FASTA_SUFFIXES),
    "peptideprophet": (".pepxml", ".pep.xml", *_FASTA_SUFFIXES),
    "crystalc": (".pepxml", ".pep.xml", *_FASTA_SUFFIXES),
    "percolator": (".pin",),
    "percolator-to-pepxml": (".tsv", ".pin", ".pepxml", ".mzml"),
    "ionquant": (".mzml", ".tsv"),
    "tmtintegrator": (".tsv",),
    "diann": (".raw", ".mzml", ".d"),
}


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _tool_contracts() -> dict[str, Any]:
    return _read_json(_HERE / "tool_contracts.json")


def _connection_rules() -> dict[str, Any]:
    return _read_json(_HERE / "connection_rules.json")


def _input_suffixes(tool: str) -> tuple[str, ...]:
    raw = _tool_contracts().get(tool, {}).get("supported_input_extensions")
    if raw:
        return tuple(str(item).lower() for item in raw)
    return _FALLBACK_INPUT_SUFFIXES.get(tool, ())


def _param_schema() -> dict[str, Any]:
    return _read_json(_HERE / "param_schema.json")


def _has_param(tool: str, name: str) -> bool:
    return name in _param_schema().get(tool, {})


def _edge(src: str, dst: str, wiring: str = "edge", *, synthetic: bool = False) -> dict:
    edge = {"from": src, "to": dst, "wiring": wiring}
    if synthetic:
        edge["synthetic"] = True
    return edge


def _selector(
    suffixes: tuple[str, ...] | list[str] = (),
    *,
    basename: str | None = None,
    fallback_all: bool = False,
) -> dict[str, Any]:
    value: dict[str, Any] = {"suffixes": [str(item).lower() for item in suffixes]}
    if basename:
        value["basename"] = basename
    if fallback_all:
        value["fallback_all"] = True
    return value


def _binding(
    name: str,
    source: str,
    suffixes: tuple[str, ...] | list[str] = (),
    *,
    input_type: str = "primary",
    fallback_all: bool = False,
    wiring: str = "edge",
    required: bool = True,
    stage_as: dict[str, str] | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "name": name,
        "source": source,
        "input_type": input_type,
        "select": _selector(suffixes, fallback_all=fallback_all),
        "wiring": wiring,
        "required": required,
    }
    if stage_as:
        value["stage_as"] = stage_as
    return value


def _normalise_edges(raw_edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for raw in raw_edges:
        src = raw.get("from", raw.get("src"))
        dst = raw.get("to", raw.get("dst"))
        if not src or not dst:
            raise ValueError(f"edge requires from/to (or src/dst): {raw!r}")
        edges.append(_edge(str(src), str(dst)))
    return edges


def _ancestors(step_id: str, edges: list[dict[str, Any]]) -> set[str]:
    parents: dict[str, set[str]] = {}
    for edge in edges:
        parents.setdefault(edge["to"], set()).add(edge["from"])
    seen: set[str] = set()
    stack = list(parents.get(step_id, ()))
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(parents.get(current, ()))
    return seen


def _assert_acyclic(
    step_ids: set[str],
    edges: list[dict[str, Any]],
) -> None:
    incoming = {step_id: set() for step_id in step_ids}
    children = {step_id: set() for step_id in step_ids}
    for edge in edges:
        incoming[edge["to"]].add(edge["from"])
        children[edge["from"]].add(edge["to"])
    ready = [step_id for step_id, parents in incoming.items() if not parents]
    visited = 0
    while ready:
        current = ready.pop()
        visited += 1
        for child in children[current]:
            incoming[child].discard(current)
            if not incoming[child]:
                ready.append(child)
    if visited != len(step_ids):
        raise ValueError("bottom-up DAG contains a cycle")


def _binding_from_template(role: str, source: str) -> dict[str, Any]:
    if source.startswith("workflow."):
        kind = source.split(".", 1)[1]
        input_type = "external" if kind in {"fasta", "annotation"} else "primary"
        return _binding(role, source, input_type=input_type, wiring="declared")
    if "." in source:
        step_id, suffix = source.split(".", 1)
        return _binding(
            role,
            step_id,
            ("." + suffix,),
            wiring="declared",
            fallback_all=False,
        )
    return _binding(role, source, wiring="declared", fallback_all=True)


def _dedupe_bindings(bindings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for binding in bindings:
        key = json.dumps(binding, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(binding)
    return result


def _load_template(template_id: str, catalog_path: Path | str | None) -> tuple[dict, int]:
    path = Path(catalog_path) if catalog_path else _HERE / "template_catalog.json"
    catalog = _read_json(path)
    version = catalog.get("catalog_version")
    if version != CATALOG_VERSION:
        raise ValueError(
            f"unsupported catalog_version {version!r}; expected {CATALOG_VERSION}"
        )
    try:
        template = catalog["templates"][template_id]
    except KeyError as exc:
        raise ValueError(f"unknown template_id: {template_id}") from exc
    return dict(template), version


def _compile_bottomup_steps(
    raw_steps: list[dict[str, Any]],
    raw_edges: list[dict[str, Any]],
    overrides: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edges = _normalise_edges(raw_edges)
    step_by_id = {str(step["step_id"]): step for step in raw_steps}
    if len(step_by_id) != len(raw_steps):
        raise ValueError("duplicate bottom-up step_id")
    for edge in edges:
        if edge["from"] not in step_by_id or edge["to"] not in step_by_id:
            raise ValueError(f"edge references unknown step: {edge}")
    _assert_acyclic(set(step_by_id), edges)
    for edge in edges:
        source_tool = str(step_by_id[edge["from"]]["tool"])
        target_tool = str(step_by_id[edge["to"]]["tool"])
        rules = _connection_rules()
        bu_tools = set(rules.get("bottom_up_tools") or [])
        if (
            source_tool in bu_tools
            and target_tool in bu_tools
            and target_tool not in rules.get("rules", {}).get(source_tool, [])
        ):
            raise ValueError(
                f"connection not allowed: {edge['from']}({source_tool}) -> "
                f"{edge['to']}({target_tool})"
            )
    for raw in raw_steps:
        mapped = raw.get("map_over")
        if mapped and str(mapped) not in _ancestors(str(raw["step_id"]), edges):
            raise ValueError(
                f"step {raw['step_id']} map_over {mapped} is not upstream"
            )

    db_step_id = next(
        (
            str(step["step_id"])
            for step in raw_steps
            if step["tool"] == "philosopher-database"
        ),
        None,
    )
    compiled: list[dict[str, Any]] = []

    for raw in raw_steps:
        step_id = str(raw["step_id"])
        tool = str(raw["tool"])
        params = {**dict(raw.get("params") or {}), **dict(overrides.get(step_id) or {})}
        parents = [edge["from"] for edge in edges if edge["to"] == step_id]

        declared_inputs = raw.get("inputs") or {}
        if declared_inputs:
            bindings = [
                _binding_from_template(str(role), str(spec["from"]))
                for role, spec in declared_inputs.items()
            ]
        elif not parents:
            source = "workflow.fasta" if tool == "philosopher-database" else "workflow.raw"
            bindings = [
                _binding(
                    "input",
                    source,
                    input_type="external" if source.endswith(".fasta") else "primary",
                    wiring="root",
                )
            ]
        else:
            suffixes = _input_suffixes(tool)
            bindings = [
                _binding(
                    "input",
                    parent,
                    suffixes,
                    fallback_all=True,
                )
                for parent in parents
            ]

        param_bindings: list[dict[str, Any]] = []
        ancestors = _ancestors(step_id, edges)
        ancestor_by_tool: dict[str, list[str]] = {}
        for ancestor in ancestors:
            ancestor_by_tool.setdefault(str(step_by_id[ancestor]["tool"]), []).append(ancestor)

        consumes_fasta = any(suffix in _FASTA_SUFFIXES for suffix in _input_suffixes(tool))
        if tool != "philosopher-database" and consumes_fasta:
            db_source = db_step_id or "workflow.fasta"
            bindings.append(
                _binding(
                    "database",
                    db_source,
                    _FASTA_SUFFIXES,
                    input_type="external",
                    fallback_all=False,
                    wiring="database_injection",
                )
            )
            if db_step_id and not any(
                edge["from"] == db_step_id and edge["to"] == step_id for edge in edges
            ):
                edges.append(
                    _edge(
                        db_step_id,
                        step_id,
                        "database_injection",
                        synthetic=True,
                    )
                )

        if tool != "philosopher-database" and _has_param(tool, "database_path"):
            if "database_path" not in overrides.get(step_id, {}):
                param_bindings.append(
                    {
                        "param": "database_path",
                        "source": db_step_id or "workflow.fasta",
                        "select": _selector(_FASTA_SUFFIXES),
                        "mode": "override" if db_step_id else "fill_if_empty",
                        "required": True,
                    }
                )
                if db_step_id and not any(
                    edge["from"] == db_step_id and edge["to"] == step_id for edge in edges
                ):
                    edges.append(
                        _edge(
                            db_step_id,
                            step_id,
                            "database_injection",
                            synthetic=True,
                        )
                    )

        if tool in {"ionquant", "tmtintegrator", "labelquant"} and "annotation_file" not in params:
            param_bindings.append(
                {
                    "param": "annotation_file",
                    "source": "workflow.annotation",
                    "select": _selector(),
                    "mode": "fill_if_empty",
                    "required": False,
                }
            )

        if tool == "percolator-to-pepxml":
            for producer_tool, suffixes in (
                ("msfragger-closed", (".pin", ".pepxml", ".pep.xml")),
                ("msconvert", (".mzml",)),
                ("diaumpire", (".mzml",)),
                ("diatracer", (".mzml",)),
            ):
                for source in ancestor_by_tool.get(producer_tool, ()):
                    bindings.append(
                        _binding(
                            "artifact",
                            source,
                            suffixes,
                            fallback_all=False,
                            wiring="artifact_injection",
                            required=False,
                        )
                    )
                    if not any(
                        edge["from"] == source and edge["to"] == step_id for edge in edges
                    ):
                        edges.append(
                            _edge(
                                source,
                                step_id,
                                "artifact_injection",
                                synthetic=True,
                            )
                        )

        transforms: list[dict[str, Any]] = []
        if tool == "tmtintegrator":
            tmt_parents = {
                edge["from"]
                for edge in edges
                if edge["to"] == step_id and not edge.get("synthetic")
            }
            for candidate in raw_steps:
                if candidate["tool"] != "ionquant":
                    continue
                candidate_id = str(candidate["step_id"])
                iq_parents = {
                    edge["from"]
                    for edge in edges
                    if edge["to"] == candidate_id and not edge.get("synthetic")
                }
                if not (tmt_parents & iq_parents):
                    continue
                transforms.append(
                    {
                        "operation": "replace_basename",
                        "basename": "psm.tsv",
                        "source": candidate_id,
                        "select": _selector(basename="psm.tsv"),
                    }
                )
                if not any(
                    edge["from"] == candidate_id and edge["to"] == step_id
                    for edge in edges
                ):
                    edges.append(
                        _edge(
                            candidate_id,
                            step_id,
                            "artifact_substitution",
                            synthetic=True,
                        )
                    )
                break

        step: dict[str, Any] = {
            "step_id": step_id,
            "tool": tool,
            "params": params,
            "bindings": _dedupe_bindings(bindings),
            "param_bindings": param_bindings,
            "transforms": transforms,
        }
        if raw.get("map_over"):
            step["map_over"] = str(raw["map_over"])
        compiled.append(step)

    _assert_acyclic(set(step_by_id), edges)
    for step_id, raw in step_by_id.items():
        if raw["tool"] == "abacus":
            parents = {edge["from"] for edge in edges if edge["to"] == step_id}
            if len(parents) < 2:
                raise ValueError(
                    f"step {step_id} ({raw['tool']}) requires at least 2 parents"
                )
    return compiled, edges


def compile_bottomup(
    config: dict[str, Any],
    *,
    catalog_path: Path | str | None = None,
) -> dict[str, Any]:
    """Compile BU template/DAG authoring form into contract version 4."""
    metadata: dict[str, Any] = {"source_contract": "bottomup-authoring-v1"}
    if config.get("template_id"):
        template_id = str(config["template_id"])
        template, catalog_version = _load_template(template_id, catalog_path)
        raw_steps = list(template["steps"])
        raw_edges = list(template.get("edges") or [])
        metadata.update(
            {
                "template_id": template_id,
                "template_catalog_version": catalog_version,
            }
        )
    else:
        raw_steps = list(config.get("steps") or [])
        raw_edges = list(config.get("edges") or [])
    if not raw_steps:
        raise ValueError("steps must not be empty")

    steps, edges = _compile_bottomup_steps(
        raw_steps,
        raw_edges,
        dict(config.get("overrides") or {}),
    )
    return {
        "contract_version": CONTRACT_VERSION,
        "domain": "bottomup",
        "inputs": {
            "raw": list(config.get("raw_files") or []),
            "fasta": config.get("fasta_path"),
            "annotation": config.get("annotation_path"),
            "named": {},
        },
        "steps": steps,
        "edges": edges,
        "collect": list(config.get("collect") or []),
        "metadata": metadata,
    }


def _td_source(previous: str | None) -> str:
    return previous or "workflow.raw"


def compile_topdown(config: dict[str, Any]) -> dict[str, Any]:
    """Compile the public linear TD ``inputs + steps`` form to contract v4."""
    raw_steps = list(config.get("steps") or [])
    if not raw_steps:
        raise ValueError("steps must not be empty")

    ids: list[str] = []
    for index, raw in enumerate(raw_steps):
        tool = str(raw["tool"])
        ids.append(str(raw.get("step_id") or f"{index:02d}_{tool}"))
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate top-down step_id")

    steps: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_steps):
        step_id = ids[index]
        tool = str(raw["tool"])
        previous = ids[index - 1] if index else None
        if previous:
            edges.append(_edge(previous, step_id))
        params = dict(raw.get("params") or {})
        bindings: list[dict[str, Any]] = []

        if tool == "toppic":
            bindings.append(
                _binding("msalign", _td_source(previous), (".msalign",))
            )
            bindings.append(
                _binding(
                    "fasta",
                    "workflow.fasta",
                    _FASTA_SUFFIXES,
                    input_type="external",
                )
            )
            flash_used = any(step["tool"] == "flashdeconv" for step in steps)
            if flash_used:
                params.setdefault("no_topfd_feature", True)
            elif previous:
                bindings.append(
                    _binding(
                        "feature",
                        previous,
                        (".feature",),
                        input_type="external",
                        required=False,
                        stage_as={
                            "match_stem_of": "msalign",
                            "suffix": ".feature",
                        },
                    )
                )
            else:
                bindings.append(
                    _binding(
                        "feature",
                        "workflow.named.feature",
                        (".feature",),
                        input_type="external",
                        required=not bool(params.get("no_topfd_feature")),
                    )
                )
        elif tool == "mspathfindert":
            pbf_source = next(
                (
                    step["step_id"]
                    for step in reversed(steps)
                    if step["tool"] == "pbfgen"
                ),
                _td_source(previous),
            )
            ms1ft_source = next(
                (
                    step["step_id"]
                    for step in reversed(steps)
                    if step["tool"] == "promex"
                ),
                "workflow.named.ms1ft",
            )
            bindings.extend(
                [
                    _binding("spectrum", pbf_source, (".pbf",)),
                    _binding(
                        "fasta",
                        "workflow.fasta",
                        _FASTA_SUFFIXES,
                        input_type="external",
                    ),
                    _binding(
                        "feature",
                        ms1ft_source,
                        (".ms1ft",),
                        input_type="external",
                    ),
                ]
            )
        else:
            suffixes = {
                "msconvert": (".raw", ".mzml", ".mzxml"),
                "topfd": (".mzml", ".mzxml"),
                "flashdeconv": (".mzml", ".mzxml"),
                "pbfgen": (".raw", ".mzml", ".mzxml"),
                "promex": (".pbf", ".mzml", ".mzxml"),
            }.get(tool, ())
            bindings.append(
                _binding(
                    "input_0",
                    _td_source(previous),
                    suffixes,
                    fallback_all=not bool(suffixes),
                )
            )

        steps.append(
            {
                "step_id": step_id,
                "tool": tool,
                "params": params,
                "bindings": bindings,
                "param_bindings": [],
                "transforms": [],
            }
        )

    inputs = dict(config.get("inputs") or {})
    return {
        "contract_version": CONTRACT_VERSION,
        "domain": "topdown",
        "inputs": {
            "raw": [inputs["spectrum"]] if inputs.get("spectrum") else [],
            "fasta": inputs.get("fasta"),
            "annotation": None,
            "named": {
                key: value
                for key, value in inputs.items()
                if key not in {"spectrum", "fasta"} and value
            },
        },
        "steps": steps,
        "edges": edges,
        "collect": list(config.get("collect") or []),
        "metadata": {"source_contract": "topdown-authoring-v1"},
    }


def compile_config(
    config: dict[str, Any],
    domain: str,
    *,
    catalog_path: Path | str | None = None,
) -> dict[str, Any]:
    if domain == "bottomup":
        return compile_bottomup(config, catalog_path=catalog_path)
    if domain == "topdown":
        return compile_topdown(config)
    raise ValueError(f"unsupported domain: {domain}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", choices=("topdown", "bottomup"), required=True)
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--output", default="execution_plan.json")
    parser.add_argument("--catalog")
    args = parser.parse_args(argv)

    config = _read_json(Path(args.pipeline))
    plan = compile_config(config, args.domain, catalog_path=args.catalog)
    Path(args.output).write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "ok": True,
                "contract_version": CONTRACT_VERSION,
                "output": args.output,
                "steps": len(plan["steps"]),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
