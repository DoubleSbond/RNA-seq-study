# GitHub Publish Plan

This note separates the local HPC recovery workspace from the public GitHub archive.

## Publish Now

These files are small, text-based, and suitable for GitHub after the current review:

- `README.md`
- `.gitignore`
- `.gitattributes`
- `docs/*.md`
- `docs/audit/*`
- `docs/notes/*`
- `scripts/R/*`
- `scripts/python/README.md`
- `scripts/shell/README.md`
- `config/README.md`
- `data/README.md`
- `environment/*`
- `results_manifest/**`
- `logs/hpc_recovery/*.tsv`
- `logs/hpc_recovery/README.md`

## Keep Local Only

These are retained as local recovery evidence and should not be committed directly:

- `collected_hpc/**`
- Raw sequencing reads.
- Transcriptome assemblies and large FASTA/FASTQ files.
- Alignment files, indexes, databases, and bulky intermediate outputs.
- Archive files such as `*.tar.gz` and `*.zip`.

## Sanitize First

Before publishing any recovered provenance copied directly from HPC, check for:

- User names and internal absolute paths.
- Private server names or SSH connection details.
- Tokens, passwords, private keys, and credential files.
- Temporary working directories that should be replaced by placeholders.

The current public DESeq2 script is `scripts/R/gene_level_deseq2_final.R`. It was reconstructed from the recovered final run script, but uses command-line arguments instead of hard-coded HPC paths.

## Current Caution

The 91-CYP to 36-HQ transition is currently best described as a reviewed and audited quality-curation layer. It is supported by review tables, gene ID lists, checksums, restored archives, and downstream scripts, but a single fully automated end-to-end filtering script has not yet been identified.
