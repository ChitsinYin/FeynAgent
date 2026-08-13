# FeynAgent Local Initialization

FeynAgent keeps machine-local runtime state outside version control under `.feynagent/`.

## Commands

Initialize local capability metadata:

```bash
python -m feynagent init
```

Run a fresh capability check without relying on stored state:

```bash
python -m feynagent doctor
```

If `wolframscript` is not on `PATH`, pass it explicitly:

```bash
python -m feynagent init --wolframscript /path/to/wolframscript
```

If FeynCalc is installed in a nonstandard location, provide a directory hint:

```bash
python -m feynagent init --feyncalc-dir /path/to/FeynCalc
```

FeynAgent does not install Wolfram, FeynCalc, FeynArts, or LaTeX.

## Wolfram Loading Policy

FeynAgent loads FeynArts through the modern FeynCalc add-on path:

```wolfram
$LoadAddOns = {"FeynArts"};
<< FeynCalc`
```

It does not intentionally mix a separately loaded unpatched FeynArts in the same kernel.

## Local Files

`init` writes:

- `.feynagent/environment.yaml`
- `.feynagent/capability_report.json`
- `.feynagent/reference_index.json`

The reference index stores metadata, hashes, and paths for official FeynCalc examples. It does not copy package source or examples into the repository.

## Supported/Tested Version Policy

FeynAgent records detected Wolfram, FeynCalc, and FeynArts versions. It does not block newer compatible versions merely because they differ from the development machine. A version mismatch is a warning only when the initialization probe succeeds and the required packages load through the tested path.

Current tested baseline from Day 4:

- Wolfram: 15.0.1 on Windows
- FeynCalc: 10.1.0
- FeynArts: 3.12

## Doctor Status

`doctor` reports PASS/WARNING/FAIL for:

- Wolfram
- FeynCalc
- FeynArts
- native QED tree capability
- LaTeX

Missing LaTeX is a WARNING for non-rendering workflows. Missing Wolfram/FeynCalc/FeynArts is a FAIL for the native QED tree backend.
