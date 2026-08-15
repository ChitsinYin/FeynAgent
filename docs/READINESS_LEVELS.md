# Readiness Levels

FeynAgent readiness labels describe what has actually passed validation. They are not interchangeable with future architecture goals.

## `STANDARD_NATIVE_RC_PASS`

The standard-native release-candidate workflow passes for the public v0.1 scope:

- tree-level QED 2->2;
- external particles `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend;
- diagrams, channel-separated amplitudes, LaTeX/PDF artifacts, executable FeynCalc artifacts, bounded benchmark M2 execution, validation/provenance reports, wheel install, and Codex skill discovery checks.

## `READY_TO_START_CUSTOM_GRAVITY_DEVELOPMENT`

The repository is ready to begin custom-gravity benchmark development only after the standard-native baseline is stable and the release scope no longer overclaims gravity production support. This label permits design, intake, provenance review, benchmark-card drafting, and backend feasibility work. It does not mean any gravity amplitude or production workflow is supported.

## `CUSTOM_GRAVITY_BENCHMARK_PASS`

A custom-gravity benchmark pass requires audited custom rules and conventions, explicit provenance, process cards, expected outputs or independently reviewed golds, deterministic native/backend artifacts where feasible, and passing regression tests for the named benchmark. This is benchmark-specific, not a general production claim.

## `CUSTOM_GRAVITY_PRODUCTION_READY`

Custom-gravity production readiness requires more than one benchmark pass. It requires documented scope, stable backend strategy, reviewed model/rule sources, robust validation across representative processes, execution policy coverage, reproducible packaging, and user-facing documentation that clearly states limits and required external dependencies.

## `PUBLIC_V0_1_READY`

Public v0.1 readiness means the validated standard-native scope is packaged, documented, licensed, installable, and reproducible for a fresh user without development-environment workarounds. It does not include arbitrary SM, QCD, BSM, or custom-gravity production support.

## Day 6 Semantics

Day 6 could honestly report `STANDARD_NATIVE_RC_PASS` because B01/B02/B03 standard-native QED runner workflows, native artifacts, generic QED M2 generation, execution gates, skill discovery, wheel installation, and release metadata checks passed for the public v0.1 scope.

Day 6 still had `CUSTOM_GRAVITY_PRODUCTION_READY = false` because no custom-gravity physics had been added or validated: there were no audited gravity rules, no gravity backend adapter, no custom-gravity benchmark golds, no gravity M2 regression suite, and no production documentation claiming a supported gravity surface.
