# Changelog

All notable public-facing changes to FeynAgent are recorded here.

## 0.1.0 - 2026-08-15

### Added

- Deterministic public runner: `python -m feynagent run`.
- Native standard-QED 2-to-2 workflow for `e-`, `e+`, `mu-`, `mu+`, and `gamma` external states.
- FeynArts/FeynCalc-native diagram and amplitude artifact generation.
- Persistent `diagrams.pdf`, diagram source, per-channel FeynCalc amplitudes, LaTeX source/PDF, logs, manifests, and validation report.
- Generic standard-QED squared-amplitude script generation with bounded benchmark-regression execution through `ExecutionRequest`.
- Official benchmark regression coverage for B01, B02, and B03.
- Codex skill metadata and manually validated local skill installation workflow.
- Wheel-install E2E verification from a fresh venv without editable install or `PYTHONPATH=src`.
- Apache-2.0 project license metadata for FeynAgent-owned code and documentation.

### Changed

- Runtime dependencies are declared explicitly: `PyYAML>=6` and `jsonschema>=4`.
- Runtime JSON schemas are packaged with the wheel.
- Public documentation now limits the support claim to the validated v0.1 standard-native scope.

### Not Supported In 0.1.0

- Arbitrary Standard Model production workflows.
- QCD benchmark production workflows.
- Custom BSM model production workflows.
- Custom graviton or gravity workflows.
- Ungated production-heavy squared-amplitude execution.
