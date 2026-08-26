# Backend Strategy

Day 4 pivoted FeynAgent from a Python-first reimplementation path to a native-backend-first architecture. The public v0.1 release candidate validates only a narrow standard-native QED surface plus one locked custom B04 benchmark route.

## Validated Current v0.1 Support

The validated public v0.1 support is:

- standard native tree-level QED 2->2 processes;
- standard external particles `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend `feynarts_feyncalc_native` for the standard QED scope;
- diagrams, channel-separated amplitudes, LaTeX, executable FeynCalc artifacts, bounded benchmark M2 execution, and validation/provenance reports for benchmarked QED runs;
- locked B04 `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, requiring separately supplied audited external knowledge.

The current release does not claim arbitrary SM, QCD, BSM, arbitrary gravity, loops, renormalization, or ungated production-heavy execution.

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Linux and macOS Python test success must not be described as full physics E2E validation on those platforms.

## Backend Roles

### `feynarts_feyncalc_native`

`feynarts_feyncalc_native` is the primary production backend for the validated public v0.1 standard-native QED scope.

- FeynArts owns standard diagram and amplitude generation.
- `FCFAConvert` owns conversion of FeynArts amplitudes into FeynCalc expressions.
- FeynCalc owns algebraic validation, manipulation, simplification, traces, spin sums, polarization sums, and squared-amplitude workflows.
- Standard QED production amplitudes in the validated v0.1 scope must not be sourced from duplicate Python-maintained canonical formulas when the native model supports the process.

### `direct_feyncalc_custom_audited`

`direct_feyncalc_custom_audited` is the only executable custom route in v0.1, and only for locked B04.

- Process: `phi phi -> h h`.
- `model_id = reheating_scalar_gravity_v1`.
- Backend profile: `profiles/backends/b04_custom_gravity_audited.yaml`.
- Knowledge manifest: `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.
- The backend must resolve the separately supplied audited external knowledge package, match the locked convention ID, and pass rule audit before amplitudes continue.
- It is not authority for arbitrary gravity or arbitrary BSM models.
- B04 topology or amplitude authorization does not authorize B04 M2.

### `custom_audited_model`

`custom_audited_model` remains the future path for additional user-supplied nonstandard interactions. Outside locked B04, custom rules are review/intake only in v0.1 and have no production execution route.

- Custom rules must retain explicit provenance and convention audit records.
- RuleRegistry remains a custom-rule intake and audit structure for user-supplied custom rules until a native model adapter is generated and audited.
- Additional custom routes require benchmark evidence and documentation before any production-readiness claim.

### `legacy_custom_backend`

`legacy_custom_backend` is the existing Days 1-3 Python topology, AmplitudeIR, LaTeX, and FeynCalc renderer implementation.

- Retained for regression tests, pedagogy, audit explainability, and fallback.
- Retained as a useful reference for explicit external-state and convention mapping.
- Not primary for standard QED production after Day 4.
- Not authority for arbitrary BSM or gravity.

## Standard-Rule Source Policy

For `feynarts_feyncalc_native`, FeynArts/FeynCalc model definitions are the production source for the validated public v0.1 standard-native QED rules.

The existing QED RuleRegistry is retained as an audit/reference snapshot for `legacy_custom_backend`; it is not the authority for native FeynArts/FeynCalc amplitudes. For future custom rules, RuleRegistry remains an intake/audit record until a reviewed executable backend exists.

## Future Architecture Target

The architecture remains designed to support additional native standard sectors such as SM and QCD, and later audited custom models, once the corresponding backend profiles, examples, validation gates, benchmark golds, and documentation exist.

Future SM/QCD/custom support must be promoted by benchmarked process families, not by the existence of installed model files alone. Custom BSM or gravity support beyond locked B04 requires explicit rule provenance, convention review, backend feasibility, and passing benchmark gates before any production-readiness claim.

## Generated Artifact Policy

Starting Day 4, new generated amplitudes, PDFs, logs, and squared-amplitude outputs must be written under `runs/` using stable run IDs. `benchmarks/` should contain specs, gold/reference fixtures, and explicitly marked historical artifacts only.
