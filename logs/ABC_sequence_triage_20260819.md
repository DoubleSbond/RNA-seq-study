# ABC sequence triage log — 2026-08-19

- Inputs: ABC second-pass table and the append-only exported broad peptide FASTA.
- Evidence: peptide length, Walker A motif, LSGGQ ABC signature, conservative hydrophobic-window proxy, historical status, and archived annotations.
- Output: `ABC/sequence_triage_20260819/ABC_sequence_triage.tsv`.
- Validation: ten Python unit tests passed.
- Safety: the operation created new files only; no prior table, sequence, or HPC result was altered.
