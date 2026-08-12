# B02 Compton Benchmark

## Process

This benchmark specifies the tree-level QED process

```text
e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)
```

It is a specification and representation benchmark only. It does not contain the final Compton amplitude, squared amplitude, Dirac traces, polarization sums, or Ward-identity checks.

## Physics Truth

The physics truth for Day 2 semantic closure lives in structured files:

- `physics_card.yaml`: process identity, external particles, external momenta, rule-set choice, tree-level restriction, requested outputs, and split approval gates.
- `convention_card.yaml`: spacetime dimension, metric signature, natural units, external momentum convention, and all-momenta-incoming vertex convention.
- `rule_manifest.yaml`: lightweight non-canonical selector for the canonical QED registry in `../../rules/qed/qed_tree_v1.yaml`.
- `diagrams.yaml`: DiagramIR representation of the two tree topologies with explicit vertex rule-slot bindings.
- `expected.yaml`: benchmark oracle for topology and binding tests.

LaTeX, TikZ-Feynman, FeynCalc code, and Mathematica notebooks are not the source of truth for this benchmark.

## Representation Convention

External momenta use the physical scattering convention:

- `p1` and `k1` are incoming external momenta.
- `p2` and `k2` are outgoing external momenta.

The QED vertex rule uses the all-momenta-incoming convention. Each vertex instance therefore binds rule slots explicitly and records whether a physical external leg is used directly or crossed into the all-incoming vertex convention. Future amplitude assembly must read `slot_bindings`; it must not infer rule-slot meaning from list order.

## Why There Are Two Diagrams

At tree level in minimal QED, Compton scattering has exactly two connected electron-exchange topologies using two electron-electron-photon vertices and one internal electron propagator:

- s-channel electron exchange with internal momentum `p1+k1`.
- u-channel electron exchange with internal momentum `p1-k2`.

There is no independent four-point electron-electron-photon-photon contact vertex in minimal QED, and loop diagrams are outside v0.1 scope.

## Rule Trust Status

The minimal QED rules in `rules/qed/qed_tree_v1.yaml` are marked `validated_pending_convention_review`. Their signs and conventions are explicitly stated, but Day 1/Day 2 semantic closure did not perform an independent convention audit. They must not be silently upgraded to trusted.

## Approval Scope

B02 is approved for topology representation only. Amplitude generation and heavy calculation approval gates remain `not_requested`.

## Day 2/3 Work

Later phases should implement diagram generation, DiagramIR slot-binding assembly, LaTeX amplitude generation, and FeynCalc code generation from the same structured artifacts. Human-controlled algebra checks can follow later.

Those calculations are intentionally not performed in this benchmark today.
