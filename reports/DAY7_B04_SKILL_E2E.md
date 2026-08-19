# Day-7 B04 Skill and Backend E2E

- Overall status: `PASS`
- Precondition: `B04_CUSTOM_GRAVITY_PASS` satisfied by the Phase-7 closure (`PASS / CLOSED`).
- Workflow scope: the single locked B04 benchmark only; arbitrary BSM/gravity is not production-ready.
- Fresh Codex task: `B04 Skill E2E Fresh Session`
- Thread ID: `01a017df-254b-7413-8ba1-3bea23b53123`
- Fresh-session run ID: `20260819_104036_B04_phi_phi_to_h_h_2ea1e98b`

## Dispatch Contract

| Request class | Classification | Backend | Production scope |
| --- | --- | --- | --- |
| Standard tree-level QED 2-to-2 | `standard_native` | `feynarts_feyncalc_native` | validated QED particles/processes only |
| Locked B04 `phi phi -> h h` | `custom_audited` | `direct_feyncalc_custom_audited` | `reheating_scalar_gravity_v1`, B04 only |
| Other custom/BSM/gravity | intake/review or `unsupported_requires_review` | none | not production-ready |

The B04 route records `standard_qed_authority: false`. Supplying the native QED profile for B04 is rejected, and a registered-but-unimplemented arbitrary custom model has no execution route.

## Required Gates

The integrated custom backend requires all of the following before execution:

- approved, linked `ExecutionRequest`: `PASS`
- registered external knowledge package: `AVAILABLE`
- knowledge hashes checked: `19`
- knowledge-lock SHA-256: `19cfb8a8de198a104c23909148aa577889c50212277bae2c0887ffe265c7c1c6`
- convention lock `conventions:reheating_scalar_gravity_v1`: `PASS`
- rule usage audit: `PASS`

Doctor/capability output now includes exactly:

```text
custom_model:reheating_scalar_gravity_v1 AVAILABLE
```

The structured capability entry also records `custom_audited`, `direct_feyncalc_custom_audited`, the B04-only production scope, and `standard_qed_authority: false`. Conflict states are reported as `CONFLICT`; missing packages remain `MISSING_KNOWLEDGE`.

## Skill Eval and Installation

The updated repository skill passed the skill-creator validator and was installed to the user-level FeynAgent skill directory. Source and installed files matched by SHA-256.

| Skill artifact | SHA-256 |
| --- | --- |
| `SKILL.md` | `55a4c9b62956e91bd4661a601d0464df091172249949198d21681cc34a83f275` |
| `scripts/run_feynagent.py` | `81ecf5363b89a34ae7dc3c1edc8334bee0cf9f6bc5770159cdea6b92e11a72e8` |
| `evals/smoke_cases.json` | `cae35a58bfb36d7ce6a4e8a76b9b3e7855b3b8fcb7ee95e5c6296fd6789381ac` |

The seven-case skill eval passed. Its natural-language B04 case resolves to:

```text
classification = custom_audited
model_id = reheating_scalar_gravity_v1
process_id = process:B04_phi_phi_to_h_h
backend = direct_feyncalc_custom_audited
standard_qed_authority = false
```

The eval also confirms standard Compton/annihilation requests remain native QED, generic custom Yukawa is intake-only with no backend, and arbitrary BSM production is rejected.

## Fresh-Session Request

The new task received only this natural-language request, with no internal file paths:

> Use the FeynAgent skill to run the audited inflaton-pair annihilation into two gravitons. Generate the topology and the per-diagram amplitudes, verify the registered knowledge package plus convention and rule-audit gates, and report the squared-amplitude execution policy. This message explicitly authorizes creation of an approved amplitude-only ExecutionRequest for this run. Do not execute the squared-amplitude calculation.

The fresh task independently discovered the installed skill, resolved and registered the external package in machine-local ignored state, ran init/doctor, created an approved amplitude-only ExecutionRequest, and invoked the public dispatcher.

## Fresh-Session Results

- runner: `feynagent.deterministic_dispatch_v0_2`
- route: `custom_audited -> direct_feyncalc_custom_audited`
- topology: `PASS`, 4 diagrams
- rule usage audit: `PASS`
- per-diagram amplitudes: `PASS`, 4 artifacts
- `amp_001`: `PASS_AFTER_EXPLICIT_CONVENTION_MAP`
- `amp_002`: `PASS_AFTER_EXPLICIT_CONVENTION_MAP`
- `amp_003`: `PASS`
- `amp_004`: `PASS`
- diagrams PDF SHA-256: `409b5f72b863a428a1dcc3c2872dc4b1514081b8f46482cc3bcef1929cf60b57`
- amplitudes PDF SHA-256: `a5f9f59380c06c83583155161c38179af1a99800984ff9ce953a72429d173551`
- run manifest SHA-256: `5cb88b8b176c669b80f0b3c8477abf5ca7feabe6ee7b394f592d49424474587e`
- validation report SHA-256: `56f5f0ffd3166d6a9e478ed46c6d6de9c4d179d8abec127d140612d0fcb8e389`
- ExecutionRequest SHA-256: `352aaa883cd351c12fd9e142eae82cd7264a3a07c1e6afc29d7a48b7db00725f`

## M2 Policy

The fresh ExecutionRequest authorized only `schema_validation`, `diagram_generation`, `amplitude_generation`, and `latex_render`. It did not authorize `m2_regression`, `polarization_sums`, or heavy simplification.

Result:

```text
status = NOT_AUTHORIZED
executed = false
automatic_execution = false
layer = REDUCED_NR_TT
```

The fresh task searched the generated run and found no M2/squared-amplitude artifacts. A future B04 M2 run requires separate explicit operations `m2_regression` and `polarization_sums`, and remains a deterministic manual Wolfram/FeynCalc run after conflict-free amplitude closure.

## Validation

- full repository suite: `121 passed`
- fresh-session focused B04 suite: `26 passed`
- skill eval: `7/7 passed`
- skill-creator validation: `PASS`
- installed skill source/hash comparison: `MATCH`
- external private absolute paths in repository report/evidence: `NONE`

No trusted rule, convention, or gold artifact was changed. The historical FeynGrav 3.0 contact candidate remains rejected as an authority.
