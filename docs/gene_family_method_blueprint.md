# Portable Gene Family Study Blueprint

This document converts the CYP family study archive into a reusable template for other RNA-seq-based gene family studies, such as CarE, GST, UGT, ABC transporter, or other detoxification-related families.

The goal is twofold:

- Faithfully preserve what was done in the CYP project.
- Make the same technical route quickly reusable after replacing the target family definition, annotation evidence, and interpretation rules.

## 1. Template Principle

Treat the workflow as a family-specific layer built on top of a common RNA-seq backbone.

```text
RNA-seq reads
-> quality control and trimming
-> de novo transcriptome assembly or reference-guided quantification
-> transcript/gene expression quantification
-> functional annotation
-> target gene family discovery
-> evidence filtering and representative selection
-> expression module analysis
-> cross-species or reference-family comparison
-> candidate prioritization
-> optional phylogeny / domain / primer-design follow-up
```

For the current archive, the family-specific layer is CYP. For a future CarE or GST study, the same structure can be reused by replacing family markers, trusted reference sequences, domain rules, and cautious interpretation language.

## 2. RNA-seq Backbone

This layer should remain mostly unchanged across gene families.

| Step | CYP archive example | Reusable rule for other families |
|---|---|---|
| Sample design | `config/rnaseq_samples.tsv`; `config/sample_info.csv` | Keep a machine-readable sample table with condition, replicate, read paths outside Git, and comparison labels. |
| Read trimming | `scripts/shell/run_fastp_paired_samples.sh` | Reuse with path variables and sample table. |
| Assembly | `scripts/shell/run_trinity_denovo_assembly.sh` | Reuse for de novo transcriptome projects; record assembly size and core QC metrics. |
| Quantification | `scripts/shell/run_salmon_quant_samples.sh` | Reuse for transcript/gene TPM and count generation. |
| Gene-level statistics | `scripts/R/gene_level_deseq2_final.R` | Reuse the DESeq2 layer; only sample design and contrast labels should change. |
| Environment | `environment/` | Record software versions and session information for every family project. |

For public GitHub archiving, raw reads, full assemblies, large indexes, and quantification directories remain outside Git. Keep only scripts, sample metadata, small summaries, and sanitized checksums or asset inventories.

## 3. Family Definition Layer

This is the first layer that must be replaced when moving from CYP to another family.

| Component | CYP implementation | CarE/GST adaptation |
|---|---|---|
| Family name | CYP / cytochrome P450 | CarE / GST / target family name |
| Keyword evidence | `CYP`, `cytochrome P450`, `P450` | Family-specific synonyms, enzyme names, and accepted abbreviations |
| Domain evidence | CYP-related Pfam/InterPro/GO records | CarE: esterase/carboxylesterase domains; GST: GST N/C-terminal domains |
| Reference species support | *B. mori* and *Spodoptera* CYP hits | Choose relevant curated references for the new family and taxa |
| Fragment caution | Peptide length and partial representatives | Replace with family-appropriate domain completeness and length expectations |
| Output labels | 91-CYP, 36-HQ, unknownCYP | Use equivalent names, for example broad-CarE, HQ-CarE, unknownCarE |

Minimum recommended family-definition record:

```text
target_family:
  short_name: CYP
  full_name: cytochrome P450
  accepted_keywords:
  required_or_supporting_domains:
  trusted_reference_fasta:
  minimum_length_or_domain_completeness_rule:
  fragment_warning_rule:
  final_core_set_rule:
```

The current public reconstruction script for CYP candidate filtering is `scripts/python/filter_cyp_candidates_from_annotation.py`. For another family, this script should be copied or generalized with a config file rather than edited by hard-coded keyword replacement.

## 4. Discovery Pool

The discovery pool should be broad and sensitive. In the CYP archive this is the 91-CYP layer.

CYP evidence:

```text
results_manifest/91CYP/
results_manifest/CYP_screening/
scripts/python/filter_cyp_candidates_from_annotation.py
```

Reusable discovery-pool logic:

1. Collect all candidates supported by annotation keywords, domains, homology, or GO terms.
2. Keep transcript, peptide, and gene identifiers linked explicitly.
3. Retain fragment and noncanonical candidates at this stage, but label them.
4. Store broad candidate tables separately from high-confidence core sets.
5. Preserve stepwise filtering tables so the candidate list can be audited later.

For CarE/GST, this stage should be renamed and documented as the broad discovery pool, not as the final biological interpretation set.

## 5. High-Confidence Core Set

The high-confidence set is the interpretation layer. In the CYP archive this is the 36-HQ layer.

CYP evidence:

```text
results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv
results_manifest/36HQ/CYP_high_quality_36_review_list.tsv
docs/audit/CYP_high_quality_36_ID_audit_note.txt
```

Reusable high-confidence rules:

| Criterion | Purpose |
|---|---|
| Complete or near-complete coding evidence | Avoid building claims from short fragments. |
| Family-defining domain support | Separate true family members from annotation noise. |
| Representative isoform selection | Prevent multiple isoforms from inflating family size. |
| Cross-species best-hit support | Improve naming and interpretation, without overclaiming orthology. |
| Expression detectability | Focus downstream analyses on genes with interpretable TPM/count evidence. |
| Manual caution labels | Keep borderline cases visible rather than silently removing them. |

For future families, keep the same separation:

```text
broad pool != high-confidence core set != special follow-up set
```

This distinction is one of the most important technical lessons from the CYP work.

## 6. Expression and Module Analysis

CYP implementation:

```text
scripts/R/classify_high_quality_CYP_modules_baseR.R
scripts/R/PCA_high_quality_CYP_logTPM_zscore_baseR.R
scripts/R/plot_CYP_module_heatmap_baseR.R
scripts/R/plot_CYP_module_scatter_baseR.R
results_manifest/36HQ/
```

Reusable expression workflow:

1. Build a family-specific TPM/count matrix for the high-confidence set.
2. Compute condition means and replicate-level variation.
3. Classify genes into expression modules using explicit thresholds.
4. Use PCA or clustering to inspect sample separation and within-condition dispersion.
5. Report candidate genes with both expression magnitude and confidence labels.
6. Avoid treating expression alone as proof of biochemical function.

For another gene family, module names should be biological but conservative. For example, use `Dan_high`, `Mul_high`, `broad_high`, `low_or_variable`, or similar transparent categories before assigning mechanistic interpretations.

## 7. Cross-Species or Reference Comparison

CYP implementation:

```text
results_manifest/Bmori_comparison/
scripts/python/make_bmori_public_cyp_tpm_tables.py
scripts/R/make_fig1_gene_order_final.R
```

Reusable comparison logic:

1. Select one or more biologically relevant reference species.
2. Build a comparable expression table for the same gene family.
3. Keep symbol-level comparisons separate from strict high-confidence core-set comparisons.
4. Label partial representatives and ambiguous matches.
5. Use comparative results as expression-pattern evidence, not direct functional proof.

For CarE/GST, the reference comparison should use curated family names and domain-supported representatives. If the reference family nomenclature is unstable, keep gene symbols and best-hit labels as provisional.

## 8. Ambiguous or Unknown Family Members

CYP implementation:

```text
results_manifest/unknownCYP/
logs/unknownCYP/
docs/notes/unknownCYP_*.md
scripts/R/*unknownCYP*.R
scripts/python/clean_unknownCYP_peptideAvailable14_headers.py
```

Reusable unknown-candidate workflow:

1. Start from the full ambiguous pool, not only high-expression candidates.
2. Record why each candidate is ambiguous.
3. Check peptide/ORF availability.
4. Apply domain and length caution labels.
5. Use phylogeny or reference placement only after unbiased inclusion rules are set.
6. Separate recovered high-confidence candidates from candidates that remain uncertain.

This layer is especially useful for other families because RNA-seq assemblies often contain partial transcripts, isoform fragments, and annotation conflicts.

## 9. Candidate Prioritization and Validation Planning

CYP implementation:

```text
results_manifest/RTqPCR/
docs/workflow.md
```

Reusable prioritization criteria:

| Criterion | Interpretation |
|---|---|
| High expression | Candidate is detectable and biologically plausible. |
| Condition contrast | Candidate may be related to diet, treatment, tissue, or phenotype differences. |
| Domain completeness | Candidate is less likely to be a transcript fragment. |
| Reference-family support | Candidate can be named and discussed more cautiously. |
| Replicate behavior | Candidate is robust or biologically variable. |
| Assay feasibility | Candidate has usable sequence for primers or downstream validation. |

Keep validation planning separate from discovery. In the public archive, final primers or assay sequences should be added only when they are intended to be part of the formal methods record.

## 10. Documentation Pattern for Each Family Project

Each future family project should have the following minimum public-safe files:

```text
README.md
docs/workflow.md
docs/gene_family_method_blueprint.md
docs/script_provenance_index.md
docs/data_versions.md
docs/archive_status.md
config/rnaseq_samples.tsv
environment/software_versions.tsv
results_manifest/results_manifest.tsv
results_manifest/<family>_screening/
results_manifest/<family>_broad_pool/
results_manifest/<family>_high_confidence/
results_manifest/<family>_unknown_or_ambiguous/
scripts/
logs/
data/README.md
```

Do not publish raw reads, large assemblies, full annotation databases, private HPC paths, or experimental data locations unless the project owner makes a separate data-release decision.

## 11. CYP-to-New-Family Conversion Checklist

Use this checklist when converting the CYP archive into a CarE, GST, or other gene family project.

- [ ] Replace target family name, synonyms, and family-specific caution language.
- [ ] Define accepted domain, InterPro, Pfam, GO, and keyword evidence.
- [ ] Select trusted reference species and reference sequence files.
- [ ] Create a broad candidate discovery table.
- [ ] Build transcript-peptide-gene mapping and representative isoform rules.
- [ ] Label fragments, noncanonical candidates, and ambiguous cases.
- [ ] Define high-confidence core-set rules before downstream interpretation.
- [ ] Generate family-specific TPM/count matrices.
- [ ] Classify expression modules with explicit thresholds.
- [ ] Run PCA, clustering, or replicate-dispersion checks.
- [ ] Keep cross-species symbol-level comparisons separate from strict core-set evidence.
- [ ] Review unknown or ambiguous family members with unbiased inclusion criteria.
- [ ] Produce candidate prioritization tables for validation.
- [ ] Record scripts, commands, versions, and small result manifests.
- [ ] Keep large experimental data local/private unless separately approved for release.

## 12. Interpretation Guardrails

The CYP project uses cautious interpretation, and the same guardrails should be retained for other families.

Allowed:

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

For CarE, GST, or other families, replace CYP-specific biological interpretation with family-specific but similarly conservative wording.
