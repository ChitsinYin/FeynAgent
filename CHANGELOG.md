# Changelog

All notable public-facing changes to FeynAgent are recorded here.

## Unreleased

### Added

- Bounded native-QED B05 feature spike for `e- mu- -> e- mu- gamma`, with a strict structured 2-to-3 PhysicsCard path.
- FeynArts `CreateTopologies[0, 2 -> 3]`, persistent diagrams, per-diagram FeynCalc/LaTeX objects, external-leg emission metadata, a total-amplitude Ward check, and a structural soft check against the B03 hard process.
- Script-only `compute_m2.wl` policy for B05; automatic full 2-to-3 M2 simplification, phase-space integration, and cross sections remain disabled.

### Changed

- Public release documentation now states the same validated v0.1 scope across README, quickstart, release scope, backend strategy, readiness levels, Codex skill instructions, citation metadata, and package metadata.
- Release-candidate wording now records that full physics E2E validation was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain, without claiming Linux or macOS full physics validation from Python test success alone.
- Citation metadata records the v0.1.0 release date from the approved public release gate.

## 0.1.0 - 2026-08-27

### Added

- Deterministic public runner: `python -m feynagent run`.
- Native standard-QED 2-to-2 workflow for `e-`, `e+`, `mu-`, `mu+`, and `gamma` external states.
- FeynArts/FeynCalc-native diagram and amplitude artifact generation.
- Persistent `diagrams.pdf`, diagram source, per-channel FeynCalc amplitudes, LaTeX source/PDF, logs, manifests, and validation report.
- Generic standard-QED squared-amplitude script generation with bounded benchmark-regression execution through `ExecutionRequest`.
- Official benchmark regression coverage for B01, B02, and B03.
- Locked custom B04 benchmark route: `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, requiring separately supplied audited external knowledge.
- Codex skill metadata and manually validated local skill installation workflow.
- Wheel-install E2E verification from a fresh Windows 11 physics-toolchain venv without editable install or `PYTHONPATH=src`.
- Apache-2.0 project license metadata for FeynAgent-owned code and documentation.

### Changed

- Runtime dependencies are declared explicitly: `PyYAML>=6` and `jsonschema>=4`.
- Runtime JSON schemas are packaged with the wheel.
- Public documentation limits support claims to the validated v0.1 standard-native QED scope and the single locked B04 route.

### Not Supported In 0.1.0

- Arbitrary Standard Model production workflows.
- QCD production workflows.
- Custom BSM model production workflows.
- Arbitrary gravity or graviton production workflows beyond locked B04.
- Loops, counterterms, renormalization, or higher-order corrections.
- Ungated production-heavy squared-amplitude execution.
- B04 M2 execution without separate explicit authorization.
