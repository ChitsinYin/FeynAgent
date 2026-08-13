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

## Request Classification

Use:

```bash
python skills/feynagent/scripts/run_feynagent.py classify "e- gamma -> e- gamma Compton scattering"
```

Classifications:

- `standard_native`: use native FeynArts/FeynCalc for standard supported sectors.
- `custom_audited`: require explicit custom rules, conventions, and provenance.
- `unsupported_requires_review`: ambiguous, unsupported, or missing reviewed rule information.

## Standard Native Workflow

For standard QED/SM/QCD requests:

1. Search `.feynagent/reference_index.json` first.
2. Use FeynArts/FeynCalc native backend.
3. Record package versions, official example provenance, hashes, and exact native calls.
4. Do not rebuild standard Feynman rules in Python.

Example search:

```bash
python skills/feynagent/scripts/run_feynagent.py search-examples "ElGa-ElGa Compton"
```

## Custom Audited Workflow

For custom interactions:

1. Require explicit rules/conventions/provenance.
2. Never invent trusted rules.
3. Map rules to FeynCalc elementary objects where possible.
4. Prefer a custom FeynArts-compatible model/adapter.
5. Use the legacy custom backend only as fallback/reference.

## Execution Boundary

Benchmark regression and production heavy computation are separate authorizations. Long Mathematica jobs should be emitted as deterministic scripts under `runs/<run_id>/`, allowed to run independently, and inspected after completion. Do not live-poll indefinitely.

## Skill Eval

Run:

```bash
python skills/feynagent/scripts/run_feynagent.py eval --cases skills/feynagent/evals/smoke_cases.json
```
