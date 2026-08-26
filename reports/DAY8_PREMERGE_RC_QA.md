# Day 8 Pre-Merge v0.1.0 RC QA

Status: PREMERGE_RC_PASS
Audit date: 2026-08-26
Branch: `release/v0.1.0`
HEAD: `591e61b6b1fb55cf384e3051cbd54f651388a287`

## Guardrails

- No new features were added.
- No physics code was changed.
- Bounded benchmark M2 was authorized and run only for B01/B02/B03 standard QED.
- B04 used the locked external knowledge package and amplitude-only authorization.
- B04 M2 was not rerun.
- No merge to `main`, release tag, GitHub release, or history rewrite was performed.

## Package QA

Result: PACKAGE_BUILD PASS

Commands:

- `python -m pip install -e .[dev]` PASS
- `python scripts/validate_examples.py` PASS
- `python -m pytest` PASS, `123 passed`
- `python -m build --sdist --wheel` PASS
- `git diff --check` PASS, with CRLF normalization warnings only
- `python scripts/check_release_invariants.py` PASS

Build artifacts:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| `dist/feynagent-0.1.0.tar.gz` | 111200 | `71E8D45A7C851CBFDA2CED02041E51D0A5D754C68ADAE5E62F308CE2B5D8647C` |
| `dist/feynagent-0.1.0-py3-none-any.whl` | 95123 | `E2EC2562994D92B1A175D64B7A475E9976D6B29BFCEFD87B145D4DE8149C3301` |

The documented wheel install command was tested in an ignored temporary venv under `runs/day8_premerge_rc_qa/wheel_install_venv`.

## Toolchain Capability

Result: PASS

Commands:

- `python -m feynagent init --timeout 60` PASS
- `python -m feynagent doctor --timeout 60` PASS

Capability summary:

- `wolfram`: PASS
- `feyncalc`: PASS
- `feynarts`: PASS
- `native_qed_tree_capability`: PASS
- `latex`: PASS
- `custom_model:reheating_scalar_gravity_v1`: AVAILABLE

## Standard QED Public Runner

Result: QED_3_OF_3 PASS

All three benchmarks were run through the public high-level runner after `python -m pip install -e .[dev]` confirmed that `python -m feynagent` imported the release-branch checkout.

| Benchmark | Run ID | Classification | Backend | M2 status | Official comparison |
| --- | --- | --- | --- | --- | --- |
| B01 `e- e+ -> mu- mu+` | `20260826_220414_b01_ee_to_mumu_9605ffdc` | `standard_native` | `feynarts_feyncalc_native` | PASS | PASS, equivalence `True`, gold `(2*(t^2 + u^2)*SMP["e"]^4)/s^2` |
| B02 `e- gamma -> e- gamma` | `20260826_220502_b02_compton_d84abb8b` | `standard_native` | `feynarts_feyncalc_native` | PASS | PASS, equivalence `True`, gold `(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)` |
| B03 `e- mu- -> e- mu-` | `20260826_220551_b03_emu_to_emu_1731fc32` | `standard_native` | `feynarts_feyncalc_native` | PASS | PASS, equivalence `True`, gold `(2*(s^2 + u^2)*SMP["e"]^4)/t^2` |

Note: an earlier B04 runner attempt failed before execution because `python -m feynagent` was importing a non-editable site-package install whose package root could not discover the repository benchmark manifest. The documented editable install fixed import provenance; B01/B02/B03 and B04 were rerun after that fix for final evidence.

## B04 Locked Custom Smoke

Result: B04_AMPLITUDE_SMOKE PASS

Run ID: `20260826_220640_B04_phi_phi_to_h_h_62fedbff`

Public runner result:

- classification: `custom_audited`
- backend: `direct_feyncalc_custom_audited`
- backend kind: `audited_custom_backend`
- model: `reheating_scalar_gravity_v1`
- process: `process:B04_phi_phi_to_h_h`
- knowledge status: AVAILABLE
- checked external lock hashes: 19
- convention lock: PASS
- topology diagrams: 4
- per-diagram amplitudes: 4
- amplitude classifications: `amp_001` and `amp_002` PASS_AFTER_EXPLICIT_CONVENTION_MAP; `amp_003` and `amp_004` PASS
- LaTeX/render artifacts: PASS
- validation report: PASS
- M2 policy: `NOT_AUTHORIZED`
- M2 executed: false

The B04 execution request allowed only `schema_validation`, `diagram_generation`, `amplitude_generation`, and `latex_render`.

## Skill QA

Result: SKILL_2_OF_2 PASS

Installed exactly one release-branch FeynAgent skill copy in the validated Codex Agent Skills location:

- installed path: `$HOME/.agents/skills/feynagent`
- legacy duplicate `$HOME/.codex/skills/feynagent`: absent
- validator: PASS, `Skill is valid!`

Fresh Codex task A:

- task id: `01a03e66-f6ac-7b51-8aa1-d047aabb8d1e`
- request: natural-language Compton request
- result: `standard_native`
- backend: `feynarts_feyncalc_native`
- no external physics execution or artifact generation requested

Fresh Codex task B:

- task id: `01a03e67-2796-72e1-879b-4ae5aae697b1`
- request: natural-language B04 request without internal source paths
- result: `custom_audited`
- backend: `direct_feyncalc_custom_audited`
- no B04 M2 rerun
- note: the fresh worktree lacked local `.feynagent` capability files, so this was route-discovery classification only, as requested for the skill smoke.

Local deterministic skill route checks also passed:

- Compton classified as `standard_native` with backend `feynarts_feyncalc_native`.
- B04 classified as `custom_audited` with backend `direct_feyncalc_custom_audited`.

## Public Documentation Commands

Result: PUBLIC_DOC_COMMAND PASS

Safely executed maintainer-testable shell commands from README/Quickstart:

- `python -m pip install -e .[dev]` PASS
- `python -m build --sdist --wheel` PASS
- `python -m pip install dist\feynagent-0.1.0-py3-none-any.whl` PASS in isolated temporary venv
- `python -m feynagent init --timeout 60` PASS
- `python -m feynagent doctor --timeout 60` PASS
- skill install block targeting `$HOME/.agents/skills/feynagent` PASS
- skill validation command with the local skill-creator validator PASS
- public B02 runner command shape PASS using `runs\requests\b02_execution_request.yaml`

Placeholder or prose-only snippets were not executed as shell commands:

- `git clone <your-feynagent-repository-url>`
- `cd FeynAgent`
- Wolfram loading snippet for `$LoadAddOns = {"FeynArts"}; << FeynCalc``.
- illustrative output path snippets.

Documented B02 public runner proof:

- run id: `20260826_221311_b02_compton_5b33b6d5`
- classification: `standard_native`
- backend: `feynarts_feyncalc_native`
- M2 comparison: PASS, equivalence `True`

## Final Tokens

- PREMERGE_RC_PASS
- QED_3_OF_3
- B04_AMPLITUDE_SMOKE
- SKILL_2_OF_2
- PACKAGE_BUILD
- PUBLIC_DOC_COMMAND
