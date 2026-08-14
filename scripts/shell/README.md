# Shell and HPC Scripts

Use this directory for public, path-parameterized shell scripts and HPC command wrappers.

Before committing, remove or generalize:

- Private usernames.
- Internal-only hostnames if the repository will be public.
- Credentials, tokens, and private paths.

## RNA-seq Upstream Processing

- `run_fastp_paired_samples.sh`
- `run_trinity_denovo_assembly.sh`
- `run_salmon_quant_samples.sh`
- `run_interproscan_core.sh`
- `collect_hpc_tool_versions.sh`
- `collect_external_asset_checksums.sh`

These scripts are sanitized public wrappers reconstructed from the local/HPC recovery material. They use command-line arguments and `config/rnaseq_samples.tsv` rather than hard-coded HPC paths.

Typical order:

```text
fastp paired-end trimming
-> Trinity de novo transcriptome assembly
-> Salmon quantification
-> tximport / DESeq2
-> InterProScan / PFAM annotation for functional/CYP evidence
```

## Final Archive Confirmation

- `collect_hpc_tool_versions.sh`: run on HPC to collect version strings for tools still marked pending in `environment/version_confirmation_checklist.tsv`.
- `collect_external_asset_checksums.sh`: run on HPC or external storage staging area to collect size/checksum information for assets tracked in `results_manifest/external_assets_manifest.tsv`.

See `docs/hpc_confirmation_runbook.md` for the recommended confirmation workflow.
