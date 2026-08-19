# Gene-family portable batch log — 2026-08-19

## Scope

Families were processed in the planned order: CarE, GST, UGT, SULT, and ABC.
The run created new timestamped code and result directories; historical family
directories were read-only.

## Outcome

The corrected batch completed successfully. Broad candidate counts were 20
CarE, 20 GST, 36 UGT, 11 SULT, and 49 ABC. All candidates matched the frozen
six-sample expression backbone. All five stderr logs were empty.

## QC correction

The first batch exposed a schema collision: the TPM table labels its first
column `GeneID` even though its values are transcript IDs. That field replaced
the normalized gene ID in the first implementation, inflating the reported
number of expressed genes. The first batch was retained privately and marked
failed QC. The builder was corrected to preserve normalized `GeneID`, retain
the source identifier as `TranscriptID`, and fail if any normalized expression
ID falls outside the candidate set. Two local regression tests cover the fix.

## Public/private split

GitHub receives scripts, configuration, tests, small candidate/expression/
evidence tables, this sanitized log, and methods documentation. Peptide FASTA,
private absolute paths, and raw HPC run metadata remain outside Git.
