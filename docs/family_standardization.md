# Gene Family Workflow Standardization

This document defines the standard project structure for detoxification-related gene family studies derived from the CYP archive. The goal is to keep future CarE, GST, UGT, SULT, ABC, and related family analyses reproducible without repeating the exploratory clutter of the first CYP study.

## 1. Core Rule

Every family analysis must keep four biological layers separate:

```text
broad discovery pool != high-confidence core set != ambiguous follow-up set != validation candidate set
```

For CYP, the historical equivalents are:

| Standard layer | CYP archive equivalent | Role |
|---|---|---|
| `01_screening` | `CYP_screening` | ID mapping, family evidence, length and fragment checks |
| `02_broad_pool` | `91CYP` | Sensitive discovery pool; not final interpretation |
| `03_high_confidence` | `36HQ` | Core set for expression figures and main claims |
| `04_reference_comparison` | `Bmori_comparison` | Cross-species/reference expression comparison |
| `05_unknown_or_ambiguous` | `unknownCYP` | Uncertain candidates, peptide/ORF review, phylogeny |
| `06_validation_design` | `RTqPCR` | Candidate prioritization and assay planning |

The old CYP directory names are retained for provenance. New families should use the standard layer names from the start.

## 2. Required Directory Layout Per Family

Use this structure under `results_manifest/<family>/`:

```text
results_manifest/<family>/
|-- README.md
|-- 01_screening/
|-- 02_broad_pool/
|-- 03_high_confidence/
|-- 04_reference_comparison/
|-- 05_unknown_or_ambiguous/
`-- 06_validation_design/
```

Each layer should contain a `README.md` once files are added. The README should state:

- purpose of the layer
- main inputs
- script or command used
- main outputs
- inclusion/exclusion rules
- unresolved caveats

## 3. Required Configuration Before Screening

Before running family screening, create or review:

```text
config/families/<family>.yaml
```

The configuration must define:

- short and full family name
- accepted keywords and synonyms
- PFAM, InterPro, GO, or domain evidence
- reference taxa and reference FASTA assets
- expected protein/domain completeness rules
- fragment and noncanonical warning rules
- representative isoform selection rule
- high-confidence core-set rule

Do not begin downstream expression interpretation until this file exists.

## 4. Standard Stage Gates

### Gate 1: screening ready

Required evidence:

- family config exists
- annotation fields are identified
- transcript, peptide, and gene ID mapping exists
- broad filtering criteria are documented

### Gate 2: broad pool frozen

Required evidence:

- broad candidate table
- candidate gene ID list
- stepwise filtering/provenance table
- fragment/noncanonical labels
- representative isoform candidates

### Gate 3: high-confidence set frozen

Required evidence:

- explicit high-confidence rules
- curated core gene ID list
- master summary table
- audit note explaining exclusions and borderline cases
- TPM/count matrix for core genes

### Gate 4: expression interpretation ready

Required evidence:

- condition means and replicate-level values
- module classification rules
- PCA or clustering QC
- replicate-dispersion notes
- candidate ranking table

### Gate 5: reference comparison ready

Required evidence:

- reference species/source version
- comparable family-specific expression table
- symbol/best-hit matching method
- partial or ambiguous match labels
- statement separating exploratory symbol-level comparison from strict core-set evidence

### Gate 6: validation design ready

Required evidence:

- ranked validation candidates
- sequence availability and length QC
- primer or assay design scope decision
- final inclusion decision for public archive/release

## 5. Naming Rules

Use clear layer names rather than generic words like `final`.

Preferred:

```text
<family>_broad_pool_geneids.txt
<family>_broad_pool_master_summary.tsv
<family>_high_confidence_geneids.txt
<family>_high_confidence_master_summary.tsv
<family>_unknown_or_ambiguous_review.tsv
<family>_validation_candidates.tsv
```

Avoid:

```text
<family>_final_geneids.txt
<family>_confirmed.tsv
<family>_candidate_final_v2.tsv
```

If a legacy file uses `final`, its README must say which layer it belongs to.

## 6. Interpretation Guardrails

Allowed wording:

```text
The expression pattern suggests candidate involvement in the response to different host plant environments.
```

Use with caution:

```text
The candidate is consistent with a detoxification-related expression signature.
```

Avoid without functional validation:

```text
This gene detoxifies compound X.
This gene explains host specialization by itself.
This family member is a confirmed ortholog based only on best-hit evidence.
```

## 7. Recommended Order For New Families

Use this order for CarE, GST, UGT, SULT, and ABC:

1. Fill `config/families/<family>.yaml`.
2. Build `01_screening` ID and evidence tables.
3. Freeze `02_broad_pool` with explicit broad inclusion rules.
4. Curate `03_high_confidence` before making main figures.
5. Run expression modules, PCA, and replicate checks only on the high-confidence set.
6. Build `04_reference_comparison` separately from the core-set evidence.
7. Review `05_unknown_or_ambiguous` without preselecting only high-expression candidates.
8. Produce `06_validation_design` as a ranked planning table, not as another discovery pool.
9. Update `docs/script_provenance_index.md`, `docs/data_versions.md`, and `docs/archive_status.md` after each family reaches a stage gate.
