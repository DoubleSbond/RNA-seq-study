# Cross-species expression background atlas workflow

## Purpose

Place Phase I–III detoxification genes in a reproducible internal expression
reference system and compare functional expression layers across species or
diets without interpreting absolute TPM alone.

## Required inputs

1. A transcript- or gene-level TPM matrix with biological replicates.
2. A stable identifier-to-function annotation table.
3. Sample metadata including species, tissue, stage, sex, and diet.
4. A separately curated detoxification-family table when family-level summaries
   are required.

## Common analysis design

1. Search the same predefined functions: housekeeping, energy metabolism,
   digestion, immunity, and development/instar regulation.
2. Retain the highest-expression annotated representative for visualization.
3. Report the full matching family's candidate count, median, interquartile
   range, and maximum so that the representative does not replace the family.
4. Draw a fixed-seed random background from each expression quintile.
5. Keep raw TPM values; use `log10(TPM+1)` only for cross-layer visualization.
6. Store source paths, sample metadata, random seed, search patterns, outputs,
   and limitations with the result package.

## Cross-species interpretation rules

- Compare expression rank, functional layer, and within-dataset ratios before
  comparing raw TPM.
- Tissue, stage, sex, diet, library construction, reference annotation, and
  transcript-versus-gene aggregation must be treated as explicit covariates.
- A transcript isoform is not a genomic gene copy, and a best functional hit is
  not an orthologue call.
- Marker non-recovery from one annotation layer is not evidence of biological
  absence.
- Strong dietary conclusions require matched tissues and developmental stages,
  preferably with biological replication in every species/diet group.

## Current adapters

- `build_expression_background_atlas.py`: P. hoenei de novo Trinity TPM plus
  Swiss-Prot matches.
- `build_bmori_expression_background_atlas.py`: B. mori RefSeq transcript TPM,
  transcript-to-gene map, and RefSeq product annotation.

Future Papilio and Spodoptera datasets should reuse the functional definitions,
random seed policy, summary fields, and interpretation rules while adding only
an input-format adapter.
