# PCA of high-quality CYP genes
# Input: TPM_high_quality_CYP_for_PCA.tsv
# Method: log2(TPM + 1) -> gene-wise z-score -> PCA
# No external R packages required

expr_file <- "TPM_high_quality_CYP_for_PCA.tsv"

expr <- read.delim(
  expr_file,
  row.names = 1,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

sample_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3")

missing_cols <- setdiff(sample_cols, colnames(expr))
if (length(missing_cols) > 0) {
  stop(paste("Missing sample columns:", paste(missing_cols, collapse = ", ")))
}

expr <- expr[, sample_cols]

# Convert to numeric matrix
expr <- as.data.frame(lapply(expr, as.numeric), row.names = rownames(expr))
expr_mat <- as.matrix(expr)

# Remove genes expressed in fewer than 2 samples
keep <- rowSums(expr_mat > 0, na.rm = TRUE) >= 2
expr_filt <- expr_mat[keep, , drop = FALSE]

cat("High-quality CYP genes before expression filter:", nrow(expr_mat), "\n")
cat("High-quality CYP genes after expression filter:", nrow(expr_filt), "\n")

# log2(TPM + 1)
log_expr <- log2(expr_filt + 1)

# Gene-wise z-score
gene_mean <- rowMeans(log_expr, na.rm = TRUE)
gene_sd <- apply(log_expr, 1, sd, na.rm = TRUE)

# Remove zero-variance genes
nonzero_var <- gene_sd > 0 & !is.na(gene_sd)
log_expr <- log_expr[nonzero_var, , drop = FALSE]
gene_mean <- gene_mean[nonzero_var]
gene_sd <- gene_sd[nonzero_var]

z_mat <- sweep(log_expr, 1, gene_mean, "-")
z_mat <- sweep(z_mat, 1, gene_sd, "/")

cat("Genes retained after z-score filtering:", nrow(z_mat), "\n")

if (nrow(z_mat) < 2) {
  stop("Too few genes retained for PCA.")
}

# PCA: samples as rows, genes as columns
pca <- prcomp(t(z_mat), center = TRUE, scale. = FALSE)

pc_var <- summary(pca)$importance[2, ] * 100

pca_df <- as.data.frame(pca$x)
pca_df$sample <- rownames(pca_df)
pca_df$diet <- ifelse(grepl("^Dan", pca_df$sample), "Dan", "Mul")

# Save coordinates
write.table(
  pca_df,
  file = "PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Save variance
var_df <- data.frame(
  PC = paste0("PC", seq_along(pc_var)),
  variance_percent = pc_var
)

write.table(
  var_df,
  file = "PCA_high_quality_CYP_logTPM_zscore_variance.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Plot settings
diet_col <- ifelse(pca_df$diet == "Dan", "firebrick", "steelblue")
diet_pch <- ifelse(pca_df$diet == "Dan", 16, 17)

# PNG
png(
  filename = "PCA_high_quality_CYP_logTPM_zscore.png",
  width = 2100,
  height = 1500,
  res = 300
)

plot(
  pca_df$PC1,
  pca_df$PC2,
  col = diet_col,
  pch = diet_pch,
  cex = 1.8,
  xlab = paste0("PC1 (", round(pc_var[1], 1), "%)"),
  ylab = paste0("PC2 (", round(pc_var[2], 1), "%)"),
  main = paste0("PCA of midgut high-quality CYP expression (n=", nrow(z_mat), ")")
)

text(
  pca_df$PC1,
  pca_df$PC2,
  labels = pca_df$sample,
  pos = 3,
  cex = 0.8
)

legend(
  "topright",
  legend = c("Dan", "Mul"),
  col = c("firebrick", "steelblue"),
  pch = c(16, 17),
  bty = "n"
)

dev.off()

# PDF
pdf(
  file = "PCA_high_quality_CYP_logTPM_zscore.pdf",
  width = 7,
  height = 5
)

plot(
  pca_df$PC1,
  pca_df$PC2,
  col = diet_col,
  pch = diet_pch,
  cex = 1.8,
  xlab = paste0("PC1 (", round(pc_var[1], 1), "%)"),
  ylab = paste0("PC2 (", round(pc_var[2], 1), "%)"),
  main = paste0("PCA of midgut high-quality CYP expression (n=", nrow(z_mat), ")")
)

text(
  pca_df$PC1,
  pca_df$PC2,
  labels = pca_df$sample,
  pos = 3,
  cex = 0.8
)

legend(
  "topright",
  legend = c("Dan", "Mul"),
  col = c("firebrick", "steelblue"),
  pch = c(16, 17),
  bty = "n"
)

dev.off()

cat("PCA finished successfully.\n")
cat("Output files:\n")
cat("  PCA_high_quality_CYP_logTPM_zscore.png\n")
cat("  PCA_high_quality_CYP_logTPM_zscore.pdf\n")
cat("  PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv\n")
cat("  PCA_high_quality_CYP_logTPM_zscore_variance.tsv\n")
