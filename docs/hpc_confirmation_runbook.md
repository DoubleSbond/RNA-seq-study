# HPC Confirmation Runbook

This runbook is for the final archive-confirmation pass after logging into the HPC environment.

## Goals

1. Confirm software versions that are still marked as pending.
2. Record sanitized private-data asset locations, file sizes, and checksums for large assets kept outside Git.
3. Search for the exact original command or script that generated the 91-CYP candidate tables.
4. Decide whether final RT-qPCR primer sequences should be added as a small Git-tracked table.

## 1. Confirm Tool Versions

From the HPC project environment, run:

```bash
bash scripts/shell/collect_hpc_tool_versions.sh logs/hpc_recovery/hpc_tool_versions_to_confirm.tsv
```

Then use the output to update:

```text
environment/version_confirmation_checklist.tsv
environment/software_versions.tsv
```

Keep tools unavailable on HPC as `not_available` or `not_used`, not blank.

## 2. Collect Private Asset Checksums

Create a two-column TSV locally on HPC:

```text
asset_id	path
raw_reads	<PATH_TO_RAW_READS_DIR_OR_ARCHIVE>
trinity_assembly	<PATH_TO_TRINITY_FASTA>
unknowncyp_alignment	<PATH_TO_UNKNOWNCYP_ALIGNMENT>
```

Then run:

```bash
bash scripts/shell/collect_external_asset_checksums.sh \
  external_asset_paths.tsv \
  logs/hpc_recovery/external_asset_checksums.tsv
```

Use the output to fill:

```text
results_manifest/external_assets_manifest.tsv
```

If an asset is a directory, checksum either a stable compressed archive or a manifest of all files under it.
Do not publish real private paths, public accessions, or download URIs unless
the project owner later approves a data-release plan.

## 3. Search for the Original 91-CYP Candidate Command

Search likely HPC areas for the original command or script:

```bash
grep -RIn \
  -e "CYP_candidates_step1" \
  -e "CYP_candidates_step2" \
  -e "PF00067" \
  -e "IPR001128" \
  -e "cytochrome P450" \
  <HPC_PROJECT_ROOT>/ph 2>/dev/null
```

If found, sanitize paths and credentials before publishing. If no exact command is found, keep the current public reconstruction script and document the original command as not recovered.

## 4. RT-qPCR Primer Decision

If final primer sequences are ready and small, add a table such as:

```text
results_manifest/RTqPCR/final_primer_sequences.tsv
```

Recommended columns:

```text
primer_id	target_species	target_symbol	target_gene_id	forward_primer	reverse_primer	amplicon_bp	design_source	validation_status	notes
```

Do not commit large FASTA sequence sources; record them in `results_manifest/external_assets_manifest.tsv`.

## Safety Rules

- Do not paste tokens, passwords, private keys, or private SSH material into Git.
- Replace private absolute paths with placeholders before publishing.
- Keep raw reads, large FASTA, alignments, and bulky tool outputs outside Git.
- Commit only small text summaries, manifests, scripts, and sanitized notes.
