# unknownCYP Result Manifests

This directory stores small result tables for the unknownCYP recheck and diagnostic phylogeny layer.

## Source Set

- `unknownCYP_24_peptide_availability_status.tsv`
- `unknownCYP_raw24_phylogeny_inclusion_summary.tsv`
- `01_all_unknownCYP_review_table.tsv`

These files document the 24 original Phoenei CYP_unknown candidates and their motif, ORF, homology, and phylogeny review status.

## Integrated Interpretation

- `unknownCYP_integrated_interpretation.with_group.domain_priority.tsv`
- `highTPM_unknownCYP_vs_phylogeny_current_mapping.tsv`
- `unknownCYP_phylogeny_interpretation.manual_v1.tsv`

These tables separate high-expression candidates from high-confidence CYP candidates. They support the conclusion that high TPM is useful for prioritization but is not sufficient without motif, ORF, homology, and phylogenetic support.

## Tree Output

- `unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.treefile`

This treefile supports the diagnostic placement of peptide-available unknownCYP candidates alongside Ph 36-HQ CYPs and Bombyx/Spodoptera references.

## Key Interpretation

DN598 is the strongest recovered unknownCYP candidate because it combines high expression, complete CYP motifs, and CYP6B-like phylogenetic placement. DN1031, DN3806, and DN420 show high TPM but remain lower-confidence because of motif, ORF, or phylogenetic limitations.
