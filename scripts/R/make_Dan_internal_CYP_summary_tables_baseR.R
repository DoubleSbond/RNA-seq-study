# Make supervisor-friendly summary tables for Dan internal CYP variation

infile <- "Dan_internal_CYP_variation_ranked.tsv"

dat <- read.delim(
  infile,
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

# Helper: short CYP annotation
short_anno <- dat$Bmori_title
short_anno <- gsub("^LOW QUALITY PROTEIN: ", "", short_anno)
short_anno <- gsub(" \\[Bombyx mori\\]", "", short_anno)
short_anno <- gsub("cytochrome P450 ", "CYP", short_anno)
short_anno <- gsub("Cyp", "CYP", short_anno)
short_anno <- gsub("monooxygenase ", "", short_anno)
short_anno <- gsub("isoform X[0-9]+", "", short_anno)
short_anno <- gsub("precursor", "", short_anno)
short_anno <- trimws(short_anno)

# Define simple family label
anno_text <- paste(dat$Bmori_title, dat$Spodo_title, sep = " ")

family <- rep("Other_CYP", nrow(dat))
family[grepl("6B|6b|6AE|6ae", anno_text)] <- "CYP6B/6AE-like"
family[grepl("6K|6k", anno_text)] <- "CYP6K-like"
family[grepl("12A|12a|12B|12b", anno_text)] <- "CYP12-like"
family[grepl("4G|4g", anno_text)] <- "CYP4G-like"
family[grepl("332A|332a", anno_text)] <- "CYP332-like"

# Pattern labels
pattern <- rep("Mixed", nrow(dat))

pattern[
  dat$Dan1_vs_Dan23_log2diff <= -1 &
  dat$Dan_highest %in% c("Dan_mg2", "Dan_mg3")
] <- "Dan1_low; Dan2/3_high"

pattern[
  dat$Dan1_vs_Dan23_log2diff <= -1 &
  dat$Dan_highest == "Dan_mg2"
] <- "Dan1_low; Dan2_high"

pattern[
  dat$Dan1_vs_Dan23_log2diff <= -1 &
  dat$Dan_highest == "Dan_mg3"
] <- "Dan1_low; Dan3_high"

pattern[
  dat$Dan1_vs_Dan23_log2diff >= 1
] <- "Dan1_high_or_Dan3_low"

pattern[
  dat$Dan_lowest == "Dan_mg3" &
  dat$Dan1_vs_Dan23_log2diff > 0
] <- "Dan3_low"

# Interpretation
interpretation <- rep("Dan replicates show moderate CYP expression variation", nrow(dat))

interpretation[
  pattern %in% c("Dan1_low; Dan2/3_high", "Dan1_low; Dan2_high", "Dan1_low; Dan3_high") &
  family %in% c("CYP6B/6AE-like", "CYP6K-like")
] <- "Dan1 weak response in CYP6-related gene"

interpretation[
  pattern %in% c("Dan1_low; Dan2/3_high", "Dan1_low; Dan2_high", "Dan1_low; Dan3_high") &
  dat$module == "Dan_biased"
] <- "Dan-biased CYP mainly induced in Dan2/3"

interpretation[
  pattern == "Dan3_low"
] <- "Exception: Dan3 is low for this CYP"

interpretation[
  dat$module == "core_shared" &
  pattern %in% c("Dan1_low; Dan2/3_high", "Dan1_low; Dan2_high", "Dan1_low; Dan3_high")
] <- "Core CYP also shows reduced Dan1 expression"

# Build clean table
out <- data.frame(
  Rank = seq_len(nrow(dat)),
  gene_id = dat$gene_id,
  module = dat$module,
  stability = dat$stability,
  CYP_family = family,
  CYP_annotation = short_anno,
  Dan_mg1_TPM = round(dat$Dan_mg1_TPM, 2),
  Dan_mg2_TPM = round(dat$Dan_mg2_TPM, 2),
  Dan_mg3_TPM = round(dat$Dan_mg3_TPM, 2),
  Dan_pattern = pattern,
  Dan_range_log2 = round(dat$Dan_range_log2, 2),
  Dan1_vs_Dan23_log2diff = round(dat$Dan1_vs_Dan23_log2diff, 2),
  Dan_highest = dat$Dan_highest,
  Dan_lowest = dat$Dan_lowest,
  Main_interpretation = interpretation,
  Bmori_title = dat$Bmori_title,
  Spodo_title = dat$Spodo_title,
  stringsAsFactors = FALSE
)

# Full supervisor summary
write.table(
  out,
  "Dan_internal_CYP_variation_summary_for_supervisor.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Top 15 variable CYPs
write.table(
  head(out, 15),
  "Dan_internal_CYP_variation_top15_for_supervisor.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Dan1 low table
dan1_low <- out[out$Dan1_vs_Dan23_log2diff <= -1, ]
write.table(
  dan1_low,
  "Dan_mg1_low_CYPs_for_supervisor.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

# Module-family summary among top 15
top15 <- head(out, 15)

module_summary <- as.data.frame(table(top15$module))
colnames(module_summary) <- c("module", "count_in_top15")
write.table(
  module_summary,
  "Dan_top15_variable_CYP_module_summary.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

family_summary <- as.data.frame(table(top15$CYP_family))
colnames(family_summary) <- c("CYP_family", "count_in_top15")
write.table(
  family_summary,
  "Dan_top15_variable_CYP_family_summary.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Generated supervisor-friendly tables:\n")
cat("  Dan_internal_CYP_variation_summary_for_supervisor.tsv\n")
cat("  Dan_internal_CYP_variation_top15_for_supervisor.tsv\n")
cat("  Dan_mg1_low_CYPs_for_supervisor.tsv\n")
cat("  Dan_top15_variable_CYP_module_summary.tsv\n")
cat("  Dan_top15_variable_CYP_family_summary.tsv\n")
