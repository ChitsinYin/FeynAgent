# FeynAgent Skill Usage

The reusable Codex skill lives under `skills/feynagent/`.

## First Step

Check local initialization:

```bash
python skills/feynagent/scripts/ensure_initialized.py
```

If `.feynagent/environment.yaml` or related local files are missing, run:

```bash
python -m feynagent init
```

If auto-detection cannot find Wolfram/FeynCalc, ask only for the missing path, for example `--wolframscript` or `--feyncalc-dir`. Do not install software silently.

For B04, also require `custom_model:reheating_scalar_gravity_v1 AVAILABLE`; the external knowledge package is separately supplied and is not installed by FeynAgent.

## Request Classification

Use:

```bash
python skills/feynagent/scripts/run_feynagent.py classify "e- gamma -> e- gamma Compton scattering"
```

Classifications:

- `standard_native`: use native FeynArts/FeynCalc only for validated tree-level QED 2->2 with `e-`, `e+`, `mu-`, `mu+`, and `gamma`.
- `custom_audited`: execute only locked B04 `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`; other custom requests are intake/review only.
- `unsupported_requires_review`: ambiguous, unsupported, or missing reviewed rule information, including arbitrary SM, QCD production, arbitrary BSM, arbitrary gravity, loops, renormalization, or ungated production-heavy execution.

## Standard Native Workflow

For validated standard QED 2->2 requests:

1. Search `.feynagent/reference_index.json` first.
2. Use FeynArts/FeynCalc native backend.
3. Record package versions, official example provenance, hashes, and exact native calls.
4. Do not rebuild standard Feynman rules in Python.

Example search:

```bash
python skills/feynagent/scripts/run_feynagent.py search-examples "ElGa-ElGa Compton"
```

## Locked B04 Workflow

For B04:

1. Use `benchmarks/B04_phi_phi_to_hh/physics_card.yaml`.
2. Use `profiles/backends/b04_custom_gravity_audited.yaml`.
3. Require `model_id = reheating_scalar_gravity_v1` and backend `direct_feyncalc_custom_audited`.
4. Resolve the separately supplied audited external knowledge package through the registered manifest.
5. Require convention lock and rule audit `PASS` before amplitudes continue.
6. Do not treat topology or amplitude authorization as M2 authorization.

## Other Custom Requests

For all custom interactions outside locked B04:

1. Require explicit rules/conventions/provenance.
2. Never invent trusted rules.
3. Stop at intake/review unless a separately validated backend is added.
4. Do not present arbitrary BSM or gravity as production-ready.

## Platform Boundary

Full physics E2E validation for v0.1 was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Do not claim Linux/macOS full physics validation merely because Python tests pass there.

## Execution Boundary

Benchmark regression and production heavy computation are separate authorizations. Long Mathematica jobs should be emitted as deterministic scripts under `runs/<run_id>/`, allowed to run independently, and inspected after completion. Do not live-poll indefinitely.

## Skill Eval

Run:

```bash
python skills/feynagent/scripts/run_feynagent.py eval --cases skills/feynagent/evals/smoke_cases.json
```
