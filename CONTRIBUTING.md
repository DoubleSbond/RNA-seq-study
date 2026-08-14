# Contributing and Archive Maintenance

This repository is a reproducible research archive for the RNA-seq and CYP family study. Contributions should keep the archive lightweight, public-safe, and easy to verify.

## Before Editing

- Work on a branch instead of committing directly to `main`.
- Keep `sources/` and `collected_hpc/` as local-only reference areas.
- Do not add credentials, tokens, SSH keys, private config, or internal-only absolute paths.
- Do not add raw FASTQ files, full assemblies, large FASTA files, search databases, bulky tool outputs, or compressed archives.

## What Belongs In Git

Commit small, public-safe files such as:

- Scripts and parameterized wrapper commands.
- README, workflow, audit, and provenance notes.
- Sample metadata that is safe to publish.
- Small TSV/CSV/TXT result summaries.
- Checksums and manifests.

Keep large or sensitive files outside Git and record them through:

- `docs/external_archive_policy.md`
- `results_manifest/external_assets_manifest.tsv`
- `data/README.md`

## After Changing Files

Run these commands from the repository root:

```bash
python scripts/python/update_public_checksums.py
python scripts/python/validate_archive.py
```

The checksum updater refreshes `logs/hpc_recovery/public_archive_sha256.tsv`. The validator checks required paths, checksum consistency, tracked large/raw-data patterns, and common sensitive text patterns.

## Pull Request Checklist

Before opening or merging a pull request:

- Confirm the changed files belong to the intended archive layer.
- Confirm new data tables are small and safe for GitHub.
- Update relevant README or provenance notes.
- Refresh `logs/hpc_recovery/public_archive_sha256.tsv`.
- Run `python scripts/python/validate_archive.py`.
- Confirm GitHub Actions archive validation passes, when available.

## Issue Tracking

Use GitHub issue templates to keep release work organized:

- Archive gap: missing scripts, tables, manifests, README coverage, or provenance notes.
- External asset record: large/raw assets that stay outside Git but need public-safe storage metadata.
- HPC confirmation: tool versions, original commands, checksums, or source files that require HPC access.
- Release decision: license, citation metadata, final primer inclusion, rendered figures, or release-tag choices.

## HPC-Dependent Updates

Do not invent missing HPC details. If an update requires HPC access, record the gap clearly and use:

- `docs/hpc_confirmation_runbook.md`
- `environment/version_confirmation_checklist.tsv`
- `results_manifest/external_assets_manifest.tsv`

HPC-derived paths should be sanitized before publication unless they are intentionally public and safe to disclose.
