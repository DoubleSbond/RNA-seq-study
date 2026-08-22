# Representative within-family all-vs-all similarity

This exploratory batch compares the longest *P. hoenei* peptide for every broad candidate gene against all other representatives in the same detoxification family using BLASTP (`evalue <= 1e-3`, SEG and soft masking enabled).

The raw HSP tables retain every hit. Non-self edge tables add query and subject coverage. Filtered edge tables retain HSPs with `evalue <= 1e-5` and at least 50% coverage of both sequences; these are useful starting points for paralog clusters and subfamily review, not final orthology calls.

| Family | Representatives | All HSPs | Non-self HSPs | Filtered directed edges |
|---|---:|---:|---:|---:|
| CarE | 20 | 400 | 380 | 370 |
| GST | 20 | 103 | 83 | 56 |
| UGT | 36 | 528 | 492 | 238 |
| SULT | 11 | 65 | 54 | 37 |
| ABC | 49 | 2,090 | 2,041 | 159 |

`failed_v1_logs` preserves the first attempt, which failed because it referenced a nonexistent Conda BLAST path. `successful_v2` uses `/usr/bin/makeblastdb` and `/usr/bin/blastp`. All files listed in the family SHA-256 manifests passed verification after transfer. BLAST database index files are retained and are covered by the checksum of the final compressed delivery archive.
