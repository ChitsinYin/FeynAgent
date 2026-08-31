"""Validate FeynAgent benchmark examples and shared backend profiles."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_ROOT = ROOT / "benchmarks"
SHARED_NATIVE_PROFILE = ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml"
SHARED_LEGACY_PROFILE = ROOT / "profiles" / "backends" / "legacy_sm_qed.yaml"
QED_RULE_REGISTRY = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"

BASE_SCHEMA_VALIDATIONS = [
    (QED_RULE_REGISTRY, ROOT / "schemas" / "rule_registry.schema.json"),
    (SHARED_NATIVE_PROFILE, ROOT / "schemas" / "backend_profile.schema.json"),
    (SHARED_LEGACY_PROFILE, ROOT / "schemas" / "backend_profile.schema.json"),
]

REQUIRED_BENCHMARK_IDS = {
    "B01_ee_to_mumu",
    "B02_compton",
    "B03_emu_to_emu",
    "B04_phi_phi_to_hh",
    "B05_emu_to_emu_gamma",
}


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


def _validate_schema(
    instance_path: Path,
    schema_path: Path,
    yaml: Any,
    jsonschema: Any,
) -> int:
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    instance = _load_yaml(instance_path, yaml)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: list(error.path),
    )

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
        _require(
            profile.get("backend_kind") == "feynarts_feyncalc_native",
            "backend_kind must be feynarts_feyncalc_native",
        )
        _require(
            profile.get("resolves", {}).get("model_id") == "sm_qed",
            "profile must resolve model_id sm_qed",
        )
        _require(
            profile.get("resolves", {}).get("sector") == "qed",
            "profile must resolve sector qed",
        )

        feynarts = profile.get("native", {}).get("feynarts", {})
        _require(feynarts.get("model") == "SM", "model must be SM")
        _require(
            feynarts.get("generic_model") == "Lorentz",
            "generic_model must be Lorentz",
        )
        _require(
            feynarts.get("restrictions") == "QEDOnly",
            "restrictions must be QEDOnly",
        )
        _require(
            feynarts.get("insertion_level") == "Classes",
            "insertion_level must be Classes",
        )
        _require(
            isinstance(feynarts.get("exclude_topologies"), list),
            "exclude_topologies must be a list",
        )

        mapped = {
            item.get("particle_id")
            for item in feynarts.get("particle_mappings", [])
        }
        _require(
            {"e-", "e+", "mu-", "mu+", "gamma"}.issubset(mapped),
            "native particle mappings must cover the validated QED particle set",
        )
    except (OSError, ValidationFailure) as exc:
        print(f"FAIL {_relative(SHARED_NATIVE_PROFILE)}")
        print(f"  $: {exc}")
        return 1

    print(f"PASS {_relative(SHARED_NATIVE_PROFILE)}")
    return 0


def _validate_legacy_profile(yaml: Any) -> int:
    try:
        profile = _load_yaml(SHARED_LEGACY_PROFILE, yaml)
        _require(
            profile.get("backend_kind") == "legacy_custom_backend",
            "backend_kind must be legacy_custom_backend",
        )
        _require(
            profile.get("resolves", {}).get("model_id") == "sm_qed",
            "profile must resolve model_id sm_qed",
        )
        _require(
            profile.get("resolves", {}).get("sector") == "qed",
            "profile must resolve sector qed",
        )

        registry = profile.get("legacy", {}).get("rule_registry", {})
        _require(
            registry.get("registry_id") == "registry:qed_tree_v1",
            "legacy profile must resolve registry:qed_tree_v1",
        )

        resolved = (
            SHARED_LEGACY_PROFILE.parent
            / registry.get("relative_path", "")
        ).resolve()
        _require(
            resolved == QED_RULE_REGISTRY.resolve(),
            "legacy profile relative_path must resolve to rules/qed/qed_tree_v1.yaml",
        )
        _require(
            "ruleset:qed_tree_v1" in registry.get("rule_set_ids", []),
            "legacy profile must select ruleset:qed_tree_v1",
        )
    except (OSError, ValidationFailure) as exc:
        print(f"FAIL {_relative(SHARED_LEGACY_PROFILE)}")
        print(f"  $: {exc}")
        return 1

    print(f"PASS {_relative(SHARED_LEGACY_PROFILE)}")
    return 0


def _validate_native_expected(path: Path, yaml: Any) -> int:
    try:
        native = _load_yaml(path, yaml)
        _require(
            isinstance(native, dict),
            "native_expected.yaml must contain a mapping",
        )
        _require(
            native.get("expected_native_backend")
            == "feynarts_feyncalc_native",
            "expected_native_backend must be feynarts_feyncalc_native",
        )

        profile_ref = native.get("backend_profile")
        _require(
            isinstance(profile_ref, str) and profile_ref,
            "backend_profile must be a non-empty string",
        )
        resolved_profile = (path.parent / profile_ref).resolve()
        _require(
            resolved_profile == SHARED_NATIVE_PROFILE.resolve(),
            "backend_profile must reference the shared FeynArts/FeynCalc QED profile",
        )

        physics_card_path = path.parent / "physics_card.yaml"
        _require(
            physics_card_path.exists(),
            "sibling physics_card.yaml must exist",
        )
        physics_card = _load_yaml(physics_card_path, yaml)
        _require(
            isinstance(physics_card, dict),
            "physics_card.yaml must contain a mapping",
        )

        particles = physics_card.get("particles", {})
        expected_incoming = particles.get("incoming", [])
        expected_outgoing = particles.get("outgoing", [])
        _require(
            isinstance(expected_incoming, list),
            "PhysicsCard incoming particles must be a list",
        )
        _require(
            isinstance(expected_outgoing, list),
            "PhysicsCard outgoing particles must be a list",
        )

        fields = native.get("expected_feynarts_fields")
        _require(
            isinstance(fields, dict),
            "expected_feynarts_fields must be a mapping",
        )
        _require(
            isinstance(fields.get("incoming"), list)
            and len(fields["incoming"]) == len(expected_incoming),
            (
                "incoming FeynArts fields must describe "
                f"{len(expected_incoming)} states"
            ),
        )
        _require(
            isinstance(fields.get("outgoing"), list)
            and len(fields["outgoing"]) == len(expected_outgoing),
            (
                "outgoing FeynArts fields must describe "
                f"{len(expected_outgoing)} states"
            ),
        )

        count = native.get("expected_diagram_count")
        _require(
            isinstance(count, int) and count > 0,
            "expected_diagram_count must be a positive integer",
        )

        official_example = native.get("official_example_id")
        expected_topology = native.get("expected_topology")

        has_official_example = (
            isinstance(official_example, str)
            and bool(official_example.strip())
        )
        has_explicit_topology_validation = (
            isinstance(expected_topology, str)
            and bool(expected_topology.strip())
        )
        _require(
            has_official_example or has_explicit_topology_validation,
            (
                "native benchmark must record a non-empty "
                "official_example_id or expected_topology"
            ),
        )

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
        _require(
            isinstance(rel, str) and rel,
            "canonical_registry.relative_path must be present",
        )
        resolved = (path.parent / rel).resolve()
        _require(
            resolved == QED_RULE_REGISTRY.resolve(),
            (
                "canonical_registry.relative_path must resolve to "
                "rules/qed/qed_tree_v1.yaml"
            ),
        )
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
        path
        for path in BENCHMARK_ROOT.iterdir()
        if (
            path.is_dir()
            and path.name.startswith("B")
            and (path / "physics_card.yaml").exists()
        )
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
        print(
            "Missing validation dependencies: " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "Install with: python -m pip install -e .[dev]",
            file=sys.stderr,
        )
        return 2

    failures = 0
    benchmarks = _discover_benchmarks()
    discovered_ids = {path.name for path in benchmarks}

    missing_required = sorted(REQUIRED_BENCHMARK_IDS - discovered_ids)
    if missing_required:
        failures += len(missing_required)
        for benchmark_id in missing_required:
            print(f"FAIL benchmarks/{benchmark_id}")
            print(
                "  $: required benchmark directory was not discovered"
            )

    schema_validations = list(BASE_SCHEMA_VALIDATIONS)

    for benchmark in benchmarks:
        schema_validations.append(
            (
                benchmark / "physics_card.yaml",
                ROOT / "schemas" / "physics_card.schema.json",
            )
        )

        convention = benchmark / "convention_card.yaml"
        if convention.exists():
            schema_validations.append(
                (
                    convention,
                    ROOT / "schemas" / "convention_card.schema.json",
                )
            )

        legacy = benchmark / "legacy"
        if legacy.exists():
            diagrams = legacy / "diagrams.yaml"
            if diagrams.exists():
                schema_validations.append(
                    (
                        diagrams,
                        ROOT / "schemas" / "diagram_ir.schema.json",
                    )
                )

            amplitude = legacy / "amplitude_ir.example.yaml"
            if amplitude.exists():
                schema_validations.append(
                    (
                        amplitude,
                        ROOT / "schemas" / "amplitude_ir.schema.json",
                    )
                )

    for example_path, schema_path in schema_validations:
        if not example_path.exists():
            print(f"FAIL {_relative(example_path)}")
            print("  $: file does not exist")
            failures += 1
            continue
        failures += _validate_schema(
            example_path,
            schema_path,
            yaml,
            jsonschema,
        )

    failures += _validate_native_profile(yaml)
    failures += _validate_legacy_profile(yaml)

    for benchmark in benchmarks:
        native_expected = benchmark / "native_expected.yaml"
        if native_expected.exists():
            failures += _validate_native_expected(native_expected, yaml)

        legacy_manifest = benchmark / "legacy" / "rule_manifest.yaml"
        if legacy_manifest.exists():
            failures += _validate_legacy_rule_manifest(
                legacy_manifest,
                yaml,
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
