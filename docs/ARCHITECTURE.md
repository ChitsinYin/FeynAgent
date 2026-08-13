# FeynAgent Architecture

## Day-4 Backend Architecture

Day 4 pivots FeynAgent from a Python-first reimplementation path to a native-backend-first architecture for standard supported sectors.

The backend roles are:

- `feynarts_feyncalc_native`: primary production backend for standard QED, SM, and QCD sectors supported by installed FeynArts/FeynCalc model files.
- `legacy_custom_backend`: retained Days 1-3 Python topology, AmplitudeIR, LaTeX, and FeynCalc renderer implementation for regression, pedagogy, audit, and fallback.
- `custom_audited_model`: future path for user-supplied nonstandard interactions; the custom RuleRegistry remains authoritative until an audited native FeynArts-compatible model or adapter exists.

Standard QED production amplitudes must not be generated from duplicate Python-maintained QED rule formulas when FeynArts/FeynCalc can generate the process natively. The legacy QED RuleRegistry remains a convention-audited reference snapshot and a useful custom-rule template, not the production source for native standard-sector amplitudes.

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

The shared Day-4 QED native profile lives at `profiles/backends/feynarts_sm_qed.yaml`. Benchmark cards reference this profile instead of carrying duplicate backend configuration.

## Legacy Custom Pipeline

```text
PhysicsCard + ConventionCard + RuleRegistry
-> approved process gates
-> legacy DiagramIR
-> derived AmplitudeIR
-> legacy LaTeX / FeynCalc renderers
-> regression, pedagogy, audit, and fallback only
```

The legacy pipeline remains valuable because it records explicit convention handling, external-state mapping, fermion flow, provenance, and renderer divergence checks. It is not the production route for standard QED after Day 4.

## Custom Rule Pipeline

Future nonstandard interactions should use `custom_audited_model`. In that mode, RuleRegistry entries remain authoritative and must retain provenance, convention audit state, and trust status. The preferred implementation target is a FeynArts-compatible model or adapter so custom interactions can use native diagram generation and FeynCalc algebra once reviewed.

## Canonical Inputs And Derived Artifacts

`PhysicsCard`, `ConventionCard`, backend profiles, and approved rule/model sources are canonical inputs. Generated amplitudes, PDFs, Wolfram scripts, logs, M2 outputs, and review bundles are derived artifacts.

Derived artifacts belong under `runs/` with stable run IDs. `benchmarks/` contains benchmark specs, gold/reference fixtures, and explicitly marked legacy fixtures only. Machine-local probes and absolute-path diagnostics belong under `.feynagent/` or run-specific locations such as `runs/init/<run_id>/`.

## Data Contracts

JSON Schemas under `schemas/` define the structured contracts currently used by the legacy and benchmark validation paths:

- `PhysicsCard`: process request, backend/rule selection, scope, and approval gates.
- `ConventionCard`: explicit metric, momentum, spinor, polarization, and calculation conventions.
- `RuleRegistry`: provenance-aware rule snapshot for legacy/custom audited paths.
- `DiagramIR`: legacy tree-level diagram structure with explicit rule bindings.
- `AmplitudeIR`: derived legacy amplitude structure used to prevent LaTeX/FeynCalc divergence in the custom backend.

Native FeynArts/FeynCalc amplitudes are not reconstructed through the legacy RuleRegistry. They are produced by the installed native model and converted by `FCFAConvert`.

## Heavy Calculation Boundary

Long-running simplification, spin sums, polarization sums, and squared-amplitude calculations require explicit human authorization. Day-4 M2 regression runs were bounded benchmark checks authorized for QA; production `heavy_calculation` approval remained not requested. This contract mismatch is recorded for Day 5 repair.

## Repository Layout

- `benchmarks/`: benchmark cards, native expected metadata, gold/reference fixtures, and benchmark-local legacy fixtures.
- `docs/`: architecture, backend strategy, setup, migration notes, and design decisions.
- `profiles/`: shared backend profiles such as native FeynArts/FeynCalc QED.
- `reports/`: human-readable milestone reports and review-package manifests.
- `rules/`: legacy/custom RuleRegistry inputs.
- `runs/`: generated amplitudes, logs, PDFs, M2 outputs, and authoritative evidence runs.
- `schemas/`: JSON Schemas for structured cards and IR.
- `scripts/`: validation and generation entry points.
- `src/feynagent/`: Python package source for native wrappers and legacy builders/renderers.
- `tests/`: regression and unit tests.
