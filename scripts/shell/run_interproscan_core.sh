#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: bash scripts/shell/run_interproscan_core.sh <interproscan.sh> <input_peptide_fasta> <output_tsv> [threads]" >&2
  exit 1
fi

interproscan_sh="$1"
input_fasta="$2"
output_tsv="$3"
threads="${4:-8}"

mkdir -p "$(dirname "$output_tsv")"

bash "$interproscan_sh" \
  -i "$input_fasta" \
  -f TSV \
  -appl Pfam,CDD,TIGRFAM,ProSiteProfiles,ProSitePatterns,Coils \
  -dp \
  -goterms \
  -iprlookup \
  -cpu "$threads" \
  -o "$output_tsv"
