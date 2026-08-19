"""Audited custom backend adapter for the single locked B04 process."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..b04_amplitudes import run_b04_amplitude_closure
from ..b04_topology import load_yaml, run_b04_topology_phase, sha256_file
from ..custom_knowledge import AVAILABLE, registered_root_for_model, verify_knowledge_lock
from ..dispatch import B04_CONVENTION_ID, B04_CUSTOM_BACKEND, B04_MODEL_ID, B04_PROCESS_ID, BackendRoute

REQUIRED_CUSTOM_OPERATIONS = {"schema_validation", "diagram_generation", "amplitude_generation", "latex_render"}


class B04CustomBackendError(RuntimeError):
    """Raised when an audited B04 execution gate fails."""


def validate_b04_custom_execution(
    repo_root: Path,
    physics_card: dict[str, Any],
    backend_profile: dict[str, Any],
    execution_request: dict[str, Any],
    route: BackendRoute,
) -> dict[str, Any]:
    if route.backend_id != B04_CUSTOM_BACKEND:
        raise B04CustomBackendError("custom backend received a non-B04 route")
    if physics_card.get("model_id") != B04_MODEL_ID or physics_card.get("process_id") != B04_PROCESS_ID:
        raise B04CustomBackendError("custom backend is restricted to the locked B04 model/process")
    if execution_request.get("status") != "approved":
        raise B04CustomBackendError("B04 custom execution requires an approved ExecutionRequest")
    if execution_request.get("physics_card_id") != physics_card.get("object_id"):
        raise B04CustomBackendError("ExecutionRequest does not link the B04 PhysicsCard")
    if execution_request.get("backend_profile_id") != backend_profile.get("backend_profile_id"):
        raise B04CustomBackendError("ExecutionRequest does not link the audited B04 backend profile")

    allowed = set(execution_request.get("allowed_operations", []))
    missing_operations = sorted(REQUIRED_CUSTOM_OPERATIONS - allowed)
    if missing_operations:
        raise B04CustomBackendError(f"ExecutionRequest is missing B04 operation(s): {missing_operations}")

    verification = verify_knowledge_lock(model_id=B04_MODEL_ID)
    if verification.status != AVAILABLE:
        raise B04CustomBackendError(f"registered B04 knowledge is not available: {verification.status}")
    external_root = registered_root_for_model(B04_MODEL_ID)
    if external_root is None:
        raise B04CustomBackendError("registered B04 external knowledge package is unresolved")

    lock_path = external_root / "KNOWLEDGE_LOCK.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    benchmark_manifest = load_yaml(repo_root / "benchmarks" / "B04_phi_phi_to_hh" / "knowledge_manifest.yaml")
    profile_custom = backend_profile.get("custom", {})
    convention_values = {
        "profile": profile_custom.get("convention_id"),
        "benchmark_manifest": benchmark_manifest.get("convention_id"),
        "knowledge_lock": lock.get("convention_id"),
    }
    if set(convention_values.values()) != {B04_CONVENTION_ID}:
        raise B04CustomBackendError(f"B04 convention lock mismatch: {convention_values}")
    if profile_custom.get("rule_audit_required") is not True:
        raise B04CustomBackendError("B04 backend profile must require a rule audit")

    return {
        "status": "PASS",
        "knowledge_status": verification.status,
        "checked_hashes": verification.checked_hashes,
        "knowledge_lock_sha256": sha256_file(lock_path),
        "convention_id": B04_CONVENTION_ID,
        "convention_lock": "PASS",
        "execution_request": "PASS",
        "required_operations": sorted(REQUIRED_CUSTOM_OPERATIONS),
    }


def run_b04_custom_backend(
    repo_root: Path,
    *,
    run_id: str,
    run_dir: Path,
    physics_card: dict[str, Any],
    backend_profile: dict[str, Any],
    execution_request: dict[str, Any],
    route: BackendRoute,
) -> dict[str, Any]:
    gate = validate_b04_custom_execution(repo_root, physics_card, backend_profile, execution_request, route)

    topology = run_b04_topology_phase(repo_root, run_id=run_id, run_root=run_dir.parent)
    if not all((topology.knowledge_lock_match, topology.topology_comparison_pass, topology.rule_usage_audit_pass, topology.diagram_pdf_pass)):
        raise B04CustomBackendError("B04 topology or rule-usage audit failed")

    amplitudes = run_b04_amplitude_closure(repo_root, run_id=run_id, run_root=run_dir.parent)
    conflicts = {name: status for name, status in amplitudes.classifications.items() if status == "CONFLICT_REQUIRES_REVIEW"}
    if conflicts:
        raise B04CustomBackendError(f"B04 amplitude conflicts block execution: {conflicts}")

    amplitude_validation_path = run_dir / "validation" / "amplitude_validation.json"
    amplitude_validation = json.loads(amplitude_validation_path.read_text(encoding="utf-8"))
    if amplitude_validation.get("rule_usage_audit") != "PASS":
        raise B04CustomBackendError("B04 rule audit is not PASS")

    allowed = set(execution_request.get("allowed_operations", []))
    m2_authorized = {"m2_regression", "polarization_sums"}.issubset(allowed)
    m2_policy = {
        "status": "AUTHORIZED_SEPARATE_MANUAL_RUN" if m2_authorized else "NOT_AUTHORIZED",
        "executed": False,
        "automatic_execution": False,
        "required_operations": ["m2_regression", "polarization_sums"],
        "requires_no_amplitude_conflicts": True,
        "layer": "REDUCED_NR_TT",
        "notes": "Heavy custom M2 remains a separate deterministic Wolfram/FeynCalc run and is never implied by topology/amplitude authorization.",
    }
    validation_report = {
        "schema_version": "0.1.0",
        "process_id": B04_PROCESS_ID,
        "backend_id": B04_CUSTOM_BACKEND,
        "status": "PASS",
        "checks": [
            {"name": "knowledge_package_resolution", "status": gate["knowledge_status"]},
            {"name": "convention_lock", "status": gate["convention_lock"]},
            {"name": "rule_usage_audit", "status": amplitude_validation["rule_usage_audit"]},
            {"name": "topology_comparison", "status": amplitude_validation["topology_comparison"]},
            {"name": "per_diagram_amplitudes", "status": "PASS", "count": len(amplitudes.classifications)},
            {"name": "m2_policy", "status": "PASS", "policy": m2_policy["status"]},
        ],
    }
    return {
        "status": "PASS",
        "backend_id": B04_CUSTOM_BACKEND,
        "backend_kind": route.backend_kind,
        "classification": route.classification,
        "standard_qed_authority": False,
        "knowledge_gate": gate,
        "topology": {
            "status": "PASS",
            "diagram_count": topology.generated_topology_count,
            "diagram_pdf": str(topology.run_dir.joinpath("diagrams", "diagrams.pdf").relative_to(run_dir)).replace("\\", "/"),
            "rule_usage_audit": "PASS",
        },
        "amplitudes": {
            "status": "PASS",
            "per_diagram_count": len(amplitudes.classifications),
            "classifications": amplitudes.classifications,
            "directory": "amplitudes",
            "pdf": "amplitudes/amplitudes.pdf",
        },
        "m2_policy": m2_policy,
        "validation_report": validation_report,
    }
