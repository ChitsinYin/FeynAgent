# Day-3 Generated Artifact Cleanup

Status: `legacy_day3_generated_removed_from_benchmarks`

Day 3 committed generated amplitude artifacts under `benchmarks/` as part of the audited review record. On Day 4, the project pivoted to a stricter separation:

- `benchmarks/` contains specs, gold fixtures, and reference structures;
- `runs/` contains ordinary generated amplitudes, PDFs, Wolfram files, logs, and M2 outputs.

The following ordinary generated Day-3 files were removed from the B01/B02 benchmark directories to avoid historical provenance bloat:

- `amplitude_ir.yaml`
- `amplitudes.tex`
- `amplitudes.pdf`
- `amplitudes.wl`
- `amplitude_audit.md`
- `amplitude_smoke.wl`
- `compute_m2.wl`
- `ward_check.wl` for B02

The hand-readable `amplitude_ir.example.yaml` files remain as benchmark reference/gold structures.

Future generated outputs must be placed under `runs/`.
