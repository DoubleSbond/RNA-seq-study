#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: bash scripts/shell/collect_external_asset_checksums.sh <asset_paths.tsv> <output.tsv>" >&2
  exit 1
fi

asset_paths="$1"
out="$2"
mkdir -p "$(dirname "$out")"

if command -v sha256sum >/dev/null 2>&1; then
  hash_cmd="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  hash_cmd="shasum -a 256"
else
  echo "No SHA256 command found: need sha256sum or shasum." >&2
  exit 1
fi

printf "asset_id\tpath_type\tpath\tbytes\tsha256\tstatus\tnotes\n" > "$out"

tail -n +2 "$asset_paths" | while IFS=$'\t' read -r asset_id path; do
  [[ -z "${asset_id:-}" ]] && continue

  if [[ -z "${path:-}" ]]; then
    printf "%s\tmissing\t\t\t\tmissing_path\t\n" "$asset_id" >> "$out"
  elif [[ -f "$path" ]]; then
    bytes="$(wc -c < "$path" | tr -d ' ')"
    sha="$($hash_cmd "$path" | awk '{print $1}')"
    printf "%s\tfile\t%s\t%s\t%s\tok\t\n" "$asset_id" "$path" "$bytes" "$sha" >> "$out"
  elif [[ -d "$path" ]]; then
    count="$(find "$path" -type f | wc -l | tr -d ' ')"
    bytes="$(find "$path" -type f -print0 | xargs -0 wc -c 2>/dev/null | awk 'END{print $1}')"
    printf "%s\tdirectory\t%s\t%s\t\tneeds_manifest\t%s files; create a stable per-file checksum manifest or archive before final release.\n" "$asset_id" "$path" "${bytes:-}" "$count" >> "$out"
  else
    printf "%s\tmissing\t%s\t\t\tpath_not_found\t\n" "$asset_id" "$path" >> "$out"
  fi
done

echo "Wrote: $out"
