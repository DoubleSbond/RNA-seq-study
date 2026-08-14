# Changelog

This changelog tracks archive-level changes to the CYP family study repository.

## Unreleased

### Added

- Repository skeleton for reproducible RNA-seq/CYP family study archiving.
- RNA-seq upstream wrapper scripts for fastp, Trinity, Salmon, and InterProScan.
- Gene-level DESeq2 public script, calibration/session records, and significant-result table.
- 91-CYP discovery-layer candidate tables, TPM tables, best-hit tables, PC1-loading tables, and a public CYP/P450 filtering reconstruction script.
- CYP screening QC tables for peptide/transcript/gene mapping, representative isoforms, length filters, fragment/noncanonical flags, and seed-gene audits.
- 36-HQ CYP review tables, ID audit note, module/PCA tables, Dan internal-variation tables, and plotting/summary scripts.
- B. mori public midgut CYP TPM tables, Figure1 inputs, and Figure1 gene-ordering script.
- RT-qPCR target mapping, sequence-length index, and B. mori target-QC/Primer3 summary tables.
- unknownCYP review, peptide-availability, diagnostic tree, IQ-TREE report, and supporting scripts.
- External asset policy, external asset manifest, version confirmation checklist, and HPC confirmation runbook.
- README coverage and archive completeness audit.
- Public archive validation script and GitHub Actions archive-validation workflow.
- Draft release notes for the first public archive tag.
- Public checksum-manifest refresh utility.
- Contribution guide and pull request template for public-safe archive updates.
- GitHub issue templates for archive gaps, external assets, HPC confirmation, and release decisions.
- Consolidated release blocker tracker for owner decisions, HPC confirmation, and external assets.

### Pending

- Confirm remaining HPC-side software versions.
- Fill external storage URIs and checksums for raw/large assets.
- Decide whether final RT-qPCR primer sequences belong in the Git archive.
- Decide repository license and formal citation metadata before first release.
