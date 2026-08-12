# FeynAgent v0.1 Scope

## Project Goal

FeynAgent aims to help HEP phenomenology researchers move from natural-language process descriptions and user-supplied Feynman rules to auditable, structured physics specifications, complete tree-level diagrams, diagram-level rule assembly, LaTeX amplitudes, and executable Mathematica/FeynCalc code.

The tool is not intended to replace human physics judgment. It should make assumptions explicit, preserve provenance, and produce artifacts that a researcher can inspect, approve, and validate.

## Supported Scope

v0.1 supports:

- Tree-level processes only.
- `1 -> n` decays and `2 -> 2` scattering.
- Initial benchmark focus on `2 -> 2` scattering.
- Scalar, Dirac fermion, vector, and symmetric rank-2 tensor fields at the representation level.
- A rules-first workflow.
- User-supplied or pre-registered Feynman rules.
- Standard QED rules as the first built-in rule set.
- A custom rule registry with provenance.
- Explicit convention records.
- A diagram intermediate representation named `DiagramIR`.
- Later generation of TikZ-Feynman, LaTeX amplitudes, and FeynCalc code from the same `DiagramIR`.

## Explicit Non-Goals

v0.1 does not support:

- Loop diagrams.
- Automatic renormalization.
- Automatic derivation of arbitrary Feynman rules from arbitrary Lagrangians.
- Full FeynRules integration.
- Automatic thermal field theory.
- Automatic phase-space integration.
- Boltzmann equations.
- Automatic paper writing.
- Autonomous long-running Mathematica calculations.
- Remote or HPC workflows.
- GUI or web app workflows.
- Arbitrary model discovery.

## Human Approval Gates

Human approval is required before:

- Accepting or changing convention choices.
- Marking custom Feynman rules as trusted.
- Resolving conflicting rule definitions.
- Freezing a process as approved for diagram generation.
- Updating benchmark gold files.
- Running heavy external symbolic calculations.
- Treating generated LaTeX, TikZ, or Mathematica code as publishable.

## Day 1 Acceptance Criteria

Day 1 is complete when:

- The repository skeleton exists with `docs`, `schemas`, `src/feynagent`, `rules`, `benchmarks`, `scripts`, `tests`, `runs`, and `reports`.
- The top-level files `README.md`, `AGENTS.md`, `.gitignore`, and `pyproject.toml` exist.
- `docs/SCOPE_V0_1.md` records supported scope, non-goals, approval gates, acceptance criteria, and the v0.1 Definition of Done.
- `docs/ARCHITECTURE.md` defines the conceptual pipeline.
- `docs/DESIGN_DECISIONS.md` records the initial architectural decisions.
- Git is initialized if the directory was not already a repository.
- No dependencies are installed and no physics calculations are attempted.

## v0.1 Definition of Done

v0.1 is done when:

- Structured cards exist for process specification and conventions.
- A provenance-aware rule registry can load built-in QED rules and user-supplied custom rules.
- Candidate processes can be promoted to approved processes only through explicit checks.
- `DiagramIR` can represent complete tree-level diagrams for the benchmark `2 -> 2` scope.
- Diagram-level rule assembly is inspectable and reproducible.
- LaTeX amplitude and FeynCalc code generation are derived from `DiagramIR`.
- Initial benchmarks have stable gold artifacts and regression tests.
- Unsupported requests fail clearly with documented reasons.
- Heavy algebra remains human-controlled outside the live agent loop.

