# Gene-family sequence export — 2026-08-19

The corrected broad candidate sets were extracted from the frozen Trinity and
TransDecoder backbone into a private local departure package. Extraction used
`scripts/python/extract_fasta_by_gene_ids.py`, which refuses existing outputs
and exports every record belonging to the requested Trinity gene IDs.

| Family | Broad genes | Transcript records | CDS records | Peptide records | Missing genes |
|---|---:|---:|---:|---:|---:|
| CarE | 20 | 119 | 112 | 112 | 0 |
| GST | 20 | 88 | 67 | 67 | 0 |
| UGT | 36 | 124 | 109 | 109 | 0 |
| SULT | 11 | 75 | 44 | 44 | 0 |
| ABC | 49 | 201 | 179 | 179 | 0 |

Small extraction-QC tables, including per-file SHA256 values, are archived
under each family directory in `results_manifest/gene_family_runs/`.
Sequence FASTA files remain outside Git under the private-data policy.

Historical longest-representative top-hit tables against B. mori and
Spodoptera were also recovered as small public-safe evidence tables. They are
explicitly labeled `historical_top_hits`: these files are not a new exhaustive
BLAST of every broad candidate and do not establish orthology.
