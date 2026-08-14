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

## Archive Validation

- `validate_archive.py`

Purpose:

```text
Public GitHub archive
-> required path checks
-> public SHA256 manifest verification
-> tracked large/raw-data file policy check
-> sensitive text pattern scan
```

Example:

```bash
python scripts/python/validate_archive.py
```

This script is intended for local/GitHub-side archive QA. It does not require HPC access and does not inspect raw data outside Git.

## 91-CYP Candidate Discovery

- `filter_cyp_candidates_from_annotation.py`

Purpose:

```text
Gene-level annotation table
-> scan PFAM, InterPro, description, and GO evidence for CYP/P450 markers
-> write broad CYP candidate table and optional gene ID list
```

This is a public reconstruction utility for the CYP/P450 evidence-screening logic. It does not claim to be the unrecovered original HPC command that emitted the restored `CYP_candidates_step1.tsv` and `CYP_candidates_step2_confirmed.tsv` tables.

## B. mori Public RNA-seq CYP Tables

- `make_bmori_public_cyp_tpm_tables.py`

Purpose:

```text
B. mori GFF annotation + public Salmon quant.sf directories
-> CYP transcript annotation table
-> transcript-level and gene/symbol-level CYP TPM summaries
-> quadrant/target CYP subsets
```

Example:

```bash
python scripts/python/make_bmori_public_cyp_tpm_tables.py \
  --base-dir <bmori_public_rnaseq_workdir> \
  --gff <GCF_030269925.1_ASM3026992v2_genomic.gff>
```

The script expects `sample_info.tsv` and `quant/<Run>/quant.sf` under `--base-dir` unless `--sample-info` is supplied.
