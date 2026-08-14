# Release Blocker Tracker

This tracker consolidates the remaining work before a formal `v0.1-cyp-archive` release. It separates items that can be handled in GitHub from items that require owner decisions, HPC access, or external storage records.

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
| [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | HPC confirmation | Remaining software versions |
| [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | HPC confirmation / archive gap | Original 91-CYP candidate-generation command |
| [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | External asset record | Storage URIs and checksums for raw/large assets |
| [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Owner decision | RT-qPCR final primer release scope |

## Owner Decisions

| Blocker | Current file | Next action | Blocks formal release? |
|---|---|---|---|
| Repository license | `docs/citation_and_license_decisions.md`; `docs/license_decision_matrix.md`; [#21](https://github.com/DoubleSbond/RNA-seq-study/issues/21) | Choose license strategy for software, docs, and small tables. | Yes |
| Citation metadata | `docs/citation_and_license_decisions.md`; `docs/citation_cff_draft.md`; [#22](https://github.com/DoubleSbond/RNA-seq-study/issues/22) | Confirm title, author order, ORCID IDs if any, affiliation/contact text, and related DOI/manuscript links. | Yes |
| RT-qPCR final primer inclusion | `docs/release_readiness_checklist.md`; `results_manifest/RTqPCR/README.md`; [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Decide whether final primer sequences belong in Git, a release asset, or remain outside this release. | Maybe |
| Rendered figure release assets | `docs/external_archive_policy.md`; `docs/release_notes_v0.1_draft.md` | Decide whether small final figures should be attached to the GitHub Release. | No, if source tables/scripts are enough |
| External storage target | `results_manifest/external_assets_manifest.tsv`; [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Decide storage targets for raw reads, assemblies, alignments, FASTA, figures, and primer-design sources. | Yes for fully public release |

## HPC-Dependent Confirmation

| Blocker | Current file | Next action | Notes |
|---|---|---|---|
| Remaining software versions | `environment/version_confirmation_checklist.tsv`; `environment/software_versions.tsv`; [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | Run `scripts/shell/collect_hpc_tool_versions.sh` on HPC. | Pending: R, fastp, Trinity, BLAST, HMMER, DIAMOND, seqkit, MAFFT. |
| Original 91-CYP command sequence | `docs/workflow.md`; `results_manifest/91CYP/README.md`; [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | Search HPC command histories/scripts using `docs/hpc_confirmation_runbook.md`. | Restored tables and public reconstruction utility are already archived. |
| External asset checksums | `results_manifest/external_assets_manifest.tsv`; [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Prepare asset path list and run `scripts/shell/collect_external_asset_checksums.sh` where assets are staged. | Do not commit large files. |
| RT-qPCR source FASTA and primer material | `results_manifest/RTqPCR/README.md`; `results_manifest/external_assets_manifest.tsv`; [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Confirm whether final primer table exists and whether source FASTA should be checksummed externally. | Git currently tracks target/QC summaries only. |

The next live HPC collection pass is consolidated in `docs/hpc_evidence_collection_checklist.md`.

## External Asset Records

| Asset ID | Current status | Release handling |
|---|---|---|
| `raw_reads` | `pending_external_record` | Record SRA/accession or safe storage URI plus sample mapping and checksum. |
| `trinity_assembly` | `pending_external_record` | Keep FASTA outside Git; record URI/checksum/version. |
| `trimmed_reads` | `pending_external_record` | Optional external record if regenerated data should be preserved. |
| `rendered_figures` | `pending_policy_decision` | Attach to GitHub Release or external repository only if desired. |
| `figure_source_assets` | `pending_policy_decision` | Keep large editable/source assets outside Git. |
| `rtqpcr_design_fasta` | `pending_external_record` | Keep FASTA outside Git; record URI/checksum if release-relevant. |
| `rtqpcr_final_primers` | `pending_project_decision` | Add small Git table only if owner decides it belongs in the release. |
| `unknowncyp_alignment` | `pending_external_record` | Keep alignment source outside Git if large; record checksum and MAFFT version. |
| `unknowncyp_reference_fasta` | `pending_external_record` | Record references/source accessions and checksum. |

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
4. Fill `results_manifest/external_assets_manifest.tsv` with public-safe URIs/checksums.
5. Decide RT-qPCR primer release scope.
6. Refresh checksums and run archive validation.
7. Create tag/release `v0.1-cyp-archive`.
