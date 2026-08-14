dat <- read.delim(
  "FigureBCD_CYP_module_classification_annotated.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

dan_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3")
mul_cols <- c("Mul_mg1", "Mul_mg2", "Mul_mg3")
sample_cols <- c(dan_cols, mul_cols)

expr <- dat[, sample_cols]
expr <- as.data.frame(lapply(expr, as.numeric))
rownames(expr) <- dat$gene_id

log_expr <- log2(as.matrix(expr) + 1)

dan_mat <- log_expr[, dan_cols, drop = FALSE]

dan_mean_log <- rowMeans(dan_mat, na.rm = TRUE)
dan_sd_log <- apply(dan_mat, 1, sd, na.rm = TRUE)
dan_range_log <- apply(dan_mat, 1, function(x) max(x, na.rm = TRUE) - min(x, na.rm = TRUE))

Dan23_mean_log <- rowMeans(log_expr[, c("Dan_mg2", "Dan_mg3"), drop = FALSE], na.rm = TRUE)
Dan1_vs_Dan23_log2diff <- log_expr[, "Dan_mg1"] - Dan23_mean_log

Dan_highest <- dan_cols[apply(dan_mat, 1, which.max)]
Dan_lowest  <- dan_cols[apply(dan_mat, 1, which.min)]

out <- data.frame(
  gene_id = dat$gene_id,
  module = dat$module,
  stability = dat$stability,
  Bmori_title = dat$Bmori_title,
  Spodo_title = dat$Spodo_title,
  Dan_mg1_TPM = dat$Dan_mg1,
  Dan_mg2_TPM = dat$Dan_mg2,
  Dan_mg3_TPM = dat$Dan_mg3,
  Mul_mean = dat$Mul_mean,
  Dan_mean = dat$Dan_mean,
  log2_Dan_mg1 = log_expr[, "Dan_mg1"],
  log2_Dan_mg2 = log_expr[, "Dan_mg2"],
  log2_Dan_mg3 = log_expr[, "Dan_mg3"],
  Dan_sd_log2 = dan_sd_log,
  Dan_range_log2 = dan_range_log,
  Dan1_vs_Dan23_log2diff = Dan1_vs_Dan23_log2diff,
  Dan_highest = Dan_highest,
  Dan_lowest = Dan_lowest,
  stringsAsFactors = FALSE
)

out <- out[order(-out$Dan_range_log2), ]

write.table(
  out,
  "Dan_internal_CYP_variation_ranked.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

dan1_low <- out[out$Dan1_vs_Dan23_log2diff <= -1, ]
write.table(
  dan1_low,
  "Dan_mg1_low_vs_Dan_mg2_mg3_CYPs.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

dan1_high <- out[out$Dan1_vs_Dan23_log2diff >= 1, ]
write.table(
  dan1_high,
  "Dan_mg1_high_vs_Dan_mg2_mg3_CYPs.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Generated:\n")
cat("  Dan_internal_CYP_variation_ranked.tsv\n")
cat("  Dan_mg1_low_vs_Dan_mg2_mg3_CYPs.tsv\n")
cat("  Dan_mg1_high_vs_Dan_mg2_mg3_CYPs.tsv\n\n")

cat("## Top 20 Dan-internal variable CYPs\n")
print(out[1:min(20, nrow(out)), c(
  "gene_id",
  "module",
  "Dan_mg1_TPM",
  "Dan_mg2_TPM",
  "Dan_mg3_TPM",
  "Dan_range_log2",
  "Dan1_vs_Dan23_log2diff",
  "Dan_highest",
  "Dan_lowest",
  "Bmori_title"
)])
