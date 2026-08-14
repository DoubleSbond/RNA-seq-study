#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/shell/run_fastp_paired_samples.sh <sample_list.tsv> [raw_dir] [trimmed_dir] [report_dir] [threads]" >&2
  echo "sample_list.tsv columns: sample,read1,read2" >&2
  exit 1
fi

sample_list="$1"
raw_dir="${2:-data/raw_fastq}"
trimmed_dir="${3:-data/trimmed_fastq}"
report_dir="${4:-reports/fastp}"
threads="${5:-8}"
log_dir="logs/trimming"

mkdir -p "$trimmed_dir" "$report_dir" "$log_dir"

tail -n +2 "$sample_list" | while IFS=$'\t,' read -r sample read1 read2; do
  [[ -z "${sample:-}" ]] && continue

  input_r1="${raw_dir}/${read1}"
  input_r2="${raw_dir}/${read2}"
  output_r1="${trimmed_dir}/${sample}_1_trimmed.fq"
  output_r2="${trimmed_dir}/${sample}_2_trimmed.fq"

  fastp \
    --in1 "$input_r1" \
    --in2 "$input_r2" \
    --out1 "$output_r1" \
    --out2 "$output_r2" \
    --json "${report_dir}/${sample}_fastp.json" \
    --html "${report_dir}/${sample}_fastp.html" \
    --qualified_quality_phred 20 \
    --unqualified_percent_limit 40 \
    --length_required 50 \
    --correction \
    --overrepresentation_analysis \
    --thread "$threads" \
    --detect_adapter_for_pe \
    2> "${log_dir}/fastp_${sample}.log"
done
