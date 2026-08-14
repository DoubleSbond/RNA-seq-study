# Private Data Asset Policy

This project keeps GitHub focused on methods: workflow architecture, scripts,
configuration patterns, small non-sensitive summaries, manifests, and
human-readable provenance. Experimental data are not public at this stage.
Large raw data and bulky intermediate outputs should remain in local/HPC
storage and be referenced only through sanitized inventory records.

## Current Storage Rule

For the current archive phase:

- Do not publish raw reads, assemblies, large FASTA/alignment files, or bulky
  intermediate outputs.
- Do not add public accessions, DOIs, or storage URIs unless the project owner
  explicitly approves data release later.
- Keep experimental data in local/HPC storage.
- GitHub may record sanitized asset IDs, file counts, byte sizes, checksums for
  selected files, and placeholder paths such as `<HPC_PROJECT_ROOT>`.

## Required Metadata

Every private data asset record should have, when available:

- Sanitized asset ID.
- Private/local storage class, without exposing a private absolute path.
- SHA256 or MD5 checksum.
- Byte size.
- Creation date or recovery date.
- Tool/version used to create it, when applicable.
- A pointer to the Git-tracked script or table that consumes or summarizes it.

The central tracking table is `results_manifest/external_assets_manifest.tsv`.

## Git vs External Boundary

Commit to Git:

- Scripts, wrapper commands, and configuration files.
- Sample sheets and non-sensitive metadata.
- Small TSV/TXT/CSV summaries.
- Checksums and manifests.
- Human-readable README/audit/provenance notes.

Keep outside Git:

- FASTQ files.
- Large FASTA assemblies and primer-design sequence sets.
- Large BLAST, HMMER, DIAMOND, InterProScan, and Salmon directories.
- Large alignments and raw phylogeny inputs.
- Rendered figure files unless they are small and intentionally part of a release.
- Compressed archives.
- Credentials, private keys, tokens, and internal-only absolute paths.

## Current Release Recommendation

For the first GitHub methods archive release:

- Do not attach experimental data files as GitHub Release assets.
- Do not attach raw reads, assemblies, alignments, primer-design FASTA, or bulky
  search outputs.
- Include only methods files, reusable scripts, sanitized logs, and small
  non-sensitive summaries.
- If a small final RT-qPCR primer table or figure is considered later, treat it
  as a separate owner decision before adding it.

Do not move raw sequencing data or bulky HPC intermediates into Git.
