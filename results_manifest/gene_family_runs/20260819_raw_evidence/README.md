# Broad raw-evidence expansion — 2026-08-19

This directory is a byte-for-byte download of the successful HPC run at:

`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/raw_evidence_20260819T180000JST`

All broad candidates and all peptide isoforms were retained. Each family
directory contains Swiss-Prot DIAMOND top-25 hits, Bombyx and Spodoptera BLASTP
top-25 hits, full Pfam-A HMMER outputs, MAFFT alignment, FastTree rough tree,
input peptide copy, logs, inventory, summary, and the original HPC checksum
table.

| Family | Peptides | Swiss-Prot hits | Bombyx hits | Spodoptera hits | Pfam domain rows |
|---|---:|---:|---:|---:|---:|
| CarE | 112 | 2,679 | 2,642 | 2,736 | 498 |
| GST | 67 | 1,293 | 699 | 793 | 496 |
| UGT | 109 | 2,145 | 1,818 | 1,832 | 326 |
| SULT | 44 | 895 | 891 | 621 | 140 |
| ABC | 179 | 4,146 | 6,441 | 6,391 | 4,341 |
| **Total** | **511** | **11,158** | **12,491** | **12,333** | **5,801** |

The original `sha256.tsv` files contain 75 entries. Seventy analysis/input
files match after download. The five `*.stdout.log` entries differ because the
job script calculated checksums and then appended its final timestamp to the
stdout log. This is a provenance-order issue, not an analysis-file transfer
failure. The original manifests and logs are preserved unchanged.

InterProScan failure attempts are documented separately in `logs/`; the
successful independent Pfam-A results in this directory are the replacement
raw domain evidence.
