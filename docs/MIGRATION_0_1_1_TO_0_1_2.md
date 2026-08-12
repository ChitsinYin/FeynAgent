# Migration 0.1.1 To 0.1.2

Status: mandatory Day 3 semantic fix before amplitude generation.

## Why This Migration Exists

The Day 2 external review found that external fermion flow was derived mainly from `incoming`/`outgoing` state role. That is not sufficient for QFT fermion-number flow and would make antifermion arrows wrong.

## Contract Changes

### PhysicsCard 0.1.2

`PhysicsCard.schema_version` is bumped to `0.1.2` because process particles and process-level presentation metadata may now carry structured rendering labels:

```yaml
latex_label: e^{-}
```

Process particles may carry `latex_label`, and `presentation.particle_latex_labels` may provide labels for internal species such as `gamma`. This metadata is only for rendering labels. It does not change `particle_id`, rule matching, topology generation, or physics identity.

### DiagramIR 0.1.2

`DiagramIR.schema_version` is bumped to `0.1.2` because the semantics of `fermion_flow.flow_direction` are corrected:

```text
psi     -> into_vertex
psi_bar -> out_of_vertex
```

This applies to external and internal Dirac field bindings. The renderer must use these explicit bindings and must fail if they are missing or inconsistent.

### Unchanged Contracts

`ConventionCard` remains at `0.1.1`.
`RuleRegistry` remains at `0.1.1`.

## External Dirac Truth Table

| physical external state | bound field | wavefunction label for later amplitude work | TikZ arrow |
| --- | --- | --- | --- |
| incoming fermion | `psi` | `u(p)` | toward vertex |
| outgoing fermion | `psi_bar` | `ubar(p)` | away from vertex |
| incoming antifermion | `psi_bar` | `vbar(p)` | away from vertex |
| outgoing antifermion | `psi` | `v(p)` | toward vertex |

No amplitude wavefunctions are generated in this migration.

## Renderer Changes

- External fermion arrows are rendered from `fermion_flow.flow_direction`, not `state_role`.
- Internal fermion arrows are oriented from the `psi_bar/out_of_vertex` endpoint toward the `psi/into_vertex` endpoint.
- The renderer no longer assumes internal fermion arrows point from display vertex `v1` to display vertex `v2`.
- Labels use structured `latex_label` presentation metadata when available.
- Render manifests use schema version `0.1.2`.

## Migrated Artifacts

- `schemas/physics_card.schema.json`
- `schemas/diagram_ir.schema.json`
- `benchmarks/B01_ee_to_mumu/physics_card.yaml`
- `benchmarks/B01_ee_to_mumu/diagrams.yaml`
- `benchmarks/B01_ee_to_mumu/expected.yaml`
- `benchmarks/B02_compton/physics_card.yaml`
- `benchmarks/B02_compton/diagrams.yaml`
- `benchmarks/B02_compton/expected.yaml`

## Explicit Non-Actions

No amplitudes, Dirac traces, polarization sums, Ward identities, loop diagrams, FeynRules integration, phase-space integration, remote workflow, or compatibility patch files were added.
