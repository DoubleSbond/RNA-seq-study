# HPC Recovery Inventory

This document lists the project files that should be recovered from HPC or local backups. Public documentation uses placeholders instead of personal usernames, private keys, or internal-only paths.

## Path Conventions

Use placeholders in public files:

```text
<HPC_PROJECT_ROOT>/ph
<LOCAL_RESEARCH_ROOT>/RNA-seq/CYP_study
```

Do not commit:

```text
Private key paths
Personal SSH config
Private usernames if the repository is public
Internal-only absolute paths unless explicitly approved
```

## Core HPC Directories

| Placeholder path | Purpose |
|---|---|
| `<HPC_PROJECT_ROOT>/ph/04_annotation/` | ORF, InterPro, KEGG, peptide chunks |
| `<HPC_PROJECT_ROOT>/ph/06_DEGsAnalysis/` | Salmon/tximport/DESeq2 and gene-level TPM |
| `<HPC_PROJECT_ROOT>/ph/07_homology/CYP-new/` | CYP discovery, 91-CYP and 36-HQ files |
| `<HPC_PROJECT_ROOT>/ph/10_RTqPCR_CYP_primer_prep/` | RT-qPCR candidate sequence preparation |
| `<HPC_PROJECT_ROOT>/ph/11_unknownCYP_annotation/` | unknownCYP review and phylogeny |

## Highest-Priority Files to Recover

| Priority | File name | Public archive target | Notes |
|---:|---|---|---|
| 1 | `CYP_high_quality_36_master_summary.tsv` | `results_manifest/` or external checksum | Core 36-HQ master table |
| 1 | `CYP_high_quality_36_ID_audit_note.txt` | `docs/` | Documents ID corrections and membership decisions |
| 1 | `TPM_high_quality_CYP_for_PCA.tsv` | `results_manifest/` if small | Input for 36-HQ PCA |
| 1 | `CYP_high_quality_expression_modules_annotated.tsv` | `results_manifest/` | Module and annotation summary |
| 1 | `PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv` | `results_manifest/` | PCA coordinates |
| 1 | `PCA_high_quality_CYP_logTPM_zscore_variance.tsv` | `results_manifest/` | PCA variance |
| 2 | `CYP_final_summary.tsv` | `results_manifest/` | Sequence-QC summary from broad CYP discovery |
| 2 | `CYP_final_geneids.txt` | `results_manifest/` | Broad CYP gene IDs |
| 2 | `TPM_gene_CYP_91.tsv` | `results_manifest/` if small | 91-CYP gene-level TPM table |
| 2 | `TPM_gene_CYP_91_withMean.tsv` | `results_manifest/` if small | 91-CYP TPM with means |
| 2 | `CYP_shared_Bmori_Phoenei_expression_comparison.pdf` | external or docs if small | Symbol-level matched comparison figure |
| 2 | matched comparison source tables | `results_manifest/` | Exact names still need recovery |
| 3 | `CYP_RTqPCR_candidates.batch1_4CYP.complete_CDS.gene_id_header.fa` | external or `results_manifest/` checksum | Primer candidate FASTA |
| 3 | `CYP_RTqPCR_candidates.combined_Batch1_plus_RankAD36CYP.cds.gene_id_header.fa` | external or `results_manifest/` checksum | Combined 14-CYP FASTA |
| 3 | `CYP_RTqPCR_candidates.combined_14CYP.sequence_quality_summary.tsv` | `results_manifest/` | Candidate quality summary |
| 3 | `unknownCYP_24_peptide_availability_final.tsv` | `results_manifest/` | all24 peptide availability table |
| 3 | `unknownCYP_raw24_phylogeny_inclusion_summary.tsv` | `results_manifest/` | unknownCYP phylogeny inclusion audit |
| 3 | `unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.treefile` | external or `results_manifest/` checksum | Diagnostic treefile |
| 3 | `unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.iqtree` | `logs/` or external | IQ-TREE result report |
| 3 | `unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.log` | `logs/` | IQ-TREE log |

## Recovery Strategy

1. Recover small TSV/TXT/R scripts first.
2. Generate checksums for every recovered file.
3. Commit only small tables and scripts that are safe for a public repository.
4. Keep FASTA, large figures, archives, and raw RNA-seq data outside Git unless explicitly approved.
5. Record external storage locations and checksums in `results_manifest/`.

## Example Sanitized Download Pattern

Use this only as a template; fill in private SSH details locally and do not commit them.

```powershell
scp -i "<PRIVATE_KEY_PATH>" "<HPC_USER>@<HPC_HOST>:<HPC_PROJECT_ROOT>/ph/07_homology/CYP-new/CYP_high_quality_36_master_summary.tsv" .
```
