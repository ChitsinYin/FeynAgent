# Day 5 ZIP Self-Test

Generated at: 2026-08-13T20:02:13.6346738+08:00

## Executive status

PASS

## Bundle

- Path: `reports/FeynAgent_Day5_Review_Bundle.zip`
- SHA256: `d56d974c0ce40f1d034d0d6ff2d5340094e2c9f1e3276954cbbabf92c23ada68`
- Bytes: `131625`

## Clean Extraction Test

- Extracted to a fresh temporary directory.
- Commands were executed from inside the extracted directory, not the development repository.
- Temporary extraction directory was removed after the test.

## Results

| command | exit code | status |
| --- | ---: | --- |
| `python scripts/validate_examples.py` | 0 | PASS |
| `python -m pytest` | 0 | PASS, 75 passed |

## Pytest Tail

```text
rootdir: C:\Users\lenovo\AppData\Local\Temp\feynagent_day5_zip_selftest_20260813_200135
collected 75 items

...

============================= 75 passed in 13.53s =============================
```

## Validation Tail

```text
PASS rules/qed/qed_tree_v1.yaml
PASS profiles/backends/feynarts_sm_qed.yaml
PASS profiles/backends/legacy_sm_qed.yaml
PASS benchmarks/B01_ee_to_mumu/physics_card.yaml
PASS benchmarks/B02_compton/physics_card.yaml
PASS benchmarks/B03_emu_to_emu/physics_card.yaml
PASS benchmarks/B01_ee_to_mumu/native_expected.yaml
PASS benchmarks/B02_compton/native_expected.yaml
PASS benchmarks/B03_emu_to_emu/native_expected.yaml
```
