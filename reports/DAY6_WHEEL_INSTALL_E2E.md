# Day 6 Wheel Install E2E Release Candidate

Status: PASS

PASS criteria: the B02 Compton workflow succeeds from a non-editable wheel install in a fresh venv, without `PYTHONPATH=src` and without inherited project packages.

## Summary

- Built sdist: `runs/day6_wheel_e2e/dist/feynagent-0.1.0.tar.gz` (69,630 bytes)
- Built wheel: `runs/day6_wheel_e2e/dist/feynagent-0.1.0-py3-none-any.whl` (59,055 bytes)
- Fresh venv: `runs/day6_wheel_e2e/venv`
- Fresh workspace: `runs/day6_wheel_e2e/fresh_workspace`
- Wheel-installed package path: `runs/day6_wheel_e2e/venv/lib/site-packages/feynagent/__init__.py`
- `PYTHONPATH`: `None`
- Editable install used: no
- Venv inherited system site packages: no (`include-system-site-packages = false`)
- High-level B02 run: PASS
- Run directory: `runs/day6_wheel_e2e/fresh_workspace/runs/20260815_114653_b02_compton_7dff0c3c`

## A. Dependency Audit

Runtime imports enumerated from `src/feynagent/**/*.py`:

```text
src/feynagent/__init__.py: none
src/feynagent/__main__.py: __future__
src/feynagent/amplitudes/__init__.py: none
src/feynagent/amplitudes/backends.py: __future__, dataclasses, pathlib, typing, yaml
src/feynagent/amplitudes/builder.py: __future__, hashlib, json, re, typing
src/feynagent/backends/__init__.py: none
src/feynagent/backends/feynarts_feyncalc.py: __future__, dataclasses, datetime, hashlib, json, pathlib, subprocess, typing
src/feynagent/diagrams/__init__.py: none
src/feynagent/diagrams/topology.py: __future__, itertools, typing
src/feynagent/init.py: __future__, argparse, dataclasses, datetime, hashlib, json, pathlib, shutil, subprocess, sys, tempfile, typing, yaml
src/feynagent/render/__init__.py: none
src/feynagent/render/tikz.py: __future__, datetime, hashlib, json, pathlib, subprocess, typing
src/feynagent/runner.py: __future__, argparse, dataclasses, datetime, hashlib, importlib.resources, json, jsonschema, pathlib, shutil, subprocess, sys, typing, uuid, yaml
```

Direct non-stdlib runtime dependencies:

```text
PyYAML>=6
jsonschema>=4
```

Dependencies previously supplied accidentally by the development environment:

```text
PyYAML
jsonschema
```

Packaging correction:

- `pyproject.toml` now declares `dependencies = ["jsonschema>=4", "PyYAML>=6"]`.
- Runtime JSON schemas are packaged under `feynagent/schemas/*.json` and included via `tool.setuptools.package-data`.
- The runner now loads schemas from the source tree when present, otherwise from packaged resources. This is required for wheel-installed operation in a fresh workspace with no repo `schemas/` directory.

Fresh wheel metadata confirmed:

```text
Requires-Dist: jsonschema>=4
Requires-Dist: PyYAML>=6
```

Fresh venv installed packages:

```text
attrs                     26.1.0
feynagent                 0.1.0
jsonschema                4.26.0
jsonschema-specifications 2025.9.1
pip                       22.3.1
PyYAML                    6.0.3
referencing               0.37.0
rpds-py                   0.30.0
setuptools                65.5.0
typing_extensions         4.16.0
```

## B. Build

First build attempt:

```powershell
python -m build --sdist --wheel --outdir runs\day6_wheel_e2e\dist
```

Runtime: 0.32 s

Result: FAIL, because the base Python environment did not have the standard `build` frontend installed.

```text
D:\miniconda3\python.exe: No module named build
```

Recovery command:

```powershell
python -m pip install build
```

Runtime: 10.04 s

Result: PASS. Installed `build-1.5.0`, `packaging-26.3`, `pyproject_hooks-1.2.0`.

Release build command:

```powershell
python -m build --sdist --wheel --outdir runs\day6_wheel_e2e\dist
```

Runtime: 11.31 s

Result: PASS.

Built artifacts:

```text
feynagent-0.1.0.tar.gz            69630 bytes
feynagent-0.1.0-py3-none-any.whl  59055 bytes
```

The build log confirmed packaged schemas were included in both sdist and wheel.

## C. Fresh Environment

Create venv:

```powershell
python -m venv runs\day6_wheel_e2e\venv
```

Runtime: 5.16 s

Result: PASS.

Venv isolation:

```text
home = D:\miniconda3
include-system-site-packages = false
version = 3.10.9
```

Install wheel normally:

```powershell
runs\day6_wheel_e2e\venv\Scripts\python.exe -m pip install runs\day6_wheel_e2e\dist\feynagent-0.1.0-py3-none-any.whl
```

Runtime: 19.71 s

Result: PASS.

Installed location:

```text
e:\003hep-ph-research\agent\feynagent\runs\day6_wheel_e2e\venv\lib\site-packages
```

Import verification:

```powershell
runs\day6_wheel_e2e\venv\Scripts\python.exe -c "import feynagent, feynagent.runner, sys, os; print(feynagent.__file__); print('PYTHONPATH='+str(os.environ.get('PYTHONPATH'))); print(sys.prefix)"
```

Runtime: 0.51 s

Output:

```text
E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\venv\lib\site-packages\feynagent\__init__.py
PYTHONPATH=None
E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\venv
```

Packaged schema verification:

```text
E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\venv\lib\site-packages\feynagent\schemas\physics_card.schema.json
```

## D. Fresh Workspace E2E

Fresh workspace:

```text
E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\fresh_workspace
```

Copied immutable inputs:

```text
inputs/physics_card.yaml
inputs/backend_profile.yaml
inputs/execution_request.yaml
```

The execution request authorized only bounded `benchmark_regression`, with fixed 180 s timeout and explicit operations including `m2_regression`, `spin_sums`, `polarization_sums`, and `heavy_simplification`. It did not authorize production-heavy work.

### Skill install/enable

Day-6 tested method:

```powershell
Copy-Item -Path skills\feynagent\* -Destination C:\Users\lenovo\.codex\skills\feynagent -Recurse -Force
```

Runtime: 0.39 s

Result: PASS.

Installed skill validation:

```powershell
python C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\lenovo\.codex\skills\feynagent
```

Runtime: 0.35 s

Result:

```text
Skill is valid!
```

### Initialize

Command run from the fresh workspace:

```powershell
..\venv\Scripts\python.exe -m feynagent init --timeout 60
```

Runtime: 6.13 s

Result: PASS.

```text
FeynAgent init: PASS
- wolfram: PASS
- feyncalc: PASS
- feynarts: PASS
- native_qed_tree_capability: PASS
- latex: PASS
wrote .feynagent\environment.yaml
wrote .feynagent\capability_report.json
wrote .feynagent\reference_index.json
```

### Doctor

Command:

```powershell
..\venv\Scripts\python.exe -m feynagent doctor --timeout 60
```

Runtime: 6.07 s

Result: PASS.

```text
FeynAgent doctor: PASS
PASS    wolfram
PASS    feyncalc
PASS    feynarts
PASS    native_qed_tree_capability
PASS    latex
```

### High-level B02 runner

Command:

```powershell
..\venv\Scripts\python.exe -m feynagent run --physics-card inputs\physics_card.yaml --backend-profile inputs\backend_profile.yaml --execution-request inputs\execution_request.yaml --run-root runs
```

Runtime: 20.97 s

Result: PASS.

```text
FeynAgent run: PASS
run_id: 20260815_114653_b02_compton_7dff0c3c
run_dir: E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\fresh_workspace\runs\20260815_114653_b02_compton_7dff0c3c
manifest: E:\003hep-ph-research\Agent\FeynAgent\runs\day6_wheel_e2e\fresh_workspace\runs\20260815_114653_b02_compton_7dff0c3c\run_manifest.json
```

### Artifact verification

Run manifest:

```text
status: PASS
validation_report.json: PASS
```

Required PDF artifacts:

```text
diagrams.pdf     exists, 20552 bytes
amplitudes.pdf   exists, 76195 bytes
```

Per-channel amplitudes from `amplitudes.json`:

```text
native:diagram:1  s  p1+k1  feyncalc_amplitudes.m
native:diagram:2  u  p1-k2  feyncalc_amplitudes.m
```

FeynCalc/native artifacts:

```text
feyncalc_amplitudes.m   exists
native_amplitude.wl     exists
compute_m2.wl           exists
m2_raw.m                exists
m2_simplified.m         exists
m2_inputform.txt        exists
```

Bounded benchmark M2:

```text
status: PASS
authorization path: benchmark_regression
script runtime: 0.5798946 s
FeynCalc comparison status: True
equivalence: True
```

Official B02 result comparison:

```text
m2_inputform.txt = (-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
```

This matches the requested official massless B02 result:

```text
-2 e^4 (s^2 + u^2)/(s u)
```

Output tree:

```text
amplitudes.aux 32
amplitudes.json 1741
amplitudes.log 9843
amplitudes.pdf 76195
amplitudes.tex 2524
compute_m2.wl 5975
diagram_source.inputform.txt 1723
diagram_source.m 1869
diagram_source.paint.inputform.txt 995
diagrams.pdf 20552
feyncalc_amplitude.inputform.txt 902
feyncalc_amplitude.m 981
feyncalc_amplitudes.m 2270
inputs\backend_profile.yaml 1506
inputs\execution_request.yaml 783
inputs\physics_card.yaml 2066
m2_inputform.txt 33
m2_manifest.json 3045
m2_raw.inputform.txt 1533
m2_raw.m 1735
m2_simplified.inputform.txt 33
m2_simplified.m 35
m2_stderr.log 0
m2_stdout.log 656
native_amplitude.wl 8842
native_summary.json 1053
raw_feynarts_amplitude.inputform.txt 2600
raw_feynarts_amplitude.m 2887
raw_feynarts_amplitudes.m 2154
run_manifest.json 17391
stderr.log 138
stdout.log 7206
validation_report.json 607
```

## E. Final Verification

Focused runner/backend tests after packaging changes:

```powershell
python -m pytest tests\test_runner_cli.py tests\test_feynarts_feyncalc_backend.py
```

Result: 23 passed in 0.84 s.

Full test suite:

```powershell
python -m pytest
```

Runtime: 10.96 s

Result: 89 passed.

Schema/example validation:

```powershell
python scripts\validate_examples.py
```

Runtime: 0.90 s

Result: PASS for all schemas/profiles/benchmark fixtures.

Whitespace check:

```powershell
git diff --check
```

Result: PASS, no output.

## Failures / Recoveries

1. Initial `python -m build` failed because `build` was not installed in the base development Python. Recovered by installing `build` and rerunning the sdist/wheel build successfully.
2. No E2E runtime failure occurred after wheel installation.
3. No `PYTHONPATH=src` was used.
4. No editable install was used for the release-candidate E2E.

## Decision

PASS.

The release-candidate workflow succeeds from a normal wheel install in an isolated venv and a fresh workspace, with accurate minimal runtime dependencies and packaged schema resources.
