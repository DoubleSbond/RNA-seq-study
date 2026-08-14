# Archive Status

This document summarizes what is currently archived in GitHub and what remains outside Git.

## Uploaded To GitHub `main`

### RNA-seq / DESeq2

- Sample metadata: `config/rnaseq_samples.tsv` and `config/sample_info.csv`
- Public upstream wrappers: `scripts/shell/run_fastp_paired_samples.sh`, `scripts/shell/run_trinity_denovo_assembly.sh`, `scripts/shell/run_salmon_quant_samples.sh`, and `scripts/shell/run_interproscan_core.sh`
- Assembly and Salmon summaries: `results_manifest/RNAseq/`
- Public gene-level DESeq2 script: `scripts/R/gene_level_deseq2_final.R`
- DESeq2 calibration and sanitized session information: `environment/`
- Significant result table: `results_manifest/DESeq2/`

### 91-CYP Layer

- Gene IDs, summary annotations, and TPM tables: `results_manifest/91CYP/`
- Stepwise candidate provenance tables: `results_manifest/91CYP/CYP_candidates_step1.tsv` and `results_manifest/91CYP/CYP_candidates_step2_confirmed.tsv`
- B. mori best-hit and PC1 loading support tables: `results_manifest/91CYP/`
- Public reconstruction utility: `scripts/python/filter_cyp_candidates_from_annotation.py`

### 36-HQ CYP Layer

- 36-gene high-quality CYP set: `results_manifest/36HQ/CYP_high_quality_36_geneids.txt`
- Review list and master summary: `results_manifest/36HQ/`
- Expression modules and PCA tables: `results_manifest/36HQ/`
- Module/PCA scripts: `scripts/R/`

### RT-qPCR Candidate Layer

- Candidate target tables and sequence-length index: `results_manifest/RTqPCR/`

### unknownCYP Layer

- 24-candidate recheck table and peptide availability status: `results_manifest/unknownCYP/`
- High-TPM vs phylogeny mapping: `results_manifest/unknownCYP/highTPM_unknownCYP_vs_phylogeny_current_mapping.tsv`
- Integrated interpretation table: `results_manifest/unknownCYP/unknownCYP_integrated_interpretation.with_group.domain_priority.tsv`
- Diagnostic tree output and IQ-TREE summary: `results_manifest/unknownCYP/` and `logs/unknownCYP/`
- Supporting scripts: `scripts/R/*unknownCYP*.R` and `scripts/python/clean_unknownCYP_peptideAvailable14_headers.py`

## Local-Only By Design

The following should not be committed directly:

- Raw FASTQ files.
- Full Trinity assemblies and large FASTA files.
- BLAST, HMMER, InterProScan, or Salmon bulky intermediate outputs.
- Large alignments and raw phylogeny FASTA inputs.
- Archive files such as `.tar.gz` and `.zip`.
- Internal HPC paths, credentials, tokens, or SSH material.

## Remaining Gaps

1. Exact original command sequence for generating the 91-CYP candidate tables. The restored tables and a public reconstruction utility are now archived.
2. A final decision on where to archive figure source files and large alignment inputs.
3. Final RT-qPCR primer sequences, if they become part of the formal archive.

## Navigation

- Workflow narrative: `docs/workflow.md`
- Data version map: `docs/data_versions.md`
- Evidence audit: `docs/collection_narrative_audit.md`
- Script map: `docs/script_provenance_index.md`
- Public checksums: `logs/hpc_recovery/public_archive_sha256.tsv`
