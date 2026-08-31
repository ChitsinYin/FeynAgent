"""Deterministic runner for native QED and the single audited B04 route."""

from __future__ import annotations

import argparse
import hashlib
import json
from importlib import resources
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .backends import (
    NativeBackendError,
    backend_config_from_dict,
    native_qed_bremsstrahlung_plan,
    native_qed_channel_plan,
    run_native_qed_backend,
    run_native_qed_m2_generator,
    validate_native_qed_artifacts,
    validate_native_qed_request,
)
from .backends.b04_custom import B04CustomBackendError, run_b04_custom_backend, validate_b04_custom_execution
from .custom_knowledge import AVAILABLE, discover_custom_model_ids
from .dispatch import B04_CUSTOM_BACKEND, B04_MODEL_ID, B04_PROCESS_ID, NATIVE_QED_BACKEND, DispatchError, resolve_backend_route
from .init import probe_environment

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


ROOT = Path(__file__).resolve().parents[2]
GOLD_M2_BY_PROCESS_ID = {
    "process:b01_ee_to_mumu": '2*SMP["e"]^4*(t^2 + u^2)/s^2',
    "process:b02_compton": '(-2*SMP["e"]^4*(s^2 + u^2))/(s*u)',
    "process:b03_emu_to_emu": '2*SMP["e"]^4*(s^2 + u^2)/t^2',
}
INPUT_NAMES = {
    "physics_card": "physics_card.yaml",
    "backend_profile": "backend_profile.yaml",
    "execution_request": "execution_request.yaml",
}


@dataclass(frozen=True)
class RunnerResult:
    """Public runner result returned to the CLI layer."""

    status: str
    run_id: str | None
    run_dir: Path | None
    manifest: dict[str, Any]

    @property
    def exit_code(self) -> int:
        return 0 if self.status == "PASS" else 1


def run_cli(args: argparse.Namespace) -> int:
    """Execute the deterministic runner and print a compact machine location."""

    result = run_from_files(
        physics_card_path=Path(args.physics_card),
        backend_profile_path=Path(args.backend_profile),
        execution_request_path=Path(args.execution_request),
        run_root=Path(args.run_root),
    )
    if result.run_dir is not None:
        print(f"FeynAgent run: {result.status}")
        print(f"run_id: {result.run_id}")
        print(f"run_dir: {result.run_dir}")
        print(f"manifest: {result.run_dir / 'run_manifest.json'}")
    else:
        print(f"FeynAgent run: {result.status}", file=sys.stderr)
        for gate in result.manifest.get("gates", []):
            if gate.get("status") == "FAIL":
                print(f"{gate['name']}: {gate.get('message', 'failed')}", file=sys.stderr)
    return result.exit_code


def run_from_files(
    *,
    physics_card_path: Path,
    backend_profile_path: Path,
    execution_request_path: Path,
    run_root: Path = Path("runs"),
) -> RunnerResult:
    """Run the deterministic native standard-QED pipeline from immutable files."""

    started_at = _now()
    run_id: str | None = None
    run_dir: Path | None = None
    gates: list[dict[str, Any]] = []
    manifest: dict[str, Any] = {
        "schema_version": "0.1.0",
        "runner": "feynagent.deterministic_dispatch_v0_2",
        "started_at": started_at,
        "status": "FAIL",
        "gates": gates,
    }

    try:
        _require_runtime_dependencies()
        physics_card = _load_structured(physics_card_path)
        backend_profile = _load_structured(backend_profile_path)
        execution_request = _load_structured(execution_request_path)
        _validate_schema(physics_card, "physics_card.schema.json")
        _validate_schema(backend_profile, "backend_profile.schema.json")
        _validate_schema(execution_request, "execution_request.schema.json")
        gates.append(_gate("structured_input_validation", "PASS"))

        _validate_request_links(physics_card, backend_profile, execution_request)
        gates.append(_gate("execution_request_links", "PASS"))

        b04_request_root = _resolve_b04_request_root(physics_card_path, physics_card)
        benchmark_root = b04_request_root / "benchmarks" if b04_request_root is not None else ROOT / "benchmarks"
        route = resolve_backend_route(
            physics_card,
            backend_profile,
            custom_model_ids=discover_custom_model_ids(benchmark_root),
        )
        gates.append(_gate("backend_dispatch", "PASS", route.as_dict()))

        doctor = probe_environment(argparse.Namespace(wolframscript=None, feyncalc_dir=None, timeout=60))
        if route.backend_id == NATIVE_QED_BACKEND:
            doctor_ready = doctor.status in {"PASS", "WARNING"} and (
                doctor.capabilities.get("checks", {}).get("native_qed_tree_capability", {}).get("status") == "PASS"
            )
            if not doctor_ready:
                raise RunnerGateError("doctor_readiness", "native_qed_tree_capability is not ready", {"doctor_status": doctor.status})
            config = backend_config_from_dict(backend_profile)
            validate_native_qed_request(physics_card, config)
            _validate_native_generation_authorization(physics_card, execution_request)
            gates.append(_gate("doctor_readiness", "PASS", {"doctor_status": doctor.status, "route": "standard_native"}))
            gates.append(_gate("backend_resolution", "PASS", {"backend_id": config.backend_id}))
            gates.append(_gate("native_generation_authorization", "PASS"))
        else:
            custom_repo_root = b04_request_root
            if custom_repo_root is None:
                raise RunnerGateError(
                    "repository_context",
                    "B04 repository root could not be resolved from the supplied PhysicsCard path",
                    {"physics_card_path": str(physics_card_path)},
                )
            custom_capability = _custom_model_capability(doctor.capabilities, route.model_id)
            if custom_capability.get("status") != AVAILABLE:
                status = custom_capability.get("status", "UNKNOWN")
                raise RunnerGateError("doctor_readiness", f"B04 custom knowledge status: {status}", custom_capability)
            custom_gate = validate_b04_custom_execution(custom_repo_root, physics_card, backend_profile, execution_request, route)
            gates.append(_gate("doctor_readiness", "PASS", {"doctor_status": doctor.status, "route": "custom_audited"}))
            gates.append(_gate("custom_knowledge_and_convention", "PASS", custom_gate))
            gates.append(_gate("backend_resolution", "PASS", {"backend_id": route.backend_id}))
            gates.append(_gate("custom_execution_authorization", "PASS"))

        run_id = _new_run_id(physics_card)
        run_dir = (run_root / run_id).resolve()
        run_dir.mkdir(parents=True, exist_ok=False)
        copied_inputs = _copy_inputs(
            run_dir,
            {
                "physics_card": physics_card_path,
                "backend_profile": backend_profile_path,
                "execution_request": execution_request_path,
            },
        )
        manifest.update(
            {
                "run_id": run_id,
                "run_dir": str(run_dir),
                "process_id": physics_card.get("process_id"),
                "backend_profile_id": backend_profile.get("backend_profile_id"),
                "dispatch": route.as_dict(),
                "inputs": copied_inputs,
            }
        )
        gates.append(_gate("immutable_input_snapshot", "PASS"))

        if route.backend_id == NATIVE_QED_BACKEND:
            native_manifest = run_native_qed_backend(physics_card, run_dir, config)
            native_status = "PASS" if native_manifest.get("exit_code") == 0 and not native_manifest.get("artifact_validation") else "FAIL"
            if native_status != "PASS":
                raise RunnerGateError("native_artifact_generation", "native backend artifact generation failed", native_manifest)
            gates.append(_gate("native_artifact_generation", "PASS"))

            gold_expression = GOLD_M2_BY_PROCESS_ID.get(physics_card.get("process_id"))
            try:
                m2_manifest = run_native_qed_m2_generator(
                    physics_card,
                    run_dir,
                    config,
                    execution_request,
                    gold_expression=gold_expression,
                )
            except NativeBackendError as exc:
                raise RunnerGateError("m2_authorization", str(exc)) from exc
            if m2_manifest.get("executed") and m2_manifest.get("status") != "PASS":
                raise RunnerGateError("m2_generation", "M2 execution failed", m2_manifest)
            gates.append(_gate("m2_generation", "PASS", {"status": m2_manifest.get("status"), "executed": m2_manifest.get("executed")}))

            validation_report = _build_validation_report(physics_card, run_dir, native_manifest, m2_manifest)
            manifest_updates = {"native_manifest": native_manifest, "m2_manifest": m2_manifest}
        else:
            try:
                custom_manifest = run_b04_custom_backend(
                    custom_repo_root,
                    run_id=run_id,
                    run_dir=run_dir,
                    physics_card=physics_card,
                    backend_profile=backend_profile,
                    execution_request=execution_request,
                    route=route,
                )
            except B04CustomBackendError as exc:
                raise RunnerGateError("custom_backend", str(exc)) from exc
            if custom_manifest.get("status") != "PASS":
                raise RunnerGateError("custom_backend", "B04 custom backend failed", custom_manifest)
            gates.append(_gate("custom_topology_generation", "PASS", custom_manifest["topology"]))
            gates.append(_gate("custom_per_diagram_amplitudes", "PASS", custom_manifest["amplitudes"]))
            gates.append(_gate("custom_m2_policy", "PASS", custom_manifest["m2_policy"]))
            validation_report = custom_manifest["validation_report"]
            manifest_updates = {"custom_manifest": custom_manifest, "m2_policy": custom_manifest["m2_policy"]}

        _write_json(run_dir / "validation_report.json", validation_report)
        if validation_report["status"] != "PASS":
            raise RunnerGateError("validation_report", "validation report contains failed checks", validation_report)
        gates.append(_gate("validation_report", "PASS"))

        manifest.update({"status": "PASS", "completed_at": _now(), "validation_report": "validation_report.json", **manifest_updates})
        manifest["outputs"] = _hash_output_tree(run_dir)
        _write_json(run_dir / "run_manifest.json", manifest)
        return RunnerResult(status="PASS", run_id=run_id, run_dir=run_dir, manifest=manifest)
    except RunnerGateError as exc:
        gates.append(_gate(exc.gate, "FAIL", exc.details, exc.message))
        manifest.update({"status": "FAIL", "completed_at": _now(), "failure": exc.to_dict()})
    except subprocess.TimeoutExpired as exc:
        details = {"cmd": exc.cmd, "timeout": exc.timeout}
        gates.append(_gate("timeout", "FAIL", details, "subprocess timed out"))
        manifest.update({"status": "FAIL", "completed_at": _now(), "failure": {"gate": "timeout", **details}})
    except (B04CustomBackendError, DispatchError, NativeBackendError, ValueError, OSError) as exc:
        gates.append(_gate("runner_exception", "FAIL", message=str(exc)))
        manifest.update({"status": "FAIL", "completed_at": _now(), "failure": {"gate": "runner_exception", "message": str(exc)}})

    if run_dir is not None:
        manifest.setdefault("run_id", run_id)
        manifest.setdefault("run_dir", str(run_dir))
        manifest["outputs"] = _hash_output_tree(run_dir)
        _write_json(run_dir / "run_manifest.json", manifest)
    return RunnerResult(status="FAIL", run_id=run_id, run_dir=run_dir, manifest=manifest)


class RunnerGateError(RuntimeError):
    """Raised for deterministic runner gate failures."""

    def __init__(self, gate: str, message: str, details: Any | None = None):
        super().__init__(message)
        self.gate = gate
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        return {"gate": self.gate, "message": self.message, "details": self.details}


def _require_runtime_dependencies() -> None:
    missing = []
    if yaml is None:
        missing.append("PyYAML")
    if jsonschema is None:
        missing.append("jsonschema")
    if missing:
        raise RunnerGateError("runner_dependencies", "missing runner validation dependencies", {"missing": missing})


def _load_structured(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RunnerGateError("structured_input_validation", f"input file does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise RunnerGateError("structured_input_validation", f"input file must contain an object: {path}")
    return data


def _validate_schema(instance: dict[str, Any], schema_name: str) -> None:
    schema = _load_schema(schema_name)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in first.path)
        raise RunnerGateError("structured_input_validation", f"{schema_name} validation failed at {path}: {first.message}")


def _load_schema(schema_name: str) -> dict[str, Any]:
    source_tree_schema = ROOT / "schemas" / schema_name
    if source_tree_schema.exists():
        with source_tree_schema.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    try:
        payload = resources.files("feynagent.schemas").joinpath(schema_name).read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError) as exc:
        raise RunnerGateError("structured_input_validation", f"packaged schema not found: {schema_name}") from exc
    return json.loads(payload)


def _validate_request_links(physics_card: dict[str, Any], backend_profile: dict[str, Any], execution_request: dict[str, Any]) -> None:
    if execution_request.get("physics_card_id") != physics_card.get("object_id"):
        raise RunnerGateError("execution_request_links", "ExecutionRequest physics_card_id does not match PhysicsCard object_id")
    if execution_request.get("backend_profile_id") != backend_profile.get("backend_profile_id"):
        raise RunnerGateError("execution_request_links", "ExecutionRequest backend_profile_id does not match BackendProfile backend_profile_id")
    if execution_request.get("status") != "approved":
        raise RunnerGateError("execution_request_links", "ExecutionRequest must be approved for the public runner")


def _resolve_b04_request_root(physics_card_path: Path, physics_card: dict[str, Any]) -> Path | None:
    if physics_card.get("model_id") != B04_MODEL_ID or physics_card.get("process_id") != B04_PROCESS_ID:
        return None
    resolved_card = physics_card_path.resolve()
    for parent in (resolved_card.parent, *resolved_card.parents):
        benchmark_root = parent / "benchmarks"
        expected_card = benchmark_root / "B04_phi_phi_to_hh" / "physics_card.yaml"
        if benchmark_root.is_dir() and expected_card.is_file() and expected_card.resolve() == resolved_card:
            return parent
    raise RunnerGateError(
        "repository_context",
        "B04 repository root could not be resolved from the supplied PhysicsCard path",
        {"physics_card_path": str(physics_card_path)},
    )


def _validate_native_generation_authorization(
    physics_card: dict[str, Any], execution_request: dict[str, Any]
) -> None:
    allowed = set(execution_request.get("allowed_operations", []))
    required = {"schema_validation", "diagram_generation", "amplitude_generation", "latex_render", "feyncalc_smoke"}
    if physics_card.get("process_type") == "scattering_2_to_3":
        required.update({"ward_identity", "soft_limit_check"})
    missing = sorted(required - allowed)
    if missing:
        raise RunnerGateError("native_generation_authorization", "ExecutionRequest is missing native generation operation(s)", {"missing": missing})


def _custom_model_capability(capabilities: dict[str, Any], model_id: str) -> dict[str, Any]:
    for item in capabilities.get("custom_models", []):
        if item.get("model_id") == model_id:
            return item
    return {"model_id": model_id, "status": "MISSING_KNOWLEDGE", "issues": ["custom model absent from doctor report"]}


def _new_run_id(physics_card: dict[str, Any]) -> str:
    process = str(physics_card.get("process_id", "process:unknown")).split(":", 1)[-1].replace(":", "_").replace("/", "_")
    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    return f"{stamp}_{process}_{uuid.uuid4().hex[:8]}"


def _copy_inputs(run_dir: Path, inputs: dict[str, Path]) -> dict[str, dict[str, Any]]:
    input_dir = run_dir / "inputs"
    input_dir.mkdir(parents=True, exist_ok=True)
    copied: dict[str, dict[str, Any]] = {}
    for key, source in inputs.items():
        target = input_dir / INPUT_NAMES[key]
        shutil.copy2(source, target)
        copied[key] = {
            "source_path": str(source.resolve()),
            "run_path": str(target.relative_to(run_dir)).replace("\\", "/"),
            "sha256": _sha256(target),
            "bytes": target.stat().st_size,
        }
    return copied


def _build_validation_report(
    physics_card: dict[str, Any],
    run_dir: Path,
    native_manifest: dict[str, Any],
    m2_manifest: dict[str, Any],
) -> dict[str, Any]:
    artifact_issues = validate_native_qed_artifacts(run_dir, physics_card)
    amplitudes = native_manifest.get("amplitudes", {})
    m2_status = m2_manifest.get("status")
    if physics_card.get("process_type") == "scattering_2_to_3":
        plan = native_qed_bremsstrahlung_plan(physics_card)
        expected_count = len(plan)
        topology_key = "classification_count"
        topology_name = "external_leg_bremsstrahlung_count"
        expected_metadata = [
            {
                "emission_leg": item.emission_leg,
                "emission_particle": item.emission_particle,
                "exchanged_virtual_particle": item.exchanged_virtual_particle,
                "radiating_fermion_routing": item.radiating_fermion_routing,
                "exchange_routing": item.exchange_routing,
            }
            for item in plan
        ]
        extra_checks = [
            {
                "name": "topology_comparison",
                "status": amplitudes.get("topology_comparison", {}).get("status", "FAIL"),
            },
            {
                "name": "total_amplitude_ward_identity",
                "status": amplitudes.get("ward_identity", {}).get("status", "FAIL"),
                "details": amplitudes.get("ward_identity", {}),
            },
            {
                "name": "soft_photon_structural_limit",
                "status": amplitudes.get("soft_limit", {}).get("status", "FAIL"),
                "details": amplitudes.get("soft_limit", {}),
            },
        ]
    else:
        plan = native_qed_channel_plan(physics_card)
        expected_count = len(plan)
        topology_key = "channel_count"
        topology_name = "channel_count"
        expected_metadata = [channel.channel for channel in plan]
        extra_checks = []
    checks = [
        {"name": "diagram_count", "status": "PASS" if amplitudes.get("diagram_count") == expected_count else "FAIL"},
        {"name": topology_name, "status": "PASS" if amplitudes.get(topology_key) == expected_count else "FAIL"},
        {
            "name": "per_diagram_amplitude_count",
            "status": "PASS" if amplitudes.get("per_diagram_amplitude_count") == expected_count else "FAIL",
        },
        {"name": "artifact_contract", "status": "PASS" if not artifact_issues else "FAIL", "issues": artifact_issues},
        {"name": "m2_artifact", "status": "PASS" if m2_status in {"PASS", "SCRIPT_GENERATED_ONLY"} else "FAIL", "m2_status": m2_status},
        *extra_checks,
    ]
    report = {
        "schema_version": "0.1.0",
        "generated_at": _now(),
        "process_id": physics_card.get("process_id"),
        "status": "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL",
        "checks": checks,
    }
    if physics_card.get("process_type") == "scattering_2_to_3":
        report["expected_diagram_metadata"] = expected_metadata
    else:
        report["expected_channels"] = expected_metadata
    return report


def _hash_output_tree(run_dir: Path) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for path in sorted(run_dir.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(run_dir)).replace("\\", "/")
            outputs[rel] = {"sha256": _sha256(path), "bytes": path.stat().st_size}
    return outputs


def _gate(name: str, status: str, details: Any | None = None, message: str | None = None) -> dict[str, Any]:
    gate = {"name": name, "status": status}
    if message:
        gate["message"] = message
    if details is not None:
        gate["details"] = details
    return gate


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8", newline="\n")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _now() -> str:
    return datetime.now().astimezone().isoformat()
