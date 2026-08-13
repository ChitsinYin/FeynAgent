# Day 5 Skill End-To-End Test

Generated at: 2026-08-13T17:40:31.149421+08:00

## Executive Status

PASS

PASS is allowed only if Test A and Test B select the correct backend mode.

## Isolation

- Temporary workspace: `C:\Users\lenovo\AppData\Local\Temp\feynagent_skill_e2e_20260813_173952`
- Development `.feynagent/` copied into temp: `False`
- Temp `.feynagent/` existed before init: `False`
- Project installed from temp source with `python -m pip install -e . --no-deps`.
- Temp workspace cleaned after this report was copied back.

## Initialization

- `python -m feynagent init --timeout 60`: return code `0`
- `ensure_initialized`: `{'action': 'ready', 'missing_cli_options': [], 'missing_files': [], 'ready': True, 'status': 'PASS'}`
- Local files generated in temp:
  - `.feynagent/environment.yaml`
  - `.feynagent/capability_report.json`
  - `.feynagent/reference_index.json`
- Reference index entry count: `200`
- Reference index external package paths: `True`

## Test A: Standard QED Compton

- Classification: `standard_native`
- Official example discovered: `QED/Tree/Markdown/ElGa-ElGa.md`
- Official example hash: `7bb2b42ccde456340a32fb436016360861779e5a89583beb95c72347d089edc4`
- Native diagram count: `2`
- Native amplitude generation return code: `0`
- Benchmark M2 comparison: `PASS`

## Test B: Toy Custom Yukawa

- Classification: `custom_audited`
- SM/QED native model used as physics authority: `False`
- Custom rule provenance requested/recorded: `True`
- Heavy M2 required: `False`

## Generated Artifacts

```text
.feynagent\capability_report.json
.feynagent\environment.yaml
.feynagent\reference_index.json
runs\skill_e2e_20260813_173952\test_a_compton_native_amplitude\native_amplitude.wl
runs\skill_e2e_20260813_173952\test_a_compton_native_amplitude\raw_feynarts_amplitude.m
runs\skill_e2e_20260813_173952\test_a_compton_native_amplitude\feyncalc_amplitude.m
runs\skill_e2e_20260813_173952\test_a_compton_native_amplitude\run_manifest.json
runs\skill_e2e_20260813_173952\test_a_compton_m2_official\stdout.log
runs\skill_e2e_20260813_173952\test_a_compton_m2_official\stderr.log
runs\skill_e2e_20260813_173952\test_a_compton_m2_official\comparison_result.json
runs\skill_e2e_20260813_173952\test_a_compton_m2_official\DONE
runs\skill_e2e_20260813_173952\test_b_toy_yukawa_custom\custom_audit_request.json
```

## Commands

```json
[
  {
    "name": "pip_install_editable",
    "args": [
      "D:\\miniconda3\\python.exe",
      "-m",
      "pip",
      "install",
      "-e",
      ".",
      "--no-deps"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 19.632,
    "stdout_tail": "ing file:///C:/Users/lenovo/AppData/Local/Temp/feynagent_skill_e2e_20260813_173952\n  Installing build dependencies: started\n  Installing build dependencies: finished with status 'done'\n  Checking if build backend supports build_editable: started\n  Checking if build backend supports build_editable: finished with status 'done'\n  Getting requirements to build editable: started\n  Getting requirements to build editable: finished with status 'done'\n  Preparing editable metadata (pyproject.toml): started\n  Preparing editable metadata (pyproject.toml): finished with status 'done'\nBuilding wheels for collected packages: feynagent\n  Building editable for feynagent (pyproject.toml): started\n  Building editable for feynagent (pyproject.toml): finished with status 'done'\n  Created wheel for feynagent: filename=feynagent-0.1.0-0.editable-py3-none-any.whl size=2333 sha256=4708117e167f78c50863c2997398c8362bcbbed78353414656074009bc83ba91\n  Stored in directory: C:\\Users\\lenovo\\AppData\\Local\\Temp\\pip-ephem-wheel-cache-06unes4h\\wheels\\6d\\2f\\15\\ab973a217fb0e0f003cd566b42240ef8e78f7b436512e6e8b0\nSuccessfully built feynagent\nInstalling collected packages: feynagent\nSuccessfully installed feynagent-0.1.0\n",
    "stderr_tail": "\n[notice] A new release of pip is available: 24.3.1 -> 26.2.1\n[notice] To update, run: python.exe -m pip install --upgrade pip\n"
  },
  {
    "name": "feynagent_init",
    "args": [
      "D:\\miniconda3\\python.exe",
      "-m",
      "feynagent",
      "init",
      "--timeout",
      "60"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 6.351,
    "stdout_tail": "FeynAgent init: PASS\n- wolfram: PASS\n- feyncalc: PASS\n- feynarts: PASS\n- native_qed_tree_capability: PASS\n- latex: PASS\nwrote .feynagent\\environment.yaml\nwrote .feynagent\\capability_report.json\nwrote .feynagent\\reference_index.json\n",
    "stderr_tail": ""
  },
  {
    "name": "ensure_initialized",
    "args": [
      "D:\\miniconda3\\python.exe",
      "skills/feynagent/scripts/ensure_initialized.py"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 0.109,
    "stdout_tail": "{\n  \"action\": \"ready\",\n  \"missing_cli_options\": [],\n  \"missing_files\": [],\n  \"ready\": true,\n  \"status\": \"PASS\"\n}\n",
    "stderr_tail": ""
  },
  {
    "name": "test_a_classify",
    "args": [
      "D:\\miniconda3\\python.exe",
      "skills/feynagent/scripts/run_feynagent.py",
      "classify",
      "Generate e- gamma -> e- gamma Compton benchmark regression"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 0.08,
    "stdout_tail": "{\n  \"backend\": \"feynarts_feyncalc_native\",\n  \"classification\": \"standard_native\",\n  \"example_hint\": \"ElGa-ElGa\",\n  \"reason\": \"matched standard-sector cue: compton\"\n}\n",
    "stderr_tail": ""
  },
  {
    "name": "test_a_search_examples",
    "args": [
      "D:\\miniconda3\\python.exe",
      "skills/feynagent/scripts/run_feynagent.py",
      "search-examples",
      "ElGa-ElGa Compton"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 0.084,
    "stdout_tail": "[\n  {\n    \"bytes\": 4557,\n    \"path\": \"C:\\\\Users\\\\lenovo\\\\AppData\\\\Roaming\\\\Wolfram\\\\Applications\\\\FeynCalc\\\\Examples\\\\QED\\\\Tree\\\\Markdown\\\\ElGa-ElGa.md\",\n    \"relative_path\": \"QED/Tree/Markdown/ElGa-ElGa.md\",\n    \"score\": 2,\n    \"sha256\": \"7bb2b42ccde456340a32fb436016360861779e5a89583beb95c72347d089edc4\",\n    \"title\": \"---\"\n  },\n  {\n    \"bytes\": 2608,\n    \"path\": \"C:\\\\Users\\\\lenovo\\\\AppData\\\\Roaming\\\\Wolfram\\\\Applications\\\\FeynCalc\\\\Examples\\\\QED\\\\Tree\\\\Mathematica\\\\ElGa-ElGa.m\",\n    \"relative_path\": \"QED/Tree/Mathematica/ElGa-ElGa.m\",\n    \"score\": 2,\n    \"sha256\": \"5dfeb52e426df1d155af336ab775add2b8e94e039f5ed126ced7c689889affc2\",\n    \"title\": \"::Package::\"\n  }\n]\n",
    "stderr_tail": ""
  },
  {
    "name": "test_a_native_amplitude",
    "args": [
      "D:\\miniconda3\\python.exe",
      "run_test_a_native.py"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 5.769,
    "stdout_tail": "tude.m\": {\n      \"bytes\": 981,\n      \"sha256\": \"9de444ded225d569961cf76a11a603edaaa2baba69ca259faac886571a1addb8\"\n    },\n    \"native_amplitude.wl\": {\n      \"bytes\": 3291,\n      \"sha256\": \"8e35abfec8593f9fffda5e3c78309cfe7a8ad65289b9dbef27fcf35ac4a3f4c5\"\n    },\n    \"native_summary.json\": {\n      \"bytes\": 786,\n      \"sha256\": \"337522797fc9c97c8ad500d0aebecb7c18a5fe8c3bf676c840477f0a224e565a\"\n    },\n    \"raw_feynarts_amplitude.inputform.txt\": {\n      \"bytes\": 2600,\n      \"sha256\": \"399cb8bb8d368daad81d57d6205c06d17a8dbf2fd286caa2374366302d07c37a\"\n    },\n    \"raw_feynarts_amplitude.m\": {\n      \"bytes\": 2887,\n      \"sha256\": \"3202dea0aba8174c320071b42727e62299958050aea50bd082b44a54716dfb71\"\n    },\n    \"stderr.log\": {\n      \"bytes\": 0,\n      \"sha256\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"\n    },\n    \"stdout.log\": {\n      \"bytes\": 3876,\n      \"sha256\": \"88e2bb804e99147ad709649db03dd099cf938cbad0bb1da8f1817271c84b52f4\"\n    }\n  },\n  \"process_id\": \"process:b02_compton\",\n  \"script_path\": \"native_amplitude.wl\",\n  \"started_at\": \"2026-08-13T17:40:18.786965+08:00\",\n  \"stderr_path\": \"stderr.log\",\n  \"stdout_path\": \"stdout.log\",\n  \"summary_path\": \"native_summary.json\"\n}\n",
    "stderr_tail": ""
  },
  {
    "name": "test_a_m2_official_example",
    "args": [
      "wolframscript",
      "-script",
      "C:\\Users\\lenovo\\AppData\\Roaming\\Wolfram\\Applications\\FeynCalc\\Examples\\QED\\Tree\\Mathematica\\ElGa-ElGa.m"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952\\runs\\skill_e2e_20260813_173952\\test_a_compton_m2_official",
    "returncode": 0,
    "runtime_seconds": 6.54,
    "stdout_tail": "El Ga -> El Ga, QED, matrix element squared, tree\n\nFrontEndObject::notavail: A front end is not available; certain operations require a front end.\n\nFrontEndObject::notavail: A front end is not available; certain operations require a front end.\n\u001b[1m\tCompare to Peskin and Schroeder, An Introduction to QFT, Eq 5.87:\u001b[0m \u001b[1m \u001b[32mCORRECT.\u001b[0m \u001b[0;39m\n\tCPU Time used: 4.578 s.\n",
    "stderr_tail": ""
  },
  {
    "name": "test_b_classify",
    "args": [
      "D:\\miniconda3\\python.exe",
      "skills/feynagent/scripts/run_feynagent.py",
      "classify",
      "Toy custom Yukawa L = - y phibar psi phi rule with explicit metric and provenance note"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 0.09,
    "stdout_tail": "{\n  \"backend_preference\": \"custom FeynArts-compatible model/adapter; legacy fallback/reference only\",\n  \"classification\": \"custom_audited\",\n  \"reason\": \"custom interaction with rule-like details present\"\n}\n",
    "stderr_tail": ""
  },
  {
    "name": "skill_eval",
    "args": [
      "D:\\miniconda3\\python.exe",
      "skills/feynagent/scripts/run_feynagent.py",
      "eval",
      "--cases",
      "skills/feynagent/evals/smoke_cases.json"
    ],
    "cwd": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\feynagent_skill_e2e_20260813_173952",
    "returncode": 0,
    "runtime_seconds": 0.087,
    "stdout_tail": "ector cue: e- e+\"\n      },\n      \"expected\": \"standard_native\",\n      \"id\": \"b01_annihilation\",\n      \"passed\": true\n    },\n    {\n      \"actual\": {\n        \"backend_preference\": \"custom FeynArts-compatible model/adapter; legacy fallback/reference only\",\n        \"classification\": \"custom_audited\",\n        \"reason\": \"custom interaction with rule-like details present\"\n      },\n      \"expected\": \"custom_audited\",\n      \"id\": \"toy_custom_yukawa\",\n      \"passed\": true\n    },\n    {\n      \"actual\": {\n        \"action\": \"check .feynagent/environment.yaml or run python -m feynagent init\",\n        \"classification\": \"unsupported_requires_review\",\n        \"reason\": \"missing initialization\"\n      },\n      \"expected\": \"unsupported_requires_review\",\n      \"id\": \"missing_initialization\",\n      \"passed\": true\n    },\n    {\n      \"actual\": {\n        \"classification\": \"unsupported_requires_review\",\n        \"reason\": \"ambiguous or unsupported custom physics request\",\n        \"requires_review\": [\n          \"custom rules\",\n          \"conventions\",\n          \"provenance\"\n        ]\n      },\n      \"expected\": \"unsupported_requires_review\",\n      \"id\": \"ambiguous_custom_rule\",\n      \"passed\": true\n    }\n  ]\n}\n",
    "stderr_tail": ""
  }
]
```

## Failures And Retries

- Failures: `[]`
- Retries: `0`
- Codex/manual interventions during automated script: `0`
- Wall time seconds: `38.840`

## Cleanup

The temporary workspace was removed after copying this report back to the development repository.
