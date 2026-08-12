# B01 e- e+ To mu- mu+ Benchmark

This benchmark specifies the tree-level QED process:

```text
e-(p1) + e+(p2) -> mu-(p3) + mu+(p4)
```

It is a topology-generation benchmark only. It does not contain amplitudes, squared amplitudes, traces, polarization sums, or rendered diagrams.

Gold topology:

- exactly one connected tree diagram;
- s-channel photon exchange;
- internal momentum `p1+p2` in the physical external momentum convention;
- two fermion-photon QED vertices;
- coupling order `e^2`;
- loop order `0`;
- symmetry factor `1`.

`rule_manifest.yaml` is a lightweight selector for the canonical QED registry in `../../rules/qed/qed_tree_v1.yaml`; it is not an editable rule copy.
