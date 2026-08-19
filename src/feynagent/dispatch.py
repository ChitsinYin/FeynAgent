"""Backend routing policy for standard QED and the audited B04 exception."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .custom_knowledge import CUSTOM_AUDITED, STANDARD_NATIVE, classify_physics_card

NATIVE_QED_BACKEND = "feynarts_feyncalc_native"
B04_CUSTOM_BACKEND_KIND = "audited_custom_backend"
B04_CUSTOM_BACKEND = "direct_feyncalc_custom_audited"
B04_MODEL_ID = "reheating_scalar_gravity_v1"
B04_PROCESS_ID = "process:B04_phi_phi_to_h_h"
B04_CONVENTION_ID = "conventions:reheating_scalar_gravity_v1"


class DispatchError(ValueError):
    """Raised when no approved backend route exactly matches the request."""


@dataclass(frozen=True)
class BackendRoute:
    classification: str
    backend_kind: str
    backend_id: str
    model_id: str
    process_id: str
    standard_qed_authority: bool
    production_ready_scope: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "backend_kind": self.backend_kind,
            "backend_id": self.backend_id,
            "model_id": self.model_id,
            "process_id": self.process_id,
            "standard_qed_authority": self.standard_qed_authority,
            "production_ready_scope": self.production_ready_scope,
        }


def resolve_backend_route(
    physics_card: dict[str, Any],
    backend_profile: dict[str, Any],
    *,
    custom_model_ids: set[str] | None = None,
) -> BackendRoute:
    """Resolve only validated native QED or the exact locked B04 custom route."""

    classification = classify_physics_card(physics_card, custom_model_ids=custom_model_ids)
    model_id = str(physics_card.get("model_id", ""))
    process_id = str(physics_card.get("process_id", ""))
    backend_kind = str(backend_profile.get("backend_kind", ""))

    if classification == STANDARD_NATIVE:
        if backend_kind != NATIVE_QED_BACKEND:
            raise DispatchError("standard QED requires backend_kind feynarts_feyncalc_native")
        resolves = backend_profile.get("resolves", {})
        if resolves.get("model_id") != "sm_qed" or resolves.get("sector") != "qed":
            raise DispatchError("native QED backend profile does not resolve sm_qed/qed")
        return BackendRoute(
            classification=STANDARD_NATIVE,
            backend_kind=NATIVE_QED_BACKEND,
            backend_id=NATIVE_QED_BACKEND,
            model_id=model_id,
            process_id=process_id,
            standard_qed_authority=True,
            production_ready_scope="validated tree-level QED 2-to-2 only",
        )

    if classification == CUSTOM_AUDITED and model_id == B04_MODEL_ID and process_id == B04_PROCESS_ID:
        if physics_card.get("sector") != "gravity":
            raise DispatchError("B04 audited custom route requires sector gravity")
        if backend_kind != B04_CUSTOM_BACKEND_KIND:
            raise DispatchError("B04 requires backend_kind audited_custom_backend")
        custom = backend_profile.get("custom", {})
        expected = {
            "backend_id": B04_CUSTOM_BACKEND,
            "model_id": B04_MODEL_ID,
            "process_id": B04_PROCESS_ID,
            "convention_id": B04_CONVENTION_ID,
        }
        mismatches = {key: {"expected": value, "actual": custom.get(key)} for key, value in expected.items() if custom.get(key) != value}
        if mismatches:
            raise DispatchError(f"B04 audited backend profile mismatch: {mismatches}")
        return BackendRoute(
            classification=CUSTOM_AUDITED,
            backend_kind=B04_CUSTOM_BACKEND_KIND,
            backend_id=B04_CUSTOM_BACKEND,
            model_id=model_id,
            process_id=process_id,
            standard_qed_authority=False,
            production_ready_scope="locked B04 benchmark only",
        )

    if classification == CUSTOM_AUDITED:
        raise DispatchError("registered custom model has no production execution route; only locked B04 is executable")
    raise DispatchError("request is outside validated native QED and locked B04 execution scopes")
