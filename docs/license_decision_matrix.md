# License Decision Matrix

This matrix summarizes license choices before adding a formal `LICENSE` file. It is not itself a license.

## Decision Boundary

No formal license has been added yet. Until a license is chosen, default copyright applies and reuse permissions are not clearly granted.

## Common Strategies

| Strategy | What it covers | Advantages | Cautions |
|---|---|---|---|
| Single permissive software license | Scripts, docs, and small tables under one license such as MIT/BSD/Apache | Simple for users to understand | Software licenses are not always ideal for data tables or documentation. |
| Software/data split | Scripts under MIT/BSD/Apache; docs and small tables under CC-BY-4.0 | Common for research archives; clearer data/documentation reuse | Requires explicit wording in README and possibly multiple license files. |
| Software only | `LICENSE` covers scripts; data/docs reuse described separately | Avoids accidentally over-licensing data | Users may be unsure about small tables unless README is explicit. |
| No public license yet | No formal reuse grant | Safest if policy is uncertain | Weakens reproducibility/reuse for public archive consumers. |

## Candidate Licenses

| License | Best fit | Notes |
|---|---|---|
| MIT | Scripts and small utilities | Short, permissive, widely recognized. |
| BSD-3-Clause | Scripts and small utilities | Permissive, academic-style, includes non-endorsement clause. |
| Apache-2.0 | Scripts and utilities | Permissive with explicit patent language; longer text. |
| CC-BY-4.0 | Documentation and small data/manifest tables | Good for attribution-based reuse of non-software materials. |
| Private data terms | Raw reads, large FASTA, alignments, private data assets | Experimental data remain in local/HPC storage and are not publicly licensed in the current methods-only archive. |

## Recommended Draft Position

For owner review, a clear split-license approach may fit this archive:

```text
Software scripts: MIT, BSD-3-Clause, or Apache-2.0
Documentation and small result manifests: CC-BY-4.0
Raw reads and large external assets: governed by the external archive terms
```

This is only a draft recommendation. The owner should confirm institutional expectations and intended reuse scope before adding formal license files.

## Files To Update After Decision

- `LICENSE`
- Optional `LICENSE-DATA` or README license section, if using a split strategy.
- `README.md`
- `docs/citation_and_license_decisions.md`
- `docs/release_blockers.md`
- `docs/release_notes_v0.1_draft.md`
- `logs/hpc_recovery/public_archive_sha256.tsv`

## Decision Links

- License decision issue: #21
- Citation metadata issue: #22
- Release blocker tracker: `docs/release_blockers.md`

## Finalization Checklist

- [ ] Owner chooses license strategy.
- [ ] Owner confirms whether a split license is acceptable.
- [ ] Any institutional or collaborator constraints are checked.
- [ ] Formal license file(s) are added.
- [ ] README and release notes describe the license scope clearly.
- [ ] `python scripts/python/update_public_checksums.py` is run.
- [ ] `python scripts/python/validate_archive.py` passes.
