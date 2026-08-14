# Annotation Summaries

This directory stores lightweight summaries from functional annotation steps.

Current files:

- `go_annotated_pep.txt`: count of peptide records with GO annotation.
- `go_annotated_tx.txt`: count of transcript records with GO annotation.
- `nr_sprot_annotated_pep.txt`: count of peptide records with NR/Swiss-Prot-style annotation.
- `PFAM_enrichment_summary.txt`: compact PFAM enrichment summary.

The public InterProScan summarization script is `scripts/R/interpro_annotation_summary.R`. Full InterProScan, BLAST, and HMMER outputs are bulky intermediate files and remain outside Git.
