# CYP6B-like focused slope plot, robust version
# Input: CYP_high_quality_expression_modules_annotated.tsv

dat <- read.delim(
  "CYP_high_quality_expression_modules_annotated.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

# Combine annotation text for robust matching
anno_text <- paste(
  dat$Bmori_title,
  dat$Spodo_title,
  sep = " "
)

# Match CYP6B / Cyp6b / CYP6AE-like annotations
is_cyp6b <- grepl(
  "6B|6b|6AE|6ae|Cyp6b|CYP6B|Cyp6ae|CYP6AE",
  anno_text
)

cyp6b <- dat[is_cyp6b, ]

cat("Matched CYP6B-like genes:", nrow(cyp6b), "\n")

if (nrow(cyp6b) == 0) {
  stop("No CYP6B-like genes matched. Please check Bmori_title and Spodo_title fields.")
}

# Sort by module and expression strength
module_order <- c("core_shared", "Dan_biased", "Mul_biased", "low_or_unstable")
cyp6b$module_order <- match(cyp6b$module, module_order)
cyp6b <- cyp6b[order(cyp6b$module_order, -cyp6b$MaxMean), ]
cyp6b$module_order <- NULL

module_cols <- c(
  core_shared = "gray30",
  Dan_biased = "firebrick",
  Mul_biased = "steelblue",
  low_or_unstable = "gray75"
)

short_anno <- cyp6b$Bmori_title
short_anno <- gsub("^LOW QUALITY PROTEIN: ", "", short_anno)
short_anno <- gsub(" \\[Bombyx mori\\]", "", short_anno)
short_anno <- gsub("cytochrome P450 ", "CYP", short_anno)
short_anno <- gsub("Cyp", "CYP", short_anno)
short_anno <- gsub("isoform X[0-9]+", "", short_anno)

labels <- paste(cyp6b$gene_id, short_anno, sep = " | ")

# Save matched table first
write.table(
  cyp6b,
  file = "CYP6B_like_genes_module_table.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

draw_slope <- function() {
  par(mar = c(5, 5, 4, 16))
  
  ymax <- max(c(cyp6b$Dan_mean, cyp6b$Mul_mean), na.rm = TRUE) * 1.18
  
  plot(
    NA,
    xlim = c(1, 2.25),
    ylim = c(0, ymax),
    xaxt = "n",
    xlab = "",
    ylab = "Mean TPM",
    main = "CYP6B-like genes across dietary modules"
  )
  
  axis(1, at = c(1, 2), labels = c("Dandelion", "Mulberry"))
  
  for (i in seq_len(nrow(cyp6b))) {
    col_i <- module_cols[cyp6b$module[i]]
    if (is.na(col_i)) col_i <- "black"
    
    lines(
      c(1, 2),
      c(cyp6b$Dan_mean[i], cyp6b$Mul_mean[i]),
      col = col_i,
      lwd = 2
    )
    
    points(
      c(1, 2),
      c(cyp6b$Dan_mean[i], cyp6b$Mul_mean[i]),
      pch = 21,
      bg = col_i,
      col = "black",
      cex = 1.25
    )
    
    text(
      2.05,
      cyp6b$Mul_mean[i],
      labels = labels[i],
      pos = 4,
      cex = 0.55,
      xpd = TRUE
    )
  }
  
  legend(
    "topright",
    legend = names(module_cols),
    col = module_cols,
    lwd = 2,
    bty = "n",
    cex = 0.8
  )
}

png("CYP6B_like_module_slope_plot.png", width = 3300, height = 2200, res = 300)
draw_slope()
dev.off()

pdf("CYP6B_like_module_slope_plot.pdf", width = 11, height = 7.2)
draw_slope()
dev.off()

cat("CYP6B-like focused plot generated:\n")
cat("  CYP6B_like_module_slope_plot.png\n")
cat("  CYP6B_like_module_slope_plot.pdf\n")
cat("  CYP6B_like_genes_module_table.tsv\n")
