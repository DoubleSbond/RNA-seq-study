#!/usr/bin/env Rscript

suppressMessages({
  library(dplyr)
  library(readr)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop(
    "Usage: Rscript scripts/R/interpro_annotation_summary.R ",
    "<interproscan.tsv> <annotation_summary.tsv>",
    call. = FALSE
  )
}

anno_file <- args[[1]]
out_file <- args[[2]]

cat("[Load] InterProScan annotation TSV ...\n")
anno <- read_tsv(anno_file, col_names = FALSE, comment = "#", show_col_types = FALSE)

expected_cols <- c(
  "transcript", "md5", "len", "db", "pfam_id", "pfam_name",
  "start", "end", "evalue", "status", "date",
  "ipr_id", "ipr_desc", "go_terms"
)

if (ncol(anno) < length(expected_cols)) {
  stop(
    "Expected at least ", length(expected_cols),
    " InterProScan TSV columns, found ", ncol(anno),
    call. = FALSE
  )
}

colnames(anno)[seq_along(expected_cols)] <- expected_cols
cat(sprintf("[Info] Loaded %d rows\n", nrow(anno)))

summary_tbl <- anno %>%
  mutate(Gene_ID = sub("_i[0-9]+.*", "", transcript)) %>%
  filter(Gene_ID != "") %>%
  group_by(Gene_ID) %>%
  summarise(
    Pfam_IDs = paste(unique(na.omit(pfam_id)), collapse = ","),
    InterPro_IDs = paste(unique(na.omit(ipr_id)), collapse = ","),
    InterPro_Descriptions = paste(unique(na.omit(ipr_desc)), collapse = "; "),
    GO_Terms = paste(unique(na.omit(go_terms)), collapse = "|"),
    .groups = "drop"
  )

write_tsv(summary_tbl, out_file)

cat(sprintf("[OK] Annotation summary saved: %s\n", out_file))
cat(sprintf("[Info] Total unique genes: %d\n", nrow(summary_tbl)))
