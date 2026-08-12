# Figure A: PCA of high-quality CYP expression
# Fixed version: expanded axes + legend outside plot area

pca_df <- read.delim(
  "PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

var_df <- read.delim(
  "PCA_high_quality_CYP_logTPM_zscore_variance.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

pc1_var <- var_df$variance_percent[var_df$PC == "PC1"]
pc2_var <- var_df$variance_percent[var_df$PC == "PC2"]

group_cols <- c(
  Dan = "#E64B35",
  Mul = "#4DBBD5"
)

group_pch <- c(
  Dan = 16,
  Mul = 17
)

pca_df$col <- group_cols[pca_df$diet]
pca_df$pch <- group_pch[pca_df$diet]

# Manual fixed axes, intentionally wider than data range
# Data range roughly:
# PC1: -5.67 to 2.76
# PC2: -2.56 to 4.30
xlim_use <- c(-7.0, 4.0)
ylim_use <- c(-3.5, 5.7)

# Manual label positions
label_pos <- c(
  Dan_mg1 = 4,
  Dan_mg2 = 4,
  Dan_mg3 = 3,
  Mul_mg1 = 3,
  Mul_mg2 = 2,
  Mul_mg3 = 3
)

draw_pca <- function() {
  # Larger right margin for external legend
  par(mar = c(6, 6, 5, 8), xpd = FALSE)
  
  plot(
    pca_df$PC1,
    pca_df$PC2,
    col = pca_df$col,
    pch = pca_df$pch,
    cex = 2,
    xlab = paste0("PC1 (", round(pc1_var, 1), "%)"),
    ylab = paste0("PC2 (", round(pc2_var, 1), "%)"),
    main = "PCA of midgut high-quality CYP expression",
    las = 1,
    xlim = xlim_use,
    ylim = ylim_use,
    cex.main = 1.35,
    cex.lab = 1.25,
    cex.axis = 1.05
  )
  
  # Subtitle below the plot, safer than placing near top points
  mtext(
    "36 high-quality CYP genes; log2(TPM + 1), gene-wise z-score",
    side = 1,
    line = 4.2,
    cex = 1.0
  )
  
  for (i in seq_len(nrow(pca_df))) {
    s <- pca_df$sample[i]
    pos_i <- ifelse(s %in% names(label_pos), label_pos[s], 3)
    
    text(
      pca_df$PC1[i],
      pca_df$PC2[i],
      labels = s,
      pos = pos_i,
      cex = 0.85,
      offset = 0.6
    )
  }
  
  # Put legend outside the plotting region
  par(xpd = TRUE)
  legend(
    x = 4.15,
    y = 5.2,
    legend = c("Dandelion", "Mulberry"),
    col = c(group_cols["Dan"], group_cols["Mul"]),
    pch = c(group_pch["Dan"], group_pch["Mul"]),
    pt.cex = 1.8,
    bty = "n",
    cex = 1.05
  )
  par(xpd = FALSE)
}

png("FigureA_highQuality_CYP_PCA.png", width = 2400, height = 1700, res = 300)
draw_pca()
dev.off()

pdf("FigureA_highQuality_CYP_PCA.pdf", width = 8, height = 5.7)
draw_pca()
dev.off()

cat("Regenerated fixed Figure A:\n")
cat("  FigureA_highQuality_CYP_PCA.png\n")
cat("  FigureA_highQuality_CYP_PCA.pdf\n")
