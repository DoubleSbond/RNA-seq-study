# Data

This directory intentionally tracks documentation only.

Do not commit large raw data or bulky intermediates to GitHub. Instead, record where data can be obtained and how integrity was checked.

Recommended records:

- Public accession identifiers, such as NCBI SRA accessions.
- External archive DOI or persistent URL.
- HPC or institutional storage path, if the repository is private and such paths are safe to share.
- File names, sizes, and checksums in `results_manifest/checksums.tsv`.

Files commonly kept outside Git:

- `*.fastq`, `*.fq`, and compressed read files.
- Large `*.fasta`, `*.fa`, and transcriptome assemblies.
- `*.bam`, `*.sam`, and alignment intermediates.
- BLAST, DIAMOND, HMMER, and other large database files.
