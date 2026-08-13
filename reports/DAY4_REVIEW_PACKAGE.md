# FeynAgent Day 4 Review Package

Generated at: 2026-08-13 16:16:07 +0800

## Milestone Summary

Day 4 adopts `feynarts_feyncalc_native` as the primary production backend for standard QED/SM/QCD sectors supported by installed native model files. The legacy Python backend and QED RuleRegistry were not deleted; they remain reference/fallback/custom-audit infrastructure.

## Repository Tree To Depth 4

~~~text
.
  .gitattributes
  .gitignore
  AGENTS.md
  README.md
  pyproject.toml
  .benchmarks/
  benchmarks/
    DAY2_BENCHMARK_SUMMARY.md
    LEGACY_DAY3_GENERATED.md
    B00_environment/
      README.md
      expected.yaml
      smoke_test.wl
      tikz_smoke_test.tex
    B01_ee_to_mumu/
      README.md
      convention_card.yaml
      native_expected.yaml
      physics_card.yaml
      legacy/
        amplitude_ir.example.yaml
        diagrams.yaml
        expected.yaml
        rule_manifest.yaml
    B02_compton/
      README.md
      convention_card.yaml
      native_expected.yaml
      physics_card.yaml
      legacy/
        amplitude_ir.example.yaml
        diagrams.yaml
        expected.yaml
        rule_manifest.yaml
    B03_emu_to_emu/
      README.md
      convention_card.yaml
      native_expected.yaml
      physics_card.yaml
  docs/
    ARCHITECTURE.md
    BACKEND_STRATEGY.md
    DAY3_DESIGN_DECISIONS.md
    DAY4_DESIGN_DECISIONS.md
    DESIGN_DECISIONS.md
    ENVIRONMENT_SETUP.md
    MIGRATION_0_1_0_TO_0_1_1.md
    MIGRATION_0_1_1_TO_0_1_2.md
    MIGRATION_DAY3_TO_NATIVE_BACKEND.md
    QED_CONVENTION_AUDIT.md
    SCOPE_V0_1.md
  profiles/
    backends/
      feynarts_sm_qed.yaml
  reports/
    DAY1_REPORT.md
    DAY1_REVIEW_PACKAGE.md
    DAY2_FEYNARTS_CROSSCHECK.md
    DAY2_REPORT.md
    DAY2_REVIEW_PACKAGE.md
    DAY3_REPORT.md
    DAY3_REVIEW_PACKAGE.md
    DAY4_BACKEND_COMPARISON.md
    DAY4_M2_REGRESSION.md
    DAY4_NATIVE_AMPLITUDE_REGRESSION.md
    DAY4_PRECLEAN_MANIFEST.md
    DAY4_REPORT.md
    DAY4_REPOSITORY_CLEANUP.md
  rules/
    qed/
      qed_tree_v1.yaml
  runs/
    .gitkeep
    day4_cleanup_actions.json
    day4_backend_comparison/
      20260813_150031/
        RUN_ID.txt
        legacy_structural_summary.json
        B01_ee_to_mumu/
        B02_compton/
        B03_emu_to_emu/
    day4_native/
      20260813_145016/
        RUN_ID.txt
        SHA256SUMS.txt
        process_results.json
        B01_ee_to_mumu/
        B02_compton/
        B03_emu_to_emu/
    day4_native_regression/
      20260813_105718/
        RUN_ID.txt
        B01_ee_to_mumu/
        B02_compton/
        B03_emu_to_emu/
  schemas/
    amplitude_ir.schema.json
    convention_card.schema.json
    diagram_ir.schema.json
    physics_card.schema.json
    rule_registry.schema.json
  scripts/
    generate_amplitudes.py
    generate_diagrams.py
    render_diagrams.py
    validate_examples.py
  src/
    feynagent/
      __init__.py
      amplitudes/
        __init__.py
        backends.py
        builder.py
      backends/
        __init__.py
        feynarts_feyncalc.py
      diagrams/
        __init__.py
        topology.py
      render/
        __init__.py
        tikz.py
  tests/
    test_amplitude_backends.py
    test_amplitude_builder.py
    test_amplitude_ir_schema.py
    test_b02_compton.py
    test_day2_benchmarks.py
    test_feynarts_feyncalc_backend.py
    test_schema_files.py
    test_tikz_renderer.py
    test_topology_generator.py
~~~

## Git Context

Current HEAD before Day-4 closeout commit:

~~~text
b31f530f82c2240918fa47df75ee2f4e11af6760
~~~

Recent commits:

~~~text
b31f530 day3: add audited QED amplitude assembly and FeynCalc generation
185f7f2 day2: add deterministic tree diagram generation and rendering
ee10a67 day1: freeze FeynAgent v0.1 scope and architecture
~~~

Tracked diff summary:

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

Tracked changed files:

~~~text
.gitignore
AGENTS.md
README.md
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
docs/ARCHITECTURE.md
docs/ENVIRONMENT_REPORT.md
pyproject.toml
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

## Architecture Closure

- Native FeynArts/FeynCalc backend: production standard backend for supported sectors.
- Legacy Python builder: reference/fallback/regression path; not deleted.
- RuleRegistry: custom-rule authority and legacy QED audit snapshot; not the source for native standard QED amplitudes.
- Generated outputs: `runs/`.
- Machine-local diagnostics: `.feynagent/` or run-specific diagnostics under `runs/init/`.

## Migration Summary

- B01/B02 legacy-only fixtures moved to benchmark-local `legacy/` directories.
- B01/B02/B03 native metadata now references `profiles/backends/feynarts_sm_qed.yaml`.
- Historical generated benchmark artifacts were removed after the pre-clean safety archive.
- Generic Day-3 `compute_m2.wl` scripts were retired from production and removed from benchmark directories.

## Native Evidence Runs

| evidence | authoritative run |
| --- | --- |
| Native amplitude regression | `runs/day4_native_regression/20260813_105718` |
| Native M2 regression | `runs/day4_native/20260813_145016` |
| Native-vs-legacy comparison | `runs/day4_backend_comparison/20260813_150031` |

## Native Regression Results

- B01 diagram count: PASS, 1.
- B02 diagram count: PASS, 2.
- B03 diagram count: PASS, 1.
- B01 M2: PASS, `2 e^4 (t^2 + u^2) / s^2`.
- B02 M2: PASS, official Compton expression; massless `-2 e^4 (s^2 + u^2)/(s u)`.
- B03 M2: PASS, `2 e^4 (s^2 + u^2) / t^2`.

## Contract Warning

The Day-4 M2 regression was explicitly authorized by the user as a bounded benchmark regression. It should not be interpreted as production `heavy_calculation` approval, which remained `not_requested`. Day 5 should repair this contract distinction.

## ZIP Contents Policy

The review ZIP includes source, schemas, benchmark specs/fixtures, profiles, docs, Markdown reports, and selected authoritative Day-4 evidence runs. It excludes `.git`, caches, old unrelated runs, ignored handoff ZIPs, and machine-local absolute-path diagnostics. Text files copied into the ZIP staging area are sanitized to replace local absolute paths with placeholders.

## Tests

- `python scripts/validate_examples.py`: PASS.
- `python -m pytest`: PASS, 67 passed.
- ZIP self-test: PASS, SHA256 `a96297f0d0f18d4a825db080e3c0e70b1f2478ba427480f06b69aeee53dcc9de`; see `reports/DAY4_ZIP_SELFTEST.md`.

## Warnings

- FeynCalc headless runs emitted front-end availability warnings in previous evidence logs; they did not affect Day-4 regression comparisons.
- B01/B02 legacy-vs-native comparison requires an explicit convention/representation map for squared-amplitude equality.
- B03 is a legacy limitation: native backend supports it; legacy benchmark entry path does not without scope changes.
