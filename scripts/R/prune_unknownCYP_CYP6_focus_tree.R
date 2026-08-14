library(ape)

tree <- read.tree("final_round/iTOL/unknownCYP_core10_Ph36_BmSf.treefile")

keep <- readLines("final_round/iTOL/CYP6_focus_keep_tips.txt")
keep <- keep[keep != ""]

missing <- setdiff(keep, tree$tip.label)
present <- intersect(keep, tree$tip.label)

cat("Original tips:", length(tree$tip.label), "\n")
cat("Keep tips requested:", length(keep), "\n")
cat("Keep tips present:", length(present), "\n")

if (length(missing) > 0) {
  cat("Missing tips:\n")
  print(missing)
}

if (length(present) < 2) {
  stop("Too few tips present to prune tree.")
}

pruned <- keep.tip(tree, present)

write.tree(pruned, file="final_round/iTOL/unknownCYP_CYP6_focus.manual_keep.treefile")
writeLines(pruned$tip.label, con="final_round/iTOL/CYP6_focus_keep_tips.present.txt")

cat("Output tree: final_round/iTOL/unknownCYP_CYP6_focus.manual_keep.treefile\n")
cat("Output tips: final_round/iTOL/CYP6_focus_keep_tips.present.txt\n")
cat("Pruned tips:", length(pruned$tip.label), "\n")
