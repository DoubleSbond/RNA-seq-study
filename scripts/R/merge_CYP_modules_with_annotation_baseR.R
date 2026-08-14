modules <- read.delim(
  "CYP_high_quality_expression_modules.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

anno <- read.delim(
  "CYP_final_summary.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

merged <- merge(
  modules,
  anno,
  by = "gene_id",
  all.x = TRUE,
  sort = FALSE
)

# Keep important columns near front
front_cols <- c(
  "gene_id",
  "module",
  "stability",
  "Dan_mean",
  "Mul_mean",
  "MaxMean",
  "log2FC_Dan_vs_Mul",
  "CV_Dan",
  "CV_Mul",
  "expressed_samples_TPM1",
  "Bmori_title",
  "Spodo_title",
  "peptide_length",
  "Bmori_pident",
  "Spodo_pident"
)

front_cols <- front_cols[front_cols %in% colnames(merged)]
other_cols <- setdiff(colnames(merged), front_cols)
merged <- merged[, c(front_cols, other_cols)]

write.table(
  merged,
  file = "CYP_high_quality_expression_modules_annotated.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Annotated module table generated:\n")
cat("  CYP_high_quality_expression_modules_annotated.tsv\n")
