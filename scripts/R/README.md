# R Scripts

This directory contains public, GitHub-safe R scripts reconstructed from the CYP family study.

## Gene-Level DESeq2

- `gene_level_deseq2_final.R`

Purpose:

```text
Salmon quant.sf files
-> tximport gene-level import
-> DESeq2 dandelion vs mulberry contrast
-> DEG tables and MA/volcano plots
```

Example:

```bash
Rscript scripts/R/gene_level_deseq2_final.R <quant_dir> <tx2gene.csv> <output_dir>
```

## 36-HQ CYP Expression Modules

- `classify_high_quality_CYP_modules_baseR.R`

Purpose:

```text
TPM table for the high-quality CYP set
-> Dan/Mul mean TPM, log2FC, CV, expression support
-> expression module and stability labels
```

Expected working-directory input:

```text
results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv
```

Example:

```bash
Rscript scripts/R/classify_high_quality_CYP_modules_baseR.R results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv results_manifest/36HQ
```

Outputs:

```text
CYP_high_quality_expression_modules.tsv
CYP_high_quality_expression_module_summary.tsv
```

## Annotation Summaries

- `interpro_annotation_summary.R`

Purpose:

```text
InterProScan TSV
-> gene-level PFAM, InterPro, description, and GO summary table
```

Example:

```bash
Rscript scripts/R/interpro_annotation_summary.R <interproscan.tsv> <annotation_summary.tsv>
```

## 36-HQ CYP PCA

- `PCA_high_quality_CYP_logTPM_zscore_baseR.R`
- `PCA_high_quality_CYP_logTPM_zscore.R`
- `plot_FigureA_PCA_highQuality_CYP_baseR.R`

Purpose:

```text
TPM_high_quality_CYP_for_PCA.tsv
-> log2(TPM + 1)
-> gene-wise z-score
-> sample-level PCA
-> coordinates, variance table, and Figure A style plot
```

Primary outputs:

```text
PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv
PCA_high_quality_CYP_logTPM_zscore_variance.tsv
FigureA_highQuality_CYP_PCA.png
FigureA_highQuality_CYP_PCA.pdf
```

## 36-HQ Module Figures and Dan Internal Variation

- `merge_CYP_modules_with_annotation_baseR.R`
- `plot_CYP_module_heatmap_baseR.R`
- `plot_CYP_module_scatter_baseR.R`
- `plot_FigureC_CYP_module_scatter_baseR.R`
- `plot_CYP6B_focused_slope_baseR.R`
- `investigate_Dan_internal_CYP_variation_baseR.R`
- `make_Dan_internal_CYP_summary_tables_baseR.R`
- `quantify_CYP_PCA_within_group_dispersion_baseR.R`

Purpose:

```text
36-HQ CYP module and PCA result tables
-> annotated module table
-> module scatter/heatmap and CYP6B-focused slope plots
-> Dan replicate-variation summaries
-> within-group PCA distance summaries
```

Most scripts use working-directory input files restored in `results_manifest/36HQ/`. Rendered PNG/PDF
figure files are not committed in this lightweight archive.

## unknownCYP Recheck and Phylogeny

- `plot_unknownCYP_TPM_ranking_final.R`
- `plot_unknownCYP_Dan_vs_Mul_scatter.R`
- `make_unknownCYP_clean_tip_labels.R`
- `make_unknownCYP_clean_tip_labels_CYP6_focus.R`
- `prune_unknownCYP_CYP6_focus_tree.R`
- `rename_unknownCYP_CYP6_focus_tree_tips.R`

Purpose:

```text
24 Phoenei CYP_unknown candidates
-> expression ranking and Dan/Mul scatter plots
-> clean tree labels for diagnostic phylogeny
-> CYP6-focused tree pruning and tip relabeling
```

Interpretation boundary:

```text
High TPM alone is not treated as sufficient support. Final candidate priority combines expression, CYP motif completeness, ORF length, homology, and phylogenetic placement.
```

## Figure1 Ph-Bm CYP Overview

- `make_fig1_gene_order_final.R`

Purpose:

```text
fig1_expression_input_full.tsv + fig1_block_map.tsv
-> block-aware gene order for the Ph-Bm CYP overview figure
```

The resulting `fig1_gene_order_final.tsv` is archived in `results_manifest/Bmori_comparison/`.
