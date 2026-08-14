# CITATION.cff Draft Inputs

This file is a draft input sheet for a future `CITATION.cff`. It is not a formal citation file. Do not rename it to `CITATION.cff` until the owner confirms all public metadata.

## Draft Citation Metadata

| Field | Draft value | Owner action |
|---|---|---|
| Citation title | `RNA-seq and CYP family study reproducibility archive` | Confirm or revise. |
| Repository URL | `https://github.com/DoubleSbond/RNA-seq-study` | Confirm. |
| Release version | `v0.1-cyp-archive` | Confirm at release time. |
| Release date | `<YYYY-MM-DD>` | Fill when tagging release. |
| Authors | `<AUTHOR_1>`; `<AUTHOR_2>`; `<AUTHOR_3>` | Confirm names and order. |
| ORCID IDs | `<ORCID_IF_ANY>` | Add only if public and approved. |
| Affiliation | `<PUBLIC_AFFILIATION_IF_APPROVED>` | Optional. |
| Contact email | `<PUBLIC_CONTACT_EMAIL_IF_APPROVED>` | Optional; do not publish private email without approval. |
| Related DOI | `<MANUSCRIPT_OR_DATASET_DOI_IF_AVAILABLE>` | Optional. |
| Related accession | `<NOT_INCLUDED_FOR_CURRENT_PRIVATE_DATA_PHASE>` | Experimental data are not public in the current phase. |
| License | `<LICENSE_AFTER_OWNER_DECISION>` | Fill after issue #21 is resolved. |

## Draft YAML Shape

The following block is a planning aid only. It intentionally contains placeholders and should not be used as a formal `CITATION.cff` until reviewed.

```yaml
cff-version: 1.2.0
message: "If you use this archive, please cite it as below."
title: "RNA-seq and CYP family study reproducibility archive"
version: "v0.1-cyp-archive"
date-released: "<YYYY-MM-DD>"
url: "https://github.com/DoubleSbond/RNA-seq-study"
authors:
  - family-names: "<FAMILY_NAME>"
    given-names: "<GIVEN_NAMES>"
    orcid: "<ORCID_IF_ANY>"
preferred-citation:
  type: generic
  title: "RNA-seq and CYP family study reproducibility archive"
  authors:
    - family-names: "<FAMILY_NAME>"
      given-names: "<GIVEN_NAMES>"
  year: 2026
  url: "https://github.com/DoubleSbond/RNA-seq-study"
```

## Decision Links

- License decision: issue #21
- Citation metadata decision: issue #22
- Release blocker tracker: `docs/release_blockers.md`
- Citation/license decision note: `docs/citation_and_license_decisions.md`

## Finalization Checklist

- [ ] Owner confirms title.
- [ ] Owner confirms author names and order.
- [ ] Owner confirms whether ORCID IDs should be included.
- [ ] Owner confirms public affiliation/contact fields, if any.
- [ ] Owner confirms that no experimental-data DOI/accession is included for the current methods-only release.
- [ ] License decision has been made.
- [ ] `CITATION.cff` is generated from this draft.
- [ ] `python scripts/python/update_public_checksums.py` is run.
- [ ] `python scripts/python/validate_archive.py` passes.
