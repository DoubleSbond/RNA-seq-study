## Summary

- 

## Archive Layer

- [ ] RNA-seq / DESeq2
- [ ] 91-CYP discovery
- [ ] CYP screening / 36-HQ
- [ ] B. mori comparison
- [ ] RT-qPCR
- [ ] unknownCYP
- [ ] Documentation / release / maintenance

## Public-Safety Checks

- [ ] No raw FASTQ, full assemblies, large FASTA files, bulky tool outputs, or compressed archives were added.
- [ ] No credentials, tokens, SSH keys, private config, or internal-only absolute paths were added.
- [ ] Large or external assets are tracked in `results_manifest/external_assets_manifest.tsv` when relevant.

## Validation

- [ ] Ran `python scripts/python/update_public_checksums.py`.
- [ ] Ran `python scripts/python/validate_archive.py`.
- [ ] Updated relevant README/provenance notes.

## HPC Dependency

- [ ] No HPC access was required.
- [ ] HPC confirmation is still needed and documented.
