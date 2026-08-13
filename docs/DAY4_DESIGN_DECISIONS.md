# Day 4 Design Decisions

## Architecture Pivot

FeynAgent will not continue expanding the Days 1-3 Python implementation into a duplicate of FeynArts/FeynCalc for standard processes. The Day-3 implementation remains valuable because it exposed convention, provenance, crossing, fermion-flow, and renderer-divergence issues in a compact auditable setting.

## Backend Selection

Use `feynarts_feyncalc_native` for standard QED/SM/QCD sectors supported by installed native models.

Use `custom_audited_model` for future user-supplied nonstandard interactions. The preferred target is a FeynArts-compatible model or adapter so custom interactions can still use native diagram generation and FeynCalc algebra.

Use `legacy_custom_backend` only for regression, pedagogy, audit, and fallback.

## No Day-4 Feature Expansion

Day 4 implements only a minimal native FeynArts/FeynCalc tree-level QED backend for B01/B02/B03 benchmark regression. It does not add gravity, loops, phase-space integration, FeynRules, HPC orchestration, or multi-agent orchestration.

## Heavy Calculation Boundary

The Day-3 `compute_m2.wl` files are historical scaffolds. They are not production-validated and must not be executed unless a human explicitly approves a future heavy-calculation task. Production squared-amplitude work should be redesigned around native FeynArts/FeynCalc examples and process-specific external states.

## Review Bundle Policy

Future review bundles must be self-contained for Python validation and tests. They should include schemas, Python source, benchmark cards/fixtures, relevant rules or native-backend adapters, test files, and small logs needed to reproduce QA decisions. They must exclude `.git`, caches, unrelated historical runs, and large transient Mathematica outputs.
