"""Check public release invariants for the FeynAgent Python/package layer."""

from __future__ import annotations

import importlib.metadata
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_INIT = ROOT / "src" / "feynagent" / "__init__.py"
SKILL_MD = ROOT / "skills" / "feynagent" / "SKILL.md"
EXPECTED_VERSION = "0.1.0"
ALLOWED_RUNS_TRACKED = {"runs/.gitkeep"}
PUBLIC_SURFACE_PREFIXES = (
    "README.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/",
    "examples/",
    "skills/feynagent/",
    "benchmarks/B04_phi_phi_to_hh/",
)
PUBLIC_SURFACE_EXCLUDES = {
    "benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml",
}
PRIVATE_KNOWLEDGE_MARKERS = [
    re.compile(r"source_material[/\\].*\.(?:pdf|nb|wl|m|yaml|yml|md)\b", re.IGNORECASE),
    re.compile(r"gold[/\\].*\.(?:pdf|nb|wl|m|tex|yaml|yml|md)\b", re.IGNORECASE),
    re.compile(r"[A-Za-z]:[/\\][^\n`]*?(?:source_material|knowledge_roots|FeynGrav|feynman_calculation|arXiv-2402|hep-th)", re.IGNORECASE),
    re.compile(r"/(?:Users|home)/[^\n`]*?(?:source_material|knowledge_roots|FeynGrav|feynman_calculation|arXiv-2402|hep-th)", re.IGNORECASE),
]


class InvariantFailure(Exception):
    """Raised when a release invariant fails."""


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _git_ls_files(*paths: str) -> list[str]:
    command = ["git", "ls-files", "-z", *paths]
    completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    output = completed.stdout.decode("utf-8")
    return sorted(item for item in output.split("\0") if item)


def _read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def _parse_pyproject_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^\[project\]\s+.*?^version\s*=\s*\"([^\"]+)\"", text)
    if not match:
        raise InvariantFailure("pyproject.toml [project].version was not found")
    return match.group(1)


def _parse_init_version() -> str:
    text = PACKAGE_INIT.read_text(encoding="utf-8")
    match = re.search(r"^__version__\s*=\s*\"([^\"]+)\"", text, re.MULTILINE)
    if not match:
        raise InvariantFailure("src/feynagent/__init__.py __version__ was not found")
    return match.group(1)


def _check_version_consistency() -> list[str]:
    pyproject_version = _parse_pyproject_version()
    init_version = _parse_init_version()
    installed_version = importlib.metadata.version("feynagent")
    versions = {
        "expected": EXPECTED_VERSION,
        "pyproject": pyproject_version,
        "package": init_version,
        "installed": installed_version,
    }
    if len(set(versions.values())) != 1:
        details = ", ".join(f"{key}={value}" for key, value in versions.items())
        raise InvariantFailure(f"package version mismatch: {details}")
    return [f"package version consistency: {pyproject_version}"]


def _split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise InvariantFailure("skills/feynagent/SKILL.md must start with YAML frontmatter")
    try:
        frontmatter, body = text.split("\n---\n", 1)
    except ValueError as exc:
        raise InvariantFailure("skills/feynagent/SKILL.md must close YAML frontmatter") from exc
    metadata = yaml.safe_load(frontmatter.removeprefix("---\n"))
    if not isinstance(metadata, dict):
        raise InvariantFailure("skills/feynagent/SKILL.md frontmatter must be a mapping")
    return metadata, body


def _check_skill_metadata() -> list[str]:
    metadata, body = _split_frontmatter(SKILL_MD.read_text(encoding="utf-8"))
    if metadata.get("name") != "feynagent":
        raise InvariantFailure("skills/feynagent/SKILL.md name must be feynagent")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        raise InvariantFailure("skills/feynagent/SKILL.md description must be non-empty")
    if "standard_native" not in body or "custom_audited" not in body:
        raise InvariantFailure("skills/feynagent/SKILL.md must describe both validated routes")
    for reference in (
        "references/BACKEND_POLICY.md",
        "references/CUSTOM_RULE_PROTOCOL.md",
        "references/OUTPUT_CONTRACT.md",
    ):
        if not (SKILL_MD.parent / reference).exists():
            raise InvariantFailure(f"missing skill reference: skills/feynagent/{reference}")
    return ["FeynAgent skill metadata and references are valid"]


def _check_tracked_output_hygiene() -> list[str]:
    tracked_dot_feynagent = _git_ls_files(".feynagent")
    if tracked_dot_feynagent:
        raise InvariantFailure("tracked .feynagent/ files are forbidden: " + ", ".join(tracked_dot_feynagent))

    tracked_runs = set(_git_ls_files("runs"))
    unexpected_runs = sorted(tracked_runs - ALLOWED_RUNS_TRACKED)
    if unexpected_runs:
        raise InvariantFailure("tracked runs/ outputs are forbidden: " + ", ".join(unexpected_runs))
    return ["no tracked .feynagent/ files", "tracked runs/ files limited to runs/.gitkeep"]


def _public_surface_files() -> Iterable[str]:
    tracked = _git_ls_files()
    for rel_path in tracked:
        if rel_path in PUBLIC_SURFACE_EXCLUDES:
            continue
        if rel_path.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip")):
            continue
        if rel_path in PUBLIC_SURFACE_PREFIXES or any(rel_path.startswith(prefix) for prefix in PUBLIC_SURFACE_PREFIXES):
            yield rel_path


def _check_private_knowledge_paths() -> list[str]:
    failures: list[str] = []
    for rel_path in _public_surface_files():
        text = _read_text(rel_path)
        for marker in PRIVATE_KNOWLEDGE_MARKERS:
            for match in marker.finditer(text):
                snippet = " ".join(match.group(0).split())[:160]
                failures.append(f"{rel_path}: {snippet}")
    if failures:
        raise InvariantFailure("private external-knowledge path markers found:\n  " + "\n  ".join(failures))
    return ["no private external-knowledge paths in public release surface"]


def run_checks() -> list[str]:
    messages: list[str] = []
    for check in (
        _check_version_consistency,
        _check_skill_metadata,
        _check_tracked_output_hygiene,
        _check_private_knowledge_paths,
    ):
        messages.extend(check())
    return messages


def main() -> int:
    try:
        messages = run_checks()
    except (InvariantFailure, subprocess.CalledProcessError) as exc:
        print("FAIL release invariants")
        print(f"  {exc}")
        return 1

    for message in messages:
        print(f"PASS {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
