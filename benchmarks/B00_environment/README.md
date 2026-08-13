# B00 Environment Smoke Test

This benchmark records local tool availability for FeynAgent v0.1.

It is intentionally bounded:

- No software is installed automatically.
- No global Mathematica initialization files are modified.
- No user-wide environment variables are changed.
- No heavy symbolic calculations are performed.
- Raw command logs are machine-local and should be written under `.feynagent/` or `runs/init/<run_id>/`, not committed under `benchmarks/`.

The smoke test checks Python, Wolfram/Mathematica, FeynCalc, FeynArts, LaTeX, and TikZ-Feynman availability.

