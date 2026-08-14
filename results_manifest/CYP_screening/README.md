# CYP Screening QC Tables

This directory contains small tables that document the transition from broad CYP-like candidates to sequence-quality-reviewed CYP sets.

## Candidate Mapping

| File | Role |
|---|---|
| `CYP_candidate_pep_tx_gene.tsv` | Peptide, transcript, and gene ID mapping for broad CYP candidates. |
| `CYP_candidate_geneids.txt` | Broad CYP candidate gene IDs. |
| `CYP_candidate_txids.txt` | Broad CYP candidate transcript IDs. |
| `CYP_candidate_pepids.txt` | Broad CYP candidate peptide IDs. |

## Representative Isoforms and Length QC

| File | Role |
|---|---|
| `CYP_longest_isoform_per_gene.tsv` | Representative longest peptide/transcript per candidate gene. |
| `CYP_longest_isoform_pepids.txt` | Peptide IDs for representative longest isoforms. |
| `CYP_len300plus_summary.tsv` | Candidates passing the peptide-length screen, with homology support columns. |
| `CYP_len300plus_geneids.txt` | Gene IDs passing the 300-aa length screen. |

## Exclusion / Audit Lists

| File | Role |
|---|---|
| `CYP_fragment_geneids.txt` | Candidate genes flagged as fragments. |
| `CYP_noncanonical_geneids.txt` | Candidate genes flagged as noncanonical. |
| `CYP_len300plus_noncanonical_candidates.txt` | Length-passing candidates still flagged as noncanonical. |
| `CYP_seed_geneids_missing_in_current_pep.txt` | Seed genes missing from the current peptide set. |
| `CYP_missing_seed_genes_in_gene_trans_map.tsv` | Seed genes missing from the gene-transcript map. |

These files do not replace the curated 36-HQ layer in `results_manifest/36HQ/`; they document the screening and QC evidence leading into that reviewed layer.
