# HPC 91-CYP Command Search: 2026-08-14

This note records the first live HPC search for the original command sequence
that produced the 91-CYP candidate layer. It is sanitized for public GitHub use:
private absolute paths are replaced by repository-relative or placeholder-style
paths.

## Scope

Searched within the known project root under:

- `04_annotation/`
- `06_DEGsAnalysis/`
- `07_homology/`
- `09_CYP_phylogeny/`
- `10_RTqPCR_CYP_primer_prep/`
- `11_unknownCYP_annotation/`

The search targeted scripts, logs, and small text notes containing terms such
as `CYP_candidates_step1`, `CYP_candidates_step2`, `CYP_confirmed_geneids`,
`CYP_final_geneids`, `PF00067`, `IPR001128`, `blastp`, `diamond`, `interpro`,
and `cytochrome P450`.

## Evidence Found

- A 91-gene confirmed CYP list was recovered at
  `04_annotation/FirstTry/01_reference_protein/CYP_confirmed_geneids.sorted.txt`.
- CYP best-hit and top-hit evidence files are present under
  `04_annotation/FirstTry/01_reference_protein/`.
- Family-level TPM helper scripts were found under `06_DEGsAnalysis/results/`,
  including `make_family_TPM_from_interproscan.sh` and related versions.
- Later CYP interpretation and high-quality filtering scripts are present under
  `07_homology/CYP-new/`.
- unknownCYP recheck inputs and diagnostic phylogeny material are present under
  `11_unknownCYP_annotation/`.

## Current Interpretation

The live HPC search supports the public reconstruction already archived in
GitHub:

- InterProScan/annotation outputs were used as a source of family/domain
  evidence.
- CYP candidate support included cytochrome P450 annotation text and reference
  protein best hits.
- The 91-CYP candidate list was preserved as a sorted gene-id file in the
  original annotation/reference-protein area.

However, the exact one-command or single-script provenance for producing the
public `CYP_candidates_step1.tsv` and `CYP_candidates_step2_confirmed.tsv`
tables was not fully recovered in this first pass. Keep issue
[#24](https://github.com/DoubleSbond/RNA-seq-study/issues/24) open until a
more exhaustive shell-history or backup-script search is completed, or until
the project owner accepts the reconstructed public workflow as the formal
provenance record.

## Public-Safety Notes

- No raw FASTQ, large FASTA, alignment, or bulky search-output files are added
  to Git.
- Private absolute paths are not copied into this note.
- The recovered gene-id list itself is already represented in the public
  archive as small result-manifest files.
