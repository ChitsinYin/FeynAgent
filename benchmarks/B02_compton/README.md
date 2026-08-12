# B02 Compton Benchmark

## Process

This benchmark specifies the tree-level QED process

```text
e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)
```

It is a specification and representation benchmark only. It does not contain the final Compton amplitude, squared amplitude, Dirac traces, polarization sums, or Ward-identity checks.

## Physics Truth

The physics truth for Day 1 lives in structured files:

- `physics_card.yaml`: process identity, external particles, external momenta, rule-set choice, tree-level restriction, and requested outputs.
- `convention_card.yaml`: spacetime dimension, metric signature, natural units, external momentum convention, and all-momenta-incoming vertex convention.
- `rule_manifest.yaml`: benchmark-local copy of the minimal QED rules required by the topology.
- `diagrams.yaml`: DiagramIR representation of the two tree topologies.
- `expected.yaml`: benchmark oracle for topology tests.

LaTeX, TikZ-Feynman, FeynCalc code, and Mathematica notebooks are not the source of truth for this benchmark.

## Representation Convention

External momenta use the physical scattering convention:

- `p1` and `k1` are incoming external momenta.
- `p2` and `k2` are outgoing external momenta.

The QED vertex rule uses the all-momenta-incoming convention. That means outgoing external legs are crossed when binding a diagram to a vertex rule, but the process card still records the physical external convention. This separation prevents a renderer or algebra backend from silently changing the process definition.

## Why There Are Two Diagrams

At tree level in QED, Compton scattering has exactly two connected electron-exchange topologies using two electron-electron-photon vertices and one internal electron propagator:

- s-channel electron exchange with internal momentum `p1+k1`.
- u-channel electron exchange with internal momentum `p1-k2`.

There is no independent four-point electron-electron-photon-photon contact vertex in minimal QED, and loop diagrams are outside v0.1 scope.

## Rule Trust Status

The minimal QED rules in `rules/qed/qed_tree_v1.yaml` and `rule_manifest.yaml` are marked `validated_pending_convention_review`. Their signs and conventions are explicitly stated, but Day 1 did not perform an independent convention audit. They must not be silently upgraded to trusted.

## Day 2/3 Work

Later phases should implement:

- Diagram generation from the `PhysicsCard`, `ConventionCard`, and `RuleRegistry` rather than hand-authored topology files.
- Diagram-level rule assembly from `DiagramIR`.
- LaTeX amplitude generation from the same `DiagramIR`.
- FeynCalc code generation from the same `DiagramIR`.
- Human-controlled algebra checks, including traces, polarization sums, simplification, and Ward-identity validation.

Those calculations are intentionally not performed in this benchmark today.
