# Quantify within-group dispersion in high-quality CYP PCA space
# Input: FigureA_PCA_coordinates.tsv

pca <- read.delim(
  "FigureA_PCA_coordinates.tsv",
  header = TRUE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

coords <- as.matrix(pca[, c("PC1", "PC2")])
rownames(coords) <- pca$sample

calc_pairwise <- function(group_name) {
  idx <- which(pca$diet == group_name)
  sub <- coords[idx, , drop = FALSE]
  d <- as.matrix(dist(sub))
  
  pairs <- which(upper.tri(d), arr.ind = TRUE)
  out <- data.frame(
    diet = group_name,
    sample1 = rownames(sub)[pairs[,1]],
    sample2 = rownames(sub)[pairs[,2]],
    distance_PC1_PC2 = d[pairs],
    stringsAsFactors = FALSE
  )
  return(out)
}

all_dist <- rbind(
  calc_pairwise("Dan"),
  calc_pairwise("Mul")
)

write.table(
  all_dist,
  "CYP_PCA_within_group_pairwise_distances.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

summary <- aggregate(
  distance_PC1_PC2 ~ diet,
  data = all_dist,
  FUN = function(x) c(
    mean = mean(x),
    sd = sd(x),
    min = min(x),
    max = max(x)
  )
)

summary2 <- data.frame(
  diet = summary$diet,
  mean_distance = summary$distance_PC1_PC2[, "mean"],
  sd_distance = summary$distance_PC1_PC2[, "sd"],
  min_distance = summary$distance_PC1_PC2[, "min"],
  max_distance = summary$distance_PC1_PC2[, "max"]
)

write.table(
  summary2,
  "CYP_PCA_within_group_distance_summary.tsv",
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cat("Generated:\n")
cat("  CYP_PCA_within_group_pairwise_distances.tsv\n")
cat("  CYP_PCA_within_group_distance_summary.tsv\n\n")

cat("## Pairwise distances\n")
print(all_dist)

cat("\n## Summary\n")
print(summary2)
