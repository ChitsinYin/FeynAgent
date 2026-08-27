# FeynAgent v0.1.0 Release Notes

Release date: 2026-08-27

FeynAgent v0.1.0 is the first public release of the deterministic FeynAgent workflow. It packages the validated public standard-QED route and the single locked B04 custom audited route, while keeping all broader physics scopes explicitly out of release support.

## Supported

- Standard QED tree-level 2-to-2 workflows for external `e-`, `e+`, `mu-`, `mu+`, and `gamma` states through the native FeynArts/FeynCalc backend.
- Locked B04 `phi phi -> h h` custom route for `model_id = reheating_scalar_gravity_v1` through `direct_feyncalc_custom_audited`, requiring the separately supplied audited external knowledge package.

## Not Supported

- Arbitrary gravity or graviton production beyond the locked B04 route.
- Arbitrary BSM model production workflows.
- Arbitrary Standard Model or QCD production workflows outside the validated standard-QED scope.
- Loops, counterterms, renormalization, or higher-order corrections.
- B04 M2 execution without separate explicit authorization.

## Release Gates

- CI = PASS
- PREMERGE_RC = PASS
- MAIN_MERGE = PASS
- GITHUB_ZERO_CLONE = PASS
- QED_PUBLIC_E2E = PASS
- B04_MISSING_KNOWLEDGE_GUARD = PASS
- B04_MAINTAINER_SMOKE = PASS
- PRIVATE_KNOWLEDGE_AUDIT = PASS
- VERSION_METADATA = READY

## Artifacts

The GitHub Release includes the source distribution, wheel, and `SHA256SUMS`. It does not include private B04 external knowledge or review ZIP artifacts.