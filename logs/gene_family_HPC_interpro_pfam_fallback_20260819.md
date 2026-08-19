# InterProScan Pfam fallback — 2026-08-19

The installed full InterProScan bundle has missing or unprepared legacy
components (`hmmpfam2`, CDD command compatibility, and several relative data
indexes). Failed full-run outputs and logs remain archived. Independent Pfam-A
HMMER jobs are unaffected and already provide the primary raw domain evidence.

An additional Pfam-only InterProScan compatibility batch was submitted from the
installation root to attempt integrated InterPro, GO, pathway, GFF3, and XML
output without invoking broken optional components.

Output root:
`/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/interpro_pfam_20260819T191500JST`

| Family | Job ID |
|---|---:|
| CarE | 19678257 |
| GST | 19678258 |
| UGT | 19678259 |
| SULT | 19678260 |
| ABC | 19678261 |
