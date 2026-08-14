# 91-CYP Discovery Layer

This directory contains small, Git-friendly tables that document the broad CYP discovery layer.

## Main Files

| File | Role |
|---|---|
| `CYP_candidates_step1.tsv` | Broad first-pass CYP/P450 evidence table from gene-level DESeq2 output plus annotation fields. |
| `CYP_candidates_step2_confirmed.tsv` | Confirmed CYP candidate table after consolidating annotation evidence. |
| `CYP_confirmed_geneids.txt` | Gene IDs represented in the confirmed CYP layer. |
| `CYP_final_summary.tsv` | Final 91-CYP summary table from the recovered project material. |
| `CYP_final_geneids.txt` | Final 91-CYP gene ID list. |
| `TPM_gene_CYP_91.tsv` | Gene-level TPM matrix for the 91-CYP layer. |
| `TPM_gene_CYP_91_withMean.tsv` | TPM matrix with group-level mean columns. |
| `TPM_gene_CYP_confirmed.tsv` | TPM table for the confirmed CYP candidate layer. |
| `CYP_Bmor_besthit_by_gene.tsv` | B. mori best-hit evidence summarized by gene. |
| `CYP_confirmed_vs_Bmor_besthit.tsv` | Confirmed CYP candidates joined to B. mori best-hit evidence. |
| `CYP_PC1_loading_rank.tsv` | Exploratory PC1/PC2 loading ranks for CYP expression variation. |
| `CYP_PC1_Top10_BmAnnotated.tsv` | Top PC1-loading candidates with B. mori annotation labels. |
| `CYP_PC1_Top10_BmBestHit.tsv` | Top PC1-loading candidates with B. mori best-hit labels. |

## Interpretation

The evidence supports a stepwise CYP discovery narrative:

1. Start from gene-level differential-expression results with functional annotation fields.
2. Retain broad CYP/P450 candidates using PFAM, InterPro, description, and GO evidence.
3. Consolidate the confirmed CYP layer and carry it into TPM, best-hit, and exploratory expression analyses.
4. Use this broad layer as the upstream source for later reviewed subsets, including the 36-HQ CYP set.

The exact original one-command script that generated the recovered `CYP_candidates_step1.tsv` and
`CYP_candidates_step2_confirmed.tsv` tables has not yet been identified. A public, path-parameterized
reconstruction utility is provided at `scripts/python/filter_cyp_candidates_from_annotation.py` so the
screening criteria can be rerun on compatible annotation tables.
