# Unknown CYP phylogeny input preparation summary

Date: 2026-06-17

The previous unknownCYP recheck module contained 23 unresolved CYP-like candidates.
Based on amino-acid length and conserved CYP motif status, candidates were classified
into domain-priority categories.

Phylogeny candidate selection:

1. Core set
   Criteria:
   - aa_length_no_terminal_stop >= 350
   - heme_Cys_motif_FxxGxxxCxG = True
   - PERF_motif = True
   - K_helix_motif_ExxR = True

   Result:
   - 10 unknownCYP candidates selected.
   - Output FASTA:
     seqs/unknownCYP_for_phylogeny_core.geneID_header.faa

2. Extended set
   Criteria:
   - aa_length_no_terminal_stop >= 250
   - heme_Cys_motif_FxxGxxxCxG = True
   - PERF_motif = True
   - K_helix_motif_ExxR = True

   Result:
   - 12 unknownCYP candidates selected.
   - Output FASTA:
     seqs/unknownCYP_for_phylogeny_extended.geneID_header.faa

The core set is recommended for the first diagnostic phylogenetic tree.
The extended set can be used as a supplementary/placement tree including partial but motif-complete CYP candidates.
