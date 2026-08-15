# FeynAgent v0.1 Release Scope

Day 6 release-candidate closure freezes the public-facing v0.1 scope to a
standard-native QED benchmark tool, not a general event-production or model
generation system.

## Public Release Scope

v0.1 is scoped to:

- tree-level QED `2 -> 2` workflows;
- external particles `e-`, `e+`, `mu-`, `mu+`, and `gamma`;
- the `feynarts_feyncalc_native` backend using installed FeynArts/FeynCalc
  model files;
- diagram generation and diagram-count validation;
- channel-separated amplitudes;
- LaTeX output;
- executable FeynCalc/Wolfram output;
- optional bounded M2 execution only through an explicit `ExecutionRequest`;
- validation and provenance reports for benchmarked runs.

FeynAgent v0.1 must not be described as supporting arbitrary SM, QCD, custom
BSM, gravity, or general model production.

## Implemented And Benchmarked

The following scope has benchmark evidence and is suitable for public v0.1
claims:

- B01 `e- e+ -> mu- mu+`: tree-level QED, one s-channel photon diagram,
  native FeynArts/FeynCalc amplitude generation, official-example provenance,
  and bounded M2 regression.
- B02 `e- gamma -> e- gamma`: tree-level QED Compton scattering, s- and
  u-channel electron diagrams, native FeynArts/FeynCalc amplitude generation,
  official-example provenance, and bounded M2 regression.
- B03 `e- mu- -> e- mu-`: tree-level QED electron-muon scattering, one
  t-channel photon diagram, native FeynArts/FeynCalc amplitude generation,
  official-example provenance, and bounded M2 regression.
- Shared native backend profile `profiles/backends/feynarts_sm_qed.yaml`
  resolving `model_id: sm_qed` and `sector: qed` to FeynArts `SM`,
  `Lorentz`, `QEDOnly`, and class-level insertion for the five in-scope
  particles.
- Benchmark validation/provenance artifacts recorded in Day 4 and Day 5
  reports, including package versions, official example identifiers, hashes,
  generated script paths, run manifests, and output hashes.
- Runtime authorization separation through `ExecutionRequest`, with bounded
  benchmark M2 regression separated from production-heavy execution.

Primary evidence:

- `reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md`
- `reports/DAY4_M2_REGRESSION.md`
- `reports/DAY5_CONTRACT_REPAIR.md`
- `reports/DAY5_REPORT.md`
- `benchmarks/B01_ee_to_mumu/native_expected.yaml`
- `benchmarks/B02_compton/native_expected.yaml`
- `benchmarks/B03_emu_to_emu/native_expected.yaml`

## Implemented But Not Yet Benchmarked For Public Claims

The following capabilities exist in the repository but should not be promoted
as public v0.1 production support without additional release benchmarks:

- Legacy Python `DiagramIR` generation beyond the three frozen public
  benchmarks, including generic rule-registry experiments and contact-diagram
  unit tests.
- Legacy `AmplitudeIR`, LaTeX amplitude rendering, executable FeynCalc
  rendering, smoke/Ward/M2 script generation, and audit markdown for B01/B02.
  These remain useful regression and audit paths, but are not the standard
  native production authority.
- TikZ-Feynman diagram rendering and PDF output from `DiagramIR`, currently
  tested as renderer behavior rather than as the public native benchmark
  evidence path.
- The `custom_audited` classification path and custom rule protocol. It can
  request explicit rules, conventions, and provenance, but v0.1 does not ship
  audited custom model production.
- `production_heavy` as an authorization mode in the `ExecutionRequest` schema.
  The schema supports the mode, but public v0.1 evidence covers only bounded
  benchmark regression.

## Planned

The following work may be pursued after v0.1, but is outside the release
candidate:

- broader Standard Model sector coverage after explicit benchmark design,
  fixtures, provenance, and review;
- QCD support after explicit benchmark design, fixtures, provenance, and
  review;
- audited custom FeynArts-compatible model or adapter generation;
- additional QED `2 -> 2` channels within the same five-particle scope;
- stronger native LaTeX/report integration directly from FeynArts/FeynCalc
  artifacts;
- expanded validation bundles and reproducibility checks for fresh release
  artifacts.

## Explicitly Unsupported

The following must be rejected or classified as requiring review in v0.1:

- arbitrary SM process production;
- QCD production support;
- custom BSM production support;
- gravity or graviton interactions;
- automatic derivation of Feynman rules from arbitrary Lagrangians;
- unproven or invented trusted Feynman rules;
- loops, counterterms, renormalization, or higher-order corrections;
- automatic phase-space integration, cross-section production, event
  generation, or detector simulation;
- autonomous long-running Mathematica/FeynCalc jobs;
- production-heavy M2 execution without a separate explicit authorization;
- new generated amplitudes, PDFs, Wolfram logs, or M2 outputs under
  `benchmarks/`.

## README/SKILL Overclaim Audit

The following public-facing wording currently overclaims or risks overclaiming
relative to the frozen v0.1 release scope. This audit records the issue only;
it does not modify README or skill files.

| file | line | sentence | issue |
| --- | ---: | --- | --- |
| `README.md` | 5 | "For standard supported sectors, the production implementation path remains native FeynArts/FeynCalc:" | "standard supported sectors" is too broad for v0.1 unless immediately constrained to benchmarked tree-level QED `2 -> 2`. |
| `README.md` | 10 | "Use `feynarts_feyncalc_native` for standard QED/SM/QCD sectors supported by installed FeynArts/FeynCalc model files." | Claims SM/QCD production support. v0.1 public scope is only tree-level QED `2 -> 2` for `e-`, `e+`, `mu-`, `mu+`, and `gamma`. |
| `README.md` | 12 | "Keep the custom RuleRegistry as the authority for future nonstandard interactions until an audited native model or adapter exists." | Acceptable as architecture direction, but public release wording should state that custom BSM production is not supported in v0.1. |
| `skills/feynagent/SKILL.md` | 3 | "Use this skill for FeynAgent HEP workflows involving QED/SM benchmark amplitudes, FeynArts/FeynCalc native generation, audited custom rules, or local environment checks." | "QED/SM benchmark amplitudes" and "audited custom rules" are broader than the frozen public v0.1 claim; restrict public wording to QED `2 -> 2` benchmarks and custom-rule review/intake only. |
| `skills/feynagent/SKILL.md` | 11 | "`standard_native`: standard QED/SM/QCD supported by native packages." | Claims SM/QCD standard-native support. For v0.1 this should be QED-only and limited to the five-particle `2 -> 2` scope. |
| `skills/feynagent/SKILL.md` | 12 | "`custom_audited`: user-supplied nonstandard interactions with explicit rules/conventions/provenance." | Risks sounding like production support for custom BSM. For v0.1, this should be a review/intake classification, not a production guarantee. |
| `skills/feynagent/SKILL.md` | 15 | "For `standard_native`, search `.feynagent/reference_index.json` first, use FeynArts/FeynCalc native backend, record package versions and example provenance, and do not rebuild standard Feynman rules in Python." | Operationally sound, but public release wording should bind `standard_native` to the QED-only v0.1 scope rather than all standard sectors. |
| `skills/feynagent/SKILL.md` | 17 | "For `custom_audited`, require explicit rules/conventions/provenance, never invent trusted rules, map to FeynCalc elementary objects where possible, prefer a custom FeynArts-compatible model/adapter, and use the legacy custom backend only as fallback/reference." | Good guardrails, but "map to FeynCalc" and "prefer a custom FeynArts-compatible model/adapter" can imply supported custom production. Mark as planned/review-only for v0.1. |

Related non-README/SKILL wording to clean before release:

- `reports/DAY5_REPORT.md` recommends `READY_FOR_CUSTOM_GRAVITY`, which conflicts
  with the Day 6 instruction not to add gravity and should not appear as a
  v0.1 public release claim.

## Release Blockers

- README and skill wording must be narrowed before public v0.1 release so they
  do not claim arbitrary SM/QCD/custom-BSM support.
- The public path for "LaTeX output" should be clarified: current evidence is
  strongest for legacy amplitude/TikZ renderers and benchmark reports, while
  the standard-native production authority is FeynArts/FeynCalc output.
- A final release validation run should confirm that `python scripts/validate_examples.py`
  and `python -m pytest` pass after any wording changes.
- Public docs should explicitly mark gravity as unsupported for v0.1, despite
  the Day 5 internal recommendation to proceed toward custom gravity.
