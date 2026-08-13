# FeynAgent

FeynAgent is a research-oriented HEP phenomenology tool for reproducible tree-level benchmark workflows with explicit backend ownership.

As of Day 4, the production path for standard supported sectors is native FeynArts/FeynCalc:

1. Capture process intent, conventions, and approvals as structured benchmark cards.
2. Use `feynarts_feyncalc_native` for standard QED/SM/QCD sectors supported by installed FeynArts/FeynCalc model files.
3. Let FeynArts generate diagrams and amplitudes, then convert with `FCFAConvert` for FeynCalc algebra and validation.
4. Keep the Days 1-3 Python topology/amplitude implementation as `legacy_custom_backend` for regression, pedagogy, audit, and fallback.
5. Keep the custom RuleRegistry as the authority for future nonstandard interactions until an audited native model or adapter exists.
6. Write generated amplitudes, PDFs, Wolfram logs, and M2 outputs under `runs/`; keep `benchmarks/` for specs, gold/reference fixtures, and explicitly marked legacy fixtures.
7. Keep machine-local probes and diagnostics under `.feynagent/` or run-specific directories such as `runs/init/<run_id>/`.

Heavy calculations remain explicitly gated. Day-4 bounded M2 regressions were benchmark QA runs, not blanket production `heavy_calculation` approval.

See:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/BACKEND_STRATEGY.md](docs/BACKEND_STRATEGY.md)
- [docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md](docs/MIGRATION_DAY3_TO_NATIVE_BACKEND.md)
- [docs/DAY4_DESIGN_DECISIONS.md](docs/DAY4_DESIGN_DECISIONS.md)
- [docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md)
