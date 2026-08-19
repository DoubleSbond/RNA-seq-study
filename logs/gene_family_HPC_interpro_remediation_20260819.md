# InterProScan input remediation — 2026-08-19

The first independent InterProScan submissions revealed terminal `*` characters
from ORF prediction in the exported peptide FASTA files. InterProScan rejects
that character before analysis. The source FASTA files and failed-run logs were
left unchanged.

A new run creates per-family sanitized copies by stripping `*` only from
sequence lines, records the original peptide count and number of stripped
characters, and then runs the same full InterProScan request.

Output root:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/interproscan_sanitized_20260819T184500JST`

| Family | Corrected job ID |
|---|---:|
| CarE | 19678148 |
| GST | 19678149 |
| UGT | 19678150 |
| SULT | 19678151 |
| ABC | 19678152 |

This preserves both the raw exported sequences and a fully documented,
InterPro-compatible derivative without overwriting either.
