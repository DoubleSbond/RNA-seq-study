#!/usr/bin/env bash
set -euo pipefail

HOME_ROOT="${1:-$HOME}"
PROJECT_ROOT="${2:-$HOME/ph}"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUTDIR="$PROJECT_ROOT/00_project_admin/inventories/$STAMP"

mkdir -p "$OUTDIR"

printf 'home_root\t%s\nproject_root\t%s\ntimestamp\t%s\n' "$HOME_ROOT" "$PROJECT_ROOT" "$STAMP" > "$OUTDIR/inventory_context.tsv"

# Top-level home inventory, limited to one level so it remains readable.
find "$HOME_ROOT" -maxdepth 1 -mindepth 1 \
  -printf '%p\t%f\t%y\t%s\t%TY-%Tm-%Td %TH:%TM:%TS\n' \
  | sort > "$OUTDIR/home_top_level.tsv"

# Project top-level inventory.
find "$PROJECT_ROOT" -maxdepth 1 -mindepth 1 \
  -printf '%p\t%f\t%y\t%s\t%TY-%Tm-%Td %TH:%TM:%TS\n' \
  | sort > "$OUTDIR/project_top_level.tsv"

# Project directory tree up to three levels deep.
find "$PROJECT_ROOT" -maxdepth 3 -type d \
  -printf '%p\t%TY-%Tm-%Td %TH:%TM:%TS\n' \
  | sort > "$OUTDIR/project_dirs_maxdepth3.tsv"

# File inventory for small-to-medium metadata review. No file contents are copied.
find "$PROJECT_ROOT" -type f \
  -printf '%p\t%s\t%TY-%Tm-%Td %TH:%TM:%TS\n' \
  | sort > "$OUTDIR/project_files.tsv"

# Home-level likely project leftovers. Keep this broad but read-only.
find "$HOME_ROOT" -maxdepth 1 -type f \
  \( -iname 'CYP*' -o -iname 'CarE*' -o -iname 'GST*' -o -iname 'UGT*' -o -iname 'SULT*' -o -iname 'ABC*' -o -iname 'core*' -o -iname '*.tsv' -o -iname '*.txt' -o -iname '*.fa' -o -iname '*.fasta' -o -iname '*.R' -o -iname '*.log' -o -iname '*.tar.gz' \) \
  -printf '%p\t%s\t%TY-%Tm-%Td %TH:%TM:%TS\n' \
  | sort > "$OUTDIR/home_project_like_files.tsv"

# Size summary for top-level project directories. du can be slow on large raw-data trees but is still read-only.
if command -v du >/dev/null 2>&1; then
  du -sh "$PROJECT_ROOT"/* 2>/dev/null | sort -h > "$OUTDIR/project_top_level_du.tsv" || true
  du -sh "$HOME_ROOT"/* 2>/dev/null | sort -h > "$OUTDIR/home_top_level_du.tsv" || true
fi

# Checksums for small public-safe candidate files only. Large files are listed separately.
: > "$OUTDIR/small_file_sha256.tsv"
: > "$OUTDIR/large_files_needing_checksum_review.tsv"

while IFS= read -r file; do
  size=$(stat -c '%s' "$file" 2>/dev/null || echo 0)
  if [ "$size" -le 104857600 ]; then
    if command -v sha256sum >/dev/null 2>&1; then
      sha256sum "$file" >> "$OUTDIR/small_file_sha256.tsv" || true
    fi
  else
    printf '%s\t%s\n' "$file" "$size" >> "$OUTDIR/large_files_needing_checksum_review.tsv"
  fi
done < "$OUTDIR/home_project_like_files.tsv"

cat > "$OUTDIR/README.txt" <<'EOF'
This inventory is read-only.

Review these files first:
- inventory_context.tsv
- home_top_level.tsv
- project_top_level.tsv
- project_top_level_du.tsv
- home_project_like_files.tsv
- large_files_needing_checksum_review.tsv

Do not delete files based only on this inventory.
Create a reviewed move manifest before moving anything.
EOF

echo "Inventory written to: $OUTDIR"
