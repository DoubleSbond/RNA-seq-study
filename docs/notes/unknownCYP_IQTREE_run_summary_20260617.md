# UnknownCYP diagnostic phylogeny IQ-TREE run summary

Date: 2026-06-17

Input alignment:
phylogeny/unknownCYP_core10_Ph36_BmSf_reference.clean_header.mafft.faa

Input sequences:
- unknownCYP core: 10
- Ph 36HQ CYP: 36
- Bmori top1 reference: 25
- Spodoptera top1 reference: 28
- Total: 99 protein sequences

Alignment:
- MAFFT completed successfully.
- Clean headers were used for tree interpretation.

IQ-TREE:
- IQ-TREE was run using ModelFinder, SH-aLRT 1000, and ultrafast bootstrap 1000.
- Command:
  iqtree -s phylogeny/unknownCYP_core10_Ph36_BmSf_reference.clean_header.mafft.faa \
    -m MFP \
    -B 1000 \
    -alrt 1000 \
    -T AUTO \
    --prefix phylogeny/unknownCYP_core10_Ph36_BmSf_reference.clean_header

Main output:
phylogeny/unknownCYP_core10_Ph36_BmSf_reference.clean_header.treefile

Purpose:
This tree is used as a diagnostic phylogenetic placement tree for assigning unresolved Ph unknownCYP candidates to likely CYP clades/families together with Ph 36HQ CYPs and Bmori/Spodoptera reference proteins.
