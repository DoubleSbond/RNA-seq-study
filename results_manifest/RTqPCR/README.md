# RT-qPCR Candidate Support

This directory contains small tables documenting candidate target selection and B. mori target QC for
RT-qPCR planning.

## P. hoenei Target Tables

| File | Role |
|---|---|
| `CYP_RTqPCR_candidate_master_from_36CYP.tsv` | Candidate target table derived from the 36-HQ CYP layer. |
| `CYP_RTqPCR_final_15CYP_sequence_length_index.tsv` | Sequence length index for the final 15-CYP target set. |
| `CYP_RTqPCR_true_target_mapping_from_Figure1.tsv` | Mapping between Figure1 CYP targets and final RT-qPCR target records. |
| `README_FINAL_15CYP_RTqPCR_targets.md` | Notes on external FASTA files used for primer design. |

## B. mori Target QC

| File | Role |
|---|---|
| `Bmori_target_CYP_gene_groups_15.tsv` | B. mori target CYP groups reviewed for RT-qPCR planning. |
| `Bmori_CYP_multi_isoform_integrated_evidence_summary.tsv` | Multi-isoform evidence summary for selected B. mori CYP targets. |
| `Bmori_CYP12_final_transcript_length_QC.tsv` | Transcript-length QC for CYP12-related B. mori targets. |
| `Bmori_CYP12_primer3_top1_candidates.tsv` | Primer3 top-candidate summary for CYP12 targets. |
| `Bmori_CYP13_primer3_top1_candidates.tsv` | Primer3 top-candidate summary for CYP13 targets. |

## External Data

Primer-design FASTA files and final primer outputs are sequence artifacts and are not committed in
this lightweight archive. If final primers become part of the formal release, add primer tables here
and store FASTA/source sequence files in durable external storage with checksums.
