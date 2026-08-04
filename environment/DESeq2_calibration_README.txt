DESeq2 calibration export (Perigrapha hoenei RNA-seq)

Environment:
- Conda env: r_deseq2
- DESeq2 version: 1.42.0

Input:
- Salmon quant.sf under: *_quant/quant.sf
- tx2gene mapping: tx2gene.csv
- sample table: sample_info.csv

tximport:
- type = "salmon"
- ignoreTxVersion = TRUE
- countsFromAbundance = "lengthScaledTPM"
- dropInfReps = TRUE (skip inferential replicates; not needed for DEG export)

DESeq2:
- design = ~ condition
- results alpha = 0.05
- DEG thresholds used in earlier scripts: |log2FC| > 1 and padj < 0.05

Outputs:
- txi.lengthScaledTPM.rds: tximport object
- dds.DESeq2.rds: DESeqDataSet after DESeq()
- res.alpha0.05.rds: DESeq2 results object
- counts_raw.tsv / counts_norm.tsv
- DESeq2_results.tsv (gene_id as rownames)
