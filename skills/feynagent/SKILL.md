# FeynAgent Skill

Use this skill for FeynAgent HEP workflows involving QED/SM benchmark amplitudes, FeynArts/FeynCalc native generation, audited custom rules, or local environment checks.

Before physics work:
1. Check `.feynagent/environment.yaml` using `scripts/ensure_initialized.py`.
2. If missing or incomplete, run `python -m feynagent init` or ask only for the missing path such as `--wolframscript` or `--feyncalc-dir`.
3. Never silently install Mathematica, FeynCalc, FeynArts, or LaTeX.

Classify each request:
- `standard_native`: standard QED/SM/QCD supported by native packages.
- `custom_audited`: user-supplied nonstandard interactions with explicit rules/conventions/provenance.
- `unsupported_requires_review`: ambiguous, unsupported, or under-specified physics.

For `standard_native`, search `.feynagent/reference_index.json` first, use FeynArts/FeynCalc native backend, record package versions and example provenance, and do not rebuild standard Feynman rules in Python.

For `custom_audited`, require explicit rules/conventions/provenance, never invent trusted rules, map to FeynCalc elementary objects where possible, prefer a custom FeynArts-compatible model/adapter, and use the legacy custom backend only as fallback/reference.

Distinguish benchmark regression from production heavy computation. Never live-poll long Mathematica jobs: generate deterministic scripts, let them run independently, then inspect completed artifacts. Preserve outputs under `runs/<run_id>/`.

Require physics review before silently changing channels, conventions, custom rules, or approximation assumptions.

References: `references/BACKEND_POLICY.md`, `references/CUSTOM_RULE_PROTOCOL.md`, `references/OUTPUT_CONTRACT.md`.
