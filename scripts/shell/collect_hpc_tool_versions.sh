#!/usr/bin/env bash
set -euo pipefail

out="${1:-hpc_tool_versions_to_confirm.tsv}"
mkdir -p "$(dirname "$out")"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

printf "tool\tcommand\tstatus\tversion_output\n" > "$out"

run_version() {
  tool="$1"
  shift
  cmd="$*"

  if command -v "$1" >/dev/null 2>&1; then
    if "$@" >"$tmp" 2>&1; then
      status="ok"
    else
      status="command_failed"
    fi
    version="$(tr '\n' ' ' < "$tmp" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
  else
    status="not_found"
    version=""
  fi

  printf "%s\t%s\t%s\t%s\n" "$tool" "$cmd" "$status" "$version" >> "$out"
}

run_version "R" "R" "--version"
run_version "Rscript" "Rscript" "--version"
run_version "fastp" "fastp" "--version"
run_version "Trinity" "Trinity" "--version"
run_version "Salmon" "salmon" "--version"
run_version "BUSCO" "busco" "--version"
run_version "InterProScan" "interproscan.sh" "-version"
run_version "IQ-TREE" "iqtree3" "--version"
run_version "BLAST blastx" "blastx" "-version"
run_version "BLAST blastp" "blastp" "-version"
run_version "HMMER hmmsearch" "hmmsearch" "-h"
run_version "DIAMOND" "diamond" "version"
run_version "seqkit" "seqkit" "version"
run_version "MAFFT" "mafft" "--version"

echo "Wrote: $out"
