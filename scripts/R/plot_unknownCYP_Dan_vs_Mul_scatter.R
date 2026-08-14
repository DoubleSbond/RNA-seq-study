library(ggplot2)

df <- read.delim(
  "final_round/tables/04_unknownCYP_TPM_focus.with_final_rank.tsv",
  check.names = FALSE
)

df$gene_short <- sub("TRINITY_", "", df$gene_id)

label_genes <- c(
  "TRINITY_DN598_c0_g1",
  "TRINITY_DN2768_c0_g1",
  "TRINITY_DN3806_c0_g2",
  "TRINITY_DN420_c0_g1",
  "TRINITY_DN1031_c0_g1",
  "TRINITY_DN2810_c0_g1",
  "TRINITY_DN414_c0_g1",
  "TRINITY_DN414_c0_g2"
)

df$label <- ifelse(df$gene_id %in% label_genes, df$gene_short, "")

p <- ggplot(df, aes(x = Dan_mean, y = Mul_mean, shape = expression_class)) +
  geom_point(aes(size = MaxMean), alpha = 0.85) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed") +
  geom_text(aes(label = label), hjust = -0.05, vjust = 0.5, size = 3) +
  scale_x_continuous(trans = "log10") +
  scale_y_continuous(trans = "log10") +
  labs(
    x = "Dan mean TPM (log10)",
    y = "Mul mean TPM (log10)",
    size = "MaxMean TPM",
    shape = "Expression class",
    title = "Dan vs Mul expression of 24 Phoenei CYP_unknown candidates",
    subtitle = "Dashed line indicates balanced expression between diets"
  ) +
  theme_bw(base_size = 11) +
  theme(
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold")
  )

ggsave(
  "final_round/plots/Figure_unknownCYP_Dan_vs_Mul_scatter_final.pdf",
  p,
  width = 8,
  height = 6
)

ggsave(
  "final_round/plots/Figure_unknownCYP_Dan_vs_Mul_scatter_final.png",
  p,
  width = 8,
  height = 6,
  dpi = 300
)
