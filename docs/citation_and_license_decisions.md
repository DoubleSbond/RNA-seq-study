# Citation and License Decisions

This repository is approaching a release-ready archive, but citation and licensing should be confirmed by
the project owner before adding formal files such as `CITATION.cff` or `LICENSE`.

Draft planning aids:

- `docs/citation_cff_draft.md`
- `docs/license_decision_matrix.md`

## Citation Metadata To Confirm

Before adding `CITATION.cff`, confirm:

- Repository title to cite.
- Author names and order.
- ORCID IDs, if any.
- Institution or affiliation text, if desired.
- Preferred contact email, if desired.
- Release version and date.
- Related manuscript, preprint, or dataset DOI, if any.

Suggested title placeholder:

```text
RNA-seq and CYP family study reproducibility archive
```

## License Decision To Confirm

Before adding `LICENSE`, decide whether scripts, documentation, and small result manifests should share the
same license.

Common choices:

- MIT: permissive software license, often suitable for scripts.
- Apache-2.0: permissive software license with explicit patent language.
- BSD-3-Clause: permissive academic-style software license.
- CC-BY-4.0: often suitable for documentation and data tables, not usually used for software.
- No public license yet: default copyright applies; reuse is not clearly granted.

Possible split approach:

```text
Software scripts: MIT / Apache-2.0 / BSD-3-Clause
Documentation and small tables: CC-BY-4.0 or project-specific terms
Raw/large data: private local/HPC storage; no public data-release terms in the current phase
```

No license file has been added yet because this choice should be made by the project owner.

Tracking issues:

- License strategy: [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21)
- Citation metadata: [#22](https://github.com/DoubleSbond/RNA-seq-study/issues/22)
