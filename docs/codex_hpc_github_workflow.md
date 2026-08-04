# Codex-Mediated HPC-to-GitHub Archive Workflow

This document describes the preferred workflow for using Codex as the controlled bridge between HPC analysis outputs and the GitHub archive.

## Principle

```text
HPC performs computation and stores raw or bulky outputs.
Codex retrieves selected small files into a local audit workspace.
GitHub stores reproducible code, small manifests, logs, and documentation.
```

This avoids placing GitHub write credentials on HPC and gives every transferred file an audit trail before publication.

## Transfer Policy

Commit to GitHub:

- Small TSV/CSV/TXT result tables.
- Reusable R, Python, or shell scripts.
- Sanitized logs.
- File inventories and SHA256 checksums.
- Documentation explaining analysis decisions.

Do not commit directly:

- Raw reads.
- Large Trinity assemblies.
- Large FASTA or database files unless explicitly reviewed.
- Private SSH configuration.
- Tokens, private keys, passwords, or personal-only absolute paths.

## Standard Recovery Steps

1. Identify target files in `results_manifest/hpc_core_files.tsv`.
2. Check file existence and size on HPC.
3. Download only reviewed small files into the matching local archive directory.
4. Scan downloaded files for private paths or credentials.
5. Generate SHA256 checksums and line counts.
6. Update manifests and workflow notes.
7. Commit locally with a narrow file list.
8. Publish to GitHub through the Codex GitHub connector.

## Current First Batch

The first Codex-mediated recovery batch focused on the 36-HQ CYP analysis layer.

Recovered file groups:

```text
results_manifest/36HQ/
docs/audit/
scripts/R/
logs/hpc_recovery/
```

Audit file:

```text
logs/hpc_recovery/hpc_recovered_files_sha256.tsv
```

## Future Automation Template

Future RNA-seq automation should preserve the same separation:

```text
1. HPC run directory
2. Codex recovery manifest
3. Local audit staging
4. GitHub archive publication
```

Each automation batch should produce:

- A manifest of files considered.
- A manifest of files recovered.
- SHA256 checksums.
- A sensitive-content scan result.
- A short recovery log.
- A GitHub publication record.
