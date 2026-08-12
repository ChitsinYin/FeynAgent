# FeynAgent

FeynAgent is a research-oriented HEP phenomenology tool for turning auditable physics specifications into tree-level diagram artifacts.

The v0.1 workflow is rules-first:

1. Capture the process, model assumptions, and conventions as structured cards.
2. Resolve user-supplied or built-in Feynman rules through a provenance-aware registry.
3. Build a complete tree-level `DiagramIR` for supported processes.
4. Derive TikZ-Feynman, LaTeX amplitude, and Mathematica/FeynCalc artifacts from the same `DiagramIR`.
5. Leave heavy symbolic simplification and validation under human control.

Day 1 freezes scope and architecture only. It does not install dependencies, run physics calculations, or attempt heavy symbolic algebra.

See:

- [docs/SCOPE_V0_1.md](docs/SCOPE_V0_1.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md)

