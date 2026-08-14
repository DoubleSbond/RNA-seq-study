# CYP Data Versions and Analysis Layers

This document defines the major CYP data versions used in the project. It exists to prevent accidental mixing of discovery, high-quality, matched-symbol, RT-qPCR, and unknownCYP analysis layers.

## 1. Version Summary

| Version | Approximate size | Main role | Manuscript confidence |
|---|---:|---|---|
| 91-CYP pool | 91 genes | Broad CYP discovery / screening | Exploratory |
| Sequence-QC CYP summary | ~71 peptide-available or sequence-reviewed records | ORF, length, and homology review | Intermediate |
| 36-HQ CYP set | 36 genes | Core expression, figures, interpretation | Main analysis set |
| Ph-Bm matched symbols | symbol-level matched set | Cross-species exploratory comparison | Requires caution |
| RT-qPCR candidate sets | Batch1 4; combined 14 | Primer design and validation | Candidate-level |
| unknownCYP raw pool | 24 candidates | Unknown CYP review | Exploratory classification |
| peptide-available unknownCYP tree | 14 genes / 17 ORFs | First-pass phylogenetic placement | Diagnostic |

## 2. 91-CYP Pool

The 91-CYP pool is the broad discovery layer from the RNA-seq and CYP annotation workflow.

Use for:

- Ensuring broad CYP candidate coverage.
- Finding additional partial CYP signals.
- Supplementary screening tables.

Do not use for:

- Main manuscript gene-level claims without quality labels.
- Primer design unless the sequence has passed ORF/motif checks.
- Unqualified statements such as "high-quality CYP gene".

Known related file names:

```text
TPM_gene_CYP_91.tsv
TPM_gene_CYP_91_withMean.tsv
CYP_final_summary.tsv
CYP_final_geneids.txt
TPM_gene_CYP_confirmed.tsv
```

## 3. 36-HQ CYP Set

The 36-HQ set is the main analysis set.

Use for:

- Core expression pattern interpretation.
- PCA and heatmap.
- Dan/Mul expression modules.
- Candidate prioritization.
- Manuscript-level CYP expression statements.

Key master table:

```text
CYP_high_quality_36_master_summary.tsv
```

Expected size:

```text
37 lines = header + 36 genes
```

Known high-level rule:

```text
The 36-HQ set was not simply a protein-length filter. It reflects expression, representative ORF/peptide availability, sequence quality, motif/domain support, and homology evidence.
```

## 4. Ph-Bm Matched Symbol Comparison

The matched comparison uses CYP symbol-level logic. A symbol may map to multiple *P. hoenei* Trinity genes, and the plotted representative may not always be a 36-HQ member.

Use for:

- Exploratory cross-species expression overview.
- Identifying comparable CYP family-level patterns.
- Designing follow-up 36-HQ-only comparison.

Caution:

```text
Symbol-level matching is not equivalent to strict one-to-one orthology.
Not all top representative P. hoenei sequences pass 36-HQ criteria.
```

Known high-risk representative sequences:

| Symbol | Representative gene | Issue |
|---|---|---|
| CYP9A20-like | TRINITY_DN13796_c0_g1 | 162 aa, severe truncation |
| CYP6AB4-like | TRINITY_DN1767_c0_g1 | 143 aa, severe truncation |
| CYP6B2-like | TRINITY_DN127_c0_g4 | 318 aa, partial; Bm hit is low-quality protein |
| CYP49A1-like | TRINITY_DN18331_c0_g2 | 303 aa, partial but possibly supported |

Recommended figure labeling:

```text
Shared CYP symbols were assigned according to best-hit annotations. Representative P. hoenei transcripts were selected for expression visualization; not all representatives satisfy the 36-HQ sequence-quality criteria.
```

## 5. RT-qPCR Candidate Versions

Batch1 4-CYP set:

```text
TRINITY_DN159_c0_g1
TRINITY_DN180_c0_g1
TRINITY_DN25915_c0_g1
TRINITY_DN598_c0_g1
```

Known Batch1 file:

```text
seqs/CYP_RTqPCR_candidates.batch1_4CYP.complete_CDS.gene_id_header.fa
```

Combined Batch1 + RankAD set:

```text
14 non-redundant CDS
```

Known combined files:

```text
seqs/CYP_RTqPCR_candidates.combined_Batch1_plus_RankAD36CYP.cds.gene_id_header.fa
candidate_table/CYP_RTqPCR_candidates.combined_14CYP.sequence_quality_summary.tsv
```

Important audit point:

```text
TRINITY_DN25915_c0_g1 must be checked against the restored 36-HQ gene list before being described as a 36-HQ candidate.
```

## 6. UnknownCYP Versions

Raw unknownCYP pool:

```text
24 candidates
```

Peptide availability result:

```text
14 gene-level entries had recoverable peptide/ORF evidence.
These were represented by 17 peptide records.
The remaining 10 candidates were retained in the evidence table but excluded from protein phylogeny.
```

Diagnostic tree input:

```text
17 PhUNK ORFs
36 Ph36HQ references
25 Bmori references
28 Spodo references
Total: 106 sequences
```

Interpretation rule:

```text
CYP6/CYP3-clan relevance is an outcome of the placement analysis, not an inclusion criterion.
```
