# Day 8 Public Scope Audit

Date: 2026-08-26
Branch: `release/v0.1.0`

## Result

Status: PASS

This audit aligns public-facing release documents to one v0.1 truth surface.

## Canonical Public Scope

### A. Standard Native

- Tree-level QED 2->2 only.
- External particles: `e-`, `e+`, `mu-`, `mu+`, `gamma`.
- Backend: `feynarts_feyncalc_native`.
- Evidence: B01, B02, B03 standard-native benchmarks and bounded benchmark-regression artifacts.

### B. Locked Custom

- Exactly B04 `phi phi -> h h`.
- `model_id = reheating_scalar_gravity_v1`.
- Backend: `direct_feyncalc_custom_audited`.
- Requires separately supplied audited external knowledge through `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.
- B04 topology/amplitude authorization does not authorize B04 M2.

### C. Explicitly Unsupported

- Arbitrary gravity.
- Arbitrary BSM.
- Arbitrary SM.
- QCD production.
- Loops.
- Renormalization.
- Ungated production-heavy execution.

## Platform Claim

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Linux and macOS Python test success must not be described as full physics E2E validation on those platforms.

## Version And Release-Date Policy

- Project version remains `0.1.0`.
- No final release date is assigned before the human release gate.
- `CITATION.cff` omits `date-released` during release-candidate preparation.
- No release tag or GitHub release was created by this audit.

## Public Claims Changed

- `README.md`: broadened the opening scope from Day-6 standard-native only to the two validated v0.1 routes; added locked B04; changed all custom/gravity language to distinguish arbitrary unsupported gravity from the single locked B04 route; added Windows 11 full physics E2E platform boundary; clarified B04 M2 is separately gated.
- `docs/QUICKSTART.md`: added locked B04 route and prerequisite; added Windows 11 platform boundary; renamed direct CLI section to standard native; added B04 section; clarified unsupported SM/QCD/BSM/gravity/loops/renormalization/production-heavy claims.
- `docs/RELEASE_SCOPE_V0_1.md`: replaced Day-6 frozen standard-native-only scope with Day-8 scope including locked B04; removed obsolete overclaim audit table; added B04 evidence, unsupported list, platform boundary, and release-date policy.
- `docs/BACKEND_STRATEGY.md`: added `direct_feyncalc_custom_audited` as the only executable custom v0.1 route; constrained `feynarts_feyncalc_native` to standard QED scope; marked arbitrary SM/QCD/BSM/gravity as future or unsupported.
- `docs/READINESS_LEVELS.md`: added `B04_CUSTOM_GRAVITY_BENCHMARK_PASS`; updated `PUBLIC_V0_1_READY` to include locked B04 while excluding arbitrary gravity/BSM/SM/QCD/loops/renormalization/production-heavy execution; added platform boundary.
- `skills/feynagent/SKILL.md`: retained two-route classification but strengthened unsupported classification for arbitrary SM/QCD/BSM/gravity/loops/renormalization; added external knowledge and platform wording.
- `skills/feynagent/references/BACKEND_POLICY.md`: narrowed `standard_native` from broad standard sectors to the validated QED 2->2 scope; limited `custom_audited` execution to B04; added unsupported and platform boundaries.
- `CHANGELOG.md`: removed historical release date assignment; added Unreleased Day-8 public-scope audit notes; kept version `0.1.0` with release date pending human release gate; added locked B04 and unsupported boundaries.
- `CITATION.cff`: removed `date-released` fields; updated abstract and message to include locked B04 conservatively; added a B04 external knowledge citation reminder.
- `pyproject.toml`: kept version `0.1.0`; updated project description to include the locked B04 custom audited benchmark route conservatively.
- `CONTRIBUTING.md`: added validated public scope, platform boundary, B04 M2 gate, release-date policy, and public-scope consistency requirement.
- `docs/SCOPE_V0_1.md`: updated the public v0.1 scope from early broad rules-first goals to current validated QED plus locked B04 scope; added unsupported/platform/release-gate wording.
- `docs/SKILL_USAGE.md`: narrowed standard workflow from broad QED/SM/QCD to validated QED 2->2; added locked B04 workflow; marked other custom requests as intake/review only.
- `docs/ARCHITECTURE.md`: narrowed public backend roles; added locked B04 pipeline; added B04 M2 and platform boundaries.`n- `benchmarks/B04_phi_phi_to_hh/README.md`: updated stale registration-only wording to the current locked B04 validated benchmark scope while preserving the no-raw-external-knowledge and no-B04-M2 boundaries.

## Validation Commands

```text
python scripts/validate_examples.py -> PASS
python -m pytest -> PASS (122 passed in 22.31s)
git diff --check -> PASS (line-ending normalization warnings only)
```
