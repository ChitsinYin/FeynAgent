# Day 4 ZIP Self-Test

Generated at: 2026-08-13 16:16:39 +0800

## Status

PASS

## ZIP Under Test

- Path: `reports/FeynAgent_Day4_Review_Bundle.zip`
- SHA256: `a96297f0d0f18d4a825db080e3c0e70b1f2478ba427480f06b69aeee53dcc9de`
- Extracted to fresh temp directory: `C:\Users\lenovo\AppData\Local\Temp\FeynAgent_day4_zip_selftest_7qmt6jyb`

## Schema Validation

- Command: `python scripts/validate_examples.py`
- Exit code: 0
- Runtime seconds: 0.586

~~~text
PASS rules/qed/qed_tree_v1.yaml
PASS benchmarks/B01_ee_to_mumu/physics_card.yaml
PASS benchmarks/B01_ee_to_mumu/convention_card.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/diagrams.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/amplitude_ir.example.yaml
PASS benchmarks/B02_compton/physics_card.yaml
PASS benchmarks/B02_compton/convention_card.yaml
PASS benchmarks/B02_compton/legacy/diagrams.yaml
PASS benchmarks/B02_compton/legacy/amplitude_ir.example.yaml
PASS benchmarks/B03_emu_to_emu/physics_card.yaml
PASS benchmarks/B03_emu_to_emu/convention_card.yaml
PASS profiles/backends/feynarts_sm_qed.yaml
PASS benchmarks/B01_ee_to_mumu/native_expected.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/rule_manifest.yaml
PASS benchmarks/B02_compton/native_expected.yaml
PASS benchmarks/B02_compton/legacy/rule_manifest.yaml
PASS benchmarks/B03_emu_to_emu/native_expected.yaml
~~~

Stderr:

~~~text

~~~

## Python Tests

- Command: `python -m pytest`
- Exit code: 0
- Runtime seconds: 5.089

~~~text
============================= test session starts =============================
platform win32 -- Python 3.10.9, pytest-7.3.1, pluggy-1.0.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: C:\Users\lenovo\AppData\Local\Temp\FeynAgent_day4_zip_selftest_7qmt6jyb
plugins: anyio-3.5.0, asyncio-0.21.0, benchmark-4.0.0, cov-4.0.0, integration-0.2.3, mock-3.10.0
asyncio: mode=strict
collected 67 items

tests\test_amplitude_backends.py .....                                   [  7%]
tests\test_amplitude_builder.py .........                                [ 20%]
tests\test_amplitude_ir_schema.py .....                                  [ 28%]
tests\test_b02_compton.py ............                                   [ 46%]
tests\test_day2_benchmarks.py ........                                   [ 58%]
tests\test_feynarts_feyncalc_backend.py ........                         [ 70%]
tests\test_schema_files.py ...                                           [ 74%]
tests\test_tikz_renderer.py ......                                       [ 83%]
tests\test_topology_generator.py ...........                             [100%]

============================= 67 passed in 4.42s ==============================
~~~

Stderr:

~~~text

~~~

## Notes

The self-test was run from the extracted ZIP payload, not from the working repository. No physics calculations or Wolfram scripts were executed by this self-test.
