# Backend Policy

## Classification

- `standard_native`: standard QED/SM/QCD process supported by installed FeynArts/FeynCalc model files.
- `custom_audited`: user supplies nonstandard interactions with explicit rules, conventions, and provenance.
- `unsupported_requires_review`: request is ambiguous, unsupported, missing rules, or asks for unreviewed assumptions.

## Standard Native

Use `feynarts_feyncalc_native` for standard supported sectors. Search `.feynagent/reference_index.json` before generation and record matching official example metadata, package versions, and hashes. FeynArts generates diagrams/amplitudes; FCFAConvert converts amplitudes; FeynCalc handles algebra and validation.

Do not maintain duplicate standard QED Feynman-rule formulas as the production source. The QED RuleRegistry is a legacy/custom audit snapshot, not the native standard-sector authority.

## Custom Audited

The only executable custom route is B04 `phi phi -> h h` with model `reheating_scalar_gravity_v1` and backend `direct_feyncalc_custom_audited`. It requires the registered external package, exact convention lock, rule audit `PASS`, and an approved linked ExecutionRequest.

Other explicit custom rules may be classified `custom_audited` for intake/review, but have no production backend. Legacy custom code remains fallback/reference and is not authority for arbitrary BSM or gravity.

## Execution Boundary

Benchmark regression is allowed only when explicitly authorized as such. Production heavy computation requires separate explicit authorization. Do not treat a benchmark regression approval as production-heavy approval.
For B04, topology/amplitude authorization never implies M2 authorization. M2 remains a separate deterministic manual run after conflict-free amplitude closure.
