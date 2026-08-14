suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

expr_file  <- "fig1_expression_input_full.tsv"
block_file <- "fig1_block_map.tsv"
out_file   <- "fig1_gene_order_final.tsv"

expr <- read_tsv(expr_file, show_col_types = FALSE)
block_map <- read_tsv(block_file, show_col_types = FALSE)

block_levels <- c(
  "CYP3-enriched candidates",
  "Other high-confidence CYPs",
  "Conserved / housekeeping-like CYPs"
)

df <- block_map %>%
  left_join(expr, by = "symbol") %>%
  mutate(
    block = factor(block, levels = block_levels),
    Ph_Dan_mean = as.numeric(Ph_Dan_mean),
    Ph_Mul_mean = as.numeric(Ph_Mul_mean),
    Bm_Dan_mean = as.numeric(Bm_Dan_mean),
    Bm_Mul_mean = as.numeric(Bm_Mul_mean),
    Ph_key = pmax(Ph_Dan_mean, Ph_Mul_mean, na.rm = TRUE),
    Overall_key = pmax(Ph_Dan_mean, Ph_Mul_mean, Bm_Dan_mean, Bm_Mul_mean, na.rm = TRUE),
    sort_key = case_when(
      block == "CYP3-enriched candidates" ~ Ph_key,
      TRUE ~ Overall_key
    )
  ) %>%
  arrange(block, desc(sort_key), desc(Ph_Dan_mean), desc(Ph_Mul_mean))

write_tsv(df %>% select(symbol, block), out_file)

cat("Wrote:", out_file, "\n\n")
print(
  df %>%
    select(symbol, block, Ph_Dan_mean, Ph_Mul_mean, Bm_Dan_mean, Bm_Mul_mean, sort_key),
  n = Inf
)
