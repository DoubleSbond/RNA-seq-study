# HPC Workspace Cleanup Runbook

This runbook standardizes cleanup of the exploratory HPC workspace used by the CYP study and future detoxification gene-family analyses.

The cleanup must be staged and reversible. Do not delete analysis files during the first pass.

## 1. Safety Principles

1. Inventory first, move later, delete last.
2. Never delete raw reads, assemblies, FASTA/FASTQ, alignments, databases, result tables, logs, or scripts during the first cleanup pass.
3. Any move must have a manifest entry recording old path, new path, size, timestamp, and checksum when practical.
4. Use `archive_pending/` or `legacy/` quarantine directories before permanent removal.
5. Keep public-safe manifests in GitHub; keep private HPC paths and raw data locations out of public files unless explicitly approved.
6. Separate home-level clutter from project-level structure.

## 2. Observed Current HPC Shape

From the user-provided listing, the home directory contains scattered early exploratory files:

```text
~/CYP3_BLASTp_nr.tsv
~/CYP5_ORF.pep.fa
~/CYP5_ORF_longest.pep.fa
~/CYP5_geneIDs.txt
~/CYP_RTqPCR_target_gene_ids.txt
~/CarE_DEGs.fasta
~/core3.ids
~/core3_Bmori.tsv
~/core3_Spodo.tsv
~/plot_fig1_overview_heatmap.R
~/trinity_results.tar.gz
~/rnaseq_data.tar.gz
~/bm_phase_detox/
~/ph/
~/scripts/
~/tmp/
~/tools/
```

The project directory `~/ph` is already closer to a project workspace:

```text
01_RawData
02_QualityControl
03_assembly
04_annotation
05_busco_results
06_DEGsAnalysis
07_functional_gene_families
07_homology
08_orthofinder
09_CYP_cross_species
09_CYP_phylogeny
09_CarE_priority
10_RTqPCR_CYP_primer_prep
11_unknownCYP_annotation
12_Bmori_RTqPCR_CYP_QC
12_housekeeper_reference
Bmori_public_RNAseq
Bombyx_mori
raw
ref
resources
results
scripts
logs
tmp
tools
db
```

## 3. Target HPC Workspace Layout

Use this layout for `~/ph` after cleanup:

```text
~/ph/
|-- 00_project_admin/
|   |-- inventories/
|   |-- manifests/
|   `-- cleanup_logs/
|-- 01_RawData/
|-- 02_QualityControl/
|-- 03_assembly/
|-- 04_annotation/
|-- 05_busco_results/
|-- 06_DEGsAnalysis/
|-- 07_family_analysis/
|   |-- CYP/
|   |   |-- 01_screening/
|   |   |-- 02_broad_pool/
|   |   |-- 03_high_confidence/
|   |   |-- 04_reference_comparison/
|   |   |-- 05_unknown_or_ambiguous/
|   |   `-- 06_validation_design/
|   |-- CarE/
|   |-- GST/
|   |-- UGT/
|   |-- SULT/
|   `-- ABC/
|-- 08_orthofinder/
|-- 09_reference_comparisons/
|-- 10_validation_design/
|-- ref/
|-- resources/
|-- db/
|-- scripts/
|-- logs/
|-- tools/
|-- tmp/
|-- legacy/
|-- archive_pending/
`-- README_HPC_WORKSPACE.md
```

Existing numbered directories do not need to be renamed immediately. The first cleanup pass should create the standard target directories and map old paths to new locations.

## 4. First-Pass Classification

### Keep in place initially

```text
01_RawData/
02_QualityControl/
03_assembly/
04_annotation/
05_busco_results/
06_DEGsAnalysis/
ref/
resources/
db/
tools/
logs/
scripts/
```

### Candidate for mapping into standardized family layers

```text
07_functional_gene_families/ -> 07_family_analysis/<family>/
09_CYP_cross_species/       -> 07_family_analysis/CYP/04_reference_comparison/
09_CYP_phylogeny/           -> 07_family_analysis/CYP/05_unknown_or_ambiguous/ or phylogeny subfolder
09_CarE_priority/           -> 07_family_analysis/CarE/06_validation_design/ or priority_planning/
10_RTqPCR_CYP_primer_prep/  -> 07_family_analysis/CYP/06_validation_design/
11_unknownCYP_annotation/   -> 07_family_analysis/CYP/05_unknown_or_ambiguous/
12_Bmori_RTqPCR_CYP_QC/     -> 07_family_analysis/CYP/06_validation_design/reference_qc/
12_housekeeper_reference/   -> 10_validation_design/housekeeper_reference/
Bmori_public_RNAseq/        -> 09_reference_comparisons/Bmori_public_RNAseq/
Bombyx_mori/                -> ref/Bombyx_mori/ or resources/Bombyx_mori/
```

### Home-level files to quarantine before moving

Create:

```text
~/ph/archive_pending/home_scattered_files_YYYYMMDD/
```

Then move only after manifesting. Candidate home-level scattered files include:

```text
~/CYP*.tsv
~/CYP*.fa
~/CYP*.txt
~/CarE_DEGs.fasta
~/core3*.tsv
~/core3.ids
~/plot_fig1_overview_heatmap.R
~/blastx_results.txt
~/step2b_blastx.log
```

Large tarballs should not be moved until their contents and checksums are recorded:

```text
~/trinity_results.tar.gz
~/rnaseq_data.tar.gz
~/ph/08_ppt_archive.tar.gz
```

## 5. Phase 0: Read-Only Inventory

Run the read-only inventory script from the repository:

```bash
bash scripts/shell/hpc_inventory_workspace.sh "$HOME" "$HOME/ph"
```

Expected outputs are written under:

```text
~/ph/00_project_admin/inventories/<timestamp>/
```

Review the inventory before any moves.

## 6. Phase 1: Create Standard Directories

After inventory review, create the standard directories only. This is safe and reversible:

```bash
mkdir -p ~/ph/00_project_admin/inventories
mkdir -p ~/ph/00_project_admin/manifests
mkdir -p ~/ph/00_project_admin/cleanup_logs
mkdir -p ~/ph/07_family_analysis/{CYP,CarE,GST,UGT,SULT,ABC}/{01_screening,02_broad_pool,03_high_confidence,04_reference_comparison,05_unknown_or_ambiguous,06_validation_design}
mkdir -p ~/ph/09_reference_comparisons
mkdir -p ~/ph/10_validation_design
mkdir -p ~/ph/legacy
mkdir -p ~/ph/archive_pending
```

## 7. Phase 2: Draft Move Manifest

Before moving files, make a TSV manifest:

```text
old_path	new_path	category	reason	move_status	checksum_status	notes
```

Only paths in this manifest should be moved.

## 8. Phase 3: Move With Manifest

Use `mv -n` for no-overwrite moves after review. Do not use `rm` in cleanup scripts.

Recommended first moves after manifest approval:

- home-level CYP exploratory files -> `archive_pending/home_scattered_files_<date>/`
- home-level CarE files -> `07_family_analysis/CarE/01_screening/` or `06_validation_design/` depending on evidence
- `09_CYP_cross_species` outputs -> CYP reference comparison layer
- `10_RTqPCR_CYP_primer_prep` -> CYP validation design layer
- `11_unknownCYP_annotation` -> CYP unknown/ambiguous layer

## 9. Phase 4: GitHub Sync

After HPC cleanup, update GitHub with only public-safe summaries:

- `docs/hpc_workspace_cleanup.md`
- `docs/archive_status.md`
- `docs/data_versions.md`
- `results_manifest/external_assets_manifest.tsv`
- `logs/hpc_recovery/*.tsv` if sanitized

Do not publish private absolute paths unless explicitly approved.

## 10. Completion Definition

HPC cleanup is considered complete when:

- read-only inventory is saved
- standard directories exist
- old-to-new move manifest is reviewed
- high-risk large files are checksummed or explicitly deferred
- scattered home-level project files are either moved to `archive_pending` or mapped to project layers
- no raw/large/private data is deleted
- GitHub has public-safe summary records
