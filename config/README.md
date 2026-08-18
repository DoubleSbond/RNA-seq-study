# Configuration

Store non-sensitive configuration files here, such as:

- Sample sheets.
- Analysis parameters.
- Tool-specific config files.
- Database version records.
- Gene family definition files.

Do not store credentials, tokens, private keys, passwords, private HPC paths, hostnames, usernames, or unpublished data locations.

## Current Files

- `rnaseq_samples.tsv`: RNA-seq sample sheet for the project backbone.
- `sample_info.csv`: compact sample metadata.
- `families/`: standardized family-definition files for CYP, CarE, GST, UGT, SULT, and ABC analyses.

## Family Definitions

Each file in `families/` defines the family-specific layer that sits on top of the common RNA-seq backbone. Review the relevant `<family>.yaml` before running screening or interpreting expression results.

Minimum required decisions before downstream interpretation:

- accepted keywords and synonyms
- PFAM, InterPro, GO, or domain evidence
- reference taxa and reference sequence source
- representative isoform rule
- broad discovery pool rule
- high-confidence core-set rule
- fragment and ambiguous-candidate warning rules

See `families/README.md` and `docs/family_standardization.md` for the full standard.
