# Agent Operating Rules

- Never modify conventions silently. Any convention change must be explicit, recorded, and approved.
- Never invent a trusted Feynman rule. Rules need source, provenance, and trust status.
- Never overwrite benchmark gold files without explicit instruction.
- Generated run artifacts belong under `runs/`.
- Avoid duplicate names such as `final_v2_new`; use stable names, timestamps, or run IDs.
- Prefer schema changes plus migration notes over local patch files.
- Keep heavy Mathematica/FeynCalc computations outside the live agent loop.
- Promote repeated failures into regression tests rather than expanding prompts indefinitely.

