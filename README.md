# CYP Family Study Archive

This repository organizes the reproducible code archive for the CYP family study after RNA-seq assembly and CYP gene family screening.

## Purpose

The archive is intended to preserve:

- Commands used during transcriptome assembly, CYP screening, annotation, filtering, and downstream summaries.
- Python and R scripts used for data processing, quality checks, and visualization.
- Configuration files and software environment records.
- Small result manifests and tabular summaries suitable for GitHub.
- Logs that document how analyses were run.

Large raw data and bulky intermediate outputs should not be committed directly. Store them in institutional storage, HPC project storage, object storage, Zenodo, Figshare, NCBI SRA, or another durable archive, and record access paths or accession identifiers in `data/README.md` and `results_manifest/`.

## Repository Layout

```text
.
|-- config/              # Parameters, sample sheets, and tool settings
|-- data/                # README only; raw data is tracked outside Git
|-- docs/                # Workflow notes, methods, and provenance records
|-- environment/         # Conda/R/session/container environment records
|-- logs/                # Curated run logs and command histories
|-- results_manifest/    # Small file inventories and result summaries
|-- scripts/             # Reusable Python, R, and shell scripts
|-- sources/             # Local read-only reference material, not committed by default
`-- README.md
```

## Quick Start

1. Place reusable analysis scripts in `scripts/`.
2. Put sample metadata, parameter files, and non-sensitive config in `config/`.
3. Record software versions in `environment/`.
4. Record command history and run provenance in `logs/`.
5. Add small summary tables and file manifests to `results_manifest/`.
6. Keep large FASTQ/FASTA/BAM/SAM, database, and assembled transcriptome files outside Git.

## Data Policy

Commit:

- Small text tables, manifests, metadata, and checksums.
- Final curated summaries needed to understand the analysis.
- Scripts, configs, and environment files.

Do not commit:

- Raw sequencing reads.
- Large transcriptome assemblies.
- Large BLAST/HMMER databases.
- Bulky intermediate outputs.
- Credentials, private keys, tokens, or internal-only HPC paths that should not be public.

## Current Status

- Local Git repository initialized.
- GitHub remote configured: `https://github.com/DoubleSbond/RNA-seq-study.git`.
- GitHub CLI was not detected in the current environment.
- GitHub Codex connector authorization completed for `DoubleSbond`.
- GitHub Codex Connector installed for `DoubleSbond/RNA-seq-study`.
- Archive skeleton published to GitHub through the connector.
- OpenSSH is available, and an active `ssh` process was detected locally.
- ChatGPT project mirror files are preserved locally and ignored by Git by default.

## Next Steps

Recover exact commands, scripts, sample metadata, and result manifests from local/HPC records, then place them in the matching directories.

If GitHub CLI is installed later, authenticate with:

```powershell
gh auth login
gh auth status
```
