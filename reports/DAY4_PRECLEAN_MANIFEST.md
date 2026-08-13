# Day 4 Pre-Cleanup Manifest

Generated at: 2026-08-13T15:52:27.8406882+08:00

## Archive

- Archive path: E:\003hep-ph-research\Agent\FeynAgent_pre_day4_closeout_20260813_155226.zip
- SHA256 path: E:\003hep-ph-research\Agent\FeynAgent_pre_day4_closeout_20260813_155226.zip.sha256
- Archive SHA256: 6f7a50c3634de22276554ad88a121224e04589648bea7d35fcad6959007c26ae
- Archive contents listing: E:\003hep-ph-research\Agent\FeynAgent_pre_day4_closeout_20260813_155226.contents.txt

## Current HEAD

b31f530f82c2240918fa47df75ee2f4e11af6760

## Authoritative Day-4 Run IDs

- Native amplitude regression: runs/day4_native_regression/20260813_105718
- Native M2 regression: runs/day4_native/20260813_145016
- Native-vs-legacy comparison: runs/day4_backend_comparison/20260813_150031

## Git Status Short

~~~text
 M AGENTS.md
 D benchmarks/B01_ee_to_mumu/amplitude_audit.md
 D benchmarks/B01_ee_to_mumu/amplitude_ir.yaml
 D benchmarks/B01_ee_to_mumu/amplitude_smoke.wl
 D benchmarks/B01_ee_to_mumu/amplitudes.pdf
 D benchmarks/B01_ee_to_mumu/amplitudes.tex
 D benchmarks/B01_ee_to_mumu/amplitudes.wl
 D benchmarks/B01_ee_to_mumu/compute_m2.wl
 D benchmarks/B02_compton/amplitude_audit.md
 D benchmarks/B02_compton/amplitude_ir.yaml
 D benchmarks/B02_compton/amplitude_smoke.wl
 D benchmarks/B02_compton/amplitudes.pdf
 D benchmarks/B02_compton/amplitudes.tex
 D benchmarks/B02_compton/amplitudes.wl
 D benchmarks/B02_compton/compute_m2.wl
 D benchmarks/B02_compton/ward_check.wl
 D reports/FeynAgent_Day3_Review_Bundle.zip
?? benchmarks/B01_ee_to_mumu/native_backend.yaml
?? benchmarks/B01_ee_to_mumu/native_expected.yaml
?? benchmarks/B02_compton/native_backend.yaml
?? benchmarks/B02_compton/native_expected.yaml
?? benchmarks/B03_emu_to_emu/
?? benchmarks/LEGACY_DAY3_GENERATED.md
?? docs/BACKEND_STRATEGY.md
?? docs/DAY4_DESIGN_DECISIONS.md
?? docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md
?? reports/DAY4_BACKEND_COMPARISON.md
?? reports/DAY4_M2_REGRESSION.md
?? reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md
?? src/feynagent/backends/
?? tests/test_feynarts_feyncalc_backend.py
~~~

## Git Log -5

~~~text
b31f530 day3: add audited QED amplitude assembly and FeynCalc generation
185f7f2 day2: add deterministic tree diagram generation and rendering
ee10a67 day1: freeze FeynAgent v0.1 scope and architecture
~~~

## Git Diff --stat

~~~text
 AGENTS.md                                    |   5 +-
 benchmarks/B01_ee_to_mumu/amplitude_audit.md |  19 -
 benchmarks/B01_ee_to_mumu/amplitude_ir.yaml  | 342 ---------------
 benchmarks/B01_ee_to_mumu/amplitude_smoke.wl |  14 -
 benchmarks/B01_ee_to_mumu/amplitudes.pdf     | Bin 100507 -> 0 bytes
 benchmarks/B01_ee_to_mumu/amplitudes.tex     |  52 ---
 benchmarks/B01_ee_to_mumu/amplitudes.wl      |  39 --
 benchmarks/B01_ee_to_mumu/compute_m2.wl      |  34 --
 benchmarks/B02_compton/amplitude_audit.md    |  20 -
 benchmarks/B02_compton/amplitude_ir.yaml     | 623 ---------------------------
 benchmarks/B02_compton/amplitude_smoke.wl    |  14 -
 benchmarks/B02_compton/amplitudes.pdf        | Bin 110138 -> 0 bytes
 benchmarks/B02_compton/amplitudes.tex        |  77 ----
 benchmarks/B02_compton/amplitudes.wl         |  59 ---
 benchmarks/B02_compton/compute_m2.wl         |  34 --
 benchmarks/B02_compton/ward_check.wl         |  12 -
 reports/FeynAgent_Day3_Review_Bundle.zip     | Bin 307683 -> 0 bytes
 17 files changed, 3 insertions(+), 1341 deletions(-)
~~~

## Git Diff --ignore-space-at-eol --stat

~~~text
 AGENTS.md                                    |   5 +-
 benchmarks/B01_ee_to_mumu/amplitude_audit.md |  19 -
 benchmarks/B01_ee_to_mumu/amplitude_ir.yaml  | 342 ---------------
 benchmarks/B01_ee_to_mumu/amplitude_smoke.wl |  14 -
 benchmarks/B01_ee_to_mumu/amplitudes.pdf     | Bin 100507 -> 0 bytes
 benchmarks/B01_ee_to_mumu/amplitudes.tex     |  52 ---
 benchmarks/B01_ee_to_mumu/amplitudes.wl      |  39 --
 benchmarks/B01_ee_to_mumu/compute_m2.wl      |  34 --
 benchmarks/B02_compton/amplitude_audit.md    |  20 -
 benchmarks/B02_compton/amplitude_ir.yaml     | 623 ---------------------------
 benchmarks/B02_compton/amplitude_smoke.wl    |  14 -
 benchmarks/B02_compton/amplitudes.pdf        | Bin 110138 -> 0 bytes
 benchmarks/B02_compton/amplitudes.tex        |  77 ----
 benchmarks/B02_compton/amplitudes.wl         |  59 ---
 benchmarks/B02_compton/compute_m2.wl         |  34 --
 benchmarks/B02_compton/ward_check.wl         |  12 -
 reports/FeynAgent_Day3_Review_Bundle.zip     | Bin 307683 -> 0 bytes
 17 files changed, 3 insertions(+), 1341 deletions(-)
~~~

## Git Diff --ignore-space-at-eol --name-only

~~~text
AGENTS.md
benchmarks/B01_ee_to_mumu/amplitude_audit.md
benchmarks/B01_ee_to_mumu/amplitude_ir.yaml
benchmarks/B01_ee_to_mumu/amplitude_smoke.wl
benchmarks/B01_ee_to_mumu/amplitudes.pdf
benchmarks/B01_ee_to_mumu/amplitudes.tex
benchmarks/B01_ee_to_mumu/amplitudes.wl
benchmarks/B01_ee_to_mumu/compute_m2.wl
benchmarks/B02_compton/amplitude_audit.md
benchmarks/B02_compton/amplitude_ir.yaml
benchmarks/B02_compton/amplitude_smoke.wl
benchmarks/B02_compton/amplitudes.pdf
benchmarks/B02_compton/amplitudes.tex
benchmarks/B02_compton/amplitudes.wl
benchmarks/B02_compton/compute_m2.wl
benchmarks/B02_compton/ward_check.wl
reports/FeynAgent_Day3_Review_Bundle.zip
~~~

## Meaningful Tracked Diff

Tracked changes currently consist of AGENTS.md Day-4 policy edits, deletion candidates for generated Day-3 benchmark artifacts that should not remain under benchmarks/, and the missing tracked Day-3 review bundle zip. The whitespace-normalized stat is recorded above.

## Untracked Day-4 Files

~~~text
?? benchmarks/B01_ee_to_mumu/native_backend.yaml
?? benchmarks/B01_ee_to_mumu/native_expected.yaml
?? benchmarks/B02_compton/native_backend.yaml
?? benchmarks/B02_compton/native_expected.yaml
?? benchmarks/B03_emu_to_emu/
?? benchmarks/LEGACY_DAY3_GENERATED.md
?? docs/DAY4_DESIGN_DECISIONS.md
?? docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md
?? reports/DAY4_BACKEND_COMPARISON.md
?? reports/DAY4_M2_REGRESSION.md
?? reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md
?? src/feynagent/backends/
?? tests/test_feynarts_feyncalc_backend.py
~~~

## Candidate Deletions

No deletion was performed in this snapshot step. Current candidate deletions already present in the worktree are:

~~~text
 D benchmarks/B01_ee_to_mumu/amplitude_audit.md
 D benchmarks/B01_ee_to_mumu/amplitude_ir.yaml
 D benchmarks/B01_ee_to_mumu/amplitude_smoke.wl
 D benchmarks/B01_ee_to_mumu/amplitudes.pdf
 D benchmarks/B01_ee_to_mumu/amplitudes.tex
 D benchmarks/B01_ee_to_mumu/amplitudes.wl
 D benchmarks/B01_ee_to_mumu/compute_m2.wl
 D benchmarks/B02_compton/amplitude_audit.md
 D benchmarks/B02_compton/amplitude_ir.yaml
 D benchmarks/B02_compton/amplitude_smoke.wl
 D benchmarks/B02_compton/amplitudes.pdf
 D benchmarks/B02_compton/amplitudes.tex
 D benchmarks/B02_compton/amplitudes.wl
 D benchmarks/B02_compton/compute_m2.wl
 D benchmarks/B02_compton/ward_check.wl
 D reports/FeynAgent_Day3_Review_Bundle.zip
~~~

## Archive Include Policy

The pre-cleanup archive includes current Day-4 reports, Day-4 run artifacts, Day-4 docs/config/specs, the native backend source package, and native backend tests. It excludes .git/, .pytest_cache/, __pycache__/, and *.pyc.

## Archive Contents

~~~text
AGENTS.md
benchmarks/B01_ee_to_mumu/native_backend.yaml
benchmarks/B01_ee_to_mumu/native_expected.yaml
benchmarks/B02_compton/native_backend.yaml
benchmarks/B02_compton/native_expected.yaml
benchmarks/B03_emu_to_emu/convention_card.yaml
benchmarks/B03_emu_to_emu/native_backend.yaml
benchmarks/B03_emu_to_emu/native_expected.yaml
benchmarks/B03_emu_to_emu/physics_card.yaml
benchmarks/B03_emu_to_emu/README.md
benchmarks/LEGACY_DAY3_GENERATED.md
docs/BACKEND_STRATEGY.md
docs/DAY4_DESIGN_DECISIONS.md
docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md
reports/DAY4_BACKEND_COMPARISON.md
reports/DAY4_M2_REGRESSION.md
reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/generated_diagrams.yaml
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_amplitude_ir.yaml
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_amplitudes.tex
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_amplitudes.wl
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_generate_diagrams.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_generate_diagrams.stderr.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_generate_diagrams.stdout.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_map_compare.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_map_compare.stderr.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_map_compare.stdout.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_map_compare.wl
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_mapped.inputform.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_mapped.m
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_mapped_comparison.inputform.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe.stderr.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe.stdout.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe.wl
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe_raw.m
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_m2_probe_simplified.m
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_smoke.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_smoke.stderr.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_smoke.stdout.log
runs/day4_backend_comparison/20260813_150031/B01_ee_to_mumu/legacy_smoke.wl
runs/day4_backend_comparison/20260813_150031/B02_compton/generated_diagrams.yaml
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_amplitude_ir.yaml
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_amplitudes.tex
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_amplitudes.wl
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_generate_diagrams.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_generate_diagrams.stderr.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_generate_diagrams.stdout.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_map_compare.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_map_compare.stderr.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_map_compare.stdout.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_map_compare.wl
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_mapped.inputform.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_mapped.m
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_mapped_comparison.inputform.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe.stderr.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe.stdout.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe.wl
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe_raw.m
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_m2_probe_simplified.m
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_smoke.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_smoke.stderr.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_smoke.stdout.log
runs/day4_backend_comparison/20260813_150031/B02_compton/legacy_smoke.wl
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.clean.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.clean.stderr.log
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.clean.stdout.log
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.exitcode.txt
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.stderr.log
runs/day4_backend_comparison/20260813_150031/B03_emu_to_emu/legacy_generate_diagrams.stdout.log
runs/day4_backend_comparison/20260813_150031/legacy_structural_summary.json
runs/day4_backend_comparison/20260813_150031/RUN_ID.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/comparison_result.inputform.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/DONE
runs/day4_native/20260813_145016/B01_ee_to_mumu/known_result.inputform.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/known_result.m
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_massless.inputform.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_massless.m
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_raw.inputform.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_raw.m
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_regression.wl
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_simplified.inputform.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/m2_simplified.m
runs/day4_native/20260813_145016/B01_ee_to_mumu/runtime_seconds.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/SHA256SUMS.txt
runs/day4_native/20260813_145016/B01_ee_to_mumu/stderr.log
runs/day4_native/20260813_145016/B01_ee_to_mumu/stdout.log
runs/day4_native/20260813_145016/B01_ee_to_mumu/summary.inputform.txt
runs/day4_native/20260813_145016/B02_compton/comparison_result.inputform.txt
runs/day4_native/20260813_145016/B02_compton/DONE
runs/day4_native/20260813_145016/B02_compton/known_massless.inputform.txt
runs/day4_native/20260813_145016/B02_compton/known_massless.m
runs/day4_native/20260813_145016/B02_compton/known_result.inputform.txt
runs/day4_native/20260813_145016/B02_compton/known_result.m
runs/day4_native/20260813_145016/B02_compton/m2_massless.inputform.txt
runs/day4_native/20260813_145016/B02_compton/m2_massless.m
runs/day4_native/20260813_145016/B02_compton/m2_raw.inputform.txt
runs/day4_native/20260813_145016/B02_compton/m2_raw.m
runs/day4_native/20260813_145016/B02_compton/m2_regression.wl
runs/day4_native/20260813_145016/B02_compton/m2_simplified.inputform.txt
runs/day4_native/20260813_145016/B02_compton/m2_simplified.m
runs/day4_native/20260813_145016/B02_compton/runtime_seconds.txt
runs/day4_native/20260813_145016/B02_compton/SHA256SUMS.txt
runs/day4_native/20260813_145016/B02_compton/stderr.log
runs/day4_native/20260813_145016/B02_compton/stdout.log
runs/day4_native/20260813_145016/B02_compton/summary.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/comparison_result.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/DONE
runs/day4_native/20260813_145016/B03_emu_to_emu/known_result.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/known_result.m
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_massless.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_massless.m
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_raw.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_raw.m
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_regression.wl
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_simplified.inputform.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/m2_simplified.m
runs/day4_native/20260813_145016/B03_emu_to_emu/runtime_seconds.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/SHA256SUMS.txt
runs/day4_native/20260813_145016/B03_emu_to_emu/stderr.log
runs/day4_native/20260813_145016/B03_emu_to_emu/stdout.log
runs/day4_native/20260813_145016/B03_emu_to_emu/summary.inputform.txt
runs/day4_native/20260813_145016/process_results.json
runs/day4_native/20260813_145016/RUN_ID.txt
runs/day4_native/20260813_145016/SHA256SUMS.txt
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/feyncalc_amplitude.inputform.txt
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/feyncalc_amplitude.m
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/native_amplitude.wl
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/native_summary.json
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/raw_feynarts_amplitude.inputform.txt
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/raw_feynarts_amplitude.m
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/run_manifest.json
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/stderr.log
runs/day4_native_backend/20260813_101642/B01_ee_to_mumu/stdout.log
runs/day4_native_backend/20260813_101642/B02_compton/feyncalc_amplitude.inputform.txt
runs/day4_native_backend/20260813_101642/B02_compton/feyncalc_amplitude.m
runs/day4_native_backend/20260813_101642/B02_compton/native_amplitude.wl
runs/day4_native_backend/20260813_101642/B02_compton/native_summary.json
runs/day4_native_backend/20260813_101642/B02_compton/raw_feynarts_amplitude.inputform.txt
runs/day4_native_backend/20260813_101642/B02_compton/raw_feynarts_amplitude.m
runs/day4_native_backend/20260813_101642/B02_compton/run_manifest.json
runs/day4_native_backend/20260813_101642/B02_compton/stderr.log
runs/day4_native_backend/20260813_101642/B02_compton/stdout.log
runs/day4_native_backend/20260813_101642/RUN_ID.txt
runs/day4_native_backend/feyncalc_dir_probe.wl
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/native_amplitude.wl
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/native_summary.json
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/run_manifest.json
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/stderr.log
runs/day4_native_regression/20260813_105543/B01_ee_to_mumu/stdout.log
runs/day4_native_regression/20260813_105543/B02_compton/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B02_compton/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105543/B02_compton/native_amplitude.wl
runs/day4_native_regression/20260813_105543/B02_compton/native_summary.json
runs/day4_native_regression/20260813_105543/B02_compton/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B02_compton/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105543/B02_compton/run_manifest.json
runs/day4_native_regression/20260813_105543/B02_compton/stderr.log
runs/day4_native_regression/20260813_105543/B02_compton/stdout.log
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/native_amplitude.wl
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/native_summary.json
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/run_manifest.json
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/stderr.log
runs/day4_native_regression/20260813_105543/B03_emu_to_emu/stdout.log
runs/day4_native_regression/20260813_105543/RUN_ID.txt
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/native_amplitude.wl
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/native_summary.json
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/run_manifest.json
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/stderr.log
runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/stdout.log
runs/day4_native_regression/20260813_105718/B02_compton/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B02_compton/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105718/B02_compton/native_amplitude.wl
runs/day4_native_regression/20260813_105718/B02_compton/native_summary.json
runs/day4_native_regression/20260813_105718/B02_compton/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B02_compton/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105718/B02_compton/run_manifest.json
runs/day4_native_regression/20260813_105718/B02_compton/stderr.log
runs/day4_native_regression/20260813_105718/B02_compton/stdout.log
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/feyncalc_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/feyncalc_amplitude.m
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/native_amplitude.wl
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/native_summary.json
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/raw_feynarts_amplitude.inputform.txt
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/raw_feynarts_amplitude.m
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/run_manifest.json
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/stderr.log
runs/day4_native_regression/20260813_105718/B03_emu_to_emu/stdout.log
runs/day4_native_regression/20260813_105718/RUN_ID.txt
src/feynagent/backends/__init__.py
src/feynagent/backends/feynarts_feyncalc.py
tests/test_feynarts_feyncalc_backend.py
~~~
