# FeynAgent

FeynAgent is a research-oriented HEP phenomenology tool for reproducible tree-level benchmark workflows with explicit backend ownership.

As of Day 5, FeynAgent separates physics intent, backend implementation, and runtime authorization. For standard supported sectors, the production implementation path remains native FeynArts/FeynCalc:

1. Capture process intent in backend-neutral `PhysicsCard` 0.2.0 objects using `model_id` and `sector`, e.g. `sm_qed` / `qed`.
2. Resolve implementation details through a `BackendProfile`, such as `profiles/backends/feynarts_sm_qed.yaml` or `profiles/backends/legacy_sm_qed.yaml`.
3. Authorize runtime work through `ExecutionRequest`; this is not canonical physics truth.
4. Use `feynarts_feyncalc_native` for standard QED/SM/QCD sectors supported by installed FeynArts/FeynCalc model files.
5. Keep the Days 1-3 Python topology/amplitude implementation as `legacy_custom_backend` for regression, pedagogy, audit, and fallback.
6. Keep the custom RuleRegistry as the authority for future nonstandard interactions until an audited native model or adapter exists.
7. Write generated amplitudes, PDFs, Wolfram logs, and M2 outputs under `runs/`; keep `benchmarks/` for specs, gold/reference fixtures, and explicitly marked legacy fixtures.
8. Keep machine-local probes and diagnostics under `.feynagent/` or run-specific directories such as `runs/init/<run_id>/`.

Heavy calculations remain explicitly gated. Day-4 bounded M2 regressions were benchmark QA runs, not blanket production `heavy_calculation` approval.

See:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/BACKEND_STRATEGY.md](docs/BACKEND_STRATEGY.md)
- [docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md](docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md)
- [docs/MIGRATION_0_1_X_TO_0_2_0.md](docs/MIGRATION_0_1_X_TO_0_2_0.md)
- [docs/DAY4_DESIGN_DECISIONS.md](docs/DAY4_DESIGN_DECISIONS.md)
- [docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md)
