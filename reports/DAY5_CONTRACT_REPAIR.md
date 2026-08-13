# Day 5 Contract Repair

Generated at: 2026-08-13T16:45:25.419015+08:00

## Executive Status

PASS

Day 5 separates physics intent, backend implementation, and runtime authorization without adding new physics models.

## Contract Split

- `PhysicsCard` 0.2.0 is backend-neutral and records `model_id` plus `sector`.
- `BackendProfile` resolves backend-neutral theory intent to an implementation.
- `ExecutionRequest` records runtime authorization and is not canonical physics truth.

## PhysicsCard Migration

B01, B02, and B03 now use:

```yaml
model_id: sm_qed
sector: qed
```

Backend-specific RuleRegistry/native-registry selection was removed from the canonical PhysicsCard path.

## Backend Profiles

- `profiles/backends/feynarts_sm_qed.yaml`: resolves `sm_qed/qed` to FeynArts `SM`, `Lorentz`, `QEDOnly`, `Classes`, and profile-local particle mappings.
- `profiles/backends/legacy_sm_qed.yaml`: resolves `sm_qed/qed` to `registry:qed_tree_v1` and `ruleset:qed_tree_v1`.

## ExecutionRequest

Created `schemas/execution_request.schema.json` with modes:

- `structural`
- `amplitude_only`
- `benchmark_regression`
- `production_heavy`

It records backend profile, authorization identity/time, timeout policy, and allowed operations. This repairs the Day-4 contract issue: bounded benchmark M2 regression can be authorized separately from production-heavy approval.

## Native Structural Smoke

Run root: `runs/day5_contract_repair/20260813_164445`

| benchmark | status | Wolfram executed |
| --- | --- | --- |
| B01 | PASS | False |
| B02 | PASS | False |
| B03 | PASS | False |

Native smoke constructed scripts only and did not execute Wolfram/FeynCalc.

## Legacy Structural Smoke

| benchmark | status | channels | internal species | internal momenta |
| --- | --- | --- | --- | --- |
| B01 | PASS | `['s']` | `['gamma']` | `['p1+p2']` |
| B02 | PASS | `['s', 'u']` | `['e-', 'e-']` | `['p1+k1', 'p1-k2']` |
| B03 | PASS | `['t']` | `['gamma']` | `['p1-p3']` |

## B03 Legacy Reclassification

`RESOLVED_CONFIGURATION_COUPLING`

B03 now works through the generic legacy path when `profiles/backends/legacy_sm_qed.yaml` supplies the QED registry/rule-set binding. The Day-4 `LEGACY_LIMITATION` was therefore configuration coupling, not a required benchmark-specific patch.

## Tests

- `python scripts/validate_examples.py`: PASS.
- `python -m pytest`: PASS, 69 passed.
- Native structural smoke: PASS for B01/B02/B03.
- Legacy structural smoke: PASS for B01/B02/B03.

## Guardrails

- No new physics models added.
- No custom gravity work started.
- No Wolfram/FeynCalc process executed during Day-5 structural smoke.
- No heavy calculation executed.
