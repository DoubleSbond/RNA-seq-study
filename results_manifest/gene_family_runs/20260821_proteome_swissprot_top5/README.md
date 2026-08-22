# Whole-proteome Swiss-Prot top-5 annotation

All 11,856 longest *P. hoenei* peptides were searched against the existing project Swiss-Prot DIAMOND database in sensitive mode. Up to five hits per query were retained at `evalue <= 1e-3`.

- Raw hit rows: 34,809
- Peptides with at least one hit: 7,605
- Normalized genes with at least one hit: 7,605
- Output fields include query and subject IDs, identity, alignment length, mismatches, gaps, query and subject coordinates and lengths, e-value, bit score, and Swiss-Prot title.

The directory preserves the complete raw table, annotated peptide/gene IDs, DIAMOND and database metadata, logs, inventory, summary, and checksums. All transferred files listed by the HPC manifest passed SHA-256 verification.

This proteome-wide table is general annotation evidence. Family membership still requires the family-specific homology, HMM, Pfam, motif, sequence architecture, and phylogenetic evidence retained elsewhere in the workflow.
