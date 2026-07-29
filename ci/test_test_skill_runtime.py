#!/usr/bin/env python3
"""Runtime regression tests for the isolated Bohrium test skills."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ("bottomup", "topdown")
AUTH_FAILURE = "json: cannot unmarshal object into Go struct field RespErr.error"


def load_script(domain: str, script: str):
    scripts = ROOT / f"{domain}-proteomics-test" / "scripts"
    name = f"{domain}_test_{script.replace('.', '_')}"
    spec = importlib.util.spec_from_file_location(name, scripts / script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {scripts / script}")

    # submit_pipeline imports its adjacent compiler and validator by module name.
    old_path = list(sys.path)
    previous = {
        dep: sys.modules.pop(dep, None)
        for dep in ("validate_pipeline", "compile_execution_plan")
    }
    try:
        sys.path.insert(0, str(scripts))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = old_path
        for dep in ("validate_pipeline", "compile_execution_plan"):
            sys.modules.pop(dep, None)
            if previous[dep] is not None:
                sys.modules[dep] = previous[dep]


class TestAkBridge(unittest.TestCase):
    def test_submit_and_collect_bridge_platform_key(self):
        for domain in DOMAINS:
            with self.subTest(domain=domain):
                for script in ("submit_pipeline.py", "collect_results.py"):
                    module = load_script(domain, script)
                    with patch.dict(
                        os.environ,
                        {"BOHR_ACCESS_KEY": "test-platform-key"},
                        clear=True,
                    ):
                        child = module._child_env()
                    self.assertEqual(child["ACCESS_KEY"], "test-platform-key")
                    self.assertEqual(child["BOHR_ACCESS_KEY"], "test-platform-key")

    def test_collect_does_not_retry_terminal_auth_failure(self):
        for domain in DOMAINS:
            with self.subTest(domain=domain), tempfile.TemporaryDirectory() as out:
                module = load_script(domain, "collect_results.py")
                calls = 0

                def downloader(_job_id: str, _out: str) -> str:
                    nonlocal calls
                    calls += 1
                    return AUTH_FAILURE

                result = module.collect("test-job", out, downloader=downloader)
                self.assertEqual(calls, 1)
                self.assertFalse(result["ok"])
                self.assertEqual(result["status"], "auth_failed")
                self.assertIn("不要向用户索取", result["next"])


class TestDatasetMountDerivation(unittest.TestCase):
    def test_bottomup_mounts_are_derived_and_deduplicated(self):
        module = load_script("bottomup", "submit_pipeline.py")
        mounts, errors = module._derive_dataset_paths(
            [
                "/bohr/spectrum-abc/v1/upload/run.mzML",
                "/bohr/spectrum-abc/v1/upload/second.mzML",
                "database.fasta",
            ],
            ["/bohr/already/v2"],
        )
        self.assertEqual(
            mounts,
            ["/bohr/already/v2", "/bohr/spectrum-abc/v1"],
        )
        self.assertEqual(errors, [])

    def test_topdown_mounts_are_derived_and_bad_paths_rejected(self):
        module = load_script("topdown", "submit_pipeline.py")
        mounts, errors = module._derive_dataset_paths(
            {
                "spectrum": "/bohr/spectrum-xyz/v3/upload/run.mzML",
                "fasta": "database.fasta",
                "feature": "/bohr/incomplete",
            },
            [],
        )
        self.assertEqual(mounts, ["/bohr/spectrum-xyz/v3"])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "inputs.feature")


class TestValidatorSubmitContract(unittest.TestCase):
    def test_bottomup_validator_accepts_submit_base_and_resolves_relative_inputs(self):
        module = load_script("bottomup", "validate_pipeline.py")
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "run.mzML").write_bytes(b"fixture")
            (base / "db.fasta").write_text(">p1\nPEPTIDE\n")
            result = module.validate_with_fs(
                {
                    "template_id": "basic-search",
                    "raw_files": ["run.mzML"],
                    "fasta_path": "db.fasta",
                },
                base=str(base),
            )
        self.assertTrue(result["ok"], result["errors"])

    def test_topdown_validator_accepts_submit_base_and_resolves_relative_inputs(self):
        module = load_script("topdown", "validate_pipeline.py")
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "run.raw").write_bytes(b"fixture")
            result = module.validate_with_fs(
                {
                    "steps": [{"tool": "msconvert", "params": {}}],
                    "inputs": {"spectrum": "run.raw"},
                },
                base=str(base),
            )
        self.assertTrue(result["ok"], result["errors"])


class TestExecutionPlanBindings(unittest.TestCase):
    def test_basic_search_does_not_duplicate_explicit_parent_bindings(self):
        module = load_script("bottomup", "compile_execution_plan.py")
        scripts = ROOT / "bottomup-proteomics-test" / "scripts"
        plan = module.compile_bottomup(
            {
                "template_id": "basic-search",
                "raw_files": ["/bohr/fixture/v1/run.mzML"],
                "fasta_path": "db.fasta",
            },
            catalog_path=scripts / "template_catalog.json",
        )
        steps = {step["step_id"]: step for step in plan["steps"]}
        self.assertEqual(
            [binding["source"] for binding in steps["report"]["bindings"]],
            ["to_pepxml", "database"],
        )
        rewrite_sources = [
            binding["source"] for binding in steps["to_pepxml"]["bindings"]
        ]
        self.assertEqual(len(rewrite_sources), len(set(rewrite_sources)))


if __name__ == "__main__":
    unittest.main()
