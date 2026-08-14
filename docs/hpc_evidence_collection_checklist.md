# HPC Evidence Collection Checklist

This checklist is for the next live HPC session. It turns the remaining
archive blockers into a short, auditable collection pass.

Use it together with `docs/hpc_confirmation_runbook.md`. Keep all raw data,
large FASTA/alignment files, private paths, credentials, and SSH material out
of Git.

## Collection Rules

- Work from the project directory on HPC, but publish only sanitized records.
- Replace private absolute paths with placeholders such as `<HPC_PROJECT_ROOT>`.
- Record checksums for large files or stable archive bundles, not the files
  themselves.
- If a command history contains tokens, private URLs, or account details, do
  not copy it directly. Summarize the public-safe command shape instead.
- Prefer small TSV/Markdown outputs that can be reviewed before committing.

## Evidence Targets

| Target | GitHub issue | Primary output to collect | Public file to update | Done criteria |
|---|---|---|---|---|
| Remaining tool versions | [#23](https://github.com/DoubleSbond/RNA-seq-study/issues/23) | `logs/hpc_recovery/hpc_tool_versions_to_confirm.tsv` | `environment/version_confirmation_checklist.tsv`; `environment/software_versions.tsv` | Pending tools have version, source, and status. |
| Original 91-CYP command sequence | [#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) | Sanitized notes or script/path evidence | `docs/workflow.md`; `results_manifest/91CYP/README.md` | Either exact command is recovered, or gap is explicitly marked not recovered. |
| External large-asset checksums | [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | `logs/hpc_recovery/external_asset_checksums.tsv` | `results_manifest/external_assets_manifest.tsv` | Required assets have URI/accession, checksum, size, and version/source notes. |
| RT-qPCR primer release scope | [#26](https://github.com/DoubleSbond/RNA-seq-study/issues/26) | Owner-approved primer table or decision note | `results_manifest/RTqPCR/README.md`; optional small primer TSV | Final primer handling is clear: Git table, release supplement, or deferred/private. |
| unknownCYP alignment provenance | [#25](https://github.com/DoubleSbond/RNA-seq-study/issues/25) | Alignment/reference checksums and MAFFT version | `results_manifest/external_assets_manifest.tsv`; `docs/notes/unknownCYP_phylogeny_input_preparation_summary.md` | Diagnostic tree inputs can be traced without committing large alignment data. |

## Minimal HPC Commands

Run the archived version collector from the repository root or from a synced
copy of the repository on HPC:

```bash
bash scripts/shell/collect_hpc_tool_versions.sh \
  logs/hpc_recovery/hpc_tool_versions_to_confirm.tsv
```

Prepare a local HPC-only asset path table:

```text
asset_id	path
raw_reads	<PATH_TO_RAW_READS_DIR_OR_ARCHIVE>
trinity_assembly	<PATH_TO_TRINITY_FASTA_OR_ARCHIVE>
interproscan_full_tsv	<PATH_TO_INTERPROSCAN_TSV_OR_ARCHIVE>
blast_hmmer_outputs	<PATH_TO_SEARCH_OUTPUTS_OR_ARCHIVE>
rtqpcr_design_fasta	<PATH_TO_RTQPCR_DESIGN_FASTA_OR_ARCHIVE>
unknowncyp_alignment	<PATH_TO_UNKNOWNCYP_ALIGNMENT_OR_ARCHIVE>
unknowncyp_reference_fasta	<PATH_TO_UNKNOWNCYP_REFERENCE_FASTA_OR_ARCHIVE>
```

Then run:

```bash
bash scripts/shell/collect_external_asset_checksums.sh \
  external_asset_paths.tsv \
  logs/hpc_recovery/external_asset_checksums.tsv
```

For the 91-CYP command search, search scripts, logs, and shell histories only
within the project areas that the owner approves:

```bash
grep -RIn \
  -e "CYP_candidates_step1" \
  -e "CYP_candidates_step2" \
  -e "CYP_confirmed_geneids" \
  -e "PF00067" \
  -e "IPR001128" \
  -e "cytochrome P450" \
  <HPC_PROJECT_ROOT> 2>/dev/null
```

## Review Before Commit

Before bringing HPC-derived records into Git:

- Check that every candidate file is small text, not raw data.
- Scan for private paths, usernames, tokens, private keys, and passwords.
- Confirm that checksums point to external assets rather than Git-tracked
  large files.
- Update `logs/hpc_recovery/public_archive_sha256.tsv` after final edits.
- Run `python scripts/python/validate_archive.py`.

## Expected Public Outputs

The final public update from this pass should normally include only:

- Updated version tables under `environment/`.
- Updated external asset manifest under `results_manifest/`.
- Sanitized notes in `docs/` or `logs/hpc_recovery/`.
- Optional small RT-qPCR primer table, if approved by the owner.
- Refreshed `logs/hpc_recovery/public_archive_sha256.tsv`.
