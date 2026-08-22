# Representative detox-family IQ-TREE results

These are rough, reference-augmented protein trees for one longest *P. hoenei* peptide per candidate gene. Reference sequences are the retained top hits from *Bombyx mori* and *Spodoptera* searches. Alignments were generated with MAFFT.

## ModelFinder runs completed

All runs used IQ-TREE 3.1.2 with ModelFinder (`-m MFP`), 1,000 ultrafast bootstrap replicates, and 1,000 SH-aLRT replicates.

| Family | *P. hoenei* genes | *B. mori* refs | *Spodoptera* refs | Total sequences | BIC model |
|---|---:|---:|---:|---:|---|
| CarE | 20 | 22 | 25 | 67 | LG+F+I+R4 |
| GST | 20 | 16 | 21 | 57 | LG+R3 |
| UGT | 36 | 39 | 37 | 112 | LG+R4 |
| SULT | 11 | 11 | 14 | 36 | LG+I+G4 |

The exhaustive ABC ModelFinder run was still active when this snapshot was made and is deliberately not copied while files are changing.

## Fixed-model fallback runs completed

UGT and ABC were also run independently with `LG+F+G4`, 1,000 ultrafast bootstrap replicates, and 1,000 SH-aLRT replicates. This provides an immediately usable supported ABC tree while its much slower ModelFinder run continues on the HPC.

| Family | Total sequences | Model |
|---|---:|---|
| UGT | 112 | LG+F+G4 |
| ABC | 142 | LG+F+G4 |

Each family directory preserves the alignment, tree files, consensus tree, split support, IQ-TREE report, logs, checkpoint/model artifacts where emitted, summary, and SHA-256 manifest. Treat these trees as exploratory evidence rather than a final curated phylogeny.
