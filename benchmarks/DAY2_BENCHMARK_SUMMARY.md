# Day 2 Topology-Generator Benchmarks

This benchmark set exercises deterministic tree-level `2 -> 2` topology generation from structured artifacts only.

No diagrams are rendered and no amplitudes are calculated.

## B01

Process:

```text
e-(p1) + e+(p2) -> mu-(p3) + mu+(p4)
```

Expected topology:

- channels: `{s}`
- internal species: `gamma`
- internal momentum: `p1+p2`
- vertices: `rule:qed_tree_v1:e_e_gamma_vertex`, `rule:qed_tree_v1:mu_mu_gamma_vertex`
- propagator: `rule:qed_tree_v1:photon_propagator`
- coupling order: `e^2`
- loop order: `0`
- symmetry factor: `1`

## B02

Process:

```text
e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)
```

Expected topology:

- channels: `{s, u}`
- internal species: `e-`
- internal momenta: `p1+k1`, `p1-k2`
- vertex: `rule:qed_tree_v1:e_e_gamma_vertex`
- propagator: `rule:qed_tree_v1:electron_propagator`
- coupling order: `e^2`
- loop order: `0`
- symmetry factor: `1`

## Comparison Method

Generated diagrams are compared to gold topology files using canonical structural signatures, not raw YAML text. The signature includes channel, coupling order, internal line species/momentum/propagator, vertex rule IDs, and explicit rule-slot binding semantics.

Benchmark-local `rule_manifest.yaml` files are lightweight selectors only. The canonical editable QED rules live in `rules/qed/qed_tree_v1.yaml`.

