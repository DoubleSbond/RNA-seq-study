library(ggplot2)

df <- read.delim(
  "final_round/tables/06_unknownCYP_TPM_focus.with_final_rank.sorted_by_MaxMean.tsv",
  check.names = FALSE
)

df$gene_short <- sub("TRINITY_", "", df$gene_id)
df$gene_short <- factor(df$gene_short, levels = rev(df$gene_short))

df$final_discussion_rank <- factor(
  df$final_discussion_rank,
  levels = c(
    "Priority_1A_best_candidate",
    "Priority_1B_CYP6B_related",
    "Priority_1C_CYP6B_6AE_like_low_expression",
    "Priority_2_CYP6K1_like_variable",
    "High_TPM_but_QC_risk",
    "Non_CYP6_supportive_CYP",
    "Motif_or_phylogeny_unresolved",
    "Exclude_likely_non_CYP",
    "Supplementary_or_low"
  )
)

p <- ggplot(df, aes(x = MaxMean, y = gene_short, fill = final_discussion_rank)) +
  geom_col(width = 0.72) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.05))) +
  labs(
    x = "MaxMean TPM",
    y = NULL,
    fill = "Final interpretation",
    title = "Expression ranking of 24 Phoenei CYP_unknown candidates",
    subtitle = "DN598 combines high expression, complete CYP motifs, and CYP6B-like phylogenetic placement"
  ) +
  theme_bw(base_size = 11) +
  theme(
    panel.grid.major.y = element_blank(),
    panel.grid.minor = element_blank(),
    legend.position = "right",
    plot.title = element_text(face = "bold")
  )

ggsave(
  "final_round/plots/Figure_unknownCYP_TPM_ranking_MaxMean_final.pdf",
  p,
  width = 10,
  height = 7
)

ggsave(
  "final_round/plots/Figure_unknownCYP_TPM_ranking_MaxMean_final.png",
  p,
  width = 10,
  height = 7,
  dpi = 300
)
