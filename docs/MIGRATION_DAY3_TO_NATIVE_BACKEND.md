# Migration: Day 3 To Native Backend

Day 3 demonstrated that FeynAgent can assemble tree-level QED amplitudes from auditable Python data structures. Day 4 changes the production strategy: standard QED/SM/QCD processes should use mature native FeynArts/FeynCalc capabilities rather than extending the custom implementation into a parallel physics engine.

## What Changes

- `feynarts_feyncalc_native` becomes the primary target for standard supported sectors.
- The Day-3 Python builder and renderers move to `legacy_custom_backend` status.
- The QED RuleRegistry remains a documented audit snapshot for legacy regression and convention review, not the production authority for native standard amplitudes.
- Future custom interactions should target `custom_audited_model`, ideally by producing or adapting FeynArts-compatible model definitions.

## Benchmark And Generated Separation

Day 3 committed generated files under `benchmarks/` as part of the review bundle and provenance record. After the Day-4 cleanup, superseded generated artifacts were removed from `benchmarks/` following the external pre-clean safety snapshot. Benchmark-local legacy fixtures remain under `legacy/` directories, while generated artifacts belong under `runs/`.

Starting Day 4:

- new generated amplitudes go under `runs/`;
- new generated PDFs go under `runs/`;
- new Wolfram logs and smoke outputs go under `runs/`;
- new M2 outputs go under `runs/`;
- `benchmarks/` is reserved for cards, approved/gold structures, references, and explicitly marked historical Day-3 generated artifacts.

## Retired Day-3 Heavy Script

The generic Day-3 `compute_m2.wl` scripts are not validated for production use. They are retained only as historical human-run scaffolds and must not be executed as a production result.

Known limitations to record before any future replacement:

- polarization sums must be selected from the external vector states present in the process;
- massless photon sums must not use the two-argument massive-vector form;
- standard QED native workflows should follow official FeynCalc example patterns for spin and polarization sums;
- heavy calculation remains gated by explicit human approval.

## Migration Boundary

The Day-4 migration records backend ownership, implements the minimal native FeynArts/FeynCalc tree-level QED backend, retires the generic Day-3 heavy script from production, and prevents new generated-output drift into `benchmarks/`.
