library(ape)

tree <- read.tree("final_round/iTOL/unknownCYP_CYP6_focus.manual_keep.treefile")
tips <- tree$tip.label

clean_label <- function(x) {
  y <- x

  if (grepl("^PhUNK\\|TRINITY_", x)) {
    y <- sub("^PhUNK\\|TRINITY_", "PhUNK_", x)
    y <- gsub("_c0_g", "_g", y)
    y <- gsub("_c1_g", "_g", y)
  } else if (grepl("^TRINITY_", x) && grepl("\\|Ph36HQ$", x)) {
    y <- sub("^TRINITY_", "PhHQ_", x)
    y <- sub("\\|Ph36HQ$", "", y)
    y <- gsub("_c0_g", "_g", y)
    y <- gsub("_c1_g", "_g", y)
  } else if (grepl("^Bmori\\|", x)) {
    y <- sub("^Bmori\\|", "Bmori_", x)
  } else if (grepl("^Spodo\\|", x)) {
    y <- sub("^Spodo\\|", "Spodo_", x)
  }

  return(y)
}

out <- data.frame(
  old = tips,
  new = vapply(tips, clean_label, character(1)),
  stringsAsFactors = FALSE
)

con <- file("final_round/iTOL/iTOL_CYP6_focus_clean_tip_labels.txt", "w")
writeLines("LABELS", con)
writeLines("SEPARATOR TAB", con)
writeLines("DATA", con)
write.table(out, con, sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
close(con)

cat("CYP6 focus tips:", length(tips), "\n")
cat("Output: final_round/iTOL/iTOL_CYP6_focus_clean_tip_labels.txt\n")
