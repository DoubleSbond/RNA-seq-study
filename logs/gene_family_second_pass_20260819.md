# Second-pass review log — 2026-08-19

- Input: append-only broad-pool domain tables and archived Bombyx/Spodoptera top hits.
- Method: family-specific conservative rules implemented in
  `scripts/python/build_gene_family_second_pass_review.py`.
- Output: one new review table under each family's `second_pass_20260819` directory.
- Validation: seven Python unit tests passed.
- Safety: no existing candidate, table, sequence, log, or HPC path was modified or removed.
