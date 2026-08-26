# B02 Compton Public Example

This example reproduces the validated standard-native FeynAgent v0.1 Compton benchmark:

```text
e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)
```

Use it only after `python -m feynagent doctor --timeout 60` passes for the standard QED native toolchain.

## Scope

- Route: `standard_native`
- Backend: `feynarts_feyncalc_native`
- Model: `sm_qed`
- Sector: `qed`
- External states: `e-`, `gamma` -> `e-`, `gamma`
- Perturbative order: tree level, coupling order `e^2`
- Unsupported here: loops, renormalization, QCD, arbitrary SM, arbitrary BSM, arbitrary gravity, and production-heavy execution

## Files

- `physics_card.yaml`: public B02 PhysicsCard copied from the canonical benchmark input.
- `backend_profile.yaml`: public FeynArts/FeynCalc QED backend profile for the standard-native route.
- `execution_request.benchmark_regression.yaml`: bounded benchmark-regression request with a fixed 180 s timeout. It is not production-heavy authorization.
- `expected_results.yaml`: expected channels and massless squared-amplitude benchmark result.

## Run

From the repository root:

```powershell
python -m feynagent run `
  --physics-card examples\B02_compton\physics_card.yaml `
  --backend-profile examples\B02_compton\backend_profile.yaml `
  --execution-request examples\B02_compton\execution_request.benchmark_regression.yaml `
  --run-root runs
```

Generated artifacts are written under `runs/<run_id>/`; this example directory intentionally does not bundle a generated run.

## Expected Channels

The native FeynArts/FeynCalc route should produce two electron-exchange channels:

| channel | internal particle | expected routing |
| --- | --- | --- |
| `s` | `e-` | `p1+k1` |
| `u` | `e-` | `p1-k2` |

## Expected Massless M2

The bounded benchmark-regression massless result is:

```text
(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
```

This result was recorded in `reports/DAY4_M2_REGRESSION.md` and reproduced by the Day-6 public runner manifest. The request here authorizes only bounded benchmark regression, with explicit spin/polarization-sum operations and a fixed timeout.
