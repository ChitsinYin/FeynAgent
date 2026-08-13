"""Check local FeynAgent initialization state for the Codex skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


REQUIRED_FILES = [
    Path(".feynagent/environment.yaml"),
    Path(".feynagent/capability_report.json"),
    Path(".feynagent/reference_index.json"),
]


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def inspect_initialization(root: Path) -> dict[str, Any]:
    missing = [str(path) for path in REQUIRED_FILES if not (root / path).exists()]
    env_path = root / ".feynagent" / "environment.yaml"
    env = _load_yaml(env_path) if env_path.exists() else {}
    missing_paths = []
    if not env.get("wolframscript"):
        missing_paths.append("--wolframscript")
    feyncalc = env.get("feyncalc", {})
    if env and not feyncalc.get("directory"):
        missing_paths.append("--feyncalc-dir")
    capabilities_path = root / ".feynagent" / "capability_report.json"
    capabilities = {}
    if capabilities_path.exists():
        capabilities = json.loads(capabilities_path.read_text(encoding="utf-8"))
    status = capabilities.get("status") or ("MISSING" if missing else "UNKNOWN")
    action = "ready"
    if missing:
        action = "run python -m feynagent init"
    elif status not in {"PASS", "WARNING"}:
        action = "run python -m feynagent doctor, then re-run init with only the missing explicit path"
    return {
        "status": status,
        "ready": not missing and status in {"PASS", "WARNING"},
        "missing_files": missing,
        "missing_cli_options": missing_paths,
        "action": action,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    result = inspect_initialization(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
