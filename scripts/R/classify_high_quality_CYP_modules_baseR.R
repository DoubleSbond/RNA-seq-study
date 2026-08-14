# Classify high-quality CYP genes into expression modules
# Input: results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv
# Output: CYP_high_quality_expression_modules.tsv

args <- commandArgs(trailingOnly = TRUE)

infile <- if (length(args) >= 1) {
  args[[1]]
} else {
  "results_manifest/36HQ/CYP_high_quality_36_master_summary.tsv"
}

if (!file.exists(infile) && file.exists("CYP_high_quality_36_master_summary.tsv")) {
  infile <- "CYP_high_quality_36_master_summary.tsv"
}

outdir <- if (length(args) >= 2) {
  args[[2]]
} else {
  dirname(infile)
}

if (!dir.exists(outdir)) {
  dir.create(outdir, recursive = TRUE)
}

dat <- read.delim(
  infile,
  header = TRUE,
  row.names = 1,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

sample_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3")

missing_cols <- setdiff(sample_cols, colnames(dat))
if (length(missing_cols) > 0) {
  stop(paste("Missing sample columns:", paste(missing_cols, collapse = ", ")))
}

expr <- dat[, sample_cols]
expr <- as.data.frame(lapply(expr, as.numeric), row.names = rownames(expr))

Dan_cols <- c("Dan_mg1", "Dan_mg2", "Dan_mg3")
Mul_cols <- c("Mul_mg1", "Mul_mg2", "Mul_mg3")

Dan_mean <- rowMeans(expr[, Dan_cols], na.rm = TRUE)
Mul_mean <- rowMeans(expr[, Mul_cols], na.rm = TRUE)

Dan_sd <- apply(expr[, Dan_cols], 1, sd, na.rm = TRUE)
Mul_sd <- apply(expr[, Mul_cols], 1, sd, na.rm = TRUE)

pseudo <- 0.1
log2FC_Dan_vs_Mul <- log2((Dan_mean + pseudo) / (Mul_mean + pseudo))

mean_TPM <- (Dan_mean + Mul_mean) / 2
MaxMean <- pmax(Dan_mean, Mul_mean)
MinMean <- pmin(Dan_mean, Mul_mean)

CV_Dan <- Dan_sd / (Dan_mean + pseudo)
CV_Mul <- Mul_sd / (Mul_mean + pseudo)

expressed_samples_TPM1 <- rowSums(expr >= 1, na.rm = TRUE)
Dan_expressed_TPM1 <- rowSums(expr[, Dan_cols] >= 1, na.rm = TRUE)
Mul_expressed_TPM1 <- rowSums(expr[, Mul_cols] >= 1, na.rm = TRUE)

module <- rep("low_or_unstable", nrow(expr))

module[
  Dan_mean >= 1 &
  Mul_mean >= 1 &
  abs(log2FC_Dan_vs_Mul) < 1 &
  expressed_samples_TPM1 >= 4
] <- "core_shared"

module[
  Dan_mean >= 1 &
  log2FC_Dan_vs_Mul >= 1 &
  Dan_expressed_TPM1 >= 2
] <- "Dan_biased"

module[
  Mul_mean >= 1 &
  log2FC_Dan_vs_Mul <= -1 &
  Mul_expressed_TPM1 >= 2
] <- "Mul_biased"

# Add stability label
stability <- rep("moderate", nrow(expr))
stability[CV_Dan < 0.75 & CV_Mul < 0.75] <- "stable"
stability[CV_Dan >= 1.25 | CV_Mul >= 1.25] <- "variable"

out <- data.frame(
  gene_id = rownames(expr),
  expr,
  Dan_mean = Dan_mean,
  Dan_sd = Dan_sd,
  Mul_mean = Mul_mean,
  Mul_sd = Mul_sd,
  mean_TPM = mean_TPM,
  MaxMean = MaxMean,
  MinMean = MinMean,
  log2FC_Dan_vs_Mul = log2FC_Dan_vs_Mul,
  CV_Dan = CV_Dan,
  CV_Mul = CV_Mul,
  expressed_samples_TPM1 = expressed_samples_TPM1,
  Dan_expressed_TPM1 = Dan_expressed_TPM1,
  Mul_expressed_TPM1 = Mul_expressed_TPM1,
  module = module,
  stability = stability,
  stringsAsFactors = FALSE
)

# Sort by module and MaxMean
module_order <- c("core_shared", "Dan_biased", "Mul_biased", "low_or_unstable")
out$module_order <- match(out$module, module_order)
out <- out[order(out$module_order, -out$MaxMean), ]
out$module_order <- NULL

write.table(
  out,
  file = file.path(outdir, "CYP_high_quality_expression_modules.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Module summary
summary_tab <- as.data.frame(table(out$module))
colnames(summary_tab) <- c("module", "gene_count")
write.table(
  summary_tab,
  file = file.path(outdir, "CYP_high_quality_expression_module_summary.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Module classification finished.\n")
cat("Output files:\n")
cat("  CYP_high_quality_expression_modules.tsv\n")
cat("  CYP_high_quality_expression_module_summary.tsv\n")
