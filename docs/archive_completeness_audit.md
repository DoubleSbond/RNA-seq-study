# Archive Completeness Audit

This audit records the GitHub archive state after the recovered local/HPC material was organized.

## README Coverage

Public-facing top-level directories have README files:

- `config/`
- `data/`
- `docs/`
- `environment/`
- `logs/`
- `results_manifest/`
- `scripts/`

Important subdirectories with dedicated README files:

- `docs/audit/`
- `docs/notes/`
- `logs/hpc_recovery/`
- `logs/unknownCYP/`
- `results_manifest/36HQ/`
- `results_manifest/91CYP/`
- `results_manifest/annotation/`
- `results_manifest/Bmori_comparison/`
- `results_manifest/CYP_screening/`
- `results_manifest/DESeq2/`
- `results_manifest/RNAseq/`
- `results_manifest/RTqPCR/`
- `results_manifest/unknownCYP/`
- `scripts/python/`
- `scripts/R/`
- `scripts/shell/`

`collected_hpc/` and `sources/` are local reference areas, not public archive targets. The project-level instructions treat `sources/` as read-only synced context.

## Archived Reproducibility Layers

The current archive contains:

- RNA-seq sample metadata, public processing wrappers, assembly QC, and Salmon summary tables.
- Gene-level DESeq2 public script, calibration/session information, and significant result table.
- Annotation summary counts and public InterProScan summarization utility.
- 91-CYP candidate discovery tables, gene IDs, best-hit tables, PC1 loading tables, TPM tables, and a public CYP/P450 evidence-filtering reconstruction utility.
- CYP screening QC tables connecting peptide/transcript/gene IDs, representative longest isoforms, length filters, fragment/noncanonical flags, and seed-gene audit lists.
- 36-HQ review tables, ID audit note, module/PCA tables, Dan internal-variation tables, and downstream R scripts.
- B. mori public midgut CYP TPM tables, Figure1 inputs, and figure ordering script.
- RT-qPCR target mapping, sequence-length index, and B. mori target QC / Primer3 summary tables.
- unknownCYP review, peptide-availability, phylogeny inclusion, diagnostic tree, IQ-TREE report, and supporting scripts.
- Public checksums for archived small files in `logs/hpc_recovery/public_archive_sha256.tsv`.

## Deliberately Outside Git

These are intentionally not committed:

- Raw FASTQ files.
- Full Trinity assemblies and large FASTA files.
- Salmon `quant.sf` directories and large quantification intermediates.
- Full BLAST, HMMER, InterProScan, and database outputs.
- Rendered figure files where source tables/scripts are already archived, unless a release policy later requires them.
- Primer-design FASTA files and large sequence sources.
- Alignment source FASTA files for phylogeny when large or better kept in private local/HPC storage.
- Compressed archives such as `.tar.gz` and `.zip`.
- Credentials, tokens, SSH keys, private config, and internal-only paths.

## Remaining Gaps

The remaining gaps are narrow and should not block narrative reconstruction:

- Exact original one-command script or shell history that generated `CYP_candidates_step1.tsv` and `CYP_candidates_step2_confirmed.tsv`, if it still exists on HPC.
- Exact fastp and Trinity version strings; public wrappers and QC summaries are archived, but the original versions remain marked as pending in `environment/version_confirmation_checklist.tsv`.
- Final rendered figure files and large figure/alignment/source FASTA assets should follow `docs/external_archive_policy.md` and be tracked in `results_manifest/external_assets_manifest.tsv`.
- Final RT-qPCR primer sequences should be added if they become part of the formal project release.

## Omission Check Result

The local comparison found two classes of apparent omissions:

- Files already represented under public names after sanitization or parameterization, such as final DESeq2, B. mori TPM generation, unknownCYP tree-label scripts, and 36-HQ variation scripts.
- Additional small QC tables that were useful for reproducibility and are now archived under `results_manifest/CYP_screening/` and `results_manifest/annotation/`.

No credentials, private keys, GitHub tokens, or raw sequencing data should be present in the public archive.
