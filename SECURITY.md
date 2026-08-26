# Security Policy

## Supported Release Surface

FeynAgent v0.1 exposes a narrow public surface:

- standard native tree-level QED 2-to-2 workflows for `e-`, `e+`, `mu-`, `mu+`, and `gamma` through an externally installed FeynArts/FeynCalc toolchain;
- the single locked B04 custom audited route, `phi phi -> h h`, with `model_id = reheating_scalar_gravity_v1` and backend `direct_feyncalc_custom_audited`.

Arbitrary Standard Model workflows, QCD production, arbitrary BSM, arbitrary gravity, loops, renormalization, and ungated production-heavy execution are outside the supported public release surface.

## Executable External Files

Wolfram Language files are executable code. Treat `.wl`, `.m`, and `.nb` files like scripts from any other language: read them, understand their provenance, and run them only in an environment you trust.

FeynAgent does not automatically trust arbitrary Wolfram notebooks or scripts. Custom Wolfram files, third-party package helpers, and pasted notebook output are not physics authority merely because they execute successfully.

## Custom Knowledge Trust Boundary

Locked custom routes require convention, rule, and hash validation before execution. For B04, FeynAgent expects the separately supplied audited external knowledge package to resolve through local machine configuration and match the committed hash-only manifest.

The private/source external knowledge package is not bundled in this repository. Do not commit private source PDFs, notebooks, raw gold files, local absolute knowledge roots, `.feynagent/` state, or generated B04 run outputs.

FeynGrav or other package-helper output is not automatically accepted as authoritative physics. Helper output can be evidence, but rules must still pass the project convention and rule audit gates.

## Heavy Execution Gate

Production-heavy execution requires explicit authorization. Benchmark-regression authorization is not production-heavy authorization, and B04 topology or amplitude authorization is not B04 M2 authorization.

GitHub Actions CI validates only the open-source Python/package layer. It must not install or run Mathematica, WolframScript, FeynCalc, FeynArts, FeynGrav, or private external knowledge packages.

## Licensing Boundary

FeynAgent-owned code and documentation are licensed under Apache-2.0. This repository does not vendor, sublicense, or relicense FeynCalc, FeynArts, Mathematica/Wolfram, FeynGrav, their source material, their examples, their documentation, or private external knowledge packages.

## Reporting Issues

For security or trust-boundary issues, open a GitHub issue or contact the repository maintainer privately if public disclosure would expose credentials, private paths, or private research material. Include the affected file path, commit SHA, and the smallest safe reproducer or description.
