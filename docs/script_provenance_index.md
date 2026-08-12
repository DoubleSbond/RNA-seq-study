# Script Provenance Index

This index maps the public scripts in `scripts/` to the project workflow blocks they support.

## RNA-seq Quantification and Differential Expression

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| Gene-level DESeq2 | `scripts/R/gene_level_deseq2_final.R` | Salmon `quant.sf` directories; `tx2gene.csv` | Gene-level DESeq2 result tables and diagnostic plots |

## 36-HQ CYP Analysis

| Workflow block | Public script | Main inputs | Main outputs |
|---|---|---|---|
| Expression module classification | `scripts/R/classify_high_quality_CYP_modules_baseR.R` | `TPM_gene_CYP_final_withMeanSD.tsv` | `CYP_high_quality_expression_modules.tsv`; module summary |
| PCA coordinates and variance | `scripts/R/PCA_high_quality_CYP_logTPM_zscore_baseR.R` | `TPM_high_quality_CYP_for_PCA.tsv` | PCA coordinate and variance tables; PCA plot |
| PCA plotting | `scripts/R/plot_FigureA_PCA_highQuality_CYP_baseR.R` | PCA coordinate and variance tables | Figure A PCA PNG/PDF |

## Current Gaps

The following recovered scripts exist in local evidence but have not yet all been converted into public, parameterized scripts:

- Raw-read trimming and Trinity assembly shell scripts.
- InterProScan / PFAM annotation shell scripts.
- 91-CYP candidate generation commands.
- B. mori public RNA-seq processing script.
- unknownCYP tree-label cleaning and plotting scripts.

Some recovered scripts contain internal absolute paths or comments with encoding damage. Those scripts should be published only after conversion to path-parameterized public versions.
