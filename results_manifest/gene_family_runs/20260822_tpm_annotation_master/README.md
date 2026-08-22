# P. hoenei detox-family TPM and annotation master

This directory integrates the current broad CarE, GST, UGT, SULT, and ABC candidate pools at one row per gene.

## Outputs

- `detox_gene_tpm_annotation_master.tsv`: 136 genes with six sample TPM values and the current sequence, domain, HMM, reference-homology, Swiss-Prot, PROSITE, review, ABC-triage, and similarity-component evidence.
- `detox_gene_tpm_long.tsv`: 816 tidy TPM observations for downstream R/Python analysis.
- `tpm_mean_reconciliation.tsv`: transparent comparison of archived group means with means recomputed from the three visible TPM values per condition.
- `source_manifest.tsv`: SHA-256, byte size, and repository-relative path for all 61 source files used by the integration script.
- `build_summary.tsv`: family and row counts.

## Candidate counts

| Family | Broad genes | TPM observations |
|---|---:|---:|
| CarE | 20 | 120 |
| GST | 20 | 120 |
| UGT | 36 | 216 |
| SULT | 11 | 66 |
| ABC | 49 | 294 |
| Total | 136 | 816 |

## TPM interpretation

The six archived sample columns (`Dan_mg1`–`Dan_mg3`, `Mul_mg1`–`Mul_mg3`) are preserved without alteration. The previously archived `Dan_mean` and `Mul_mean` fields differ from the arithmetic means of these visible triplicates for all 136 genes, indicating that they came from a different upstream aggregation or statistical basis. Neither series was overwritten: the archived values remain in the master table, while the Excel workbook recomputes transparent triplicate means, standard deviations, delta, and log2 fold change from the six visible TPM cells.

The reconciliation table records this difference gene by gene. Until the original upstream definition is revisited, use the recalculated columns for plots explicitly based on these six TPM values and label the archived mean fields separately.

## Annotation interpretation

The table is a discovery and triage resource, not a final nomenclature table. HMM and whole-proteome reference scans are intentionally permissive. `provisional_HQ_domain`, second-pass recommendations, ABC triage, protein architecture, phylogenetic position, and modern signal/topology predictions should guide final inclusion.

All 61 source entries passed SHA-256 verification before the table and workbook were generated.
