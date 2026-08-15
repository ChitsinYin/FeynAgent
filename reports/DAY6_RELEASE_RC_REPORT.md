# Day 6 Release Candidate QA Report

Status: STANDARD_NATIVE_RC_PASS

## Decision

FeynAgent standard-native v0.1 release-candidate QA passes. The release candidate remains limited to tree-level standard-QED 2-to-2 workflows with external `e-`, `e+`, `mu-`, `mu+`, and `gamma` states. It is not ready for custom gravity or arbitrary SM/BSM production claims.

## Mandatory Gates

| # | Gate | Status | Evidence |
|---:|---|---:|---|
| 1 | one-command high-level runner exists | PASS | `python -m feynagent run --help` exposes `--physics-card`, `--backend-profile`, `--execution-request`, and `--run-root`. |
| 2 | B01/B02/B03 runner PASS | PASS | Fresh QA runs under `runs/day6_rc_qa/runner`; all returned 0 and manifest `PASS`. |
| 3 | diagrams.pdf exists and is physics-correct | PASS | B01 has one `s` diagram, B02 has `s/u`, B03 has one `t`; all `diagrams.pdf` files are nonempty. |
| 4 | per-channel amplitudes exist | PASS | `amplitudes.json` maps every diagram to channel/routing and `feyncalc_amplitudes.m`. |
| 5 | amplitudes.tex/pdf exist | PASS | All three runs produced `amplitudes.tex` and nonempty `amplitudes.pdf`. |
| 6 | FeynCalc amplitude artifacts exist | PASS | All three runs produced `native_amplitude.wl` and `feyncalc_amplitudes.m`. |
| 7 | generic QED M2 reproduces official results | PASS | B01, B02, B03 M2 manifests report `fc_compare_status=True`, `equivalence=True`, `status=PASS`. |
| 8 | ExecutionRequest gates heavy execution | PASS | M2 execution request is missing required operation(s): ['heavy_simplification'] |
| 9 | real Codex skill install/discovery tested | PASS_WITH_MANUAL_INSTALL | `reports/DAY6_CODEX_SKILL_INSTALL.md`; fresh task discovered FeynAgent skill and invoked `python -m feynagent run`. |
| 10 | wheel non-editable install E2E PASS | PASS | `reports/DAY6_WHEEL_INSTALL_E2E.md`; fresh venv wheel install and B02 workflow passed. |
| 11 | no PYTHONPATH workaround required | PASS | Wheel E2E recorded `PYTHONPATH=None` and import from `site-packages`. |
| 12 | no accidental dev-only runtime dependency | PASS | Wheel metadata direct runtime requirements: `jsonschema>=4`, `PyYAML>=6`. |
| 13 | README newbie quickstart tested | PASS | Commands and workflow covered by wheel E2E, skill discovery test, and release metadata audit. |
| 14 | LICENSE decision resolved | PASS | User selected Apache-2.0; root `LICENSE`, `pyproject.toml`, `CITATION.cff`, README updated. |
| 15 | no caches/local .feynagent/runs/review ZIP staged | PASS | Verified during final staging audit before commit; generated runs and ZIP are kept untracked/ignored. |

## Fresh B01/B02/B03 Runner Evidence

### B01_ee_to_mumu

- status: `PASS`
- validation: `PASS`
- runtime: `23.756 s`
- run_dir: `E:\003hep-ph-research\Agent\FeynAgent\runs\day6_rc_qa\runner\20260815_123819_b01_ee_to_mumu_8a74040c`
- diagram_count: `1`
- channels: `s`
- routings: `p1+p2`
- diagrams.pdf bytes: `17687`
- amplitudes.pdf bytes: `66886`
- M2 status: `PASS` via `benchmark_regression`
- M2 comparison: `{'equivalence': 'True', 'fc_compare_status': 'True', 'status': 'PASS'}`
- M2 result: `(2*(t^2 + u^2)*SMP["e"]^4)/s^2`

### B02_compton

- status: `PASS`
- validation: `PASS`
- runtime: `23.334 s`
- run_dir: `E:\003hep-ph-research\Agent\FeynAgent\runs\day6_rc_qa\runner\20260815_123842_b02_compton_62c27c31`
- diagram_count: `2`
- channels: `s, u`
- routings: `p1+k1, p1-k2`
- diagrams.pdf bytes: `20552`
- amplitudes.pdf bytes: `76195`
- M2 status: `PASS` via `benchmark_regression`
- M2 comparison: `{'equivalence': 'True', 'fc_compare_status': 'True', 'status': 'PASS'}`
- M2 result: `(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)`

### B03_emu_to_emu

- status: `PASS`
- validation: `PASS`
- runtime: `23.799 s`
- run_dir: `E:\003hep-ph-research\Agent\FeynAgent\runs\day6_rc_qa\runner\20260815_123905_b03_emu_to_emu_db46b696`
- diagram_count: `1`
- channels: `t`
- routings: `p1-p3`
- diagrams.pdf bytes: `17657`
- amplitudes.pdf bytes: `66696`
- M2 status: `PASS` via `benchmark_regression`
- M2 comparison: `{'equivalence': 'True', 'fc_compare_status': 'True', 'status': 'PASS'}`
- M2 result: `(2*(s^2 + u^2)*SMP["e"]^4)/t^2`

## Readiness

- `STANDARD_NATIVE_RC_PASS`
- `READY_FOR_CUSTOM_GRAVITY`: no
- `NOT_READY`: custom gravity/graviton workflows have no passing benchmarks and remain explicitly unsupported.

## Validation Commands

```text
python -m feynagent run --help -> PASS
python scripts\validate_examples.py -> PASS
python -m pytest -> 89 passed
python -m build --sdist --wheel -> PASS
git diff --check -> PASS
```
