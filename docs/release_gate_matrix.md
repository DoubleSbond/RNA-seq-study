# Release Gate Matrix

This matrix defines the practical gates for a first public archive tag such as
`v0.1-cyp-archive`. It is meant to be checked after the GitHub archive is stable
and before creating a formal release.

## Gate Summary

| Gate | Required for tag? | Owner | Evidence file | Current status |
|---|---|---|---|---|
| Public repository structure | Yes | Codex / owner review | `README.md`; `docs/archive_status.md` | Ready |
| Archive validation | Yes | Codex / GitHub Actions | `scripts/python/validate_archive.py`; `.github/workflows/archive-validation.yml` | Ready locally; confirm Actions on `main` |
| Public checksum manifest | Yes | Codex | `logs/hpc_recovery/public_archive_sha256.tsv` | Ready, refresh after final edits |
| Large/raw data exclusion | Yes | Codex / owner review | `.gitignore`; `docs/external_archive_policy.md`; validator output | Ready |
| Sensitive material exclusion | Yes | Codex / owner review | validator output; manual review | Ready locally; repeat after HPC-derived updates |
| License decision | Yes | Owner | `docs/license_decision_matrix.md`; issue [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21) | Pending owner decision |
| Citation metadata | Yes | Owner | `docs/citation_cff_draft.md`; issue [#22](https://github.com/DoubleSbond/RNA-seq-study/issues/22) | Pending owner decision |
| Remaining HPC software versions | Yes for full reproducibility | Owner / HPC pass | `environment/version_confirmation_checklist.tsv`; issue [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | Pending HPC confirmation |
| Original 91-CYP command recovery | Preferred; may be released as known gap | Owner / HPC pass | `docs/workflow.md`; `results_manifest/91CYP/README.md`; issue [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | Pending HPC search |
| External asset URIs/checksums | Yes for fully public data traceability | Owner / storage decision | `results_manifest/external_assets_manifest.tsv`; issue [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Pending external records |
| RT-qPCR primer release scope | Required if primers are claimed as release content | Owner | `results_manifest/RTqPCR/README.md`; issue [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Pending owner decision |
| Release notes | Yes | Owner / Codex | `docs/release_notes_v0.1_draft.md` | Draft ready for review |

## Minimum GitHub-Only Release Candidate

The repository can be treated as a GitHub-only release candidate when:

- `scripts/python/update_public_checksums.py` has been run after all final
  documentation and script edits.
- `scripts/python/validate_archive.py` passes locally.
- GitHub Actions archive validation passes on `main`.
- The owner either resolves license/citation decisions or explicitly defers
  a formal release tag until those files can be added.
- Remaining HPC/external-asset gaps are listed in GitHub issues and release
  notes, not hidden in private notes.

This GitHub-only state is useful for review, collaboration, and archive
development, but it is not the same as a complete public data release.

## Full Public Archive Release

A full public archive release additionally needs:

- A chosen license strategy and any approved `LICENSE` file.
- Confirmed citation metadata and any approved `CITATION.cff`.
- Confirmed software versions for the remaining HPC tools.
- External storage identifiers, accessions, or durable URIs plus checksums for
  raw reads, assemblies, large FASTA/alignment inputs, and other large assets.
- A clear decision on whether final RT-qPCR primer sequences are included,
  attached as release assets, or deferred.

## Release Decision Rule

Use this rule before tagging:

```text
Tag only if every "Required for tag?" item is either resolved in public files
or explicitly deferred in release notes with an open tracking issue.
```

The recommended conservative path is to wait for license and citation metadata
before creating the formal tag.
