# FeynAgent Architecture

## Conceptual Pipeline

```text
Natural language
-> PhysicsCard
-> ConventionCard
-> RuleRegistry
-> candidate/approved process
-> DiagramIR
-> renderers/builders
-> LaTeX / FeynCalc artifacts
-> human-controlled heavy calculation
-> validators
```

## Pipeline Responsibilities

### Natural Language

Natural language input is a convenience interface only. It may suggest particles, processes, assumptions, and requested outputs, but it is not the canonical state of the calculation.

### PhysicsCard

`PhysicsCard` records the requested process and physics model information in structured form. It should capture external states, allowed internal fields, model name, rule-set references, and unsupported features requested by the user.

For v0.1, it is the source of truth for the process identity, incoming and outgoing particle identifiers, process type, tree-level restriction, requested coupling order or named order assumption, selected rule set, optional internal-species policy, requested output artifacts, and approval state. As of schema 0.1.1, approval is split into topology, amplitude-generation, and heavy-calculation gates.

### ConventionCard

`ConventionCard` records signs, metric, momentum flow, spinor ordering, polarization conventions, propagator conventions, and naming conventions. Convention changes require explicit approval.

For v0.1, it records spacetime dimension, metric signature, Fourier and momentum-flow conventions, all-momenta-incoming vertex convention, external-state momentum convention, natural units, spin/polarization sum and average policy, and optional gravity conventions. It is separate from `PhysicsCard` so the same process can be reviewed against explicit convention choices.

### RuleRegistry

`RuleRegistry` loads and resolves Feynman rules from built-in and custom sources. Every rule must carry provenance, trust status, applicable fields, Lorentz structure metadata, coupling symbols, and convention compatibility notes.

For v0.1, the registry represents vertices and propagators. Each rule records participating particle identifiers, field identifiers, field roles, quantum-field roles such as `psi` and `psi_bar`, momentum order, Lorentz/index structure, LaTeX representation, FeynCalc template, coupling order, mass dimension, symmetries, provenance entries, and trust status. As of schema 0.1.1, the registry also carries a minimal particle catalog for conjugation/crossing checks. Untrusted or conflicting rules may be stored for review, but they cannot silently become trusted inputs.

### Candidate and Approved Process

A candidate process is a structured interpretation that may still contain unresolved assumptions or untrusted rules. An approved process is frozen for diagram generation after conventions, rules, and process scope are accepted.

Approval requires a compatible `PhysicsCard`, `ConventionCard`, and `RuleRegistry`: the process must be in v0.1 scope, conventions must be explicit, and every required rule must be selected by identifier with acceptable trust status.

### DiagramIR

`DiagramIR` is the canonical representation of generated diagrams. It should represent graph topology, external and internal lines, vertices, rule bindings, momentum labels, field identities, and diagram-level metadata.

For v0.1, each diagram records a diagram identifier, process identifier, loop order fixed to zero, channel, external legs, vertex instances, internal lines, momentum routing, referenced rule identifiers, coupling order, symmetry factor, and diagram status. As of schema 0.1.1, each vertex instance must bind every Feynman-rule field slot explicitly through `slot_bindings`; endpoint order is not physics truth. It does not encode TikZ layout or Mathematica formatting as physics truth.

### Renderers and Builders

Renderers and builders consume `DiagramIR`; they do not define physics state. Initial targets include:

- TikZ-Feynman rendering.
- LaTeX amplitude assembly.
- Mathematica/FeynCalc code generation.

### LaTeX and FeynCalc Artifacts

LaTeX and FeynCalc outputs are derived artifacts. They should be reproducible from structured cards, the rule registry, and `DiagramIR`.

### Human-Controlled Heavy Calculation

Long-running simplification, tensor reduction, trace evaluation, and model validation happen outside the live agent loop. FeynAgent may prepare code and checklists, but humans decide when and how to run heavy calculations.

### Validators

Validators check structure, provenance, scope compliance, convention consistency, rule compatibility, and benchmark reproducibility. Failed validations should be actionable and testable.

## Canonical Data Contracts

The four v0.1 contracts are JSON Schemas under `schemas/`:

- `PhysicsCard`: describes what process is being requested and which rule set may be used.
- `ConventionCard`: describes the explicit physics conventions used to interpret rules and generated artifacts.
- `RuleRegistry`: stores provenance-aware vertex and propagator rules.
- `DiagramIR`: stores tree-level diagram structure and references back to approved rule identifiers.

Human-readable notes are optional metadata only. They cannot replace required structured fields.

## Data Flow

```text
PhysicsCard + ConventionCard
    -> scoped candidate process
    -> RuleRegistry compatibility and trust checks
    -> approved process
    -> DiagramIR generation
    -> derived renderers/builders
    -> TikZ-Feynman / LaTeX / FeynCalc artifacts
    -> human-controlled calculation
    -> validators and regression tests
```

The data flow is intentionally one-way for derived artifacts. TikZ, LaTeX, and Mathematica/FeynCalc outputs may expose mistakes, but corrections must flow back into structured cards, registry entries, schemas, or `DiagramIR`, not into derived files as hidden sources of truth.

## Repository Layout

- `docs/`: scope, architecture, decisions, and human-readable design notes.
- `schemas/`: future JSON/YAML schemas for structured cards and IR.
- `src/feynagent/`: Python package source.
- `rules/`: built-in and custom rule registry inputs.
- `benchmarks/`: benchmark cases and gold artifacts.
- `scripts/`: small maintenance and validation scripts.
- `tests/`: regression and unit tests.
- `runs/`: generated run artifacts.
- `reports/`: generated reports and summaries.
