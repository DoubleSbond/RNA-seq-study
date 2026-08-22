# P. hoenei general expression background atlas v1

This directory places Phase I–III detoxification candidates in an internal
whole-transcriptome TPM reference system.

## Design

- `functional_reference_panel.tsv`: highest-expressed Swiss-Prot-annotated
  representative for each recovered predefined biological function.
- `functional_family_distribution.tsv`: candidate count and TPM distribution
  for every predefined function, preventing a single top transcript from being
  interpreted as the whole family.
- `random_background_panel.tsv`: fixed-seed (`20260822`) stratified random
  sample, with four annotated expressed transcripts from each TPM quintile.
- `run_summary.json`: input counts, seed, and selection metadata.
- `P_hoenei_general_expression_atlas_20260822_v1.xlsx`: readable workbook with
  source TPM values, formula-derived means, detoxification genes, methods, and
  an overview chart on a `log10(TPM+1)` display scale.

## Interpretation limits

The predefined panel is a contextual expression reference, not a validated
normalization-gene set. Trinity isoforms and fragments can inflate annotation
counts. Whole-body or composite samples cannot distinguish tissue specificity.
Failure to recover a marker from the Swiss-Prot-matched table is not evidence
of biological absence.
