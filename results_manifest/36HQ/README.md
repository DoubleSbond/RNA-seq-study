# 36-HQ CYP Result Manifests

This directory stores the small, GitHub-suitable result tables for the 36 high-quality CYP analysis layer.

## Core Set

- `CYP_high_quality_36_geneids.txt`
- `CYP_high_quality_36_geneids_master_order.txt`
- `CYP_high_quality_36_review_list.tsv`
- `CYP_high_quality_36_master_summary.tsv`
- `CYP_high_quality_36_master_summary.sha256`

These files define the reviewed 36-gene high-quality CYP set and preserve the master order used by downstream summaries.

## Expression Modules

- `CYP_high_quality_expression_modules.tsv`
- `CYP_high_quality_expression_modules_annotated.tsv`
- `CYP_high_quality_expression_module_summary.tsv`

These tables support the Dan/Mul expression module interpretation.

## PCA

- `TPM_high_quality_CYP_for_PCA.tsv`
- `PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv`
- `PCA_high_quality_CYP_logTPM_zscore_variance.tsv`
- `CYP_PCA_within_group_distance_summary.tsv`
- `CYP_PCA_within_group_pairwise_distances.tsv`
- `Dan_CYP_PCA_dispersion_summary.tsv`

These tables support the high-quality CYP PCA figure and sample-level expression separation narrative.

## Dan Internal Variation

- `Dan_internal_CYP_variation_summary.tsv`
- `Dan_internal_CYP_variation_top15.tsv`
- `Dan_mg1_low_CYPs.tsv`
- `Dan_top15_variable_CYP_family_summary.tsv`
- `Dan_top15_variable_CYP_module_summary.tsv`

These tables document within-dandelion replicate variation among 36-HQ CYPs. They support the observation
that some CYPs show strong Dan replicate heterogeneity, including cases where Dan_mg1 is lower than
Dan_mg2/Dan_mg3. This layer should be interpreted as replicate-variation provenance rather than a separate
candidate-ranking system.

## Provenance Note

The 36-HQ layer is currently documented as a reviewed and audited quality-curation layer. The evidence includes review tables, matching gene ID lists, checksums, restored archives, and downstream scripts. A single fully automated script that starts from the complete 91-CYP table and emits the final 36-HQ set has not yet been identified.
