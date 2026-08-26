# Readiness Levels

FeynAgent readiness labels describe what has actually passed validation. They are not interchangeable with future architecture goals.

## `STANDARD_NATIVE_RC_PASS`

The standard-native release-candidate workflow passes for the public v0.1 scope:

- tree-level QED 2->2;
- external particles `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend;
- diagrams, channel-separated amplitudes, LaTeX/PDF artifacts, executable FeynCalc artifacts, bounded benchmark M2 execution, validation/provenance reports, wheel install, and Codex skill discovery checks.

## `B04_CUSTOM_GRAVITY_BENCHMARK_PASS`

The locked B04 custom benchmark passes only for:

- process `phi phi -> h h`;
- `model_id = reheating_scalar_gravity_v1`;
- backend `direct_feyncalc_custom_audited`;
- separately supplied audited external knowledge resolved through the registered knowledge manifest;
- approved topology, amplitude, LaTeX, rule-audit, dispatch, and skill-route checks.

This label is benchmark-specific. It does not imply arbitrary gravity, arbitrary BSM, B04 M2 execution, or production-heavy readiness.

## `CUSTOM_GRAVITY_PRODUCTION_READY`

Custom-gravity production readiness requires more than the locked B04 benchmark pass. It requires documented broader scope, stable backend strategy, reviewed model/rule sources, robust validation across representative processes, execution policy coverage, reproducible packaging, and user-facing documentation that clearly states limits and required external dependencies.

## `PUBLIC_V0_1_READY`

Public v0.1 readiness means the validated standard-native QED scope and the single locked B04 route are packaged, documented, licensed, installable, and reproducible for a fresh user without development-environment workarounds.

It does not include arbitrary SM, QCD production, arbitrary BSM, arbitrary gravity, loops, renormalization, or ungated production-heavy execution.

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Linux and macOS Python test success must not be treated as full physics E2E validation on those platforms.

## Day 6 Semantics

Day 6 could honestly report `STANDARD_NATIVE_RC_PASS` because B01/B02/B03 standard-native QED runner workflows, native artifacts, generic QED M2 generation, execution gates, skill discovery, wheel installation, and release metadata checks passed for the then-current public v0.1 standard-native scope.

Day 6 still had `CUSTOM_GRAVITY_PRODUCTION_READY = false` because the locked B04 route had not yet closed. That Day-6 statement remains historical evidence, not the current Day-8 public release scope.

## Day 7 Semantics

Day 7 closed the single locked B04 route as a custom audited benchmark. The closeout does not add arbitrary gravity support, arbitrary BSM support, loops, renormalization, QCD production, or ungated production-heavy execution. B04 M2 remains separately gated and is not implied by topology or amplitude authorization.
