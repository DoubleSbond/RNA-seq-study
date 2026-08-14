# Script Provenance Index

This index maps the public scripts in `scripts/` to the project workflow blocks they support.

## RNA-seq Quantification and Differential Expression

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| Read trimming | `scripts/shell/run_fastp_paired_samples.sh` | `config/rnaseq_samples.tsv`; paired FASTQ files outside Git | Trimmed paired reads and fastp reports |
| Trinity assembly | `scripts/shell/run_trinity_denovo_assembly.sh` | `config/rnaseq_samples.tsv`; trimmed paired reads | Trinity transcriptome assembly outside Git |
| Salmon quantification | `scripts/shell/run_salmon_quant_samples.sh` | `config/rnaseq_samples.tsv`; Salmon index; paired FASTQ files | Per-sample Salmon `quant.sf` directories outside Git |
| Gene-level DESeq2 | `scripts/R/gene_level_deseq2_final.R` | Salmon `quant.sf` directories; `tx2gene.csv` | Gene-level DESeq2 result tables and diagnostic plots |

## Annotation

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| InterProScan core annotation | `scripts/shell/run_interproscan_core.sh` | InterProScan executable; peptide FASTA outside Git | InterProScan TSV annotation output outside Git |

## 91-CYP Candidate Discovery

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| CYP/P450 evidence filtering | `scripts/python/filter_cyp_candidates_from_annotation.py` | Gene-level annotation TSV with PFAM, InterPro, description, and GO fields | Broad CYP candidate TSV and optional gene ID list |

## 36-HQ CYP Analysis

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| Expression module classification | `scripts/R/classify_high_quality_CYP_modules_baseR.R` | `TPM_gene_CYP_final_withMeanSD.tsv` | `CYP_high_quality_expression_modules.tsv`; module summary |
| PCA coordinates and variance | `scripts/R/PCA_high_quality_CYP_logTPM_zscore_baseR.R` | `TPM_high_quality_CYP_for_PCA.tsv` | PCA coordinate and variance tables; PCA plot |
| PCA plotting | `scripts/R/plot_FigureA_PCA_highQuality_CYP_baseR.R` | PCA coordinate and variance tables | Figure A PCA PNG/PDF |
| Module table annotation | `scripts/R/merge_CYP_modules_with_annotation_baseR.R` | CYP module table; CYP final summary | Annotated CYP module table |
| Module figures | `scripts/R/plot_CYP_module_heatmap_baseR.R`; `scripts/R/plot_CYP_module_scatter_baseR.R`; `scripts/R/plot_FigureC_CYP_module_scatter_baseR.R` | Annotated CYP module table | Heatmap/scatter figure files outside Git |
| CYP6B-focused view | `scripts/R/plot_CYP6B_focused_slope_baseR.R` | Annotated CYP module table | CYP6B-focused slope plot outside Git |
| Dan internal variation | `scripts/R/investigate_Dan_internal_CYP_variation_baseR.R`; `scripts/R/make_Dan_internal_CYP_summary_tables_baseR.R` | Annotated CYP module table | Dan replicate-variation summary tables |
| PCA within-group dispersion | `scripts/R/quantify_CYP_PCA_within_group_dispersion_baseR.R` | PCA coordinate table | Pairwise and summary PCA distance tables |

## B. mori Comparison and Figure1

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| B. mori public CYP TPM table generation | `scripts/python/make_bmori_public_cyp_tpm_tables.py` | B. mori GFF; `sample_info.tsv`; public Salmon `quant.sf` directories outside Git | B. mori CYP transcript/gene TPM tables |
| Figure1 gene ordering | `scripts/R/make_fig1_gene_order_final.R` | `fig1_expression_input_full.tsv`; `fig1_block_map.tsv` | `fig1_gene_order_final.tsv` |

## Current Gaps

The following recovered scripts exist in local evidence but have not yet all been converted into public, parameterized scripts:

- Raw-read trimming and Trinity assembly shell scripts.
- InterProScan / PFAM annotation shell scripts.
- The exact original 91-CYP candidate-generation command that emitted the recovered tables.
- Rendered final figure files and large figure source artifacts.

Some recovered scripts contain internal absolute paths or comments with encoding damage. Those scripts should be published only after conversion to path-parameterized public versions.

## unknownCYP Recheck

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| FASTA header cleanup | `scripts/python/clean_unknownCYP_peptideAvailable14_headers.py` | Raw peptide FASTA for peptide-available unknownCYP candidates | Clean PhUNK FASTA headers and header mapping table |
| Expression ranking plot | `scripts/R/plot_unknownCYP_TPM_ranking_final.R` | unknownCYP final-round TPM ranking table | MaxMean TPM ranking plot |
| Dan/Mul scatter plot | `scripts/R/plot_unknownCYP_Dan_vs_Mul_scatter.R` | unknownCYP final-round TPM table | Dan vs Mul expression scatter plot |
| Tree label cleanup | `scripts/R/make_unknownCYP_clean_tip_labels.R` | Diagnostic tree labels | Clean labels for tree visualization |
| CYP6-focused tree handling | `scripts/R/prune_unknownCYP_CYP6_focus_tree.R`; `scripts/R/rename_unknownCYP_CYP6_focus_tree_tips.R` | Core diagnostic tree and keep-tip list | CYP6-focused tree and relabeled tips |
