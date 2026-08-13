# Backend Strategy

Day 4 pivots FeynAgent from a Python-first reimplementation path to a native-backend-first architecture for standard field-theory sectors.

## Backend Roles

### `feynarts_feyncalc_native`

`feynarts_feyncalc_native` is the primary production backend for standard QED, SM, and QCD sectors supported by installed FeynArts/FeynCalc model files.

- FeynArts owns standard diagram and amplitude generation.
- `FCFAConvert` owns conversion of FeynArts amplitudes into FeynCalc expressions.
- FeynCalc owns algebraic validation, manipulation, simplification, traces, spin sums, polarization sums, and squared-amplitude workflows.
- Standard QED production amplitudes must not be sourced from duplicate Python-maintained canonical formulas when the native model supports the process.

### `custom_audited_model`

`custom_audited_model` is the future primary path for user-supplied nonstandard interactions.

- Custom rules retain explicit provenance and convention audit records.
- RuleRegistry remains authoritative for user-supplied custom rules until a native model adapter is generated and audited.
- The preferred implementation target is a custom FeynArts-compatible model or adapter, so nonstandard interactions can still flow through the mature native diagram and algebra stack.

### `legacy_custom_backend`

`legacy_custom_backend` is the existing Days 1-3 Python topology, AmplitudeIR, LaTeX, and FeynCalc renderer implementation.

- Retained for regression tests, pedagogy, audit explainability, and fallback.
- Retained as a useful reference for explicit external-state and convention mapping.
- Not primary for standard QED production after Day 4.

## Standard-Rule Source Policy

For `feynarts_feyncalc_native`, FeynArts/FeynCalc model definitions are the production source for standard supported QED/SM/QCD rules.

The existing QED RuleRegistry is retained as an audit/reference snapshot for `legacy_custom_backend`; it is not the authority for native FeynArts/FeynCalc amplitudes. For future custom rules, RuleRegistry remains authoritative until a reviewed native model/adapter exists.

## Generated Artifact Policy

Starting Day 4, new generated amplitudes, PDFs, logs, and squared-amplitude outputs must be written under `runs/` using stable run IDs. `benchmarks/` should contain specs, gold/reference fixtures, and explicitly marked historical artifacts only.
