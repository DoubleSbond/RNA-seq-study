# Draft Release Notes: v0.1-cyp-archive

This is a draft note for the first public archive release. It should be reviewed before creating a formal GitHub Release.

## Proposed Tag

```text
v0.1-cyp-archive
```

## Proposed Release Title

```text
First public CYP family study reproducibility archive
```

## Scope

This release would provide the first GitHub-suitable code-and-manifest archive for the RNA-seq and CYP family study. It focuses on reproducible scripts, lightweight result tables, curated manifests, and human-readable provenance records.

## Included

- RNA-seq processing wrapper scripts for read trimming, Trinity assembly, Salmon quantification, and InterProScan annotation.
- Sample metadata, assembly QC summaries, and Salmon mapping summaries.
- Gene-level DESeq2 script, calibration note, sanitized session information, and significant result table.
- 91-CYP discovery-layer candidate tables, gene IDs, TPM tables, B. mori best-hit support, and PC1-loading summaries.
- CYP screening QC tables for peptide/transcript/gene mapping, representative isoforms, length filtering, fragment/noncanonical flags, and seed-gene audits.
- 36-HQ CYP review tables, ID audit note, master summary, expression modules, PCA tables, Dan internal-variation tables, and supporting R scripts.
- Public B. mori midgut CYP TPM tables, Figure1 Ph-Bm overview inputs, and gene-ordering script.
- RT-qPCR target mapping, sequence-length index, B. mori multi-isoform QC, and Primer3 candidate summaries.
- unknownCYP review tables, peptide-availability status, high-TPM versus phylogeny mapping, integrated interpretation table, diagnostic tree, IQ-TREE report/log, and supporting scripts.
- External asset policy, external asset manifest, version-confirmation checklist, HPC confirmation runbook, public checksums, and archive validation script.
- GitHub Actions workflow for automatic archive validation.

## Not Included

The following remain outside Git by design:

- Raw FASTQ files.
- Full Trinity assemblies and large FASTA files.
- Salmon `quant.sf` directories and bulky quantification intermediates.
- Full BLAST, HMMER, DIAMOND, InterProScan, and database outputs.
- Large alignments, raw phylogeny FASTA inputs, and large figure source assets.
- Primer-design FASTA files and bulky sequence sources.
- Credentials, tokens, SSH keys, private config, and internal-only absolute paths.

## Reproducibility Notes

Before tagging this release, run:

```bash
python scripts/python/validate_archive.py
```

The validator checks required paths, the public SHA256 manifest, tracked large/raw-data file patterns, and common sensitive text patterns.

## Known Gaps

- Remaining HPC-side software versions still need confirmation in `environment/version_confirmation_checklist.tsv`.
- External storage URIs/checksums still need to be filled in `results_manifest/external_assets_manifest.tsv`.
- The exact original 91-CYP candidate-generation command sequence has not yet been recovered, although the restored candidate tables and public reconstruction utility are archived.
- Final RT-qPCR primer sequences should be added only if they become part of the formal release.
- License and citation metadata remain pending owner decision.

## Owner Decisions Needed Before Formal Release

- Choose repository license strategy.
- Confirm `CITATION.cff` metadata and author order.
- Decide whether final primer sequences belong in this Git release.
- Decide whether any small rendered figures should be attached as GitHub Release assets.
- Confirm external asset storage locations or accessions for large/raw assets.

## Suggested Release Body

```text
This first public archive release captures the GitHub-suitable reproducibility layer for the RNA-seq and CYP family study. It includes processing wrappers, DESeq2 provenance, CYP discovery and screening tables, the 36-HQ CYP analysis layer, B. mori comparison assets, RT-qPCR target-design summaries, unknownCYP recheck material, public checksums, and archive-validation tooling.

Raw sequencing reads, full assemblies, bulky search outputs, large alignments, and other large intermediates remain outside Git by design and should be referenced through the external asset manifest once public accessions or storage URIs are finalized.
```
