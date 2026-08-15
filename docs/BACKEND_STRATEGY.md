# Backend Strategy

Day 4 pivoted FeynAgent from a Python-first reimplementation path to a native-backend-first architecture. The public v0.1 release candidate validates only a narrow standard-native surface; broader SM/QCD/custom-model coverage remains an architecture target.

## Validated Current v0.1 Support

The validated public v0.1 standard-native support is:

- tree-level QED 2->2 processes;
- external particles `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend;
- diagrams, channel-separated amplitudes, LaTeX, executable FeynCalc artifacts, bounded benchmark M2 execution, and validation/provenance reports.

The current release does not claim arbitrary SM, QCD, BSM, or custom-gravity production support.

## Backend Roles

### `feynarts_feyncalc_native`

`feynarts_feyncalc_native` is the primary production backend for the validated public v0.1 standard-native QED scope.

- FeynArts owns standard diagram and amplitude generation.
- `FCFAConvert` owns conversion of FeynArts amplitudes into FeynCalc expressions.
- FeynCalc owns algebraic validation, manipulation, simplification, traces, spin sums, polarization sums, and squared-amplitude workflows.
- Standard QED production amplitudes in the validated v0.1 scope must not be sourced from duplicate Python-maintained canonical formulas when the native model supports the process.

### `custom_audited_model`

`custom_audited_model` is the future primary path for user-supplied nonstandard interactions.

- Custom rules retain explicit provenance and convention audit records.
- RuleRegistry remains a custom-rule intake and audit structure for user-supplied custom rules until a native model adapter is generated and audited.
- The preferred implementation target is a custom FeynArts-compatible model or adapter, so nonstandard interactions can still flow through the mature native diagram and algebra stack.

### `legacy_custom_backend`

`legacy_custom_backend` is the existing Days 1-3 Python topology, AmplitudeIR, LaTeX, and FeynCalc renderer implementation.

- Retained for regression tests, pedagogy, audit explainability, and fallback.
- Retained as a useful reference for explicit external-state and convention mapping.
- Not primary for standard QED production after Day 4.

## Standard-Rule Source Policy

For `feynarts_feyncalc_native`, FeynArts/FeynCalc model definitions are the production source for the validated public v0.1 standard-native QED rules.

The existing QED RuleRegistry is retained as an audit/reference snapshot for `legacy_custom_backend`; it is not the authority for native FeynArts/FeynCalc amplitudes. For future custom rules, RuleRegistry remains authoritative until a reviewed native model/adapter exists.

## Future Architecture Target

The architecture remains designed to support additional native standard sectors such as SM and QCD, and later audited custom models, once the corresponding backend profiles, examples, validation gates, benchmark golds, and documentation exist.

Future SM/QCD/custom support must be promoted by benchmarked process families, not by the existence of installed model files alone. Custom BSM or gravity support requires explicit rule provenance, convention review, native-backend feasibility, and passing benchmark gates before any production-readiness claim.

## Generated Artifact Policy

Starting Day 4, new generated amplitudes, PDFs, logs, and squared-amplitude outputs must be written under `runs/` using stable run IDs. `benchmarks/` should contain specs, gold/reference fixtures, and explicitly marked historical artifacts only.
