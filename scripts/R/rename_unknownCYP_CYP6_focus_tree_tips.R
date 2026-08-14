library(ape)

infile <- "final_round/iTOL/unknownCYP_CYP6_focus.manual_keep.treefile"
outfile <- "final_round/iTOL/unknownCYP_CYP6_focus.clean_labels.treefile"

tree <- read.tree(infile)

clean_label <- function(x) {
  y <- x

  if (grepl("^PhUNK\\|TRINITY_", x)) {
    y <- sub("^PhUNK\\|TRINITY_", "PhUNK-", x)
    y <- gsub("_c0_g", "-g", y)
    y <- gsub("_c1_g", "-g", y)
  } else if (grepl("^TRINITY_", x) && grepl("\\|Ph36HQ$", x)) {
    y <- sub("^TRINITY_", "PhHQ-", x)
    y <- sub("\\|Ph36HQ$", "", y)
    y <- gsub("_c0_g", "-g", y)
    y <- gsub("_c1_g", "-g", y)
  } else if (grepl("^Bmori\\|", x)) {
    y <- sub("^Bmori\\|", "Bmori-", x)
  } else if (grepl("^Spodo\\|", x)) {
    y <- sub("^Spodo\\|", "Spodo-", x)
  }

  return(y)
}

old <- tree$tip.label
new <- vapply(old, clean_label, character(1))

tree$tip.label <- new

write.tree(tree, file = outfile)

outmap <- data.frame(old_label = old, clean_label = new)
write.table(
  outmap,
  file = "final_round/iTOL/CYP6_focus_clean_label_mapping.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Input tips:", length(old), "\n")
cat("Output tree:", outfile, "\n")
cat("Mapping table: final_round/iTOL/CYP6_focus_clean_label_mapping.tsv\n")
