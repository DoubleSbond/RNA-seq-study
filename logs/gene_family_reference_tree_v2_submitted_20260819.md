# Reference-tree extraction fallback v2 — 2026-08-19

The first extraction jobs (19678588–19678592) failed because the existing
BLAST databases permit searching but were not built with accession-based entry
retrieval. Their directories and `blastdbcmd` skipped-entry logs are retained.

Fallback job 19678604 exports each complete local reference database once,
filters FASTA records by the top-hit accession lists, then builds the five
reference-augmented MAFFT alignments and FastTree trees sequentially.

Output root:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/reference_trees_v2_20260819T210000JST`
