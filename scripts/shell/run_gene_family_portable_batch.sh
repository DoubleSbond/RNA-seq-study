#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 PROJECT_ROOT RUN_ROOT REPOSITORY_ROOT" >&2
  exit 2
fi

PROJECT_ROOT=$1
RUN_ROOT=$2
REPOSITORY_ROOT=$3
CONFIG="$REPOSITORY_ROOT/config/gene_families.tsv"
BUILDER="$REPOSITORY_ROOT/scripts/python/build_gene_family_portable_package.py"
TPM="$PROJECT_ROOT/06_DEGsAnalysis/results/TPM_gene_all_withMeanSD.tsv"
DESEQ2="$PROJECT_ROOT/06_DEGsAnalysis/results/_calibration_exports/DESeq2_results_all_genes.tsv"

[[ ! -e "$RUN_ROOT" ]] || { echo "[ERROR] Refusing existing run root: $RUN_ROOT" >&2; exit 1; }
for path in "$CONFIG" "$BUILDER" "$TPM" "$DESEQ2"; do
  [[ -f "$path" ]] || { echo "[ERROR] Missing input: $path" >&2; exit 1; }
done

mkdir -p "$RUN_ROOT"
printf 'started_utc\t%s\nproject_root\t%s\nrun_root\t%s\n' "$(date -u +%FT%TZ)" "$PROJECT_ROOT" "$RUN_ROOT" > "$RUN_ROOT/batch_metadata.tsv"

tail -n +2 "$CONFIG" | while IFS=$'\t' read -r family phase candidate_ids final_ids candidate_peptides evidence_table; do
  candidate_ids=${candidate_ids//<PROJECT_ROOT>/$PROJECT_ROOT}
  final_ids=${final_ids//<PROJECT_ROOT>/$PROJECT_ROOT}
  candidate_peptides=${candidate_peptides//<PROJECT_ROOT>/$PROJECT_ROOT}
  evidence_table=${evidence_table//<PROJECT_ROOT>/$PROJECT_ROOT}
  python3 "$BUILDER" \
    --family "$family" \
    --phase "$phase" \
    --candidate-ids "$candidate_ids" \
    --final-ids "$final_ids" \
    --tpm "$TPM" \
    --deseq2 "$DESEQ2" \
    --candidate-peptides "$candidate_peptides" \
    --evidence-table "$evidence_table" \
    --output-dir "$RUN_ROOT/$family" \
    > "$RUN_ROOT/${family}.stdout.log" 2> "$RUN_ROOT/${family}.stderr.log"
done

printf 'completed_utc\t%s\n' "$(date -u +%FT%TZ)" >> "$RUN_ROOT/batch_metadata.tsv"
find "$RUN_ROOT" -maxdepth 2 -type f -printf '%s\t%p\n' | sort -k2 > "$RUN_ROOT/output_inventory.tsv"
