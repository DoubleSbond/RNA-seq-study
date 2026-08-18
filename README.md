# CYP Family Study Archive

This repository organizes the reproducible code archive for the CYP family study after RNA-seq assembly and CYP gene family screening.

## Purpose

The archive is intended to preserve:

- Commands used during transcriptome assembly, CYP screening, annotation, filtering, and downstream summaries.
- Python and R scripts used for data processing, quality checks, and visualization.
- Configuration files and software environment records.
- Small result manifests and tabular summaries suitable for GitHub.
- Logs that document how analyses were run.

It is also intended to serve as a portable technical template for other RNA-seq-based gene family studies, such as CarE, GST, UGT, SULT, ABC transporter, or other detoxification-related families. The CYP-specific evidence is kept explicit so the reusable workflow can be adapted without losing the original project record.

Large raw data and bulky intermediate outputs should not be committed directly.
For the current project phase, experimental data remain private in local/HPC
storage. GitHub records only method files and sanitized asset inventories, not
public data accessions or data-release locations.

## Repository Layout

```text
.
|-- config/              # Parameters, sample sheets, family definitions, and tool settings
|-- data/                # README only; raw data is tracked outside Git
|-- docs/                # Workflow notes, methods, standardization rules, and provenance records
|-- environment/         # Conda/R/session/container environment records
|-- logs/                # Curated run logs and command histories
|-- results_manifest/    # Small file inventories and result summaries
|-- scripts/             # Reusable Python, R, and shell scripts
|-- sources/             # Local read-only reference material, not committed by default
`-- README.md
```

## Quick Start

1. Place reusable analysis scripts in `scripts/`.
2. Put sample metadata, parameter files, and non-sensitive config in `config/`.
3. For a new detoxification gene family, fill `config/families/<family>.yaml` before screening.
4. Follow `docs/family_standardization.md` to keep screening, broad-pool, high-confidence, unknown, and validation layers separate.
5. Record software versions in `environment/`.
6. Record command history and run provenance in `logs/`.
7. Add small summary tables and file manifests to `results_manifest/`.
8. Keep large FASTQ/FASTA/BAM/SAM, database, and assembled transcriptome files outside Git.

## Standardized Family Workflow

Future CYP-like analyses should use the same stage-gated structure:

```text
01_screening
02_broad_pool
03_high_confidence
04_reference_comparison
05_unknown_or_ambiguous
06_validation_design
```

The key rule is:

```text
broad discovery pool != high-confidence core set != ambiguous follow-up set != validation candidate set
```

For the legacy CYP archive, the historical equivalents are `CYP_screening`, `91CYP`, `36HQ`, `Bmori_comparison`, `unknownCYP`, and `RTqPCR`. These legacy names are retained for provenance; new families should use the standardized layer names from the start.

Standardization entry points:

- `docs/family_standardization.md`: standard layers, naming rules, stage gates, and interpretation guardrails.
- `docs/gene_family_method_blueprint.md`: portable RNA-seq-to-gene-family workflow narrative.
- `config/families/`: family-specific definition templates for CYP, CarE, GST, UGT, SULT, and ABC.

## Data Policy

Commit:

- Small text tables, manifests, metadata, and checksums.
- Final curated summaries needed to understand the analysis.
- Scripts, configs, and environment files.

Do not commit:

- Raw sequencing reads.
- Large transcriptome assemblies.
- Large BLAST/HMMER databases.
- Bulky intermediate outputs.
- Credentials, private keys, tokens, or internal-only HPC paths that should not be public.

## Current Archive Contents

This repository now contains the first public, GitHub-suitable archive of the project. The most useful entry points are:

- `docs/archive_status.md`: current archive status and remaining gaps.
- `docs/archive_completeness_audit.md`: README coverage and omission-check summary.
- `docs/external_archive_policy.md`: policy for raw data, figures, FASTA, alignments, and other external assets.
- `docs/hpc_confirmation_runbook.md`: final HPC-side version/checksum confirmation workflow.
- `docs/hpc_evidence_collection_checklist.md`: concise checklist for the next live HPC evidence-collection pass.
- `docs/release_readiness_checklist.md`: checklist for a first archive release.
- `docs/release_gate_matrix.md`: release gate table for deciding whether a formal tag is ready.
- `docs/release_blockers.md`: remaining release blockers grouped by owner decision, HPC confirmation, and external assets.
- `docs/release_notes_v0.1_draft.md`: draft release notes for `v0.1-cyp-archive`.
- `docs/citation_and_license_decisions.md`: citation metadata and license decision notes.
- `docs/citation_cff_draft.md` and `docs/license_decision_matrix.md`: draft-only citation/license planning aids.
- `docs/workflow.md`: end-to-end workflow from RNA-seq assembly to CYP interpretation.
- `docs/gene_family_method_blueprint.md`: reusable RNA-seq-to-gene-family study template for CYP, CarE, GST, and similar families.
- `docs/family_standardization.md`: standard layer names, stage gates, naming rules, and reusable structure for future detoxification gene families.
- `config/families/`: family-definition templates for CYP, CarE, GST, UGT, SULT, and ABC.
- `docs/collection_narrative_audit.md`: evidence audit for the recovered local/HPC material.
- `docs/script_provenance_index.md`: public scripts mapped to workflow blocks.
- `docs/data_versions.md`: 91-CYP, 36-HQ, matched-symbol, RT-qPCR, and unknownCYP analysis layers.
- `results_manifest/`: small result tables and manifests suitable for GitHub.
- `scripts/`: public R/Python scripts reconstructed from the analysis.
- `CONTRIBUTING.md`: maintenance rules for public-safe archive updates.

## Archive QA

Run the local archive validator before release-oriented updates:

```bash
python scripts/python/update_public_checksums.py
python scripts/python/validate_archive.py
```

The checksum updater refreshes the public SHA256 manifest for Git-tracked public files. The validator then checks required paths, public SHA256 entries, tracked large/raw-data file patterns, and common sensitive text patterns. Neither command requires HPC access.

The same validator is also run by GitHub Actions for pushes to `main` and pull requests.

## Archived Analysis Layers

The current `main` branch includes:

- Gene-level DESeq2 provenance and significant result table.
- RNA-seq sample metadata, upstream processing wrappers, Trinity assembly QC, and Salmon mapping summaries.
- Annotation summary counts and CYP screening QC tables.
- 91-CYP discovery-layer summaries, stepwise candidate tables, B. mori best-hit support, PC1 loading tables, and TPM tables.
- 36-HQ CYP core set, review list, expression modules, PCA tables, and supporting R scripts.
- Public B. mori midgut CYP TPM tables and Figure1 Ph-Bm overview inputs.
- RT-qPCR target-design and B. mori target-QC summary tables.
- 36-HQ Dan internal-variation and module-figure provenance tables/scripts.
- unknownCYP recheck tables, high-TPM vs phylogeny mapping, diagnostic tree output, and supporting scripts.

Large raw reads, assemblies, alignments, raw FASTA files, databases, and bulky logs remain outside Git by design.

## Remaining Work

The main remaining gaps are:

- Recover the exact original 91-CYP candidate generation command sequence, if it still exists on HPC. The current archive already includes the recovered candidate tables and a public reconstruction utility.
- Maintain sanitized private asset inventories in `results_manifest/external_assets_manifest.tsv`; do not publish experimental data locations unless a later data-release decision is made.
- Add final primer sequences if RT-qPCR primer outputs become part of the formal archive.
- Confirm citation metadata and repository license before creating a formal release.
