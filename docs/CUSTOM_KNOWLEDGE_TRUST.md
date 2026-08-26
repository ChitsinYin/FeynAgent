# Custom Knowledge Trust

FeynAgent treats custom physics knowledge as a trust-boundary crossing, not as ordinary configuration.

## Executable Code

Custom Wolfram files are executable code. A `.wl`, `.m`, or `.nb` file can run arbitrary Wolfram Language commands, load external packages, read local files, or write outputs. Review and trust the file and its source before execution.

FeynAgent does not automatically trust arbitrary Wolfram notebooks, scripts, helper package output, pasted expressions, or generated files. Successful execution is not the same thing as validated physics authority.

## Locked Custom Route Policy

The public v0.1 custom route is exactly:

- process: `phi phi -> h h`;
- model: `reheating_scalar_gravity_v1`;
- backend: `direct_feyncalc_custom_audited`;
- knowledge: separately supplied audited external knowledge package;
- manifest: `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.

This route requires convention, rule, and hash validation. The backend must resolve the local knowledge package, match the expected convention ID, and pass rule audit before amplitude execution continues.

The committed repository contains only sanitized benchmark metadata and a hash-only knowledge manifest. It does not bundle the private/source external knowledge package, source PDFs, notebooks, raw gold files, or machine-local absolute knowledge roots.

## Helper Output Is Evidence, Not Authority

FeynGrav and other package helper outputs can help identify candidate rules or compare expressions, but they are not automatically physics authority. Candidate rules remain untrusted until they have explicit provenance, convention mapping, hash or source checks where applicable, and project rule-audit approval.

Historical helper output that conflicts with the locked B04 rule set remains rejected or review-only. Do not promote it to trusted status without a new recorded audit.

## Execution Authorization

Production-heavy execution requires explicit authorization in an `ExecutionRequest` or equivalent release-gate record. Bounded benchmark regression is a separate authorization mode and must not be reused as production-heavy approval.

B04 topology generation and B04 amplitude generation do not authorize B04 M2. B04 M2 requires separate explicit operations and remains outside automatic public execution.

## Repository Hygiene

Do not commit:

- `.feynagent/` state;
- `runs/` outputs other than intentional placeholders or curated public-gallery artifacts outside `runs/`;
- private/source external knowledge package contents;
- local absolute knowledge-root paths;
- raw private notebooks, PDFs, Wolfram scripts, or gold files;
- credentials, tokens, passwords, or authentication logs;
- stale review ZIP/archive binaries.

Apache-2.0 applies to FeynAgent-owned code and documentation only. It does not relicense external physics packages, private knowledge packages, or third-party source material referenced for provenance.
