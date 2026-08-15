---
name: feynagent
description: Use for FeynAgent public v0.1 standard-native workflows: tree-level QED 2-to-2 with external e-, e+, mu-, mu+, gamma through the FeynArts/FeynCalc native backend; deterministic `python -m feynagent run`; validation/provenance; or local init/doctor checks. Use custom_audited only for custom-rule intake, convention/provenance review, and backend-feasibility assessment, not arbitrary custom BSM/gravity production.
---

# FeynAgent Skill

Use this skill for FeynAgent HEP workflows within the validated public v0.1 standard-native scope:

- tree-level QED 2->2;
- external particles `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend.

It may also be used for `custom_audited` intake, where the current release means custom-rule intake, convention/provenance review, and backend-feasibility assessment only. It is not a claim that arbitrary custom BSM or gravity production is supported.

Before physics work:
1. Check `.feynagent/environment.yaml` using `scripts/ensure_initialized.py`.
2. If missing or incomplete, run `python -m feynagent init` or ask only for the missing path such as `--wolframscript` or `--feyncalc-dir`.
3. Never silently install Mathematica, FeynCalc, FeynArts, or LaTeX.

Classify each request:
- `standard_native`: validated public v0.1 tree-level QED 2->2 with external `e-`, `e+`, `mu-`, `mu+`, `gamma` through FeynArts/FeynCalc native generation.
- `custom_audited`: user-supplied nonstandard interactions with explicit rules/conventions/provenance, for intake/review/feasibility only in the current release.
- `unsupported_requires_review`: ambiguous, unsupported, or under-specified physics.

For `standard_native`, search `.feynagent/reference_index.json` first, use FeynArts/FeynCalc native backend, record package versions and example provenance, and do not rebuild standard Feynman rules in Python.

For `custom_audited`, require explicit rules/conventions/provenance, never invent trusted rules, map to FeynCalc elementary objects where possible, assess whether a custom FeynArts-compatible model/adapter is feasible, and use the legacy custom backend only as fallback/reference. Do not present this as production support for arbitrary custom BSM or gravity processes.

Distinguish benchmark regression from production heavy computation. Never live-poll long Mathematica jobs: generate deterministic scripts, let them run independently, then inspect completed artifacts. Preserve outputs under `runs/<run_id>/`.

Require physics review before silently changing channels, conventions, custom rules, or approximation assumptions.

References: `references/BACKEND_POLICY.md`, `references/CUSTOM_RULE_PROTOCOL.md`, `references/OUTPUT_CONTRACT.md`.
