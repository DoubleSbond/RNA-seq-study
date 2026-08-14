#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: bash scripts/shell/run_salmon_quant_samples.sh <sample_list.tsv> <salmon_index> [read_dir] [output_dir] [threads]" >&2
  echo "sample_list.tsv columns: sample,read1,read2" >&2
  exit 1
fi

sample_list="$1"
salmon_index="$2"
read_dir="${3:-data/raw_fastq}"
output_dir="${4:-salmon_quant}"
threads="${5:-8}"

mkdir -p "$output_dir"

tail -n +2 "$sample_list" | while IFS=$'\t,' read -r sample read1 read2; do
  [[ -z "${sample:-}" ]] && continue

  salmon quant \
    -i "$salmon_index" \
    -l A \
    -1 "${read_dir}/${read1}" \
    -2 "${read_dir}/${read2}" \
    -p "$threads" \
    --validateMappings \
    --gcBias \
    -o "${output_dir}/${sample}_quant"
done
