# Results Manifest

Use this directory for small, Git-friendly inventories and result summaries.

Current CYP-era subdirectories:

- `91CYP/`: 91-CYP discovery-layer candidate provenance, gene IDs, summaries, best-hit tables, PC1 loading tables, and TPM tables.
- `RNAseq/`: upstream assembly QC and Salmon quantification summaries.
- `annotation/`: lightweight functional annotation summaries.
- `Bmori_comparison/`: public B. mori midgut CYP TPM tables and Figure1 Ph-Bm overview inputs.
- `CYP_screening/`: candidate peptide/transcript/gene mapping, length-QC, and fragment/noncanonical audit tables.
- `36HQ/`: 36 high-quality CYP core set, review list, module tables, and PCA tables.
- `DESeq2/`: gene-level DESeq2 significant result table.
- `RTqPCR/`: candidate target tables and RT-qPCR design summaries.
- `unknownCYP/`: unknownCYP recheck, motif/ORF/phylogeny review, and diagnostic tree outputs.

Top-level manifest files:

- `results_manifest.tsv`: compact curated result inventory.
- `hpc_core_files.tsv`: original HPC recovery checklist.
- `key_cyp_candidates.tsv`: candidate gene notes and caution labels.
- `external_assets_manifest.tsv`: large/raw/external asset tracking table.

Large result files should be stored outside Git and referenced here.

## Standard Layout For New Families

For CarE, GST, UGT, SULT, ABC, and later detoxification-related families, use this standardized structure instead of the historical CYP names:

```text
results_manifest/<family>/
|-- README.md
|-- 01_screening/
|-- 02_broad_pool/
|-- 03_high_confidence/
|-- 04_reference_comparison/
|-- 05_unknown_or_ambiguous/
`-- 06_validation_design/
```

Layer meanings:

- `01_screening/`: ID mapping, annotation evidence, family keywords/domains, fragments, noncanonical candidates.
- `02_broad_pool/`: sensitive discovery pool; not used alone for main biological claims.
- `03_high_confidence/`: curated core set for figures, expression modules, and main interpretation.
- `04_reference_comparison/`: B. mori, Spodoptera, or other reference-family comparison tables.
- `05_unknown_or_ambiguous/`: weak, partial, conflicting, or unknown candidates reviewed separately.
- `06_validation_design/`: RT-qPCR or other assay candidate prioritization and design records.

Do not use generic `final` filenames unless the README states which layer is final. Prefer names such as `<family>_broad_pool_geneids.txt` and `<family>_high_confidence_geneids.txt`.
