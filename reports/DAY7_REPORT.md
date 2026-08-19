# FeynAgent Day-7 Final QA Report

## Scope

This is the bounded Day-7 closeout for branch `feature/b04-custom-gravity`. No new physics was added, no B04 M2 calculation was rerun, no trusted gravity rules/conventions/gold files were changed, no external knowledge package content was changed, and no merge/tag/release was performed.

## Worktree Reconciliation

Canonical checkout:

- path: `E:/003hep-ph-research/Agent/FeynAgent`
- branch: `feature/b04-custom-gravity`
- HEAD before closeout: `27f82d029ba1725b6f994ee996f0539f3ac3aeb6`
- log: `27f82d0 day7: close B04 custom gravity topology benchmark`; `29be00b day7: register B04 custom gravity benchmark inputs`; `3ef996a fix: validate Codex skill metadata and install path`

Codex worktrees inspected:

- `C:/Users/lenovo/.codex/worktrees/b767/FeynAgent`: detached at `27f82d029ba1725b6f994ee996f0539f3ac3aeb6`; same Day-7 working changes as canonical plus scratch patch files. Meaningful source/spec/test/docs/report changes were already present in the canonical working tree. Scratch patch files and generated/private/transient files were excluded.
- `C:/Users/lenovo/.codex/worktrees/a324/FeynAgent`: detached at `836d0dc0d7f48be2f29a0953849da5b5e0740d84`; that commit is an ancestor of canonical. Its uncommitted tracked edits were older QED/backend scratch edits against a Day-5 base, not unique Phase-6/7/8 B04 evidence absent from the canonical feature branch. No worktree commit needed cherry-pick or provenance-preserving transfer.

Conclusion: `WORKTREE_RECONCILIATION = PASS`. No ambiguous overwrite was required and no worktree was removed.

## GitHub Bootstrap And Skill Metadata Repair

Day 7 began with a GitHub bootstrap/authentication pass and a clean-clone skill smoke test. The initial local HTTPS push was blocked by missing local Git credentials, while repository identity and empty remote state were recorded. The subsequent clone smoke exposed invalid YAML frontmatter in `skills/feynagent/SKILL.md`. That metadata was repaired by quoting the description and adding/retaining skill metadata validation. The installed/user skill policy was aligned to `$HOME/.agents/skills/feynagent`, while the repository source remains `skills/feynagent/`.

The deterministic skill helper now classifies standard QED requests as `standard_native`, the single locked B04 request as `custom_audited`, and arbitrary/ambiguous custom physics as review-only or unsupported.

## External Gravity Knowledge Lock

B04 remains locked to `model_id: reheating_scalar_gravity_v1` and `process:B04_phi_phi_to_h_h`. The external package is referenced only through the registered knowledge manifest and local ignored mapping. Required hashes were checked and the capability state is `custom_model:reheating_scalar_gravity_v1 AVAILABLE`.

Knowledge lock SHA-256: `19cfb8a8de198a104c23909148aa577889c50212277bae2c0887ffe265c7c1c6`.

No private source material, private PDFs/notebooks, or raw external gravity payloads were committed.

## B04 Conventions And Required Rule Authority

The locked conventions remain: `kappa = 2/M_P`, metric signature `+---`, weak-field expansion `g_mu_nu = eta_mu_nu + kappa h_mu_nu + ...`, de Donder graviton propagator, and the approved B04 `REDUCED_NR_TT` layer only after exact/raw amplitude preservation.

Required rule authority remains exactly:

- `propagator:phi`
- `vertex:h_phi_phi`
- `propagator:h`
- `vertex:h_h_h`
- `vertex:h_h_phi_phi`
- `polarization_sum:massless_graviton_b04` for the separately authorized M2 closure already completed before this closeout

The historical FeynGrav 3.0 scalar-scalar-graviton-graviton/contact candidate remains rejected as authority because of the recorded contact-rule conflict. FeynGrav may be used only as a labeled helper/validator behind the lock.

## Backend Feasibility Decision

`PRIMARY_BACKEND = DIRECT_FEYNCALC_CUSTOM` for the locked B04 route. FeynCalc is used for deterministic tensor/amplitude algebra, not as a topology enumerator. FeynArts-native spin-2 support was not feasible within the bounded spike, and FeynGrav-assisted use remains limited validator/helper only.

## B04 Topology

The generic topology path produced exactly four diagrams: scalar t/u exchange, s-channel graviton exchange, and the contact diagram. Structural comparison is `PASS`; the t/u scalar-exchange momenta pass after explicit internal-line orientation maps. Rule usage audit is `PASS` and no unexpected rule IDs were used.

## EXACT_RAW vs REDUCED_NR_TT Amplitude Separation

Day-7 amplitude closure preserves per-diagram `EXACT_RAW` amplitudes first, with `REDUCED_NR_TT` applied only as a separate comparison layer. The reduced layer records `Ma = 0` and `Mb = 0` only after the approved NR/TT reduction. The reduced total is `+(i/8) kappa^2 M^2 T`.

## Per-Diagram Classifications

| Gold | Generated | Artifact | Classification |
| --- | --- | --- | --- |
| a | t | `amp_001` | `PASS_AFTER_EXPLICIT_CONVENTION_MAP` |
| b | u | `amp_002` | `PASS_AFTER_EXPLICIT_CONVENTION_MAP` |
| c | s | `amp_003` | `PASS` |
| d | contact | `amp_004` | `PASS` |

## Phase-7 M2 Closure

The reduced M2 gold regression was already `PASS / CLOSED` before this closeout. It was not rerun here. Recorded results remain: `Mc2 = 18 M^4/MP^4`, `Md2 = 32 M^4/MP^4`, interference `-48 M^4/MP^4`, raw total `2 M^4/MP^4`, and rate-convention result `M^4/(2 MP^4)` after the locked identical-particle factors.

## Final Skill E2E And Execution Policy

The B04 Skill E2E fresh-session route passed topology, four per-diagram amplitudes, rule audit, and execution-policy checks. The fresh request authorized schema validation, diagram generation, amplitude generation, and LaTeX rendering only. It did not authorize `m2_regression`, `polarization_sums`, or heavy simplification, so squared-amplitude execution reported `NOT_AUTHORIZED`, `executed = false`, and `automatic_execution = false`.

The standard QED regression remains `PASS`.

## Diagram-Label Refinement

The B04 PhysicsCard presentation metadata now renders external labels as `\phi`, `h_{\mu\nu}`, and `h_{\sigma\gamma}`. The generic/internal graviton presentation label is `h_{\rho\sigma}`. Particle IDs, topology, momentum routing, and graviton line style were not changed.

Focused regression: `python -m pytest tests\test_b04_topology_phase5.py -k b04_tex -q` -> `1 passed, 8 deselected`.

Regenerated topology-only diagram artifact:

- path: `runs/day7_final_b04_diagram_labels_20260819/diagrams/diagrams.pdf`
- SHA-256: `ea59ae5f9e87bae9ed7bb80dfa0dc9e6a28c9af798d689030eb71b75d715701e`

## Final QA Commands

- `python scripts\validate_examples.py` -> PASS
- `python -m pytest` -> PASS, `122 passed in 19.00s`
- `python -m build --sdist --wheel` -> PASS, built `feynagent-0.1.0.tar.gz` and `feynagent-0.1.0-py3-none-any.whl`
- `git diff --check` -> PASS
- `python skills\feynagent\scripts\run_feynagent.py eval --cases skills\feynagent\evals\smoke_cases.json` -> PASS, `7/7`
- Review ZIP clean-extraction self-test -> PASS, `validate_examples` exit 0 and extracted `python -m pytest` -> `121 passed, 1 skipped`

## Final Readiness

B04_CUSTOM_GRAVITY_BENCHMARK = PASS
B04_LOCKED_PRODUCTION_PATH = PASS
GENERAL_CUSTOM_GRAVITY_PRODUCTION_READY = NO
PUBLIC_V0_1_READY = NO
READY_FOR_DAY8 = YES
