# Python Scripts

Use this directory for Python utilities used in the CYP family study.

Recommended naming:

- `parse_*.py`
- `filter_*.py`
- `summarize_*.py`
- `plot_*.py`

## unknownCYP

- `clean_unknownCYP_peptideAvailable14_headers.py`

Purpose:

```text
Raw peptide FASTA headers for peptide-available unknownCYP candidates
-> clean PhUNK-prefixed FASTA headers
-> old/new header mapping table
```

This script supports the diagnostic unknownCYP phylogeny workflow.

## 91-CYP Candidate Discovery

- `filter_cyp_candidates_from_annotation.py`

Purpose:

```text
Gene-level annotation table
-> scan PFAM, InterPro, description, and GO evidence for CYP/P450 markers
-> write broad CYP candidate table and optional gene ID list
```

This is a public reconstruction utility for the CYP/P450 evidence-screening logic. It does not claim to be the unrecovered original HPC command that emitted the restored `CYP_candidates_step1.tsv` and `CYP_candidates_step2_confirmed.tsv` tables.
