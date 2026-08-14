#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/shell/run_trinity_denovo_assembly.sh <sample_list.tsv> [trimmed_dir] [output_dir] [cpu] [max_memory]" >&2
  echo "sample_list.tsv columns: sample,read1,read2; read names are converted to <sample>_1_trimmed.fq and <sample>_2_trimmed.fq by default." >&2
  exit 1
fi

sample_list="$1"
trimmed_dir="${2:-data/trimmed_fastq}"
output_dir="${3:-trinity_assembly/trinity_out}"
cpu="${4:-32}"
max_memory="${5:-100G}"

left_reads=()
right_reads=()

while IFS=$'\t,' read -r sample _read1 _read2; do
  [[ -z "${sample:-}" ]] && continue
  left_reads+=("${trimmed_dir}/${sample}_1_trimmed.fq")
  right_reads+=("${trimmed_dir}/${sample}_2_trimmed.fq")
done < <(tail -n +2 "$sample_list")

left_csv=$(IFS=,; echo "${left_reads[*]}")
right_csv=$(IFS=,; echo "${right_reads[*]}")

Trinity \
  --seqType fq \
  --left "$left_csv" \
  --right "$right_csv" \
  --CPU "$cpu" \
  --max_memory "$max_memory" \
  --min_kmer_cov 2 \
  --output "$output_dir" \
  --full_cleanup \
  --verbose
