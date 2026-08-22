# P. hoenei detoxification-family broad-pool batch

This directory contains the public-safe, small-table outputs from the corrected
2026-08-19 portable batch. Historical HPC family results were used as read-only
candidate evidence and were joined to the frozen six-sample expression and
DESeq2 backbone.

| Family | Phase | Broad candidates | Expression coverage | Historical final set |
|---|---:|---:|---:|---:|
| CarE | I | 20 | 20/20 | 20 |
| GST | II | 20 | 20/20 | 9 |
| UGT | II | 36 | 36/36 | 13 |
| SULT | II | 11 | 11/11 | 7 |
| ABC | III | 49 | 49/49 | 34 |

The `HistoricalFinal` column is provenance, not a new high-confidence call.
Broad candidates must still undergo family-specific domain completeness,
representative-isoform, fragment, and homology review.

Each family directory contains:

- `<family>_candidate_ids.tsv`: broad IDs and historical-final flag;
- `<family>_broad_master_by_transcript.tsv`: six-sample TPM plus DESeq2 fields;
- `<family>_broad_master_by_gene.tsv`: transcript-summed gene-level TPM summary;
- `<family>_source_evidence.tsv`: small historical evidence snapshot.

Candidate peptide FASTA files and raw run summaries remain on private storage.
Private hostnames, usernames, credentials, and absolute HPC paths are excluded.

## QC

- Candidate IDs were normalized from Trinity transcript/peptide IDs to gene IDs.
- Every broad candidate matched at least one transcript in the frozen TPM table.
- Gene-row counts equal broad-candidate counts for all five families.
- Corrected batch stderr logs were empty.
- A prior batch from the same day is retained privately as failed-QC evidence;
  it is not included here because a field-name collision mislabeled transcript
  IDs as gene IDs in the summary layer.
