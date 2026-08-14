# Figure C: Dan_mean vs Mul_mean scatter for CYP modules
# Input: CYP_high_quality_expression_modules_annotated.tsv

dat <- read.delim(
  "CYP_high_quality_expression_modules_annotated.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

module_cols <- c(
  core_shared = "gray30",
  Dan_biased = "firebrick",
  Mul_biased = "steelblue",
  low_or_unstable = "gray75"
)

dat$color <- module_cols[dat$module]

x <- dat$Mul_mean + 0.1
y <- dat$Dan_mean + 0.1

# 标注重点基因：高表达或代表性基因
label_genes <- dat$gene_id[
  dat$MaxMean >= 20 |
  dat$gene_id %in% c(
    "TRINITY_DN5241_c0_g1",
    "TRINITY_DN127_c0_g1",
    "TRINITY_DN241_c0_g2",
    "TRINITY_DN3752_c0_g1",
    "TRINITY_DN1632_c1_g1",
    "TRINITY_DN276_c0_g1"
  )
]

draw_scatter <- function() {
  par(mar = c(5, 5, 4, 2))
  
  plot(
    x,
    y,
    log = "xy",
    pch = 21,
    bg = dat$color,
    col = "black",
    cex = 1.6,
    xlab = "Mulberry mean TPM + 0.1",
    ylab = "Dandelion mean TPM + 0.1",
    main = "CYP expression module classification"
  )
  
  # 参考线
  xx <- seq(min(x), max(x), length.out = 200)
  lines(xx, xx, lwd = 2, lty = 1)
  lines(xx, 2 * xx, lwd = 1.5, lty = 2)
  lines(xx, 0.5 * xx, lwd = 1.5, lty = 2)
  
  idx <- which(dat$gene_id %in% label_genes)
  text(
    x[idx],
    y[idx],
    labels = dat$gene_id[idx],
    pos = 3,
    cex = 0.55
  )
  
  legend(
    "topleft",
    legend = names(module_cols),
    pt.bg = module_cols,
    pch = 21,
    bty = "n",
    cex = 0.9
  )
  
  legend(
    "bottomright",
    legend = c("y = x", "2-fold threshold"),
    lty = c(1, 2),
    lwd = c(2, 1.5),
    bty = "n",
    cex = 0.8
  )
}

png("FigureC_CYP_module_scatter.png", width = 2100, height = 1800, res = 300)
draw_scatter()
dev.off()

pdf("FigureC_CYP_module_scatter.pdf", width = 7, height = 6)
draw_scatter()
dev.off()

cat("Generated:\n")
cat("  FigureC_CYP_module_scatter.png\n")
cat("  FigureC_CYP_module_scatter.pdf\n")
