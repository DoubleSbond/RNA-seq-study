# CYP Family Study Workflow

This document is the working reconstruction of the CYP family study workflow. It separates confirmed project logic from items that still require recovery from original HPC files and command histories.

## 1. Project Scope

The project analyzes midgut RNA-seq data from *Perigrapha hoenei* under two host plant diets and reconstructs a CYP-centered workflow from transcriptome assembly to candidate prioritization.

Core biological question:

```text
Do broad-feeding P. hoenei and mulberry-specialized Bombyx mori show different midgut CYP expression profiles, especially in CYP3-clan / CYP6-like genes?
```

Evidence boundary:

```text
The current workflow supports expression-, homology-, and phylogeny-based interpretation. It does not by itself prove direct enzymatic substrate specificity.
```

## 2. RNA-seq Input and Assembly

Known sample design from project notes:

```text
P. hoenei midgut RNA-seq
- Dandelion-fed midgut: Dan_mg1, Dan_mg2, Dan_mg3
- Mulberry-fed midgut: Mul_mg1, Mul_mg2, Mul_mg3
```

Known assembly-level result:

```text
Trinity assembly: 179,924 transcripts
```

Known downstream expression workflow:

```text
Trinity assembly
-> Salmon quantification
-> tximport
-> DESeq2
-> gene-level TPM tables
-> CYP-focused expression analysis
```

Exact assembly, quantification, and DESeq2 commands still need to be recovered from HPC logs or shell history.

## 3. Global RNA-seq Interpretation

Global analysis indicated that Dan and Mul samples separate at the transcriptome level. Detoxification-related categories, including CYPs, ABC transporters, and xenobiotic metabolism-related terms, helped motivate focusing on CYP family analysis.

This stage establishes CYPs as a data-driven target gene family rather than a manually selected topic.

## 4. Initial CYP Discovery: 91-CYP Pool

The broad discovery layer is the 91-CYP pool.

Role:

```text
Discovery / screening pool
```

Known related files:

```text
CYP_final_summary.tsv
CYP_final_geneids.txt
TPM_gene_CYP_final.tsv
TPM_gene_CYP_final_withMeanSD.tsv
TPM_gene_CYP_91.tsv
TPM_gene_CYP_91_withMean.tsv
```

Important caution:

```text
The 91-CYP pool and the 36-HQ CYP set must not be mixed without explicit membership labels.
```

## 5. High-Quality CYP Set: 36-HQ

The main interpretation layer is the 36 high-quality CYP set.

Role:

```text
Core analysis set for figures, expression modules, candidate prioritization, and manuscript-level interpretation
```

Key recovered master table:

```text
CYP_high_quality_36_master_summary.tsv
```

Known properties:

```text
37 lines total = 1 header + 36 genes
36 unique gene IDs
```

Known columns include:

```text
gene_id
module
stability
Dan_mean
Mul_mean
MaxMean
log2FC_Dan_vs_Mul
CV_Dan
CV_Mul
sample-level TPM columns
representative transcript / peptide IDs
peptide length
B. mori top hit
Spodoptera top hit
identity and bitscore fields
```

Known related files:

```text
TPM_high_quality_CYP_for_PCA.tsv
CYP_high_quality_expression_module_summary.tsv
CYP_high_quality_expression_modules.tsv
CYP_high_quality_expression_modules_annotated.tsv
PCA_high_quality_CYP_logTPM_zscore_coordinates.tsv
PCA_high_quality_CYP_logTPM_zscore_variance.tsv
CYP_high_quality_36_ID_audit_note.txt
```

Known related scripts:

```text
PCA_high_quality_CYP_logTPM_zscore.R
PCA_high_quality_CYP_logTPM_zscore_baseR.R
classify_high_quality_CYP_modules_baseR.R
plot_FigureA_PCA_highQuality_CYP_baseR.R
```

## 6. 36-HQ Expression Analysis

Main observations:

```text
Mul group triplicates clustered relatively well.
Dan group triplicates were more dispersed.
Dan group showed stronger within-group CYP expression variation.
P. hoenei showed a CYP3-clan / CYP6-like or CYP6B-like expression signature.
```

Important metric:

```text
log2-scale Max-Min across biological replicates was used to interpret within-group expression range.
```

Representative high-expression CYP6B29-like candidates:

```text
TRINITY_DN180_c0_g2: Dan mean TPM ~182.8, Mul mean TPM ~149.5
TRINITY_DN169_c0_g1: Dan mean TPM ~90.2, Mul mean TPM ~57.9
TRINITY_DN180_c0_g1: Dan mean TPM ~35.8, Mul mean TPM ~21.1
TRINITY_DN241_c0_g2: Dan mean TPM ~13.7, Mul mean TPM ~76.1
```

Interpretation:

```text
Multiple CYP6B29-like candidates form a broadly active CYP6B-related expression module, with member-specific Dan/Mul expression shifts.
```

## 7. Ph-Bm Comparative CYP Analysis

Public *B. mori* reference dataset:

```text
PRJNA729897
Condition: mulberry-fed B. mori midgut samples
Mapping rate: approximately 89.56-89.91%
```

Representative *B. mori* CYPs with notable expression:

```text
CYP4M5
CYP12A2
CYP9A20
```

Main comparative interpretation:

```text
P. hoenei appears to show a CYP3 / CYP6-like biased CYP expression profile, whereas B. mori under mulberry feeding shows a more restricted or different CYP expression pattern, with prominent expression of CYP4M5, CYP12A2, and CYP9A20.
```

Recommended wording:

```text
The comparative expression pattern suggests that P. hoenei and B. mori may adopt different midgut CYP expression profiles, with a stronger CYP3/CYP6-like signature in P. hoenei.
```

Avoid overstatement:

```text
Do not claim that specific CYPs detoxify specific plant compounds without functional validation.
```

## 8. CYP Matched Symbol-Level Comparison

The Ph-Bm matched CYP comparison is a symbol-level exploratory layer, not a strict 36-HQ-only layer.

Known issue:

```text
Some top P. hoenei representatives in the matched plot are partial or not suitable as 36-HQ core evidence.
```

High-risk partial representatives:

```text
CYP9A20-like: TRINITY_DN13796_c0_g1, 162 aa
CYP6AB4-like: TRINITY_DN1767_c0_g1, 143 aa
```

Moderate-risk partial representatives:

```text
CYP6B2-like: TRINITY_DN127_c0_g4, 318 aa
CYP49A1-like: TRINITY_DN18331_c0_g2, 303 aa
```

Recommendation:

```text
Keep the symbol-level matched figure as exploratory, but build a separate 36-HQ-only core comparison for manuscript-level claims.
```

## 9. RT-qPCR Candidate Prioritization

The RT-qPCR logic was refined to test a clear comparison rather than many unrelated CYPs.

Core first-round candidates:

```text
CYP6B29
CYP6B2
CYP9A20
CYP9A21
CYP4M5
CYP12A2
```

Optional addition if capacity allows:

```text
CYP6B1
```

Candidate logic:

```text
CYP6B29, CYP6B2, CYP9A20, and CYP9A21 test whether CYP3-clan candidates prominent in P. hoenei are low or limited in B. mori.
CYP4M5 and CYP12A2 test whether B. mori has reproducible high expression of a different CYP profile.
```

Targets that were deprioritized for the detoxification-centered story:

```text
CYP303A1
CYP306A1
CYP332A1
```

Reason:

```text
These are more plausibly associated with development, molting, ecdysteroid metabolism, or broader physiology than with the main plant-xenobiotic detoxification hypothesis.
```

## 10. Unknown CYP Analysis

Raw unknownCYP pool:

```text
24 unknownCYP candidates from the unmatched CYP layer
```

First-pass phylogeny principle:

```text
Do not preselect unknownCYP candidates based on CYP6/CYP3 relevance.
Include all candidates with usable peptide/ORF evidence and sufficient CYP structural support.
Interpret CYP6/CYP3 relevance only after unbiased placement.
```

Peptide-available diagnostic tree:

```text
14 gene-level unknownCYP entries
17 peptide records
36 Ph36HQ references
25 B. mori references
28 Spodoptera references
Total: 106 sequences
```

Known tree input name:

```text
unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.mafft.faa
```

Known IQ-TREE setting:

```text
LG+F+R6
UFBoot: 1000
SH-aLRT: 1000
```

Known warning:

```text
Some PhUNK records had composition warnings, including DN5504, DN6927, and one DN521 ORF.
```

Recommended interpretation:

```text
The first-pass tree indicates that a substantial subset of peptide-available unknownCYP candidates is associated with CYP6/CYP3-clan regions, but this should be described as an observed placement pattern rather than a preselection criterion.
```

## 11. Plant Chemistry Interpretation

Mulberry-associated phytochemical categories discussed:

```text
alkaloids / iminosugars
indole amines
stilbenoids
flavonoids / polyphenols
coumarins
latex-associated defenses
```

Dandelion-associated phytochemical categories discussed:

```text
sesquiterpene lactones
terpenoids
triterpenoids
phytosterols / steroids
latex-associated defenses
```

Recommended wording:

```text
These CYPs may participate in the metabolic response to distinct phytochemical environments, but direct substrate specificity remains to be experimentally validated.
```

## 12. Reproducibility Checklist

- [x] Archive public Trinity/Salmon/InterProScan wrapper scripts and RNA-seq QC summaries.
- [x] Archive final gene-level tximport/DESeq2 script and significant result table.
- [x] Archive 91-CYP discovery tables and a public CYP/P450 evidence-filtering reconstruction utility.
- [x] Archive 36-HQ review tables, audit note, expression modules, PCA tables, and downstream scripts.
- [x] Archive expression module, PCA, heatmap/scatter, CYP6B-focused, and Dan internal-variation provenance.
- [x] Archive Ph-Bm matched comparison inputs and Figure1 gene-ordering script.
- [x] Archive unknownCYP raw24 review, peptide-availability, diagnostic tree, IQ-TREE report, and supporting scripts.
- [x] Record checksums for archived small result files.
- [ ] Recover exact original 91-CYP candidate-generation command, if it still exists on HPC.
- [ ] Archive rendered figure files and large alignment/source FASTA files through an external storage policy.
- [ ] Add final RT-qPCR primer sequences if they become part of the formal archive.
