"""Render DiagramIR 0.1.1 to deterministic TikZ-Feynman artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.render import RenderError, render_tikz_feynman


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: PyYAML. Install manually with: python -m pip install -e .[dev]"
        ) from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid YAML object: {path}")
    return data


def _validate(schema_name: str, instance: dict) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: jsonschema. Install manually with: python -m pip install -e .[dev]"
        ) from exc

    schema_path = ROOT / "schemas" / schema_name
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator_cls(schema).validate(instance)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physics-card", required=True, type=Path)
    parser.add_argument("--convention-card", required=True, type=Path)
    parser.add_argument("--diagram-ir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Output directory")
    parser.add_argument("--latex-command", default="lualatex")
    args = parser.parse_args(argv)

    physics = _load_yaml(args.physics_card)
    convention = _load_yaml(args.convention_card)
    diagram_ir = _load_yaml(args.diagram_ir)

    try:
        _validate("physics_card.schema.json", physics)
        _validate("convention_card.schema.json", convention)
        _validate("diagram_ir.schema.json", diagram_ir)
        manifest = render_tikz_feynman(
            physics,
            convention,
            diagram_ir,
            args.output,
            latex_command=args.latex_command,
        )
    except RenderError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"rendered {manifest['diagram_count']} diagram(s): {', '.join(manifest['channels'])}")
    print(f"wrote {manifest['outputs']['tex']}")
    print(f"wrote {manifest['outputs']['pdf']}")
    print(f"wrote {manifest['outputs']['manifest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
