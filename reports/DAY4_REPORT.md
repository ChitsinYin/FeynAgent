# FeynAgent Day 4 Report

Generated at: 2026-08-13 16:16:07 +0800

## Executive Status

PASS

Day 4 closes as an architecture-pivot milestone. The standard-sector production path now uses the native FeynArts/FeynCalc backend, while the Days 1-3 Python backend remains present as a reference, regression, pedagogy, audit, and fallback path.

## Backend Roles

| backend role | status | authority |
| --- | --- | --- |
| `feynarts_feyncalc_native` | Primary for standard supported QED/SM/QCD sectors | Installed FeynArts/FeynCalc model files; `FCFAConvert`; FeynCalc algebra |
| `legacy_custom_backend` | Reference/fallback for Days 1-3 custom topology and AmplitudeIR path | Legacy schemas, explicit provenance, audited QED registry snapshot |
| `custom_audited_model` | Future path for nonstandard interactions | RuleRegistry remains authoritative until an audited native model/adapter exists |

## Day-4 Implementation

- Added minimal native backend source: `src/feynagent/backends/feynarts_feyncalc.py`.
- Added shared native QED profile: `profiles/backends/feynarts_sm_qed.yaml`.
- Added B03 native benchmark specification: `benchmarks/B03_emu_to_emu/`.
- Updated B01/B02/B03 native metadata to reference the shared profile.
- Kept native particle mapping backend-local.
- Did not parse or rewrite native amplitudes through the legacy QED RuleRegistry.

## Benchmark And Artifact Layout

- `benchmarks/` now holds specs, native expected metadata, gold/reference fixtures, and benchmark-local `legacy/` fixtures.
- `runs/` holds generated amplitudes, logs, PDFs, M2 outputs, and authoritative Day-4 evidence runs.
- `.feynagent/` is reserved for machine-local diagnostics and probes.
- Superseded generated artifacts previously tracked under benchmark directories were removed after the external pre-clean snapshot.

## Native Amplitude Regression

PASS for B01/B02/B03.

| benchmark | expected diagrams | observed diagrams | reference example |
| --- | ---: | ---: | --- |
| B01 `e- e+ -> mu- mu+` | 1 | 1 | `ElAel-MuAmu` |
| B02 `e- gamma -> e- gamma` | 2 | 2 | `ElGa-ElGa` |
| B03 `e- mu- -> e- mu-` | 1 | 1 | `ElMu-ElMu` |

Authoritative run: `runs/day4_native_regression/20260813_105718`.

## Native M2 Regression

PASS for bounded benchmark regression runs.

| benchmark | status | runtime s | result |
| --- | --- | ---: | --- |
| B01 | PASS | 10.165 | `2 e^4 (t^2 + u^2) / s^2` |
| B02 | PASS | 7.734 | official Compton expression; massless `-2 e^4 (s^2 + u^2)/(s u)` |
| B03 | PASS | 5.956 | `2 e^4 (s^2 + u^2) / t^2` |

Authoritative run: `runs/day4_native/20260813_145016`.

## Known Contract Issue For Day 5

Day-4 M2 regression was explicitly user-authorized as a bounded benchmark regression. Production `heavy_calculation` approval in the PhysicsCard/runtime contract remained `not_requested`. This is a known contract issue: Day 5 should distinguish bounded benchmark QA authorization from production heavy-calculation approval without rewriting historical timestamps or changing the meaning of existing approval records.

## Backend Comparison

PASS WITH WARNINGS.

| benchmark | classification |
| --- | --- |
| B01 | `CONVENTION_MAP_REQUIRED` |
| B02 | `CONVENTION_MAP_REQUIRED` |
| B03 | `LEGACY_LIMITATION` |

Native FeynArts/FeynCalc remains the primary standard-sector regression reference. The legacy backend remains useful for reference/custom fallback but should not be promoted back to standard-QED production.

## Repository Cleanup

PASS. Cleanup report: `reports/DAY4_REPOSITORY_CLEANUP.md`.

The cleanup retained the authoritative Day-4 evidence runs and removed caches, machine-local environment outputs, tracked Day-3 generated benchmark artifacts, redundant `.gitkeep` files, and superseded runs covered by the pre-clean snapshot.

## Tests

Latest in-repo results before packaging:

- `python scripts/validate_examples.py`: PASS.
- `python -m pytest`: PASS, 67 passed.
- `git diff --check`: PASS.

ZIP self-test: PASS. SHA256 `a96297f0d0f18d4a825db080e3c0e70b1f2478ba427480f06b69aeee53dcc9de`. Validation exit code 0; pytest exit code 0. Full record: `reports/DAY4_ZIP_SELFTEST.md`.

## Git Diff Summary

~~~text
.gitignore                                         |   4 +-
 AGENTS.md                                          |   3 +-
 README.md                                          |  25 +-
 benchmarks/.gitkeep                                |   1 -
 benchmarks/B00_environment/README.md               |   2 +-
 benchmarks/B00_environment/outputs/.gitkeep        |   1 -
 .../B00_environment/outputs/commands_executed.txt  |  11 -
 .../outputs/lualatex_command.stderr.log            |   1 -
 .../outputs/lualatex_command.stdout.log            |  35 --
 .../outputs/lualatex_version.stderr.log            | Bin 718 -> 0 bytes
 .../outputs/lualatex_version.stdout.log            | Bin 930 -> 0 bytes
 benchmarks/B00_environment/outputs/os.stderr.log   |   1 -
 benchmarks/B00_environment/outputs/os.stdout.log   |  10 -
 .../outputs/pdflatex_command.stderr.log            |   1 -
 .../outputs/pdflatex_command.stdout.log            |  35 --
 .../outputs/pdflatex_version.stderr.log            | Bin 718 -> 0 bytes
 .../outputs/pdflatex_version.stdout.log            | Bin 1742 -> 0 bytes
 .../outputs/python_version.stderr.log              |   0
 .../outputs/python_version.stdout.log              | Bin 296 -> 0 bytes
 .../outputs/tikz_compile.exitcode.txt              |   1 -
 .../outputs/tikz_compile.stderr.log                | Bin 838 -> 0 bytes
 .../outputs/tikz_compile.stdout.log                | Bin 18310 -> 0 bytes
 .../outputs/tikz_compile/tikz_smoke_test.aux       |   2 -
 .../outputs/tikz_compile/tikz_smoke_test.log       | 554 ------------------
 .../outputs/tikz_compile/tikz_smoke_test.pdf       | Bin 18881 -> 0 bytes
 .../outputs/wolframscript_command.stderr.log       |   1 -
 .../outputs/wolframscript_command.stdout.log       |  35 --
 .../outputs/wolframscript_file_smoke.stderr.log    |   0
 .../outputs/wolframscript_file_smoke.stdout.log    | Bin 3664 -> 0 bytes
 .../outputs/wolframscript_version.stderr.log       |   0
 .../outputs/wolframscript_version.stdout.log       | Bin 108 -> 0 bytes
 benchmarks/B01_ee_to_mumu/README.md                |   4 +-
 benchmarks/B01_ee_to_mumu/amplitude_audit.md       |  19 -
 .../B01_ee_to_mumu/amplitude_ir.example.yaml       | 337 -----------
 benchmarks/B01_ee_to_mumu/amplitude_ir.yaml        | 342 -----------
 benchmarks/B01_ee_to_mumu/amplitude_smoke.wl       |  14 -
 benchmarks/B01_ee_to_mumu/amplitudes.pdf           | Bin 100507 -> 0 bytes
 benchmarks/B01_ee_to_mumu/amplitudes.tex           |  52 --
 benchmarks/B01_ee_to_mumu/amplitudes.wl            |  39 --
 benchmarks/B01_ee_to_mumu/compute_m2.wl            |  34 --
 benchmarks/B01_ee_to_mumu/diagrams.yaml            | 164 ------
 benchmarks/B01_ee_to_mumu/expected.yaml            |  29 -
 benchmarks/B01_ee_to_mumu/rule_manifest.yaml       |  18 -
 benchmarks/B02_compton/README.md                   |   6 +-
 benchmarks/B02_compton/amplitude_audit.md          |  20 -
 benchmarks/B02_compton/amplitude_ir.example.yaml   | 328 -----------
 benchmarks/B02_compton/amplitude_ir.yaml           | 623 ---------------------
 benchmarks/B02_compton/amplitude_smoke.wl          |  14 -
 benchmarks/B02_compton/amplitudes.pdf              | Bin 110138 -> 0 bytes
 benchmarks/B02_compton/amplitudes.tex              |  77 ---
 benchmarks/B02_compton/amplitudes.wl               |  59 --
 benchmarks/B02_compton/compute_m2.wl               |  34 --
 benchmarks/B02_compton/diagrams.yaml               | 316 -----------
 benchmarks/B02_compton/expected.yaml               |  32 --
 benchmarks/B02_compton/rule_manifest.yaml          |  17 -
 benchmarks/B02_compton/ward_check.wl               |  12 -
 docs/ARCHITECTURE.md                               | 136 ++---
 docs/ENVIRONMENT_REPORT.md                         |  70 ---
 pyproject.toml                                     |   2 +-
 reports/.gitkeep                                   |   1 -
 reports/FeynAgent_Day3_Review_Bundle.zip           | Bin 307683 -> 0 bytes
 rules/.gitkeep                                     |   1 -
 schemas/.gitkeep                                   |   1 -
 scripts/.gitkeep                                   |   1 -
 scripts/generate_amplitudes.py                     |   9 +-
 scripts/validate_examples.py                       | 185 +++++-
 tests/.gitkeep                                     |   1 -
 tests/test_amplitude_backends.py                   |   4 +-
 tests/test_amplitude_builder.py                    |   4 +-
 tests/test_amplitude_ir_schema.py                  |   4 +-
 tests/test_b02_compton.py                          |   9 +-
 tests/test_day2_benchmarks.py                      |   4 +-
 72 files changed, 251 insertions(+), 3494 deletions(-)
~~~

## Human Decisions Still Required

- Repair the Day-5 approval contract around bounded benchmark M2 regression versus production `heavy_calculation` approval.
- Decide when to begin custom nonstandard-interaction model adapter work.
- Keep legacy backend as reference/custom fallback unless future custom-model requirements demand repair of the executable legacy convention map.

## Day 5 Readiness

READY_FOR_DAY5, assuming the Day-5 first task addresses the approval-contract issue before any new heavy-production workflow is introduced.
