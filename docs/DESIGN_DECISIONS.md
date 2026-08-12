# Design Decisions

## Accepted Decisions

### Canonical physics state lives in structured artifacts, not chat history

Conversation may help draft a process, but reproducibility requires structured cards, schemas, registry entries, and IR files.

### TikZ and Mathematica code are derived artifacts, not sources of truth

TikZ-Feynman diagrams, LaTeX amplitudes, and Mathematica/FeynCalc code must be generated from the canonical structured state. Manual edits to derived files should not redefine the physics.

### Custom Feynman rules require provenance and trust status

Each custom rule must record where it came from, who supplied it, when it was added, which conventions it assumes, and whether it is trusted, untrusted, or rejected.

### Untrusted or conflicting rules cannot silently become trusted

Rules with missing provenance, convention conflicts, duplicate definitions, or unresolved ambiguity must remain blocked until explicitly reviewed.

### Heavy computations are outside the live agent loop

The live agent may prepare Mathematica/FeynCalc code, validation checklists, and run instructions, but long-running symbolic calculations require human control.

### Normal runs must not generate ad-hoc patch files

Routine output belongs in structured run directories, reports, or derived artifact files. Patch files are for explicit review workflows, not normal operation.

### Repeated failures should become regression tests rather than prompt growth

If the same issue recurs, encode it as a schema rule, validator, benchmark, or regression test instead of relying on longer instructions.

## Open Decision Log

Future decisions should record:

- Date.
- Context.
- Decision.
- Consequences.
- Migration notes, if existing artifacts are affected.

