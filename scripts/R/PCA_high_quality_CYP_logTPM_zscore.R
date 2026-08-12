library(tidyverse)

# Input
expr_file <- "TPM_high_quality_CYP_for_PCA.tsv"

expr <- read.delim(expr_file, row.names = 1, check.names = FALSE)

# Keep only sample columns
sample_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3")
expr <- expr[, sample_cols]

# Metadata
meta <- data.frame(
  sample = sample_cols,
  diet = c("Dan", "Dan", "Dan", "Mul", "Mul", "Mul"),
  row.names = sample_cols
)

# Remove genes with all-zero or near-zero expression if any
keep <- rowSums(expr > 0) >= 2
expr_filt <- expr[keep, ]

cat("High-quality CYP genes before expression filter:", nrow(expr), "\n")
cat("High-quality CYP genes used for PCA:", nrow(expr_filt), "\n")

# log2(TPM + 1)
log_expr <- log2(expr_filt + 1)

# Gene-wise z-score
z_mat <- t(scale(t(log_expr)))

# Remove genes with zero variance
z_mat <- z_mat[complete.cases(z_mat), ]

cat("Genes retained after z-score filtering:", nrow(z_mat), "\n")

# PCA: samples as rows
pca <- prcomp(t(z_mat), center = TRUE, scale. = FALSE)

pca_df <- as.data.frame(pca$x)
pca_df$sample <- rownames(pca_df)
pca_df$diet <- meta[pca_df$sample, "diet"]

pc_var <- summary(pca)$importance[2, ] * 100

# Save PCA coordinates
write.table(
  pca_df,
  file = "PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Plot
p <- ggplot(pca_df, aes(x = PC1, y = PC2, color = diet)) +
  geom_point(size = 5) +
  theme_classic(base_size = 18) +
  labs(
    title = paste0("PCA of midgut high-quality CYP expression (n=", nrow(z_mat), ")"),
    x = paste0("PC1 (", round(pc_var[1], 1), "%)"),
    y = paste0("PC2 (", round(pc_var[2], 1), "%)"),
    color = "diet"
  )

ggsave("PCA_high_quality_CYP_logTPM_zscore.png", p, width = 7, height = 5, dpi = 300)
ggsave("PCA_high_quality_CYP_logTPM_zscore.pdf", p, width = 7, height = 5)

# Also save variance
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
