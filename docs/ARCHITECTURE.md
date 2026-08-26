# FeynAgent Architecture

## Backend Architecture

FeynAgent uses explicit backend contracts instead of treating every installed model or rule registry entry as production support.

The public v0.1 backend roles are:

- `feynarts_feyncalc_native`: primary production backend for validated standard tree-level QED 2->2 with external `e-`, `e+`, `mu-`, `mu+`, and `gamma`.
- `direct_feyncalc_custom_audited`: executable only for locked B04 `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, with separately supplied audited external knowledge.
- `legacy_custom_backend`: retained Days 1-3 Python topology, AmplitudeIR, LaTeX, and FeynCalc renderer implementation for regression, pedagogy, audit, and fallback.
- `custom_audited_model`: future path for additional user-supplied nonstandard interactions; outside locked B04, custom requests are intake/review only in v0.1.

Standard QED production amplitudes must not be generated from duplicate Python-maintained QED rule formulas when FeynArts/FeynCalc can generate the process natively. The legacy QED RuleRegistry remains a convention-audited reference snapshot and a useful custom-rule template, not the production source for native standard-sector amplitudes.

## Day-5 Contract Separation

Day 5 separates three concerns that were coupled during Days 1-4:

- `PhysicsCard` records backend-neutral physics intent: process, external particles, perturbative order, `model_id`, and `sector`.
- `BackendProfile` records how an implementation resolves that intent: native FeynArts/FeynCalc model settings, locked custom backend settings, or legacy RuleRegistry selection.
- `ExecutionRequest` records runtime authorization: structural, amplitude-only, bounded benchmark regression, or production-heavy execution, including who authorized it, when, timeout policy, and allowed operations.

`ExecutionRequest` is not canonical physics truth. It grants permission for a particular run mode. Benchmark-regression approval is not production-heavy approval, and B04 topology/amplitude approval is not B04 M2 approval.

## Standard Native Pipeline

```text
PhysicsCard + backend profile
-> feynarts_feyncalc_native
-> FeynArts CreateTopologies / InsertFields
-> FeynArts CreateFeynAmp
-> FeynCalc FCFAConvert
-> native amplitude artifacts under runs/
-> bounded validation or human-approved heavy calculation
```

The shared QED native profile lives at `profiles/backends/feynarts_sm_qed.yaml`. Benchmark cards reference this profile instead of carrying duplicate backend configuration.

## Locked B04 Pipeline

```text
B04 PhysicsCard + B04 backend profile + registered external knowledge manifest
-> direct_feyncalc_custom_audited
-> convention and rule-audit gates
-> locked topology and per-diagram amplitude artifacts under runs/
-> LaTeX/render validation
-> no M2 unless separately authorized
```

The B04 backend profile lives at `profiles/backends/b04_custom_gravity_audited.yaml`. It resolves only `model_id = reheating_scalar_gravity_v1` and `process:B04_phi_phi_to_h_h`. It is not a general gravity or BSM backend.

## Legacy Custom Pipeline

```text
PhysicsCard + ConventionCard + RuleRegistry
-> approved process gates
-> legacy DiagramIR
-> derived AmplitudeIR
-> legacy LaTeX / FeynCalc renderers
-> regression, pedagogy, audit, and fallback only
```

The legacy pipeline remains valuable because it records explicit convention handling, external-state mapping, fermion flow, provenance, and renderer divergence checks. It is not the production route for standard QED after Day 4 and is not authority for arbitrary BSM or gravity.

## Custom Rule Pipeline

Future nonstandard interactions should use a separately audited custom route. In that mode, RuleRegistry entries must retain provenance, convention audit state, and trust status. Additional production routes require reviewed backend feasibility, benchmark evidence, execution gates, and public documentation updates.

## Canonical Inputs And Derived Artifacts

`PhysicsCard`, `ConventionCard`, backend profiles, execution requests, and approved rule/model sources are structured inputs. `PhysicsCard` remains backend-neutral physics intent; `BackendProfile` and `ExecutionRequest` are implementation/runtime contracts. Generated amplitudes, PDFs, Wolfram scripts, logs, M2 outputs, and review bundles are derived artifacts.

Derived artifacts belong under `runs/` with stable run IDs. `benchmarks/` contains benchmark specs, gold/reference fixtures, and explicitly marked legacy fixtures only. Machine-local probes and absolute-path diagnostics belong under `.feynagent/` or run-specific locations such as `runs/init/<run_id>/`.

## Data Contracts

JSON Schemas under `schemas/` define the structured contracts currently used by the legacy and benchmark validation paths:

- `PhysicsCard`: backend-neutral process request, `model_id`, `sector`, scope, and approval gates.
- `ConventionCard`: explicit metric, momentum, spinor, polarization, and calculation conventions.
- `RuleRegistry`: provenance-aware rule snapshot for legacy/custom audited paths.
- `DiagramIR`: legacy tree-level diagram structure with explicit rule bindings.
- `AmplitudeIR`: derived legacy amplitude structure used to prevent LaTeX/FeynCalc divergence in the custom backend.
- `BackendProfile`: implementation mapping from backend-neutral theory intent to native package settings, locked custom backend settings, or legacy RuleRegistry sources.
- `ExecutionRequest`: runtime authorization contract for structural, amplitude-only, benchmark-regression, or production-heavy operations.

Native FeynArts/FeynCalc amplitudes are not reconstructed through the legacy RuleRegistry. They are produced by the installed native model and converted by `FCFAConvert`.

## Heavy Calculation Boundary

Long-running simplification, spin sums, polarization sums, and squared-amplitude calculations require explicit human authorization. Bounded M2 regression runs are QA evidence, not production-heavy approval. B04 M2 requires separate explicit authorization and must not be inferred from topology or amplitude authorization.

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Python tests on Linux or macOS are useful software checks, but not full physics E2E validation claims for those platforms.

## Repository Layout

- `benchmarks/`: benchmark cards, native expected metadata, gold/reference fixtures, and benchmark-local legacy fixtures.
- `docs/`: architecture, backend strategy, setup, migration notes, and design decisions.
- `profiles/`: shared backend profiles such as native FeynArts/FeynCalc QED and locked B04 custom audited backend.
- `reports/`: human-readable milestone reports and review-package manifests.
- `rules/`: legacy/custom RuleRegistry inputs.
- `runs/`: generated amplitudes, logs, PDFs, M2 outputs, and authoritative evidence runs.
- `schemas/`: JSON Schemas for structured cards and IR.
- `scripts/`: validation and generation entry points.
- `src/feynagent/`: Python package source for native wrappers and legacy builders/renderers.
- `tests/`: regression and unit tests.
