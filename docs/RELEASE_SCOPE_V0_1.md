# FeynAgent v0.1 Release Scope

The public v0.1 scope is deliberately narrow. It contains one standard native route and one locked custom benchmark route. It is not a general event-production, Standard Model, BSM, QCD, or gravity system.

## Public Release Scope

v0.1 is scoped to:

- tree-level QED `2 -> 2` workflows with external particles `e-`, `e+`, `mu-`, `mu+`, and `gamma`;
- the `feynarts_feyncalc_native` backend using installed FeynArts/FeynCalc model files for that standard QED scope;
- diagram generation and diagram-count validation;
- channel-separated amplitudes;
- LaTeX output;
- executable FeynCalc/Wolfram output;
- optional bounded M2 execution only through an explicit `ExecutionRequest`;
- validation and provenance reports for benchmarked runs;
- the single locked custom B04 route `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, requiring separately supplied audited external knowledge.

FeynAgent v0.1 must not be described as supporting arbitrary SM, arbitrary gravity, arbitrary BSM, QCD production, loops, renormalization, or ungated production-heavy execution.

## Implemented And Benchmarked

The following scope has benchmark evidence and is suitable for public v0.1 claims:

- B01 `e- e+ -> mu- mu+`: tree-level QED, one s-channel photon diagram, native FeynArts/FeynCalc amplitude generation, official-example provenance, and bounded M2 regression.
- B02 `e- gamma -> e- gamma`: tree-level QED Compton scattering, s- and u-channel electron diagrams, native FeynArts/FeynCalc amplitude generation, official-example provenance, and bounded M2 regression.
- B03 `e- mu- -> e- mu-`: tree-level QED electron-muon scattering, one t-channel photon diagram, native FeynArts/FeynCalc amplitude generation, official-example provenance, and bounded M2 regression.
- Shared native backend profile `profiles/backends/feynarts_sm_qed.yaml` resolving `model_id: sm_qed` and `sector: qed` to FeynArts `SM`, `Lorentz`, `QEDOnly`, and class-level insertion for the five in-scope particles.
- B04 `phi phi -> h h`: locked custom audited benchmark with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and backend profile `profiles/backends/b04_custom_gravity_audited.yaml`.
- B04 requires the registered external knowledge package from `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`; only hashes and logical locks are committed, not the raw external package.
- Runtime authorization separation through `ExecutionRequest`, with bounded benchmark M2 regression separated from production-heavy execution.

Primary evidence:

- `reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md`
- `reports/DAY4_M2_REGRESSION.md`
- `reports/DAY5_CONTRACT_REPAIR.md`
- `reports/DAY5_REPORT.md`
- `reports/DAY7_B04_TOPOLOGY.md`
- `reports/DAY7_B04_AMPLITUDE_CLOSURE.md`
- `reports/DAY7_B04_PHASE7_CLOSURE.md`
- `reports/DAY7_B04_SKILL_E2E.md`
- `benchmarks/B01_ee_to_mumu/native_expected.yaml`
- `benchmarks/B02_compton/native_expected.yaml`
- `benchmarks/B03_emu_to_emu/native_expected.yaml`
- `benchmarks/B04_phi_phi_to_hh/expected_topology.yaml`
- `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Linux and macOS Python test success may be useful smoke evidence, but it must not be described as full physics E2E validation on those platforms.

## Implemented But Not General Public Scope

The following capabilities exist in the repository but must not be promoted as general v0.1 production support:

- Legacy Python `DiagramIR` generation beyond the benchmarked public cases, including generic rule-registry experiments and contact-diagram unit tests.
- Legacy `AmplitudeIR`, LaTeX amplitude rendering, executable FeynCalc rendering, smoke/Ward/M2 script generation, and audit markdown. These remain useful regression and audit paths, but are not the standard native production authority.
- TikZ-Feynman diagram rendering and PDF output from `DiagramIR`, currently tested as renderer behavior rather than as a public native benchmark evidence path.
- `custom_audited` intake for explicit custom rules, conventions, and provenance outside B04. Only the locked B04 route has an executable custom production path in v0.1.
- `production_heavy` as an authorization mode in the `ExecutionRequest` schema. The schema supports the mode, but public v0.1 evidence covers only bounded benchmark regression.

## Planned Or Future Work

The following work may be pursued after v0.1, but is outside the release candidate:

- broader Standard Model sector coverage after explicit benchmark design, fixtures, provenance, and review;
- QCD support after explicit benchmark design, fixtures, provenance, and review;
- additional audited custom FeynArts-compatible model or adapter generation;
- additional QED `2 -> 2` channels within the same five-particle scope;
- stronger native LaTeX/report integration directly from FeynArts/FeynCalc artifacts;
- expanded validation bundles and reproducibility checks for fresh release artifacts.

## Explicitly Unsupported

The following must be rejected or classified as requiring review in v0.1:

- arbitrary Standard Model process production;
- arbitrary gravity or graviton production beyond locked B04;
- arbitrary BSM production;
- QCD production support;
- automatic derivation of Feynman rules from arbitrary Lagrangians;
- unproven or invented trusted Feynman rules;
- loops, counterterms, renormalization, or higher-order corrections;
- automatic phase-space integration, cross-section production, event generation, or detector simulation;
- autonomous long-running Mathematica/FeynCalc jobs;
- ungated production-heavy execution;
- B04 M2 execution without a separate explicit authorization;
- new generated amplitudes, PDFs, Wolfram logs, or M2 outputs under `benchmarks/`.

## Release Date Policy

The project version remains `0.1.0` during release-candidate hardening. The final release date must not be assigned until the human release gate creates the actual GitHub release and tag.

## Day 8 Public Claim Resolution

Earlier Day-6 scope wording that described all gravity as unsupported is superseded by the Day-7 locked B04 validation. Current public wording must say exactly this: arbitrary gravity remains unsupported, while the single locked B04 `phi phi -> h h` route is validated only with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and the separately supplied audited external knowledge package.
