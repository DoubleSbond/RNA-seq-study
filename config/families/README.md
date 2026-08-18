# Gene Family Configuration Files

This directory stores non-sensitive family-definition files used before screening detoxification-related gene families.

Each `<family>.yaml` defines the search vocabulary, domain evidence, reference support, completeness rules, and high-confidence criteria for one gene family. These files should be reviewed before any family-specific filtering or downstream expression interpretation.

## Required Files

```text
CYP.yaml
CarE.yaml
GST.yaml
UGT.yaml
SULT.yaml
ABC.yaml
```

## Required Fields

Each family config should include:

```yaml
target_family:
  short_name:
  full_name:
  analysis_status:
  accepted_keywords:
  excluded_keywords:
  domain_evidence:
    pfam:
    interpro:
    go:
  trusted_reference_sets:
  representative_isoform_rule:
  broad_pool_rule:
  high_confidence_rule:
  fragment_warning_rule:
  unknown_or_ambiguous_rule:
  validation_candidate_rule:
  interpretation_guardrail:
```

Values may start as `TBD`, but the high-confidence rule must be filled before core-set figures or biological claims are made.

## Public-Safety Rule

Do not include private storage paths, usernames, hostnames, credentials, unpublished accessions, or internal sample locations. Reference FASTA and raw sequence assets should be described by public-safe names and tracked in external manifests when needed.
