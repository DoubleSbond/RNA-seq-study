# Reference-augmented rough family trees — 2026-08-19

Successful fallback output from:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/reference_trees_v2_20260819T210000JST`

| Family | P. hoenei isoforms | Bombyx references | Spodoptera references | Alignment sequences |
|---|---:|---:|---:|---:|
| CarE | 112 | 22 | 25 | 159 |
| GST | 67 | 16 | 21 | 104 |
| UGT | 109 | 39 | 37 | 185 |
| SULT | 44 | 11 | 14 | 69 |
| ABC | 179 | 44 | 49 | 272 |

Each directory contains the two reference sets, accession lists, P. hoenei
input, combined FASTA, MAFFT alignment, FastTree tree, summary, inventory, and
HPC checksum table. The root stderr file contains normal MAFFT/FastTree progress
messages and is retained as execution provenance.

These are deliberately inclusive all-isoform trees. A separate HPC batch uses
one longest P. hoenei isoform per gene with IQ-TREE ModelFinder and support
replicates.
