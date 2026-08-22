# Whole-proteome scans against family reference sets

This high-recall screen searches all 11,856 longest *P. hoenei* peptides against the combined retained *Bombyx mori* and *Spodoptera* reference sequences for each detoxification family. BLASTP was run with `evalue <= 1`, SEG, soft masking, and all target hits retained.

Each family directory contains the complete raw HSP table, a coverage-annotated table, loose `evalue <= 1e-3` gene IDs, a more restrictive `evalue <= 1e-5` plus at least 40% query and subject coverage gene list, reference FASTA, BLAST database files, logs, inventory, summary, and checksums.

| Family | Proteome peptides | Reference sequences | Raw HSPs | Genes at E≤1e-3 | Genes at E≤1e-5 and ≥40%/40% coverage |
|---|---:|---:|---:|---:|---:|
| CarE | 11,856 | 47 | 10,481 | 114 | 54 |
| GST | 11,856 | 37 | 7,499 | 127 | 69 |
| UGT | 11,856 | 76 | 9,187 | 289 | 115 |
| SULT | 11,856 | 25 | 7,106 | 150 | 89 |
| ABC | 11,856 | 93 | 13,916 | 73 | 34 |

These lists are intentionally permissive discovery pools. They must be intersected with HMM, Pfam, motif, sequence-completeness, and phylogenetic evidence before final classification. All files listed in the transferred family manifests passed SHA-256 verification.
