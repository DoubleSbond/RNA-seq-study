# Gene-family portable batch runbook

This batch converts existing HPC candidate evidence into a consistent, portable
rough-results package for CarE, GST, UGT, SULT, and ABC. It does not replace the
historical family directories and does not reinterpret the historical curated
`final` lists as new high-confidence calls.

## Inputs

- Family-specific candidate, historical-final, peptide, and evidence paths are
  declared in `config/gene_families.tsv`.
- Six-sample expression comes from the frozen transcript-level TPM table.
- Differential-expression fields come from the frozen DESeq2 export.

## Safety model

- Every run uses a new timestamped `RUN_ROOT`.
- The Python builder refuses an existing family output directory.
- The shell wrapper refuses an existing batch root.
- Historical files are read-only inputs; no file is removed, moved, truncated,
  or edited in place.

## Outputs per family

- broad candidate IDs with a historical-final flag;
- transcript-level TPM and DESeq2 join;
- gene-level summed TPM summary;
- broad candidate peptide FASTA when available;
- source evidence snapshot;
- run summary and SHA256 manifest.

The historical-final flag is provenance only. A future high-confidence review
must apply family-appropriate domain completeness, representative-isoform,
fragment, and homology rules.

## Run audit

- `run_20260819T132500JST` is retained as a failed-QC batch. Its transcript
  records are intact, but a field-name collision caused the normalized
  `GeneID` column and gene-count summary to contain transcript IDs.
- The correction preserves normalized `GeneID` and records the original value
  separately as `TranscriptID`. Corrected results must use a new run root.
