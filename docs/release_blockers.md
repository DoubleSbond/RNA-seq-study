# Release Blocker Tracker

This tracker consolidates the remaining work before a formal `v0.1-cyp-methods-archive` release. It separates items that can be handled in GitHub from items that require owner decisions, HPC access, or private-data inventory records.

## Current Readiness

| Area | Status | Notes |
|---|---|---|
| Repository structure | Ready | README coverage, docs, scripts, manifests, logs, environment records, and data policy are in place. |
| Archive validation | Ready | `scripts/python/validate_archive.py` passes locally and is wired into GitHub Actions. |
| Checksum maintenance | Ready | `scripts/python/update_public_checksums.py` refreshes `logs/hpc_recovery/public_archive_sha256.tsv`. |
| Public-safe maintenance workflow | Ready | `CONTRIBUTING.md`, PR template, and issue templates are available. |
| Release notes draft | Ready for owner review | See `docs/release_notes_v0.1_draft.md`. |
| Scientific narrative | Ready with documented caveats | Workflow and audit documents support the narrative while marking unresolved HPC-dependent gaps. |

## Tracking Issues

| Issue | Type | Topic |
|---|---|---|
| [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21) | Owner decision | Repository license strategy |
| [#22](https://github.com/DoubleSbond/RNA-seq-study/issues/22) | Owner decision | `CITATION.cff` metadata |
| [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | HPC confirmation | Remaining software versions; first live confirmation pass completed |
| [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | HPC confirmation / archive gap | Original 91-CYP candidate-generation command |
| [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Private data asset record | Sanitized inventory for raw/large assets; first HPC inventory completed |
| [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Owner decision | RT-qPCR final primer release scope |

## Owner Decisions

| Blocker | Current file | Next action | Blocks formal release? |
|---|---|---|---|
| Repository license | `docs/citation_and_license_decisions.md`; `docs/license_decision_matrix.md`; [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21) | Choose license strategy for software, docs, and small tables. | Yes |
| Citation metadata | `docs/citation_and_license_decisions.md`; `docs/citation_cff_draft.md`; [#22](https://github.com/DoubleSbond/RNA-seq-study/issues/22) | Confirm title, author order, ORCID IDs if any, affiliation/contact text, and related DOI/manuscript links. | Yes |
| RT-qPCR final primer inclusion | `docs/release_readiness_checklist.md`; `results_manifest/RTqPCR/README.md`; [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Decide whether final primer sequences belong in Git, a release asset, or remain outside this release. | Maybe |
| Rendered figure release assets | `docs/external_archive_policy.md`; `docs/release_notes_v0.1_draft.md` | Decide whether small final figures should be attached to the GitHub Release. | No, if source tables/scripts are enough |
| Private data handling | `results_manifest/external_assets_manifest.tsv`; `logs/hpc_recovery/hpc_external_asset_inventory_20260814.tsv`; [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Keep experimental data local/HPC-only; record only sanitized inventory metadata in GitHub. | Yes |

## HPC-Dependent Confirmation

| Blocker | Current file | Next action | Notes |
|---|---|---|---|
| Remaining software versions | `environment/version_confirmation_checklist.tsv`; `environment/software_versions.tsv`; `logs/hpc_recovery/hpc_tool_versions_confirmed_20260814.tsv`; [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | Review and close issue if owner accepts the recovered/live confirmation records. | First live HPC confirmation pass completed on 2026-08-14. |
| Original 91-CYP command sequence | `docs/workflow.md`; `results_manifest/91CYP/README.md`; `logs/hpc_recovery/hpc_91cyp_command_search_20260814.md`; [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | Continue shell-history or deeper backup-script search if exact command is still required. | First HPC search found source lists/scripts but not a single exact command. |
| Private asset checksums | `results_manifest/external_assets_manifest.tsv`; `logs/hpc_recovery/hpc_external_asset_inventory_20260814.tsv`; [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Add per-file manifests for local integrity only if needed; do not publish data access locations. | First HPC inventory completed; key single-file checksums recorded. |
| RT-qPCR source FASTA and primer material | `results_manifest/RTqPCR/README.md`; `results_manifest/external_assets_manifest.tsv`; [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Confirm whether final primer table exists and whether source FASTA should be checksummed externally. | Git currently tracks target/QC summaries only. |

The next live HPC collection pass is consolidated in `docs/hpc_evidence_collection_checklist.md`.

## External Asset Records

| Asset ID | Current status | Release handling |
|---|---|---|
| `raw_reads` | `located_hpc_private_needs_manifest` | Keep local/HPC-only; record sample mapping and checksum only as sanitized metadata if needed. |
| `trinity_assembly` | `located_hpc_private_checksum_recorded` | Keep FASTA outside Git; record checksum/version without publishing data location. |
| `trimmed_reads` | `located_hpc_needs_manifest` | Optional external record if regenerated data should be preserved. |
| `rendered_figures` | `located_hpc_policy_pending` | Keep outside Git unless owner separately approves small figure release assets. |
| `figure_source_assets` | `pending_policy_decision` | Keep large editable/source assets outside Git. |
| `rtqpcr_design_fasta` | `located_hpc_needs_scope_decision` | Keep FASTA outside Git; record checksum only as sanitized metadata if release-relevant. |
| `rtqpcr_final_primers` | `pending_project_decision` | Add small Git table only if owner decides it belongs in the release. |
| `unknowncyp_alignment` | `located_hpc_private_checksum_recorded` | Keep alignment source outside Git; record checksum and MAFFT version. |
| `unknowncyp_reference_fasta` | `located_hpc_private_needs_manifest` | Record references/checksums as sanitized metadata only. |

## GitHub-Side Completion Criteria

Before tagging `v0.1-cyp-archive`, GitHub-side criteria are:

- `python scripts/python/update_public_checksums.py` has been run after final edits.
- `python scripts/python/validate_archive.py` passes.
- GitHub Actions archive-validation workflow passes on `main`.
- `docs/release_gate_matrix.md` has been reviewed for required and deferrable gates.
- `docs/release_notes_v0.1_draft.md` has been reviewed and converted into final release notes.
- Open GitHub issues exist for any remaining owner/HPC/external-storage decisions that are intentionally deferred. Current core tracking issues are [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21)-[#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26).

## Recommended Next Sequence

1. Owner decides license and citation metadata.
2. Add `LICENSE` and `CITATION.cff`, if approved.
3. Run final HPC confirmation pass for versions, original 91-CYP command search, and external checksums.
4. Keep `results_manifest/external_assets_manifest.tsv` as a sanitized private-data inventory, without publishing data access locations.
5. Decide RT-qPCR primer release scope.
6. Refresh checksums and run archive validation.
7. Create tag/release `v0.1-cyp-archive`.
