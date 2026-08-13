# Day 4 Repository Cleanup

Generated at: 2026-08-13 16:07:20 +0800

## Executive Status

PASS

The controlled cleanup was performed after verifying the Phase-0 external safety snapshot. No physics code was modified for new calculations, no new physics calculations were run, the legacy custom backend source was retained, and the legacy QED RuleRegistry was retained.

## Safety Snapshot

- Archive: `E:\003hep-ph-research\Agent\FeynAgent_pre_day4_closeout_20260813_155226.zip`
- SHA256: `6f7a50c3634de22276554ad88a121224e04589648bea7d35fcad6959007c26ae`
- Sidecar: `E:\003hep-ph-research\Agent\FeynAgent_pre_day4_closeout_20260813_155226.zip.sha256`
- In-repository manifest: `reports/DAY4_PRECLEAN_MANIFEST.md`
- HEAD during cleanup: `b31f530f82c2240918fa47df75ee2f4e11af6760`

## Files Deleted

- Transient caches:
  - `.pytest_cache/`
  - all `__pycache__/`
  - all `*.pyc`
  - `.benchmarks/`
- Tracked historical review bundle:
  - `reports/FeynAgent_Day3_Review_Bundle.zip`
- Tracked machine-local environment probe outputs:
  - `benchmarks/B00_environment/outputs/`
- Superseded environment report:
  - `docs/ENVIRONMENT_REPORT.md`
- Day-3 generated artifacts formerly tracked under B01/B02 benchmark directories:
  - `amplitude_audit.md`
  - `amplitude_ir.yaml`
  - `amplitude_smoke.wl`
  - `amplitudes.tex`
  - `amplitudes.pdf`
  - `amplitudes.wl`
  - `compute_m2.wl`
  - `ward_check.wl` for B02
- Benchmark-local native backend profile files superseded by the shared profile:
  - `benchmarks/B01_ee_to_mumu/native_backend.yaml`
  - `benchmarks/B02_compton/native_backend.yaml`
  - `benchmarks/B03_emu_to_emu/native_backend.yaml`
- Unnecessary `.gitkeep` files in directories that now contain tracked files:
  - `benchmarks/.gitkeep`
  - `reports/.gitkeep`
  - `rules/.gitkeep`
  - `schemas/.gitkeep`
  - `scripts/.gitkeep`
  - `tests/.gitkeep`

## Files Moved

Legacy-only B01 fixtures were moved into `benchmarks/B01_ee_to_mumu/legacy/`:

- `diagrams.yaml`
- `expected.yaml`
- `rule_manifest.yaml`
- `amplitude_ir.example.yaml`

Legacy-only B02 fixtures were moved into `benchmarks/B02_compton/legacy/`:

- `diagrams.yaml`
- `expected.yaml`
- `rule_manifest.yaml`
- `amplitude_ir.example.yaml`

The moved rule manifests were updated so their canonical QED RuleRegistry relative paths still resolve correctly.

## Files Intentionally Retained

- Legacy custom backend source under `src/feynagent/`, including the custom diagram and amplitude implementation.
- Legacy QED RuleRegistry snapshot: `rules/qed/qed_tree_v1.yaml`.
- Benchmark specifications, gold/reference fixtures, and native expected metadata under `benchmarks/`.
- Authoritative Day-4 evidence runs:
  - `runs/day4_native_regression/20260813_105718`
  - `runs/day4_native/20260813_145016`
  - `runs/day4_backend_comparison/20260813_150031`
- `runs/.gitkeep`, retained so the generated-artifact root remains present in a fresh checkout.

## Old Runs Archived/Deleted

The following superseded run directories were removed after confirming the external safety archive exists:

- `runs/day2_benchmarks`
- `runs/day2_feynarts_crosscheck`
- `runs/day2_final_qa`
- `runs/day2_render`
- `runs/day3_fermion_flow`
- `runs/day3_final_qa`
- `runs/qed_convention_audit`
- `runs/day4_native_backend`
- `runs/day4_native_regression/20260813_105543`

The authoritative Day-4 evidence runs listed above were not removed.

## Environment Cleanup

- Added `docs/ENVIRONMENT_SETUP.md` for reproducible local setup expectations.
- Added `benchmarks/B00_environment/expected.yaml` as the benchmark-side expected environment contract.
- Updated `benchmarks/B00_environment/README.md` to state that local probe logs belong in `.feynagent/` or `runs/init/<run_id>/`, not under tracked benchmark outputs.
- Added `.feynagent/` to `.gitignore`.

## Benchmark Organization

- B01/B02 legacy-only fixtures now live under benchmark-local `legacy/` directories.
- Tests and legacy scripts were updated to read those fixtures from the new locations.
- New generated amplitude artifacts are kept out of `benchmarks/`; generated artifacts belong under `runs/`.

## Backend Profile Deduplication

- Added shared profile: `profiles/backends/feynarts_sm_qed.yaml`.
- B01, B02, and B03 native benchmark metadata now reference this shared profile via `backend_profile`.
- The profile keeps the native FeynArts/FeynCalc QED setup centralized:
  - `model: SM`
  - `generic_model: Lorentz`
  - `restrictions: QEDOnly`
  - `insertion_level: Classes`

## EOL Hygiene

- Added `.gitattributes` with repository-wide LF normalization and binary declarations for PDF/ZIP/image artifacts.
- Normalized `AGENTS.md` without changing its content meaningfully.

## Tests

- `python scripts/validate_examples.py`: PASS, 9 examples validated.
- `python -m pytest`: PASS, 67 passed.
- `git diff --check`: PASS.
- Post-test cache cleanup: `.pytest_cache`, `.benchmarks`, `__pycache__`, and `*.pyc` removed again.

## Git Diff Summary

Tracked diff summary using `git diff --ignore-space-at-eol --stat`:

~~~text
.gitignore                                         |   4 +-
 AGENTS.md                                          |   3 +-
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
 docs/ENVIRONMENT_REPORT.md                         |  70 ---
 reports/.gitkeep                                   |   1 -
 reports/FeynAgent_Day3_Review_Bundle.zip           | Bin 307683 -> 0 bytes
 rules/.gitkeep                                     |   1 -
 schemas/.gitkeep                                   |   1 -
 scripts/.gitkeep                                   |   1 -
 scripts/generate_amplitudes.py                     |   9 +-
 scripts/validate_examples.py                       |   6 +-
 tests/.gitkeep                                     |   1 -
 tests/test_amplitude_backends.py                   |   4 +-
 tests/test_amplitude_builder.py                    |   4 +-
 tests/test_amplitude_ir_schema.py                  |   4 +-
 tests/test_b02_compton.py                          |   9 +-
 tests/test_day2_benchmarks.py                      |   4 +-
 69 files changed, 33 insertions(+), 3370 deletions(-)
~~~

Tracked changed files using `git diff --ignore-space-at-eol --name-only`:

~~~text
.gitignore
AGENTS.md
benchmarks/.gitkeep
benchmarks/B00_environment/README.md
benchmarks/B00_environment/outputs/.gitkeep
benchmarks/B00_environment/outputs/commands_executed.txt
benchmarks/B00_environment/outputs/lualatex_command.stderr.log
benchmarks/B00_environment/outputs/lualatex_command.stdout.log
benchmarks/B00_environment/outputs/lualatex_version.stderr.log
benchmarks/B00_environment/outputs/lualatex_version.stdout.log
benchmarks/B00_environment/outputs/os.stderr.log
benchmarks/B00_environment/outputs/os.stdout.log
benchmarks/B00_environment/outputs/pdflatex_command.stderr.log
benchmarks/B00_environment/outputs/pdflatex_command.stdout.log
benchmarks/B00_environment/outputs/pdflatex_version.stderr.log
benchmarks/B00_environment/outputs/pdflatex_version.stdout.log
benchmarks/B00_environment/outputs/python_version.stderr.log
benchmarks/B00_environment/outputs/python_version.stdout.log
benchmarks/B00_environment/outputs/tikz_compile.exitcode.txt
benchmarks/B00_environment/outputs/tikz_compile.stderr.log
benchmarks/B00_environment/outputs/tikz_compile.stdout.log
benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.aux
benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.log
benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.pdf
benchmarks/B00_environment/outputs/wolframscript_command.stderr.log
benchmarks/B00_environment/outputs/wolframscript_command.stdout.log
benchmarks/B00_environment/outputs/wolframscript_file_smoke.stderr.log
benchmarks/B00_environment/outputs/wolframscript_file_smoke.stdout.log
benchmarks/B00_environment/outputs/wolframscript_version.stderr.log
benchmarks/B00_environment/outputs/wolframscript_version.stdout.log
benchmarks/B01_ee_to_mumu/README.md
benchmarks/B01_ee_to_mumu/amplitude_audit.md
benchmarks/B01_ee_to_mumu/amplitude_ir.example.yaml
benchmarks/B01_ee_to_mumu/amplitude_ir.yaml
benchmarks/B01_ee_to_mumu/amplitude_smoke.wl
benchmarks/B01_ee_to_mumu/amplitudes.pdf
benchmarks/B01_ee_to_mumu/amplitudes.tex
benchmarks/B01_ee_to_mumu/amplitudes.wl
benchmarks/B01_ee_to_mumu/compute_m2.wl
benchmarks/B01_ee_to_mumu/diagrams.yaml
benchmarks/B01_ee_to_mumu/expected.yaml
benchmarks/B01_ee_to_mumu/rule_manifest.yaml
benchmarks/B02_compton/README.md
benchmarks/B02_compton/amplitude_audit.md
benchmarks/B02_compton/amplitude_ir.example.yaml
benchmarks/B02_compton/amplitude_ir.yaml
benchmarks/B02_compton/amplitude_smoke.wl
benchmarks/B02_compton/amplitudes.pdf
benchmarks/B02_compton/amplitudes.tex
benchmarks/B02_compton/amplitudes.wl
benchmarks/B02_compton/compute_m2.wl
benchmarks/B02_compton/diagrams.yaml
benchmarks/B02_compton/expected.yaml
benchmarks/B02_compton/rule_manifest.yaml
benchmarks/B02_compton/ward_check.wl
docs/ENVIRONMENT_REPORT.md
reports/.gitkeep
reports/FeynAgent_Day3_Review_Bundle.zip
rules/.gitkeep
schemas/.gitkeep
scripts/.gitkeep
scripts/generate_amplitudes.py
scripts/validate_examples.py
tests/.gitkeep
tests/test_amplitude_backends.py
tests/test_amplitude_builder.py
tests/test_amplitude_ir_schema.py
tests/test_b02_compton.py
tests/test_day2_benchmarks.py
~~~

## Git Status

~~~text
M .gitignore
 M AGENTS.md
 D benchmarks/.gitkeep
 M benchmarks/B00_environment/README.md
 D benchmarks/B00_environment/outputs/.gitkeep
 D benchmarks/B00_environment/outputs/commands_executed.txt
 D benchmarks/B00_environment/outputs/lualatex_command.stderr.log
 D benchmarks/B00_environment/outputs/lualatex_command.stdout.log
 D benchmarks/B00_environment/outputs/lualatex_version.stderr.log
 D benchmarks/B00_environment/outputs/lualatex_version.stdout.log
 D benchmarks/B00_environment/outputs/os.stderr.log
 D benchmarks/B00_environment/outputs/os.stdout.log
 D benchmarks/B00_environment/outputs/pdflatex_command.stderr.log
 D benchmarks/B00_environment/outputs/pdflatex_command.stdout.log
 D benchmarks/B00_environment/outputs/pdflatex_version.stderr.log
 D benchmarks/B00_environment/outputs/pdflatex_version.stdout.log
 D benchmarks/B00_environment/outputs/python_version.stderr.log
 D benchmarks/B00_environment/outputs/python_version.stdout.log
 D benchmarks/B00_environment/outputs/tikz_compile.exitcode.txt
 D benchmarks/B00_environment/outputs/tikz_compile.stderr.log
 D benchmarks/B00_environment/outputs/tikz_compile.stdout.log
 D benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.aux
 D benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.log
 D benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.pdf
 D benchmarks/B00_environment/outputs/wolframscript_command.stderr.log
 D benchmarks/B00_environment/outputs/wolframscript_command.stdout.log
 D benchmarks/B00_environment/outputs/wolframscript_file_smoke.stderr.log
 D benchmarks/B00_environment/outputs/wolframscript_file_smoke.stdout.log
 D benchmarks/B00_environment/outputs/wolframscript_version.stderr.log
 D benchmarks/B00_environment/outputs/wolframscript_version.stdout.log
 M benchmarks/B01_ee_to_mumu/README.md
 D benchmarks/B01_ee_to_mumu/amplitude_audit.md
 D benchmarks/B01_ee_to_mumu/amplitude_ir.example.yaml
 D benchmarks/B01_ee_to_mumu/amplitude_ir.yaml
 D benchmarks/B01_ee_to_mumu/amplitude_smoke.wl
 D benchmarks/B01_ee_to_mumu/amplitudes.pdf
 D benchmarks/B01_ee_to_mumu/amplitudes.tex
 D benchmarks/B01_ee_to_mumu/amplitudes.wl
 D benchmarks/B01_ee_to_mumu/compute_m2.wl
 D benchmarks/B01_ee_to_mumu/diagrams.yaml
 D benchmarks/B01_ee_to_mumu/expected.yaml
 D benchmarks/B01_ee_to_mumu/rule_manifest.yaml
 M benchmarks/B02_compton/README.md
 D benchmarks/B02_compton/amplitude_audit.md
 D benchmarks/B02_compton/amplitude_ir.example.yaml
 D benchmarks/B02_compton/amplitude_ir.yaml
 D benchmarks/B02_compton/amplitude_smoke.wl
 D benchmarks/B02_compton/amplitudes.pdf
 D benchmarks/B02_compton/amplitudes.tex
 D benchmarks/B02_compton/amplitudes.wl
 D benchmarks/B02_compton/compute_m2.wl
 D benchmarks/B02_compton/diagrams.yaml
 D benchmarks/B02_compton/expected.yaml
 D benchmarks/B02_compton/rule_manifest.yaml
 D benchmarks/B02_compton/ward_check.wl
 D docs/ENVIRONMENT_REPORT.md
 D reports/.gitkeep
 D reports/FeynAgent_Day3_Review_Bundle.zip
 D rules/.gitkeep
 D schemas/.gitkeep
 D scripts/.gitkeep
 M scripts/generate_amplitudes.py
 M scripts/validate_examples.py
 D tests/.gitkeep
 M tests/test_amplitude_backends.py
 M tests/test_amplitude_builder.py
 M tests/test_amplitude_ir_schema.py
 M tests/test_b02_compton.py
 M tests/test_day2_benchmarks.py
?? .gitattributes
?? benchmarks/B00_environment/expected.yaml
?? benchmarks/B01_ee_to_mumu/legacy/
?? benchmarks/B01_ee_to_mumu/native_expected.yaml
?? benchmarks/B02_compton/legacy/
?? benchmarks/B02_compton/native_expected.yaml
?? benchmarks/B03_emu_to_emu/
?? benchmarks/LEGACY_DAY3_GENERATED.md
?? docs/BACKEND_STRATEGY.md
?? docs/DAY4_DESIGN_DECISIONS.md
?? docs/ENVIRONMENT_SETUP.md
?? docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md
?? profiles/
?? reports/DAY4_BACKEND_COMPARISON.md
?? reports/DAY4_M2_REGRESSION.md
?? reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md
?? reports/DAY4_PRECLEAN_MANIFEST.md
?? src/feynagent/backends/
?? tests/test_feynarts_feyncalc_backend.py
~~~

## Notes

- The repository still contains Day-4 implementation/report files from earlier Day-4 work; this cleanup did not remove review-relevant Day-4 source, docs, tests, or reports.
- The native FeynArts/FeynCalc backend remains the production standard backend for standard QED/SM/QCD sectors, while the legacy Python builder remains reference/fallback/custom-audit infrastructure.
- The legacy QED RuleRegistry remains a legacy audit/reference snapshot and future custom-rule authority, not the production source for native standard QED amplitudes.
