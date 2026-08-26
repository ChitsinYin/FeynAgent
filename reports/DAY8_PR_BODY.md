# Release PR Body: FeynAgent v0.1.0

## Summary

Prepare the public FeynAgent v0.1.0 release candidate for merge from `release/v0.1.0` into `main`.

Validated public scope:

- Standard native route: tree-level QED 2-to-2 processes with external `e-`, `e+`, `mu-`, `mu+`, and `gamma`, routed through `standard_native` and backend `feynarts_feyncalc_native`.
- Locked custom route: exactly B04 `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, routed through `custom_audited` and backend `direct_feyncalc_custom_audited`.
- B04 requires a separately supplied audited external knowledge package. Private/source external knowledge is not bundled in this repository.

Explicitly unsupported in v0.1.0:

- arbitrary gravity;
- arbitrary BSM;
- arbitrary Standard Model workflows outside the validated QED scope;
- QCD production;
- loops;
- renormalization;
- ungated production-heavy execution.

## Validation

- Full physics E2E validation was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain.
- GitHub Actions public Python/package CI passed on `release/v0.1.0` at commit `591e61b6b1fb55cf384e3051cbd54f651388a287`: https://github.com/ChitsinYin/FeynAgent/actions/runs/32952672750
- Final PR-head CI must pass again after the PR branch update.
- Local pre-merge RC QA result: `PREMERGE_RC_PASS`.
- Standard QED result: `QED_3_OF_3`.
- B04 result: `B04_AMPLITUDE_SMOKE`; B04 M2 was not rerun.
- Skill smoke result: `SKILL_2_OF_2`.
- Package result: `PACKAGE_BUILD`.
- Public documentation command result: `PUBLIC_DOC_COMMAND`.

## Trust And Release Gates

- Custom Wolfram `.wl`, `.m`, and `.nb` files are executable code and require user trust.
- FeynAgent does not automatically trust arbitrary Wolfram files, notebooks, helper package output, or pasted expressions.
- Locked custom routes require convention, rule, and hash validation.
- Apache-2.0 applies only to FeynAgent-owned content and does not relicense FeynCalc, FeynArts, Mathematica/Wolfram, FeynGrav, or private external knowledge packages.

Do not merge until:

- GitHub CI passes on the PR head;
- local `PREMERGE_RC_PASS` remains accepted;
- human diff review is approved.
