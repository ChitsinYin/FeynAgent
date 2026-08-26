# B04 Locked Scalar-Gravity Example Manifest

This directory is a public documentation/example manifest for the single locked FeynAgent v0.1 custom route. It is not a bundled private knowledge package and it is not a generated run.

## Locked Route

```text
process = phi phi -> h h
process_id = process:B04_phi_phi_to_h_h
model_id = reheating_scalar_gravity_v1
backend = direct_feyncalc_custom_audited
```

Canonical repository inputs:

```text
benchmarks/B04_phi_phi_to_hh/physics_card.yaml
profiles/backends/b04_custom_gravity_audited.yaml
benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml
```

## External Knowledge Boundary

The B04 route requires separately supplied audited external knowledge. The repository commits only sanitized benchmark metadata and a hash-only knowledge manifest. The private/source external knowledge package is not bundled here.

Do not add private source PDFs, private notebooks, raw gold files, absolute local paths, or unapproved third-party content to this example.

## Required Rule IDs

- `propagator:phi`
- `vertex:h_phi_phi`
- `propagator:h`
- `vertex:h_h_h`
- `vertex:h_h_phi_phi`

## Expected Four Topology Classes

| gold label | topology | generated channel | internal species | momentum | classification |
| --- | --- | --- | --- | --- | --- |
| `a` | scalar exchange | `t` | `phi` | gold `k1-p1`, generated `p1-k1` | `MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP` |
| `b` | scalar exchange | `u` | `phi` | gold `k2-p1`, generated `p1-k2` | `MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP` |
| `c` | s-channel graviton exchange | `s` | `h` | `p1+p2` | `MATCH` |
| `d` | contact h h phi phi | `contact` | none | none | `MATCH` |

## Per-Diagram Reduced-Layer Summary

The exact/raw amplitudes remain preserved before reduction. In the approved `REDUCED_NR_TT` comparison layer:

| diagram | reduced summary |
| --- | --- |
| `a` / `amp_001` | `Ma = 0` |
| `b` / `amp_002` | `Mb = 0` |
| `c` / `amp_003` | `Mc = -(3 i/8) kappa^2 M^2 T` |
| `d` / `amp_004` | `Md = +(i/2) kappa^2 M^2 T` |
| total | `+(i/8) kappa^2 M^2 T` |

with

```text
T = eta^(gamma nu) eta^(mu sigma) + eta^(gamma mu) eta^(nu sigma)
```

## Reduced Benchmark M2 Summary

The reduced benchmark M2 evidence is summarized as:

| quantity | value |
| --- | --- |
| raw polarization-summed total | `2 M^4/M_P^4` |
| initial identical factor | `1/2` |
| final identical phase-space factor | `1/2` |
| rate-convention M2 | `M^4/(2 M_P^4)` |

This summary records the Day-7 reduced benchmark evidence. B04 topology or amplitude authorization does not authorize automatic B04 M2 execution.

## Explicit Non-Support

This example does not support arbitrary gravity, arbitrary BSM, arbitrary Standard Model workflows, QCD production, loops, renormalization, or ungated production-heavy execution. The route is valid only for locked B04 with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and the separately supplied audited external knowledge package.

See `manifest.yaml` for the machine-readable public summary.
