# Day 6 Codex Skill Installation And Discovery Test

Status: PASS_WITH_MANUAL_INSTALL

## Scope

This was a real Codex skill installation and discovery test for FeynAgent. It was not counted as a pass based on direct execution of `skills/feynagent/scripts/*`.

## Codex Version / Surface

- Surface: Codex desktop app, local project task/worktree surface.
- Local project: `FeynAgent` at `E:\003hep-ph-research\Agent\FeynAgent`.
- App package observed from `Get-Command codex`: `OpenAI.Codex_26.810.4967.0_x64__2p2nqsd0c76g0`.
- Packaged executable path: `C:\Program Files\WindowsApps\OpenAI.Codex_26.810.4967.0_x64__2p2nqsd0c76g0\app\resources\codex.exe`.
- Executable file version reported by PowerShell: `0.0.0.0`.
- The packaged `codex.exe` could not be executed from this sandboxed PowerShell surface: process start failed with Windows app-package access denied. Therefore no `codex skills ...` CLI install/discovery command was verified.

## Supported Installation Mechanism Observed

The installed system skill guidance in this client describes local skills as folders under `$CODEX_HOME/skills`, defaulting to `~/.codex/skills` when `CODEX_HOME` is unset. The skill-installer guidance also states that installed skills land in `$CODEX_HOME/skills/<skill-name>`.

Observed local user-skill root:

```text
C:\Users\lenovo\.codex\skills
```

Existing entries before install included:

```text
.system
hatch-pet
```

## Metadata Update

Updated only `skills/feynagent/SKILL.md` discovery metadata by adding standards-compliant YAML front matter with required fields:

```yaml
---
name: feynagent
description: Use for FeynAgent high-energy physics workflows involving standard tree-level QED 2-to-2 processes, Compton scattering, electron/muon/photon amplitudes, FeynArts/FeynCalc native artifacts, deterministic `python -m feynagent run` executions, validation reports, provenance, or local FeynAgent initialization/doctor checks.
---
```

No skill workflow body changes were made in this phase.

Validation command:

```powershell
python C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\feynagent
```

Result:

```text
Skill is valid!
```

## Installation Method

Installed by copying the validated skill folder into the real Codex user skills root:

```powershell
Copy-Item -Path skills\feynagent -Destination C:\Users\lenovo\.codex\skills\feynagent -Recurse
```

Installed skill path:

```text
C:\Users\lenovo\.codex\skills\feynagent
```

Installed files observed:

```text
C:\Users\lenovo\.codex\skills\feynagent\SKILL.md
C:\Users\lenovo\.codex\skills\feynagent\evals\smoke_cases.json
C:\Users\lenovo\.codex\skills\feynagent\references\BACKEND_POLICY.md
C:\Users\lenovo\.codex\skills\feynagent\references\CUSTOM_RULE_PROTOCOL.md
C:\Users\lenovo\.codex\skills\feynagent\references\OUTPUT_CONTRACT.md
C:\Users\lenovo\.codex\skills\feynagent\scripts\ensure_initialized.py
C:\Users\lenovo\.codex\skills\feynagent\scripts\run_feynagent.py
```

Permissions/prompts:

- The main task required sandbox approval to read system skill instructions and to copy into `C:\Users\lenovo\.codex\skills`.
- The fresh Codex task encountered workspace ACL limits and requested elevated execution for project commands.
- No separate Codex UI skill-install confirmation prompt was exposed to this agent surface.

## Fresh Session Test

Fresh Codex task created through the app thread API:

```text
thread_id: 01a0035e-9f22-7691-949d-f2e2dd56db5a
host_id: local
title: FeynAgent Compton Discovery Test
cwd: C:\Users\lenovo\.codex\worktrees\a324\FeynAgent
```

Prompt issued to the fresh session:

```text
Generate the standard tree-level Compton scattering artifact bundle for e- gamma -> e- gamma, including diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output, bounded M2 regression if authorized, and validation/provenance. Report the run directory and whether it passed.
```

The prompt did not mention:

- `SKILL.md`
- `run_feynagent.py`
- source paths

## Discovery Evidence

The fresh session explicitly reported skill/workflow discovery behavior:

```text
I’ll use the FeynAgent workflow for this one, since the request is specifically a standard QED 2-to-2 artifact bundle. I’m going to read the local skill instructions first, then I’ll inspect the repo entry points and run the bundle generation in the project’s expected way.
```

It then reported:

```text
I’ve got the FeynAgent operating rules now. This is a `standard_native` request, so I’m going to follow the native FeynArts/FeynCalc path, check initialization first, and keep generated outputs under `runs/`.
```

Conclusion: Codex did discover and use the installed FeynAgent skill instructions in the fresh session.

## Deterministic Runner Evidence

The fresh session did not count direct skill-script execution as success. It discovered the public package commands:

```text
The package exposes `init`, `doctor`, and `run`; that’s enough to proceed without the missing helper.
```

It created a bounded run-scoped execution request under `runs/requests/`, then invoked the deterministic high-level runner. Final fresh-session result:

```text
Generated and validated the Compton bundle. It passed.
Run directory: runs/20260815_110632_b02_compton_b50bfdb3
validation_report.json: PASS
Diagrams/channels: 2 diagrams, s and u
Native backend: feynarts_feyncalc_native
PDFs generated: diagrams.pdf, amplitudes.pdf
M2 regression: executed under bounded benchmark_regression, PASS
M2 comparison: FeynCalc comparison/equivalence both true
Versions recorded: Wolfram 15.0.1, FeynArts 3.12, FeynCalc 10.1.0
```

The fresh session also reported verification:

```text
python -m feynagent init --timeout 60: PASS
python -m unittest discover -s tests -p test_runner_cli.py: 6 tests OK
python -m unittest discover -s tests -p test_feynarts_feyncalc_backend.py: 17 tests OK
```

Conclusion: the resulting workflow invoked the deterministic public runner path, not direct execution of skill helper scripts.

## Limitation

This Codex surface exposed reliable filesystem-based skill installation and fresh-thread discovery evidence, but it did not expose a separately verifiable first-class skill installation UI/CLI command to this agent. The status is therefore `PASS_WITH_MANUAL_INSTALL`, not unconditional `PASS`.
