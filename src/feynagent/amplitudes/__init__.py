"""Deterministic tree-level AmplitudeIR construction and derived backends."""

from .backends import (
    RenderedAmplitudeBackend,
    render_audit_markdown,
    render_backends,
    render_compute_m2_wolfram,
    render_latex_document,
    render_smoke_wolfram,
    render_ward_check_wolfram,
    render_wolfram_amplitudes,
    write_backend_outputs,
)
from .builder import AmplitudeBuildError, build_amplitude_ir, validate_amplitude_ir_semantics

__all__ = [
    "AmplitudeBuildError",
    "RenderedAmplitudeBackend",
    "build_amplitude_ir",
    "render_audit_markdown",
    "render_backends",
    "render_compute_m2_wolfram",
    "render_latex_document",
    "render_smoke_wolfram",
    "render_ward_check_wolfram",
    "render_wolfram_amplitudes",
    "validate_amplitude_ir_semantics",
    "write_backend_outputs",
]
