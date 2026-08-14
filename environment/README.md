# Environment

Record software environments needed to reproduce the CYP family study.

Recommended files:

- `environment.yml`: Conda environment definition.
- `renv.lock` or `sessionInfo.txt`: R package record.
- `containers.md`: Singularity/Apptainer/Docker image references.
- `software_versions.tsv`: exact tool versions.
- `version_confirmation_checklist.tsv`: version confirmation status and commands to run later on HPC.

If the analysis was run on HPC, include module names and versions when available.

The first live HPC version-confirmation pass is summarized in
`logs/hpc_recovery/hpc_tool_versions_confirmed_20260814.tsv`.
