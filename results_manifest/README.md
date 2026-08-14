# Results Manifest

Use this directory for small, Git-friendly inventories and result summaries.

Current subdirectories:

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

Large result files should be stored outside Git and referenced here.
