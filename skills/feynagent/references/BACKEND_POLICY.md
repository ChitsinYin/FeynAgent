# Backend Policy

## Classification

- `standard_native`: validated public v0.1 tree-level QED 2->2 plus only the bounded B05 `e- mu- -> e- mu- gamma` v0.2 spike, through `feynarts_feyncalc_native`.
- `custom_audited`: only the locked B04 `phi phi -> h h` route is executable in v0.1, with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and separately supplied audited external knowledge. Other custom requests are intake/review only.
- `unsupported_requires_review`: request is ambiguous, unsupported, missing rules, or asks for unreviewed assumptions. This includes arbitrary SM, QCD production, arbitrary BSM, arbitrary gravity, loops, renormalization, and ungated production-heavy execution.

## Standard Native

Use `feynarts_feyncalc_native` only for the validated standard QED 2->2 public scope and the exact B05 2->3 spike. Search `.feynagent/reference_index.json` before generation and record matching official example metadata, package versions, and hashes. FeynArts generates diagrams/amplitudes; FCFAConvert converts amplitudes; FeynCalc handles algebra and validation. B05 is amplitude-only: generate `compute_m2.wl` but do not execute a full 2->3 M2 simplification.

Do not maintain duplicate standard QED Feynman-rule formulas as the production source. The QED RuleRegistry is a legacy/custom audit snapshot, not the native standard-sector authority.

## Custom Audited

The only executable custom route is B04 `phi phi -> h h` with model `reheating_scalar_gravity_v1` and backend `direct_feyncalc_custom_audited`. It requires the registered external package, exact convention lock, rule audit `PASS`, and an approved linked ExecutionRequest.

Other explicit custom rules may be classified `custom_audited` for intake/review, but have no production backend. Legacy custom code remains fallback/reference and is not authority for arbitrary BSM or gravity.

## Platform Boundary

Full physics E2E validation for v0.1 was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Do not claim Linux/macOS full physics validation merely because Python tests pass there.

## Execution Boundary

Benchmark regression is allowed only when explicitly authorized as such. Production heavy computation requires separate explicit authorization. Do not treat a benchmark regression approval as production-heavy approval.

For B04, topology/amplitude authorization never implies M2 authorization. M2 remains a separate deterministic manual run after conflict-free amplitude closure.
