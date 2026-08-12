# Environment Report

Status: PASS WITH WARNINGS

Bounded local smoke test run on 2026-08-12. No software was installed automatically, no global Mathematica initialization files were changed, no user-wide environment variables were modified, and no heavy symbolic calculations were performed.

| tool | status | version | command | notes |
| --- | --- | --- | --- | --- |
| Operating system | PASS | Microsoft Windows 11 家庭版 中文版 10.0.26200, build 26200, 64-bit | `Get-CimInstance Win32_OperatingSystem \| Select-Object Caption,Version,BuildNumber,OSArchitecture` | Raw logs: `benchmarks/B00_environment/outputs/os.stdout.log`, `os.stderr.log`. |
| Python | PASS | Python 3.10.9, executable `D:\miniconda3\python.exe` | `python -c "import sys,platform; print(sys.executable); print(sys.version); print(platform.platform())"` | Raw logs: `python_version.stdout.log`, `python_version.stderr.log`. |
| WolframScript executable | PASS | WolframScript 1.14.0 for Microsoft Windows (64-bit) | `Get-Command wolframscript`; `wolframscript -version` | Executable: `C:\Program Files\Wolfram Research\WolframScript\wolframscript.exe`. |
| Mathematica / Wolfram Engine fresh process | PASS | 15.0.1 for Microsoft Windows (64-bit), July 2, 2026 | `wolframscript -file benchmarks\B00_environment\smoke_test.wl` | Fresh process completed with exit code 0. Raw logs: `wolframscript_file_smoke.stdout.log`, `wolframscript_file_smoke.stderr.log`. |
| FeynCalc | PASS | 10.1.0 | `wolframscript -file benchmarks\B00_environment\smoke_test.wl` | Loaded from a fresh Wolfram process. Harmless smoke expression `FCI[SP[p, p]]` returned `Pair[Momentum[p], Momentum[p]]`. Symbolic backend available. |
| FeynArts | PASS WITH WARNINGS | unknown | `wolframscript -file benchmarks\B00_environment\smoke_test.wl` | The FeynArts context exposed FeynArts symbols and the smoke check returned `20`; no version symbol was detected by the bounded script. |
| pdflatex | PASS | MiKTeX-pdfTeX 4.23 (MiKTeX 25.12) | `Get-Command pdflatex`; `pdflatex --version` | Executable: `D:\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`. |
| lualatex | PASS WITH WARNINGS | LuaHBTeX 1.24.0 (MiKTeX 25.12) | `Get-Command lualatex`; `lualatex --version` | Executable: `D:\Programs\MiKTeX\miktex\bin\x64\lualatex.exe`. MiKTeX emitted a warning that updates have not been checked. |
| TikZ-Feynman render backend | PASS WITH WARNINGS | TikZ-Feynman package found by LaTeX | `lualatex -interaction=nonstopmode -halt-on-error -output-directory benchmarks\B00_environment\outputs\tikz_compile benchmarks\B00_environment\tikz_smoke_test.tex` | Minimal two-vertex diagram compiled successfully. PDF: `benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.pdf`. Stderr contains the MiKTeX update warning. |
| FeynGrav manual observation | PASS, MANUAL | FeynGrav 3.0; FeynCalc 10.1.0 | User-supplied notebook check: `<< FeynGrav`` | Screenshot indicates FeynGrav starts normally in a notebook. This was recorded as manual evidence, separate from the fresh `wolframscript -file` smoke requirement. |

## Commands Executed

Raw command manifest: `benchmarks/B00_environment/outputs/commands_executed.txt`.

```text
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture
python -c "import sys,platform; print(sys.executable); print(sys.version); print(platform.platform())"
Get-Command wolframscript
wolframscript -version
wolframscript -file benchmarks\B00_environment\smoke_test.wl
Get-Command pdflatex
pdflatex --version
Get-Command lualatex
lualatex --version
lualatex -interaction=nonstopmode -halt-on-error -output-directory benchmarks\B00_environment\outputs\tikz_compile benchmarks\B00_environment\tikz_smoke_test.tex
```

## Raw Logs

- `benchmarks/B00_environment/outputs/os.stdout.log`
- `benchmarks/B00_environment/outputs/os.stderr.log`
- `benchmarks/B00_environment/outputs/python_version.stdout.log`
- `benchmarks/B00_environment/outputs/python_version.stderr.log`
- `benchmarks/B00_environment/outputs/wolframscript_command.stdout.log`
- `benchmarks/B00_environment/outputs/wolframscript_command.stderr.log`
- `benchmarks/B00_environment/outputs/wolframscript_version.stdout.log`
- `benchmarks/B00_environment/outputs/wolframscript_version.stderr.log`
- `benchmarks/B00_environment/outputs/wolframscript_file_smoke.stdout.log`
- `benchmarks/B00_environment/outputs/wolframscript_file_smoke.stderr.log`
- `benchmarks/B00_environment/outputs/pdflatex_command.stdout.log`
- `benchmarks/B00_environment/outputs/pdflatex_command.stderr.log`
- `benchmarks/B00_environment/outputs/pdflatex_version.stdout.log`
- `benchmarks/B00_environment/outputs/pdflatex_version.stderr.log`
- `benchmarks/B00_environment/outputs/lualatex_command.stdout.log`
- `benchmarks/B00_environment/outputs/lualatex_command.stderr.log`
- `benchmarks/B00_environment/outputs/lualatex_version.stdout.log`
- `benchmarks/B00_environment/outputs/lualatex_version.stderr.log`
- `benchmarks/B00_environment/outputs/tikz_compile.stdout.log`
- `benchmarks/B00_environment/outputs/tikz_compile.stderr.log`
- `benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.log`
- `benchmarks/B00_environment/outputs/tikz_compile/tikz_smoke_test.pdf`

## Blockers

None.

## Warnings

- FeynArts loaded in the fresh Wolfram process, but the bounded smoke script did not detect a version symbol.
- MiKTeX emitted: `lualatex: major issue: So far, you have not checked for MiKTeX updates.` This did not prevent PDF generation.

