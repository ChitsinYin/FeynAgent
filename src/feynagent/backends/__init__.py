"""Backend integrations for FeynAgent."""

from .feynarts_feyncalc import (
    BackendConfig,
    NativeBremsstrahlungDiagram,
    NativeChannel,
    backend_config_from_dict,
    NativeBackendError,
    build_native_qed_script,
    build_native_qed_m2_script,
    native_qed_channel_plan,
    native_qed_bremsstrahlung_plan,
    run_native_qed_backend,
    run_native_qed_m2_generator,
    validate_native_qed_artifact_metadata,
    validate_native_qed_artifacts,
    validate_native_qed_request,
)

__all__ = [
    "BackendConfig",
    "NativeBremsstrahlungDiagram",
    "NativeChannel",
    "backend_config_from_dict",
    "NativeBackendError",
    "build_native_qed_script",
    "build_native_qed_m2_script",
    "native_qed_channel_plan",
    "native_qed_bremsstrahlung_plan",
    "run_native_qed_backend",
    "run_native_qed_m2_generator",
    "validate_native_qed_artifact_metadata",
    "validate_native_qed_artifacts",
    "validate_native_qed_request",
]
