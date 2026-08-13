"""Validate FeynAgent benchmark examples and shared Day-4 profiles."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_ROOT = ROOT / "benchmarks"
SHARED_NATIVE_PROFILE = ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml"
QED_RULE_REGISTRY = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"

SCHEMA_VALIDATIONS = [
    (QED_RULE_REGISTRY, ROOT / "schemas" / "rule_registry.schema.json"),
]

REQUIRED_BENCHMARK_IDS = {"B01_ee_to_mumu", "B02_compton", "B03_emu_to_emu"}


class ValidationFailure(Exception):
    """Raised for hand-written validations that do not have JSON Schemas yet."""


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


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_yaml(path: Path, yaml: Any) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _validate_schema(instance_path: Path, schema_path: Path, yaml: Any, jsonschema: Any) -> int:
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    instance = _load_yaml(instance_path, yaml)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))

    if errors:
        print(f"FAIL {_relative(instance_path)}")
        for error in errors:
            print(f"  {_format_path(error.path)}: {error.message}")
        return len(errors)

    print(f"PASS {_relative(instance_path)}")
    return 0


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def _validate_native_profile(yaml: Any) -> int:
    try:
        profile = _load_yaml(SHARED_NATIVE_PROFILE, yaml)
        _require(profile.get("backend_id") == "feynarts_feyncalc_native", "backend_id must be feynarts_feyncalc_native")
        _require(profile.get("model") == "SM", "model must be SM")
        _require(profile.get("generic_model") == "Lorentz", "generic_model must be Lorentz")
        _require(profile.get("restrictions") == "QEDOnly", "restrictions must be QEDOnly")
        _require(profile.get("insertion_level") == "Classes", "insertion_level must be Classes")
        _require(isinstance(profile.get("exclude_topologies"), list), "exclude_topologies must be a list")
    except (OSError, ValidationFailure) as exc:
        print(f"FAIL {_relative(SHARED_NATIVE_PROFILE)}")
        print(f"  $: {exc}")
        return 1

    print(f"PASS {_relative(SHARED_NATIVE_PROFILE)}")
    return 0


def _validate_native_expected(path: Path, yaml: Any) -> int:
    try:
        native = _load_yaml(path, yaml)
        _require(native.get("expected_native_backend") == "feynarts_feyncalc_native", "expected_native_backend must be feynarts_feyncalc_native")
        profile_ref = native.get("backend_profile")
        _require(isinstance(profile_ref, str) and profile_ref, "backend_profile must be a non-empty string")
        resolved_profile = (path.parent / profile_ref).resolve()
        _require(resolved_profile == SHARED_NATIVE_PROFILE.resolve(), "backend_profile must reference the shared FeynArts/FeynCalc QED profile")
        fields = native.get("expected_feynarts_fields")
        _require(isinstance(fields, dict), "expected_feynarts_fields must be a mapping")
        _require(isinstance(fields.get("incoming"), list) and len(fields["incoming"]) == 2, "incoming FeynArts fields must describe 2 states")
        _require(isinstance(fields.get("outgoing"), list) and len(fields["outgoing"]) == 2, "outgoing FeynArts fields must describe 2 states")
        count = native.get("expected_diagram_count")
        _require(isinstance(count, int) and count > 0, "expected_diagram_count must be a positive integer")
        _require(isinstance(native.get("official_example_id"), str) and native["official_example_id"], "official_example_id must be recorded")
    except (OSError, ValidationFailure) as exc:
        print(f"FAIL {_relative(path)}")
        print(f"  $: {exc}")
        return 1

    print(f"PASS {_relative(path)}")
    return 0


def _validate_legacy_rule_manifest(path: Path, yaml: Any) -> int:
    try:
        manifest = _load_yaml(path, yaml)
        registry = manifest.get("canonical_registry", {})
        rel = registry.get("relative_path")
        _require(isinstance(rel, str) and rel, "canonical_registry.relative_path must be present")
        resolved = (path.parent / rel).resolve()
        _require(resolved == QED_RULE_REGISTRY.resolve(), "canonical_registry.relative_path must resolve to rules/qed/qed_tree_v1.yaml")
    except (OSError, ValidationFailure) as exc:
        print(f"FAIL {_relative(path)}")
        print(f"  $: {exc}")
        return 1

    print(f"PASS {_relative(path)}")
    return 0


def _discover_benchmarks() -> list[Path]:
    if not BENCHMARK_ROOT.exists():
        return []
    return sorted(
        path for path in BENCHMARK_ROOT.iterdir()
        if path.is_dir() and path.name.startswith("B") and (path / "physics_card.yaml").exists()
    )


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
    benchmarks = _discover_benchmarks()
    discovered_ids = {path.name for path in benchmarks}
    missing_required = sorted(REQUIRED_BENCHMARK_IDS - discovered_ids)
    if missing_required:
        failures += len(missing_required)
        for benchmark_id in missing_required:
            print(f"FAIL benchmarks/{benchmark_id}")
            print("  $: required Day-4 benchmark directory was not discovered")

    for benchmark in benchmarks:
        SCHEMA_VALIDATIONS.append((benchmark / "physics_card.yaml", ROOT / "schemas" / "physics_card.schema.json"))
        convention = benchmark / "convention_card.yaml"
        if convention.exists():
            SCHEMA_VALIDATIONS.append((convention, ROOT / "schemas" / "convention_card.schema.json"))
        legacy = benchmark / "legacy"
        if legacy.exists():
            diagrams = legacy / "diagrams.yaml"
            if diagrams.exists():
                SCHEMA_VALIDATIONS.append((diagrams, ROOT / "schemas" / "diagram_ir.schema.json"))
            amplitude = legacy / "amplitude_ir.example.yaml"
            if amplitude.exists():
                SCHEMA_VALIDATIONS.append((amplitude, ROOT / "schemas" / "amplitude_ir.schema.json"))

    for example_path, schema_path in SCHEMA_VALIDATIONS:
        if not example_path.exists():
            print(f"FAIL {_relative(example_path)}")
            print("  $: file does not exist")
            failures += 1
            continue
        failures += _validate_schema(example_path, schema_path, yaml, jsonschema)

    failures += _validate_native_profile(yaml)

    for benchmark in benchmarks:
        native_expected = benchmark / "native_expected.yaml"
        if native_expected.exists():
            failures += _validate_native_expected(native_expected, yaml)
        legacy_manifest = benchmark / "legacy" / "rule_manifest.yaml"
        if legacy_manifest.exists():
            failures += _validate_legacy_rule_manifest(legacy_manifest, yaml)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
