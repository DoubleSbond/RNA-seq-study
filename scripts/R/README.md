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
TPM_gene_CYP_final_withMeanSD.tsv
```

Outputs:

```text
CYP_high_quality_expression_modules.tsv
CYP_high_quality_expression_module_summary.tsv
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
