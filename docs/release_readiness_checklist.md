# Release Readiness Checklist

Use this checklist before creating the first GitHub release, for example `v0.1-cyp-archive`.

## Required Before Release

- [ ] Confirm repository license and add `LICENSE` if appropriate.
- [ ] Confirm citation metadata and add `CITATION.cff` if appropriate.
- [x] Open GitHub issues for release decisions and HPC/external-asset blockers that still need owner input.
- [ ] Review `docs/release_blockers.md`.
- [ ] Review `docs/release_gate_matrix.md`.
- [ ] Review `docs/release_notes_v0.1_draft.md`.
- [ ] Review `README.md` entry points from a fresh-reader perspective.
- [ ] Review `CONTRIBUTING.md` and the pull request template.
- [ ] Review `docs/workflow.md` for method-order consistency.
- [ ] Run `python scripts/python/update_public_checksums.py` after final documentation/script edits.
- [ ] Run `python scripts/python/validate_archive.py`.
- [ ] Confirm the GitHub Actions archive-validation workflow passes on `main`.
- [ ] Confirm public archive has no credentials, tokens, private keys, or internal-only paths.
- [ ] Confirm large/raw assets are not committed to Git.
- [ ] Confirm `logs/hpc_recovery/public_archive_sha256.tsv` is current.

## HPC Confirmation

- [x] Run the first live HPC software-version confirmation pass.
- [x] Update `environment/version_confirmation_checklist.tsv`.
- [x] Update `environment/software_versions.tsv`.
- [x] Search for the original 91-CYP candidate-generation command or script.
- [x] Record whether the original command was recovered or remains unavailable.
- [ ] Decide whether a deeper shell-history or backup-script search is still needed for 91-CYP.

## External Assets

- [x] Confirm experimental data remain private and local/HPC-only for this release.
- [x] Run first HPC external-asset inventory and selected checksum pass.
- [x] Fill initial located/checksum statuses in `results_manifest/external_assets_manifest.tsv`.
- [ ] Add private per-file manifests for large directories only if needed for local integrity checks.
- [ ] Do not add public accession, DOI, GitHub Release asset URL, or data storage URI unless a later owner-approved data-release decision is made.

## RT-qPCR

- [ ] Decide whether final primer sequences are part of this archive release.
- [ ] If yes, add `results_manifest/RTqPCR/final_primer_sequences.tsv`.
- [ ] Keep primer-design FASTA and bulky sequence sources outside Git.

## Suggested Release Notes

Initial release scope:

```text
First public methods-and-manifest archive for the CYP family study. Includes RNA-seq processing wrappers,
DESeq2 provenance, CYP discovery/QC layers, 36-HQ CYP analysis, B. mori comparison, RT-qPCR target
support, unknownCYP recheck, README coverage, checksums, and external-asset/version-confirmation
tracking. Raw reads, large FASTA, alignments, and bulky intermediate outputs remain outside Git and are not public in this release.
```
