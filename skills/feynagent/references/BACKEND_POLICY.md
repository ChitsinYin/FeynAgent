# Backend Policy

## Classification

- `standard_native`: standard QED/SM/QCD process supported by installed FeynArts/FeynCalc model files.
- `custom_audited`: user supplies nonstandard interactions with explicit rules, conventions, and provenance.
- `unsupported_requires_review`: request is ambiguous, unsupported, missing rules, or asks for unreviewed assumptions.

## Standard Native

Use `feynarts_feyncalc_native` for standard supported sectors. Search `.feynagent/reference_index.json` before generation and record matching official example metadata, package versions, and hashes. FeynArts generates diagrams/amplitudes; FCFAConvert converts amplitudes; FeynCalc handles algebra and validation.

Do not maintain duplicate standard QED Feynman-rule formulas as the production source. The QED RuleRegistry is a legacy/custom audit snapshot, not the native standard-sector authority.

## Custom Audited

Use `custom_audited` only when custom rules, conventions, and provenance are explicit. Prefer producing or adapting a FeynArts-compatible model so mature native tooling still owns diagram and algebra mechanics. Use the legacy custom backend only as fallback/reference.

## Execution Boundary

Benchmark regression is allowed only when explicitly authorized as such. Production heavy computation requires separate explicit authorization. Do not treat a benchmark regression approval as production-heavy approval.
