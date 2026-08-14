# B. mori Comparison and Figure1 Inputs

This directory contains small, Git-friendly tables supporting the exploratory comparison between
*Perigrapha hoenei* and public *Bombyx mori* midgut CYP expression.

## Public B. mori RNA-seq CYP Tables

| File | Role |
|---|---|
| `Bm_ML_midgut_runs.txt` | Public run accessions used for the B. mori midgut dataset. |
| `Bm_ML_midgut_runs_with_info.tsv` | Run accessions with compact sample annotations. |
| `Bm_public_RNAseq_sample_info.tsv` | Sample metadata consumed by the B. mori TPM script. |
| `Bmori_GCF_ASM3026992v2_CYP_transcripts_from_GFF.tsv` | CYP transcript annotations parsed from the B. mori GFF. |
| `Bm_ML_midgut_CYP_TPM_annotated.tsv` | Annotated B. mori CYP TPM table used for comparison and target prioritization. |

The public reconstruction script is `scripts/python/make_bmori_public_cyp_tpm_tables.py`.

## Figure1 Inputs

| File | Role |
|---|---|
| `fig1_expression_input.tsv` | Compact expression input table for the Ph-Bm CYP overview. |
| `fig1_expression_input_full.tsv` | Full expression input table with Ph and Bm mean TPM columns. |
| `fig1_block_map.tsv` | Manual block labels used to group Figure1 CYP targets. |
| `fig1_gene_order_final.tsv` | Final plotting order after block-aware sorting. |

The ordering script is `scripts/R/make_fig1_gene_order_final.R`.

## Interpretation Boundary

The Ph-Bm comparison is symbol-level and exploratory. Shared CYP labels are based on best-hit or
annotation-derived symbols and should not be treated as strict one-to-one orthology. Some P. hoenei
representatives used in the overview figure are partial and should not replace the 36-HQ CYP set for
sequence-quality claims.
