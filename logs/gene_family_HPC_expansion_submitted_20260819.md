# Gene-family HPC expansion submission — 2026-08-19

Goal: preserve the widest useful raw evidence before HPC access becomes
unavailable. All broad candidates and every exported peptide isoform are used;
no current review/exclusion label is applied to these jobs.

## Raw-evidence batch

HPC output root:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/raw_evidence_20260819T180000JST`

Per family, this batch runs:

- DIAMOND sensitive search against Swiss-Prot, retaining up to 25 targets;
- BLASTP against Bombyx mori, retaining up to 25 targets;
- BLASTP against Spodoptera frugiperda, retaining up to 25 targets;
- full Pfam-A hmmscan raw, table, and domain-table output;
- MAFFT alignment of all candidate isoforms;
- FastTree rough tree;
- inventories, summaries, logs, and checksums.

| Family | Job ID |
|---|---:|
| CarE | 19678115 |
| GST | 19678117 |
| UGT | 19678119 |
| SULT | 19678121 |
| ABC | 19678123 |

## Full InterProScan batch

HPC output root:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/interproscan_20260819T181500JST`

TSV, GFF3, and XML outputs are requested with InterPro lookup, GO terms, and
pathway annotations for all broad candidate isoforms.

| Family | Job ID |
|---|---:|
| CarE | 19678116 |
| GST | 19678118 |
| UGT | 19678120 |
| SULT | 19678122 |
| ABC | 19678124 |

The ten corrected jobs were accepted in the `epyc` queue. An earlier pair of
array submissions (19678053 and 19678095) completed without expanding array
elements and produced no data. Their empty timestamped directories are retained
as an audit record; no cleanup was performed.
