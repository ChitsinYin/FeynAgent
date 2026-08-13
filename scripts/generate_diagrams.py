"""Generate deterministic v0.1.1 tree-level 2->2 DiagramIR."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.diagrams import DiagramGenerationError, generate_tree_2_to_2


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


def _dump_yaml(path: Path, data: dict) -> None:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: PyYAML. Install manually with: python -m pip install -e .[dev]"
        ) from exc

    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def _validate(schema_name: str, instance: dict) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: jsonschema. Install manually with: python -m pip install -e .[dev]"
        ) from exc

    import json

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
    parser.add_argument("--rule-registry", required=True, type=Path)
    parser.add_argument("--backend-profile", type=Path, help="BackendProfile resolving the backend-neutral PhysicsCard")
    parser.add_argument("--output", required=True, type=Path, help="Output directory")
    args = parser.parse_args(argv)

    physics = _load_yaml(args.physics_card)
    convention = _load_yaml(args.convention_card)
    rules = _load_yaml(args.rule_registry)
    backend_profile = _load_yaml(args.backend_profile) if args.backend_profile else None

    try:
        _validate("physics_card.schema.json", physics)
        _validate("convention_card.schema.json", convention)
        _validate("rule_registry.schema.json", rules)
        if backend_profile is not None:
            _validate("backend_profile.schema.json", backend_profile)
        generated = generate_tree_2_to_2(physics, convention, rules, backend_profile)
        _validate("diagram_ir.schema.json", generated)
    except DiagramGenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    args.output.mkdir(parents=True, exist_ok=True)
    output_file = args.output / "generated_diagrams.yaml"
    if output_file.exists():
        print(f"ERROR: refusing to overwrite existing output file: {output_file}", file=sys.stderr)
        return 1

    _dump_yaml(output_file, generated)
    channels = ", ".join(diagram["channel"] for diagram in generated["diagrams"]) or "none"
    print(f"generated {len(generated['diagrams'])} diagram(s): {channels}")
    print(f"wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


