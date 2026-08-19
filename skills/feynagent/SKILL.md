---
name: feynagent
description: "Use FeynAgent for validated tree-level QED 2-to-2 workflows and the single locked B04 scalar-to-two-graviton custom_audited route; includes init/doctor, backend dispatch, and ExecutionRequest gates. Do not treat arbitrary BSM or gravity as production-ready."
---

# FeynAgent Skill

Use this skill for two disjoint validated routes:

- `standard_native`: tree-level QED 2->2 with `e-`, `e+`, `mu-`, `mu+`, and `gamma`, through `feynarts_feyncalc_native`.
- `custom_audited`: only locked B04 `phi phi -> h h`, model `reheating_scalar_gravity_v1`, through `direct_feyncalc_custom_audited`.

Other custom models may be reviewed as audited-rule intake, but they have no production execution route. Never use standard-QED rules or backend authority for B04.

Before physics work:
1. Check `.feynagent/environment.yaml` using `scripts/ensure_initialized.py`.
2. If missing or incomplete, run `python -m feynagent init` or ask only for the missing path such as `--wolframscript` or `--feyncalc-dir`.
3. For B04, require doctor/capability output `custom_model:reheating_scalar_gravity_v1 AVAILABLE`.
4. Never silently install Mathematica, FeynCalc, FeynArts, or LaTeX.

Classify each request:
- `standard_native`: validated public v0.1 tree-level QED 2->2 with external `e-`, `e+`, `mu-`, `mu+`, `gamma` through FeynArts/FeynCalc native generation.
- `custom_audited`: locked B04 may execute; other explicit custom interactions are intake/review only and are not production-ready.
- `unsupported_requires_review`: ambiguous, unsupported, or under-specified physics.

For `standard_native`, search `.feynagent/reference_index.json` first, use FeynArts/FeynCalc native backend, record package versions and example provenance, and do not rebuild standard Feynman rules in Python.

For B04 execution, use the repository B04 PhysicsCard and `backend_profile:b04_custom_gravity_audited`. Require an explicit approved ExecutionRequest linked to both, with `schema_validation`, `diagram_generation`, `amplitude_generation`, and `latex_render`. The backend must resolve the registered external knowledge package, match `conventions:reheating_scalar_gravity_v1`, and obtain rule audit `PASS` before amplitudes continue.

B04 M2 is never implied by topology or amplitude authorization. Report `NOT_AUTHORIZED` unless the ExecutionRequest separately includes `m2_regression` and `polarization_sums`; even then, use a separate deterministic manual Wolfram/FeynCalc run after all amplitude conflicts are absent.

For any other custom interaction, require explicit rules/conventions/provenance, never invent trusted rules, and stop at intake/review unless a separately validated backend is added. Do not present arbitrary BSM or gravity as production support.

Distinguish benchmark regression from production heavy computation. Never live-poll long Mathematica jobs: generate deterministic scripts, let them run independently, then inspect completed artifacts. Preserve outputs under `runs/<run_id>/`.

Require physics review before silently changing channels, conventions, custom rules, or approximation assumptions.

Use `scripts/run_feynagent.py classify "<natural-language request>"` for the deterministic skill route eval. References: `references/BACKEND_POLICY.md`, `references/CUSTOM_RULE_PROTOCOL.md`, `references/OUTPUT_CONTRACT.md`.
