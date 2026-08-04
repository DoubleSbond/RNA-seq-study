#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(tximport)
  library(DESeq2)
  library(dplyr)
  library(ggplot2)
  library(readr)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop(
    "Usage: Rscript scripts/R/gene_level_deseq2_final.R ",
    "<quant_dir> <tx2gene.csv> <output_dir>\n",
    "quant_dir should contain sample-specific directories named ",
    "Dan_mg1_quant, Dan_mg2_quant, Dan_mg3_quant, Mul_mg1_quant, ",
    "Mul_mg2_quant, and Mul_mg3_quant, each with quant.sf."
  )
}

quant_dir <- args[[1]]
tx2gene_path <- args[[2]]
output_dir <- args[[3]]
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

sample_info <- tibble::tibble(
  sample = c("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3"),
  condition = c("dandelion", "dandelion", "dandelion", "mulberry", "mulberry", "mulberry")
)

files <- file.path(quant_dir, paste0(sample_info$sample, "_quant"), "quant.sf")
names(files) <- sample_info$sample

cat("[Info] Checking quant.sf files:\n")
print(tibble::tibble(sample = names(files), exists = file.exists(files)))
if (!all(file.exists(files))) {
  stop("Some quant.sf files are missing.")
}

if (!file.exists(tx2gene_path)) {
  stop("tx2gene.csv not found: ", tx2gene_path)
}

tx2gene <- read.csv(tx2gene_path, header = TRUE)
colnames(tx2gene) <- c("TXNAME", "GENEID") %>% head(ncol(tx2gene))

txi <- tximport(files, type = "salmon", tx2gene = tx2gene)

sample_info$condition <- factor(sample_info$condition, levels = c("mulberry", "dandelion"))
dds <- DESeqDataSetFromTximport(txi, colData = sample_info, design = ~ condition)

keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]
cat("[Info] Genes after filtering:", nrow(dds), "\n")

dds <- DESeq(dds)

# Positive log2FoldChange means higher expression in the dandelion-fed group.
res <- results(dds, contrast = c("condition", "dandelion", "mulberry"))
res <- res[order(res$padj), ]
res_df <- as.data.frame(res)
res_df$GeneID <- rownames(res_df)

all_csv <- file.path(output_dir, "Gene-level_DESeq2_all.csv")
up_csv <- file.path(output_dir, "Gene-level_DESeq2_upregulated.csv")
down_csv <- file.path(output_dir, "Gene-level_DESeq2_downregulated.csv")
sum_tsv <- file.path(output_dir, "Gene-level_DEG_summary.tsv")
count_tsv <- file.path(output_dir, "Gene-level_DEG_updown_count.tsv")

readr::write_csv(res_df %>% dplyr::relocate(GeneID), all_csv)

up_tbl <- subset(res_df, log2FoldChange > 1 & padj < 0.05)
down_tbl <- subset(res_df, log2FoldChange < -1 & padj < 0.05)

readr::write_csv(up_tbl %>% dplyr::relocate(GeneID), up_csv)
readr::write_csv(down_tbl %>% dplyr::relocate(GeneID), down_csv)

cat(sprintf("[OK] Upregulated: %d  Downregulated: %d\n", nrow(up_tbl), nrow(down_tbl)))

summary_tbl <- tibble::tibble(
  total_genes_after_filter = nrow(res_df),
  upregulated_dandelion = nrow(up_tbl),
  downregulated_dandelion = nrow(down_tbl),
  lfc_threshold = 1,
  padj_threshold = 0.05
)
readr::write_tsv(summary_tbl, sum_tsv)
readr::write_tsv(
  tibble::tibble(
    status = c("Up in Dandelion", "Down in Dandelion"),
    count = c(nrow(up_tbl), nrow(down_tbl))
  ),
  count_tsv
)

deg_data <- res_df
deg_data$status <- "Not significant"
deg_data$status[deg_data$log2FoldChange > 1 & deg_data$padj < 0.05] <- "Upregulated in Dandelion group"
deg_data$status[deg_data$log2FoldChange < -1 & deg_data$padj < 0.05] <- "Upregulated in Mulberry group"

p_ma <- ggplot(deg_data, aes(x = log10(baseMean + 1), y = log2FoldChange)) +
  geom_point(aes(color = status), alpha = 0.6, size = 0.8) +
  scale_color_manual(
    values = c(
      "Upregulated in Mulberry group" = "blue",
      "Upregulated in Dandelion group" = "red",
      "Not significant" = "grey70"
    ),
    drop = FALSE,
    limits = c("Upregulated in Mulberry group", "Not significant", "Upregulated in Dandelion group")
  ) +
  geom_hline(yintercept = c(-1, 1), linetype = "dashed", color = "black") +
  labs(
    title = "MA Plot - Gene-level DESeq2",
    x = "log10(baseMean + 1)",
    y = "log2 Fold Change",
    color = "Status"
  ) +
  theme_minimal(base_size = 14) +
  theme(legend.position = "right")

ggsave(file.path(output_dir, "Gene-level_MA_plot.png"), p_ma, width = 9, height = 6.5, dpi = 300)
ggsave(file.path(output_dir, "Gene-level_MA_plot_standardized.png"), p_ma, width = 9, height = 6.5, dpi = 300)

vol_df <- deg_data
vol_df$neglog10 <- -log10(vol_df$padj)
finite_max <- suppressWarnings(max(vol_df$neglog10[is.finite(vol_df$neglog10)], na.rm = TRUE))
vol_df$neglog10[!is.finite(vol_df$neglog10)] <- finite_max + 1

p_volcano <- ggplot(vol_df, aes(x = log2FoldChange, y = neglog10)) +
  geom_point(aes(color = status), alpha = 0.6, size = 0.8) +
  scale_color_manual(
    values = c(
      "Upregulated in Mulberry group" = "blue",
      "Upregulated in Dandelion group" = "red",
      "Not significant" = "grey70"
    ),
    drop = FALSE,
    limits = c("Upregulated in Mulberry group", "Not significant", "Upregulated in Dandelion group")
  ) +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed", color = "black") +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "black") +
  labs(
    title = "Volcano Plot - Gene-level DESeq2",
    x = "log2 Fold Change",
    y = "-log10(padj)",
    color = "Status"
  ) +
  theme_minimal(base_size = 14) +
  theme(legend.position = "right")

ggsave(file.path(output_dir, "Gene-level_volcano_plot.png"), p_volcano, width = 9, height = 6.5, dpi = 300)
ggsave(file.path(output_dir, "Gene-level_volcano_plot_standardized.png"), p_volcano, width = 9, height = 6.5, dpi = 300)

cat("\n[sessionInfo]\n")
print(sessionInfo())

quit(save = "no", status = 0)
