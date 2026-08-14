# Data

This directory intentionally tracks documentation only.

Do not commit large raw data or bulky intermediates to GitHub. At this stage,
experimental data are private and should remain in local/HPC storage.

Recommended records:

- Sanitized asset IDs.
- File names or directory roles when safe.
- Byte sizes and checksums when useful for local integrity checks.
- Placeholder paths such as `<HPC_PROJECT_ROOT>`, not real private paths.

Files commonly kept outside Git:

- `*.fastq`, `*.fq`, and compressed read files.
- Large `*.fasta`, `*.fa`, and transcriptome assemblies.
- `*.bam`, `*.sam`, and alignment intermediates.
- BLAST, DIAMOND, HMMER, and other large database files.

For the current external-asset policy and tracking table, see:

- `docs/external_archive_policy.md`
- `results_manifest/external_assets_manifest.tsv`
