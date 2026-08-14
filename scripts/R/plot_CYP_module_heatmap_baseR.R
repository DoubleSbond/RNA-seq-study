# CYP module heatmap
# Input: CYP_high_quality_expression_modules_annotated.tsv
# Output: CYP_module_heatmap_logTPM_zscore.png/pdf

dat <- read.delim(
  "CYP_high_quality_expression_modules_annotated.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

sample_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3")

expr <- dat[, sample_cols]
expr <- as.data.frame(lapply(expr, as.numeric))
rownames(expr) <- dat$gene_id

# log2(TPM + 1)
log_expr <- log2(as.matrix(expr) + 1)

# gene-wise z-score
gene_mean <- rowMeans(log_expr, na.rm = TRUE)
gene_sd <- apply(log_expr, 1, sd, na.rm = TRUE)
nonzero <- gene_sd > 0 & !is.na(gene_sd)

log_expr <- log_expr[nonzero, , drop = FALSE]
dat2 <- dat[nonzero, , drop = FALSE]
gene_mean <- gene_mean[nonzero]
gene_sd <- gene_sd[nonzero]

z <- sweep(log_expr, 1, gene_mean, "-")
z <- sweep(z, 1, gene_sd, "/")

# Order rows by module and MaxMean
module_order <- c("core_shared", "Dan_biased", "Mul_biased", "low_or_unstable")
dat2$module_order <- match(dat2$module, module_order)
ord <- order(dat2$module_order, -dat2$MaxMean)
z <- z[ord, , drop = FALSE]
dat2 <- dat2[ord, , drop = FALSE]

# Labels: gene_id + shortened annotation
short_anno <- dat2$Bmori_title
short_anno <- gsub("^LOW QUALITY PROTEIN: ", "", short_anno)
short_anno <- gsub(" \\[Bombyx mori\\]", "", short_anno)
short_anno <- gsub("cytochrome P450 ", "CYP", short_anno)
short_anno <- gsub("monooxygenase ", "", short_anno)
short_anno <- gsub("probable ", "", short_anno)

row_labels <- paste(dat2$gene_id, short_anno, sep = " | ")

# Cap z-score for display
z_plot <- z
z_plot[z_plot > 2] <- 2
z_plot[z_plot < -2] <- -2

# Color palette
heat_cols <- colorRampPalette(c("navy", "white", "firebrick"))(101)

# Module side colors
module_cols <- c(
  core_shared = "gray30",
  Dan_biased = "firebrick",
  Mul_biased = "steelblue",
  low_or_unstable = "gray75"
)

row_side_cols <- module_cols[dat2$module]

# Function to draw heatmap
draw_heatmap <- function() {
  op <- par(no.readonly = TRUE)
  layout(matrix(c(1,2), nrow = 1), widths = c(0.18, 0.82))
  
  # Module color strip
  par(mar = c(8, 1, 4, 0))
  image(
    x = 1,
    y = seq_len(nrow(z_plot)),
    z = matrix(seq_len(nrow(z_plot)), nrow = 1),
    col = row_side_cols,
    axes = FALSE,
    xlab = "",
    ylab = ""
  )
  title("Module", cex.main = 0.9)
  
  # Heatmap body
  par(mar = c(8, 1, 4, 14))
  image(
    x = seq_len(ncol(z_plot)),
    y = seq_len(nrow(z_plot)),
    z = t(z_plot[nrow(z_plot):1, ]),
    col = heat_cols,
    axes = FALSE,
    xlab = "",
    ylab = "",
    main = "High-quality CYP expression modules"
  )
  
  axis(
    1,
    at = seq_len(ncol(z_plot)),
    labels = colnames(z_plot),
    las = 2,
    cex.axis = 0.9
  )
  
  axis(
    4,
    at = seq_len(nrow(z_plot)),
    labels = rev(row_labels),
    las = 2,
    cex.axis = 0.45
  )
  
  # Add vertical separator between Dan and Mul
  abline(v = 3.5, lwd = 2)
  
  legend(
    "topright",
    inset = c(-0.55, 0),
    legend = names(module_cols),
    fill = module_cols,
    bty = "n",
    cex = 0.8,
    xpd = TRUE
  )
  
  par(op)
}

png("CYP_module_heatmap_logTPM_zscore.png", width = 3000, height = 3600, res = 300)
draw_heatmap()
dev.off()

pdf("CYP_module_heatmap_logTPM_zscore.pdf", width = 10, height = 12)
draw_heatmap()
dev.off()

cat("Heatmap generated:\n")
cat("  CYP_module_heatmap_logTPM_zscore.png\n")
cat("  CYP_module_heatmap_logTPM_zscore.pdf\n")
