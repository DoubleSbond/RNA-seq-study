# Lepidoptera expression-atlas extension roadmap

## Priority 1: Spodoptera frugiperda

Use PRJNA1159780 first. It contains fourth-instar midgut RNA-seq after 24 hours
on fresh maize leaves versus artificial diet, with three biological replicates
per treatment. This is unusually well matched to a host-plant metabolism
question and explicitly includes UGT-mediated benzoxazinoid detoxification.

- NCBI example SRA record and study design:
  https://www.ncbi.nlm.nih.gov/sra/SRX26057378%5Baccn%5D
- NCBI BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1159780

Secondary historical context can use PRJNA209056/SRX312156, a pooled
third–fourth instar midgut/fat-body resource from insecticide-resistant strains,
but it lacks the replication and diet matching of PRJNA1159780.

## Priority 2: Papilio xuthus

The most reusable broad resource currently identified is GSE65280/PRJNA270384,
which contains ten developmental RNA-seq samples from egg to adult and has a
RefSeq-annotated genome. It is strong for developmental background and low-instar
expression layers, but it is not a matched larval-midgut host-plant experiment.

- NCBI GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65280
- NCBI SRA example: https://www.ncbi.nlm.nih.gov/sra/SRX843966
- RefSeq annotation report:
  https://www.ncbi.nlm.nih.gov/refseq/annotation_euk/Papilio_xuthus/100/

SRA1096681 provides three control and three immune-challenged whole-larva
transcriptomes with de novo assembly, TPM/RSEM analysis, and immune annotations.
It is useful for the immune layer, not for a clean diet comparison.

## Recommended order

1. Process S. frugiperda PRJNA1159780 with maize and artificial-diet groups.
2. Process P. xuthus GSE65280 as a developmental reference atlas.
3. Add P. xuthus SRA1096681 as a separate immune-context module.
4. Search specifically for replicated P. xuthus larval midgut datasets with a
   defined Rutaceae host before making direct specialist-versus-generalist diet
   conclusions.

All extensions should preserve the 22-marker definitions, fixed-seed quintile
sampling, raw TPM, log-only visualization, and the comparability matrix.
