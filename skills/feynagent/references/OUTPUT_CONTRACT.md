# Output Contract

Generated artifacts belong under `runs/<run_id>/`. Do not place new amplitudes, Wolfram logs, PDFs, or squared-amplitude outputs under `benchmarks/`.

Local machine state belongs under `.feynagent/`:

- `.feynagent/environment.yaml`
- `.feynagent/capability_report.json`
- `.feynagent/reference_index.json`

For native standard workflows, record:

- package versions;
- exact CreateTopologies/InsertFields calls;
- official example metadata and hashes when available;
- run manifest and output hashes;
- stdout/stderr logs.

For long Mathematica jobs, generate deterministic scripts and manifests, let the job run independently, and inspect completed artifacts. Never live-poll indefinitely.

Review bundles may include metadata and small logs but must not copy external FeynCalc/FeynArts documentation or package examples into the repository.
