# Environment Setup

FeynAgent does not track machine-local probe output as canonical project state.

Local environment probes should write to one of:

- `.feynagent/` for developer-local scratch/probe state;
- `runs/init/<run_id>/` for bounded initialization or smoke-test evidence that should be reviewable.

`benchmarks/B00_environment/` contains only the portable smoke-test inputs and expectations. It should not contain local command outputs, host-specific paths, generated PDFs, or tool logs.

Expected tools for the current development line:

- Python 3.10 or compatible project-supported Python;
- WolframScript / Mathematica capable of loading FeynCalc;
- FeynCalc with FeynArts support;
- pdflatex or lualatex for renderer smoke tests when needed.

Probe outputs are intentionally not canonical because executable paths, OS versions, MiKTeX state, and Wolfram installation paths are machine-local.
