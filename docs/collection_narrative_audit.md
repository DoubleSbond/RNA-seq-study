# Collected Material Narrative Audit

This note evaluates whether the currently collected HPC material can support a reproducible investigation narrative for the CYP family study.

## Overall Assessment

The collected material is sufficient to support a strong first-pass investigation narrative from RNA-seq processing to CYP-focused interpretation.

The strongest evidence chain is:

```text
read QC / trimming scripts
-> Trinity assembly script and assembly QC
-> Salmon quantification logs and sample metadata
-> tximport / DESeq2 scripts and gene-level expression exports
-> CYP candidate discovery and 91-CYP tables
-> CYP length / isoform / homology screening
-> 36-HQ CYP expression modules, PCA, and candidate summaries
-> B. mori comparison and RT-qPCR candidate design
-> unknownCYP recheck and diagnostic phylogeny
```

## Supported Narrative Blocks

### 1. RNA-seq Processing and Assembly

Supported by:

- `collected_hpc/upstream_RNAseq/scripts/02_quality_trimming*.sh`
- `collected_hpc/upstream_RNAseq/scripts/03_trinity_assembly.sh`
- `collected_hpc/upstream_RNAseq/assembly_qc/TrinityStats_fromFASTA.txt`
- `collected_hpc/upstream_RNAseq/assembly_qc/short_summary.specific.insecta_odb10.trinity_insecta_busco.txt`
- `collected_hpc/upstream_RNAseq/assembly_qc/assembly_quality_report.txt`

Key facts currently supported:

- Six midgut RNA-seq samples were used.
- Trinity was run with paired-end reads, 32 CPU threads, 100G memory, and `--min_kmer_cov 2`.
- The assembled transcriptome has 179,924 transcripts.
- BUSCO insecta_odb10 completeness is 97.0%.

Limitations:

- Some shell comments are mojibake, but the commands remain readable.
- Full raw-read QC reports and MultiQC-style summary are not yet collected.

### 2. Salmon Quantification and Expression Import

Supported by:

- `collected_hpc/upstream_RNAseq/salmon_logs/*/cmd_info.json`
- `collected_hpc/upstream_RNAseq/salmon_logs/*/salmon_quant.log`
- `collected_hpc/upstream_RNAseq/DESeq2/salmon_summary.tsv`
- `collected_hpc/upstream_RNAseq/DESeq2/sample_info.csv`
- `collected_hpc/upstream_RNAseq/DESeq2/export_TPM_gene.R`
- `collected_hpc/provenance_DESeq2/Gene-level_DESeq2_final.R`
- `collected_hpc/provenance_DESeq2/README_calibration.txt`
- `collected_hpc/provenance_DESeq2/sessionInfo_DESeq2.txt`
- `collected_hpc/provenance_DESeq2/DESeq2_results_significant.tsv`

Key facts currently supported:

- Salmon version 1.10.2 was used.
- The Salmon index contained 179,924 targets, matching the Trinity assembly.
- Mapping rates are high, approximately 91.82% to 94.21%.
- The sample design has three dandelion-fed midgut samples and three mulberry-fed midgut samples.
- The recovered final DESeq2 script defines the six-sample condition table inline, uses `tximport` on Salmon `quant.sf` files, builds a gene-level `DESeqDataSetFromTximport`, and runs `design = ~ condition`.
- The final contrast is `condition: dandelion vs mulberry`; therefore positive log2 fold change indicates higher expression in the dandelion-fed group.
- The recovered calibration note records Conda environment `r_deseq2`, DESeq2 1.42.0, alpha 0.05, and DEG thresholds `|log2FC| > 1` with `padj < 0.05`.
- The recovered session information records R 4.3.3 and the attached Bioconductor/R package versions used for the DESeq2 calibration export.

Limitations:

- `collected_hpc/upstream_RNAseq/DESeq2/DEGs_analysis.R` appears to be an earlier or non-final copy because it expects a `condition` column while the collected `sample_info.csv` contains `diet`.
- `collected_hpc/provenance_DESeq2/Gene-level_DESeq2_final.R` should be treated as the stronger final provenance source for the gene-level DESeq2 narrative.
- The recovered DESeq2 provenance files contain environment and path details that should be sanitized before public GitHub publication.

### 3. CYP Discovery and 91-CYP Layer

Supported by:

- `collected_hpc/upstream_RNAseq/gene_level_CYP/CYP_candidates_step1.tsv`
- `collected_hpc/upstream_RNAseq/gene_level_CYP/CYP_candidates_step2_confirmed.tsv`
- `collected_hpc/upstream_RNAseq/gene_level_CYP/CYP_confirmed_geneids.txt`
- `results_manifest/91CYP/CYP_candidates_step1.tsv`
- `results_manifest/91CYP/CYP_candidates_step2_confirmed.tsv`
- `results_manifest/91CYP/CYP_confirmed_geneids.txt`
- `results_manifest/91CYP/CYP_final_summary.tsv`
- `results_manifest/91CYP/CYP_final_geneids.txt`
- `results_manifest/91CYP/TPM_gene_CYP_91.tsv`
- `results_manifest/91CYP/TPM_gene_CYP_91_withMean.tsv`
- `results_manifest/91CYP/CYP_Bmor_besthit_by_gene.tsv`
- `results_manifest/91CYP/CYP_confirmed_vs_Bmor_besthit.tsv`
- `results_manifest/91CYP/CYP_PC1_loading_rank.tsv`

Key facts currently supported:

- CYP candidates were identified using PFAM/InterPro CYP evidence.
- The 91-CYP discovery layer is represented by gene IDs, summary annotations, and TPM tables.
- There is evidence of a stepwise process from broader candidates to confirmed CYP entries.
- B. mori best-hit and PC1 loading tables provide downstream annotation and expression-prioritization context.

Limitations:

- The exact original command or script that produced `CYP_candidates_step1.tsv` and `CYP_candidates_step2_confirmed.tsv` has not yet been explicitly identified. The recovered tables and a public reconstruction utility are now archived.

### 4. CYP Quality Filtering and 36-HQ Layer

Supported by:

- `collected_hpc/CYP_screening/tables/CYP_candidate_pep_tx_gene.tsv`
- `collected_hpc/CYP_screening/tables/CYP_longest_isoform_per_gene.tsv`
- `collected_hpc/CYP_screening/tables/CYP_len300plus_summary.tsv`
- `collected_hpc/CYP_screening/tables/CYP_fragment_geneids.txt`
- `results_manifest/CYP_screening/CYP_candidate_pep_tx_gene.tsv`
- `results_manifest/CYP_screening/CYP_longest_isoform_per_gene.tsv`
- `results_manifest/CYP_screening/CYP_len300plus_summary.tsv`
- `results_manifest/CYP_screening/CYP_fragment_geneids.txt`
- `results_manifest/CYP_screening/CYP_noncanonical_geneids.txt`
- `docs/audit/CYP_high_quality_36_ID_audit_note.txt`
- `results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv`
- `results_manifest/36HQ/CYP_high_quality_36_review_list.tsv`
- `results_manifest/36HQ/CYP_high_quality_36_geneids.txt`
- `results_manifest/36HQ/CYP_high_quality_36_geneids_master_order.txt`
- `results_manifest/36HQ/CYP_high_quality_36_master_summary.sha256`
- `results_manifest/36HQ/CYP_high_quality_expression_modules.tsv`
- `results_manifest/36HQ/CYP_high_quality_expression_modules_annotated.tsv`
- `results_manifest/36HQ/TPM_high_quality_CYP_for_PCA.tsv`
- `results_manifest/36HQ/PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv`
- `results_manifest/36HQ/PCA_high_quality_CYP_logTPM_zscore_variance.tsv`
- `docs/audit/CYP_high_quality_36_ID_audit_note.txt`
- `collected_hpc/provenance_91_to_36HQ/CYP_high_quality_36_review_list.tsv`
- `collected_hpc/provenance_91_to_36HQ/CYP_high_quality_36_geneids.txt`
- `collected_hpc/provenance_91_to_36HQ/CYP_high_quality_36_geneids_master_order.txt`
- `collected_hpc/provenance_91_to_36HQ/CYP_high_quality_36_master_summary.sha256`
- `collected_hpc/provenance_91_to_36HQ/unpacked_20260527/*`
- `collected_hpc/provenance_91_to_36HQ/unpacked_20260722/restored_36HQ_20260722/*`

Key facts currently supported:

- The high-quality layer used representative transcript/peptide IDs, peptide length, and homology evidence.
- Fragment and noncanonical CYP candidates were explicitly tracked.
- Candidate peptide/transcript/gene mapping, representative longest isoforms, 300-aa length filtering, and seed-gene audit lists are now archived as small QC tables.
- The 36-HQ master table contains expression, module, stability, homology, and sequence-length fields.
- The recovered review list has exactly 36 rows and includes gene ID, module, stability, dandelion/mulberry mean TPM, maximum mean TPM, log2FC, peptide length, Bombyx mori hit, Spodoptera frugiperda hit, representative transcript ID, and representative peptide ID.
- The recovered gene ID lists contain exactly 36 IDs and preserve the master order used by the high-quality CYP summaries.
- The recovered ID audit note states that three 36-gene files contain exactly the same 36 gene IDs, and that the 71-gene `CYP_final_summary.tsv` should not be used as the master summary for the current 36-HQ PCA/module/Dan-variation analysis.
- The restored 20260722 package contains the current 36-HQ master summary, annotated expression modules, PCA scripts and coordinates, plotting scripts, the ID audit note, and an empty current-vs-archive diff, supporting continuity with the 20260527 archived package.

Limitations:

- The evidence now supports the 36-HQ set as a reviewed, audited, and reproducible analysis layer, but a single one-command script that starts from the full 91-CYP table and automatically emits the final 36-HQ set has not yet been identified.
- The public archive should describe this transition as a quality review / curation step supported by tables, audit notes, checksums, and downstream scripts, unless a fully automated selection script is recovered later.

### 5. 36-HQ Expression Modules and Figures

Supported by:

- `scripts/R/classify_high_quality_CYP_modules_baseR.R`
- `scripts/R/PCA_high_quality_CYP_logTPM_zscore_baseR.R`
- `scripts/R/PCA_high_quality_CYP_logTPM_zscore.R`
- `scripts/R/plot_FigureA_PCA_highQuality_CYP_baseR.R`
- `scripts/R/plot_CYP_module_heatmap_baseR.R`
- `scripts/R/plot_CYP_module_scatter_baseR.R`
- `scripts/R/plot_CYP6B_focused_slope_baseR.R`
- `scripts/R/investigate_Dan_internal_CYP_variation_baseR.R`
- `scripts/R/make_Dan_internal_CYP_summary_tables_baseR.R`
- `scripts/R/quantify_CYP_PCA_within_group_dispersion_baseR.R`
- `results_manifest/36HQ/*`
- `collected_hpc/CYP_screening/scripts/plot_CYP_module_heatmap_baseR.R`
- `collected_hpc/CYP_screening/scripts/plot_CYP_module_scatter_baseR.R`
- `collected_hpc/CYP_screening/scripts/quantify_CYP_PCA_within_group_dispersion_baseR.R`
- `results_manifest/36HQ/Dan_internal_CYP_variation_summary.tsv`
- `results_manifest/36HQ/Dan_internal_CYP_variation_top15.tsv`
- `results_manifest/36HQ/Dan_mg1_low_CYPs.tsv`
- `results_manifest/36HQ/CYP_PCA_within_group_distance_summary.tsv`
- `results_manifest/36HQ/CYP_PCA_within_group_pairwise_distances.tsv`

Key facts currently supported:

- 36-HQ CYPs were classified into expression modules.
- PCA coordinates and variance tables were preserved.
- Dan/Mul expression differences and within-Dan replicate variation can be supported by scripts and summary tables.
- Dan internal-variation tables explicitly record high-variation CYPs, Dan_mg1-low cases, and family/module summaries.
- Within-group PCA distance summaries support the replicate-dispersion interpretation.

Limitations:

- Figure image/PDF files are only partially collected or not formally archived yet.

### 6. B. mori Comparison and Figure1

Supported by:

- `collected_hpc/Bmori_comparison/public_RNAseq/make_Bm_public_CYP_TPM_tables.py`
- `collected_hpc/Bmori_comparison/public_RNAseq/Bm_ML_midgut_CYP_TPM_annotated.tsv`
- `collected_hpc/Bmori_comparison/Figure1_CYP_overview/fig1_expression_input_full.tsv`
- `collected_hpc/Bmori_comparison/Figure1_CYP_overview/make_fig1_gene_order_final.R`
- `results_manifest/Bmori_comparison/Bm_ML_midgut_CYP_TPM_annotated.tsv`
- `results_manifest/Bmori_comparison/Bmori_GCF_ASM3026992v2_CYP_transcripts_from_GFF.tsv`
- `results_manifest/Bmori_comparison/fig1_expression_input_full.tsv`
- `results_manifest/Bmori_comparison/fig1_gene_order_final.tsv`
- `scripts/python/make_bmori_public_cyp_tpm_tables.py`
- `scripts/R/make_fig1_gene_order_final.R`

Key facts currently supported:

- Public B. mori midgut RNA-seq CYP expression was processed into CYP TPM tables.
- A symbol-level Ph-Bm comparison table exists.
- The Figure1 input supports the narrative that P. hoenei and B. mori have different CYP expression profiles.
- Figure1 block mapping and final gene order are now archived as lightweight provenance tables.

Limitations:

- Symbol-level matching should be framed as exploratory, not strict one-to-one orthology.
- Some P. hoenei representatives in Figure1 are partial or not 36-HQ-grade.

### 7. RT-qPCR Candidate Design

Supported by:

- `results_manifest/RTqPCR/README_FINAL_15CYP_RTqPCR_targets.md`
- `results_manifest/RTqPCR/CYP_RTqPCR_true_target_mapping_from_Figure1.tsv`
- `collected_hpc/Bmori_comparison/RTqPCR_QC/*`
- `results_manifest/RTqPCR/Bmori_CYP_multi_isoform_integrated_evidence_summary.tsv`
- `results_manifest/RTqPCR/Bmori_CYP12_primer3_top1_candidates.tsv`
- `results_manifest/RTqPCR/Bmori_CYP13_primer3_top1_candidates.tsv`

Key facts currently supported:

- The final candidate set was connected back to Figure1 CYP targets.
- Primer-design logic used CDS FASTA files.
- B. mori multi-isoform targets were checked for common regions and primer feasibility.
- B. mori CYP12/CYP13 Primer3 top-candidate summaries are archived as small QC tables.

Limitations:

- Primer FASTA files and final primer sequences are mostly not collected in this lightweight pass.

### 8. unknownCYP Recheck and Phylogeny

Supported by:

- `docs/notes/unknownCYP_final_round_summary.md`
- `docs/notes/unknownCYP_phylogeny_input_preparation_summary.md`
- `docs/notes/unknownCYP_IQTREE_run_summary_20260617.md`
- `results_manifest/unknownCYP/01_all_unknownCYP_review_table.tsv`
- `results_manifest/unknownCYP/unknownCYP_raw24_phylogeny_inclusion_summary.tsv`
- `results_manifest/unknownCYP/highTPM_unknownCYP_vs_phylogeny_current_mapping.tsv`
- `results_manifest/unknownCYP/unknownCYP_integrated_interpretation.with_group.domain_priority.tsv`
- `results_manifest/unknownCYP/unknownCYP_phylogeny_interpretation.manual_v1.tsv`
- `logs/unknownCYP/*.log`
- `logs/unknownCYP/*.iqtree`
- `scripts/python/clean_unknownCYP_peptideAvailable14_headers.py`
- `scripts/R/plot_unknownCYP_TPM_ranking_final.R`
- `scripts/R/plot_unknownCYP_Dan_vs_Mul_scatter.R`
- `scripts/R/prune_unknownCYP_CYP6_focus_tree.R`
- `collected_hpc/unknownCYP/scripts/*`
- `collected_hpc/unknownCYP/tables/*`

Key facts currently supported:

- 24 raw unknownCYP candidates were reviewed.
- 14 gene-level candidates with 17 ORFs were included in the diagnostic tree.
- IQ-TREE used 106 amino-acid sequences and model `LG+F+R6`.
- The interpretation distinguishes expression strength from motif/ORF/phylogenetic support.
- High-TPM candidates were explicitly cross-checked against phylogenetic placement and motif/ORF support.
- DN598 is currently the strongest recovered unknownCYP candidate because it combines high expression, complete CYP motifs, and CYP6B-like phylogenetic placement.
- DN1031, DN3806, and DN420 are retained as examples where high TPM alone does not provide enough confidence for CYP candidate prioritization.

Limitations:

- The final alignment FASTA is not collected in the lightweight Git-oriented set.

## Main Gaps Before Final Archival

1. Continue converting any newly recovered shell/Python/R scripts with internal paths into public parameterized versions.
2. Find the exact original script or command sequence that generated the 91-CYP candidate tables, if it still exists on HPC.
3. Fill external storage URIs and checksums in `results_manifest/external_assets_manifest.tsv` for large/raw assets that remain outside Git.
4. Confirm pending software versions using `environment/version_confirmation_checklist.tsv` after logging into HPC.
4. Decide whether small final figures and tree/alignment files should be archived in Git or only checksummed externally.
5. Collect final primer-design outputs if RT-qPCR methods are part of the archive.

## Conclusion

The current collection is strong enough to support the investigation narrative, especially from CYP candidate discovery onward. The two previously weakest transitions have improved:

```text
DESeq2 final run provenance: mostly resolved by the recovered final script, calibration README, and sessionInfo.
91-CYP discovery -> 36-HQ filtering provenance: substantially strengthened by stepwise candidate tables, best-hit support, review tables, ID audit notes, checksums, restored archives, and downstream scripts.
```

The remaining caution is that the 36-HQ transition appears to be review/curation based rather than fully represented by one automated end-to-end script. This is acceptable for a reproducible research archive if the review criteria, input tables, output lists, and checksum/audit notes are published clearly.
