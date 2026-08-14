# External Archive Policy

This project keeps GitHub focused on code, small result tables, manifests, and human-readable provenance. Large raw data and bulky intermediate outputs should be stored outside Git and referenced from manifest files.

## Preferred Storage Targets

Use the most durable available location for each asset:

- Public sequencing archives such as NCBI SRA for raw RNA-seq reads.
- Zenodo, Figshare, institutional repositories, or GitHub Releases for release-ready supplemental assets.
- Managed HPC or object storage for reproducible but bulky intermediate files.

## Required Metadata

Every external asset should eventually have:

- Stable URI, accession, DOI, or storage path safe to publish.
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

For the first GitHub archive release, attach only if needed:

- Final rendered manuscript figures as release assets.
- RT-qPCR final primer table if finalized and small.
- A compressed external data manifest containing checksums and public accessions, not raw private data.

Do not move raw sequencing data or bulky HPC intermediates into Git.
