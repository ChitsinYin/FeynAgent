# Day-7 B04 Amplitude Closure

- Run directory: `C:/Users/lenovo/.codex/worktrees/b767/FeynAgent/runs/20260819_104036_B04_phi_phi_to_h_h_2ea1e98b`
- Amplitude artifacts: `C:/Users/lenovo/.codex/worktrees/b767/FeynAgent/runs/20260819_104036_B04_phi_phi_to_h_h_2ea1e98b/amplitudes`
- Compiled PDF: `C:/Users/lenovo/.codex/worktrees/b767/FeynAgent/runs/20260819_104036_B04_phi_phi_to_h_h_2ea1e98b/amplitudes/amplitudes.pdf`
- PDF sha256: `a5f9f59380c06c83583155161c38179af1a99800984ff9ce953a72429d173551`
- Backend: `DIRECT_FEYNCALC_CUSTOM`
- Amplitude layers: `EXACT_RAW` first, then `REDUCED_NR_TT`.
- M2: not constructed; closure stops before M2 because this request is diagram-amplitude closure only.

## Gold Mapping

| Gold | Generated | Artifact | Classification |
| --- | --- | --- | --- |
| a | t | `amp_001` | `PASS_AFTER_EXPLICIT_CONVENTION_MAP` |
| b | u | `amp_002` | `PASS_AFTER_EXPLICIT_CONVENTION_MAP` |
| c | s | `amp_003` | `PASS` |
| d | contact | `amp_004` | `PASS` |

## Validation Hierarchy

- A exact/structural gold comparison: `PASS`
- B explicit convention-map comparison: `PASS`
- C mass dimension: `PASS`
- D external graviton transversality/tracelessness: `PASS`
- E permutation/crossing relations: `PASS`

## Convention Maps

- `a <-> generated t`: `qt = p1-k1 = -(k1-p1)_gold`; scalar propagator orientation is mapped, and each vertex scalar momentum slot is mapped explicitly.
- `b <-> generated u`: `qu = p1-k2 = -(k2-p1)_gold`; scalar propagator orientation is mapped, and each vertex scalar momentum slot is mapped explicitly.
- `c <-> generated s`: `vertex:h_h_h` uses the locked audited helper-compatible `GravitonVertex` implementation; the locked rule remains the authority.
- `d <-> generated contact`: canonical source is the locked corrected manual `TauLocked`; historical FeynGrav 3.0 `ssgg` is not used.

## Reduced Layer

- `amp_001`: `Ma = 0` only after approved NR/TT reduction.
- `amp_002`: `Mb = 0` only after approved NR/TT reduction.
- `amp_003`: `Mc = -(3 i/8) kappa^2 M^2 T` after approved NR/TT reduction.
- `amp_004`: `Md = +(i/2) kappa^2 M^2 T` after approved NR/TT reduction.
- `amp_total`: `+(i/8) kappa^2 M^2 T` in the reduced layer.

## Rule Authority

- Used only locked rule IDs: `propagator:phi`, `vertex:h_phi_phi`, `propagator:h`, `vertex:h_h_h`, `vertex:h_h_phi_phi`.
- Saved per-diagram manifests include the exact rule IDs, per-rule record hashes, knowledge-lock hash, and gold/provenance hashes.
- No rule was changed to force agreement; no disagreements were averaged.
