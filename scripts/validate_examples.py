"""Validate benchmark YAML examples against the FeynAgent JSON Schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXAMPLES = [
    ("benchmarks/B02_compton/physics_card.yaml", "schemas/physics_card.schema.json"),
    ("benchmarks/B02_compton/convention_card.yaml", "schemas/convention_card.schema.json"),
    ("benchmarks/B02_compton/rule_manifest.yaml", "schemas/rule_registry.schema.json"),
    ("benchmarks/B02_compton/diagrams.yaml", "schemas/diagram_ir.schema.json"),
    ("rules/qed/qed_tree_v1.yaml", "schemas/rule_registry.schema.json"),
]


def _format_path(path_parts: object) -> str:
    parts = list(path_parts)
    if not parts:
        return "$"
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def main() -> int:
    missing = []
    try:
        import yaml
    except ImportError:
        yaml = None
        missing.append("PyYAML")

    try:
        import jsonschema
    except ImportError:
        jsonschema = None
        missing.append("jsonschema")

    if missing:
        print("Missing validation dependencies: " + ", ".join(missing), file=sys.stderr)
        print("Install with: python -m pip install -e .[dev]", file=sys.stderr)
        return 2

    failures = 0
    for example_path, schema_path in EXAMPLES:
        example_file = ROOT / example_path
        schema_file = ROOT / schema_path

        with schema_file.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        with example_file.open("r", encoding="utf-8") as handle:
            instance = yaml.safe_load(handle)

        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator = validator_cls(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))

        if errors:
            failures += len(errors)
            print(f"FAIL {example_path}")
            for error in errors:
                print(f"  {_format_path(error.path)}: {error.message}")
        else:
            print(f"PASS {example_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
