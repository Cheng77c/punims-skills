#!/usr/bin/env python3
"""Fail release when isolated test skills lose Bohrium AK hardening."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_V2 = "registry.dp.tech/dptech/dp/native/prod-3712867/msrea:v2"
DOMAINS = ("bottomup", "topdown")


def require(
    failures: list[str],
    condition: bool,
    domain: str,
    message: str,
) -> None:
    if not condition:
        failures.append(f"{domain}: {message}")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_domain(domain: str, failures: list[str]) -> None:
    skill_dir = ROOT / f"{domain}-proteomics-test"
    skill = text(skill_dir / "SKILL.md")
    setup = text(skill_dir / "scripts/setup.sh")

    require(
        failures,
        f"name: {domain}-proteomics-test" in skill,
        domain,
        "test skill name changed",
    )
    require(
        failures,
        text(skill_dir / "image.txt").strip() == IMAGE_V2,
        domain,
        "image.txt is not pinned to msrea:v2",
    )
    require(
        failures,
        "primaryEnv: BOHR_ACCESS_KEY" in skill,
        domain,
        "primaryEnv must use the platform-injected BOHR_ACCESS_KEY",
    )
    require(
        failures,
        (skill_dir / "scripts/fetch_file.py").is_file(),
        domain,
        "scripts/fetch_file.py is missing",
    )

    require(
        failures,
        'export OPENAPI_HOST=https://open.bohrium.com' in setup,
        domain,
        "setup.sh still uses the legacy OpenAPI gateway",
    )
    require(
        failures,
        'export ACCESS_KEY="\\${BOHR_ACCESS_KEY:-\\$ACCESS_KEY}"' in setup,
        domain,
        "setup.sh does not persist a literal ACCESS_KEY reference",
    )
    require(
        failures,
        'export BOHR_ACCESS_KEY="\\${BOHR_ACCESS_KEY:-\\$ACCESS_KEY}"' in setup,
        domain,
        "setup.sh does not persist a literal BOHR_ACCESS_KEY reference",
    )
    require(
        failures,
        'export ACCESS_KEY="${ACCESS_KEY:-${BOHR_ACCESS_KEY:-}}"' not in setup,
        domain,
        "setup.sh expands the live key into .bohr_env",
    )
    require(
        failures,
        'host = "https://open.bohrium.com"' in setup and 'PROBE="' in setup,
        domain,
        "setup.sh AK probe is missing",
    )

    require(
        failures,
        "fetch_file.py" in skill and "不要手写 curl" in skill,
        domain,
        "SKILL.md does not require the wrapped FASTA downloader",
    )
    require(
        failures,
        "/v1/file/download/" not in skill,
        domain,
        "SKILL.md still teaches a key-bearing manual download curl",
    )
    require(
        failures,
        "绝不向用户索取" in skill,
        domain,
        "SKILL.md does not forbid asking the user for an access key",
    )

    expected = {
        "scripts/make_dataset.py": ("def _api_json",),
        "scripts/submit_pipeline.py": (
            "def _child_env",
            "def _looks_unauthenticated",
            "env=_child_env()",
        ),
        "scripts/poll_job.py": ('status="auth_failed"',),
        "scripts/collect_results.py": (
            "def _child_env",
            "def _looks_unauthenticated",
            "env=_child_env()",
        ),
    }
    for relative, markers in expected.items():
        value = text(skill_dir / relative)
        for marker in markers:
            require(
                failures,
                marker in value,
                domain,
                f"{relative} is missing security marker {marker!r}",
            )


def check_dataset_manager(failures: list[str]) -> None:
    domain = "dataset-manager"
    skill = text(ROOT / "bohrium-dataset-manager-test" / "SKILL.md")
    require(
        failures,
        "name: bohrium-dataset-manager-test" in skill,
        domain,
        "test skill name changed",
    )
    require(
        failures,
        "dataset_manager.py" in skill
        and "fetch_file.py" in skill
        and "不要手写 curl" in skill,
        domain,
        "safe dataset/FASTA routing is missing",
    )
    require(
        failures,
        "绝不向用户索取" in skill,
        domain,
        "SKILL.md does not forbid asking the user for an access key",
    )
    for forbidden in (
        'AK="${BOHR_ACCESS_KEY',
        'export ACCESS_KEY="$BOHR_ACCESS_KEY"',
        "Authorization: Bearer $AK",
        "/v1/file/download/",
    ):
        require(
            failures,
            forbidden not in skill,
            domain,
            f"SKILL.md still contains key-bearing manual API example {forbidden!r}",
        )


def main() -> int:
    failures: list[str] = []
    for domain in DOMAINS:
        check_domain(domain, failures)
    check_dataset_manager(failures)
    if failures:
        print("test-skill security gate: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("test-skill security gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
