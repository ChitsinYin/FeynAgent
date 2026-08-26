# FeynAgent v0.1 Scope

## Project Goal

FeynAgent helps HEP phenomenology researchers move from bounded, reviewed process descriptions to auditable, structured physics specifications, diagram and amplitude artifacts, LaTeX output, executable Mathematica/FeynCalc code, and validation/provenance records.

The tool is not intended to replace human physics judgment. It should make assumptions explicit, preserve provenance, and produce artifacts that a researcher can inspect, approve, and validate.

## Supported Public Scope

v0.1 supports only:

- Standard native tree-level QED 2->2 workflows.
- External QED particles `e-`, `e+`, `mu-`, `mu+`, and `gamma`.
- The `feynarts_feyncalc_native` backend for the validated standard QED scope.
- B01, B02, and B03 benchmarked standard-native examples.
- The single locked custom B04 route `phi phi -> h h`.
- B04 `model_id = reheating_scalar_gravity_v1`.
- B04 backend `direct_feyncalc_custom_audited`.
- B04 execution only with separately supplied audited external knowledge and exact convention/rule audit gates.
- Explicit convention records, provenance records, and human approval gates.
- Generated artifacts under `runs/<run_id>/`.

## Explicit Non-Goals

v0.1 does not support:

- Arbitrary Standard Model process production.
- QCD production.
- Arbitrary BSM production.
- Arbitrary gravity or graviton production beyond the locked B04 route.
- Loop diagrams.
- Automatic renormalization.
- Counterterms or higher-order corrections.
- Automatic derivation of arbitrary Feynman rules from arbitrary Lagrangians.
- Full FeynRules integration.
- Automatic thermal field theory.
- Automatic phase-space integration.
- Boltzmann equations.
- Automatic paper writing.
- Autonomous long-running Mathematica calculations.
- Ungated production-heavy execution.
- B04 M2 execution without separate explicit authorization.
- Remote or HPC workflows.
- GUI or web app workflows.
- Arbitrary model discovery.

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Passing Python tests on Linux or macOS do not establish full physics E2E validation on those platforms.

## Human Approval Gates

Human approval is required before:

- Accepting or changing convention choices.
- Marking custom Feynman rules as trusted.
- Resolving conflicting rule definitions.
- Freezing a process as approved for diagram generation.
- Updating benchmark gold files.
- Running heavy external symbolic calculations.
- Treating generated LaTeX, TikZ, or Mathematica code as publishable.
- Running B04 M2 or other squared-amplitude calculations outside already approved bounded benchmark-regression requests.

## v0.1 Definition of Done

v0.1 is done when:

- Public documentation states the same validated scope across README, quickstart, release scope, backend strategy, readiness levels, skill instructions, citation metadata, and package metadata.
- Structured cards exist for process specification, conventions, backend profiles, and execution requests.
- Candidate processes can be promoted to approved processes only through explicit checks.
- Standard-native QED benchmark artifacts and regression tests pass for B01/B02/B03.
- Locked B04 topology, amplitude, LaTeX, backend dispatch, rule audit, and skill-route checks pass for the single audited custom route.
- Unsupported requests fail clearly with documented reasons.
- Heavy algebra remains human-controlled outside the live agent loop.
- The final release date is assigned only at the human release gate.
