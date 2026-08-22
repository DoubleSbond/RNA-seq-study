#!/bin/bash
set -euo pipefail
out=/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/environment_snapshot_v2_20260819T231500JST
test ! -e "$out"
mkdir -p "$out/failed_run_logs"
date -Is >"$out/captured_at.txt"
hostname >"$out/hostname.txt"
uname -a >"$out/uname.txt"
df -h /lustre10/home/tuatchenjh9703 >"$out/filesystem.txt"

for item in \
  diamond:/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/diamond \
  blastp:/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastp \
  hmmscan:/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/hmmscan \
  mafft:/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/mafft \
  FastTree:/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/FastTree \
  iqtree:/home/tuatchenjh9703/miniconda3/bin/iqtree \
  pepstats:/usr/bin/pepstats \
  tmap:/usr/bin/tmap; do
  name="${item%%:*}"; path="${item#*:}"
  sha256sum "$path" >>"$out/executable_sha256.tsv"
  printf '%s\t%s\n' "$name" "$path" >>"$out/executable_paths.tsv"
done

/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/diamond version >"$out/diamond_version.txt" 2>&1
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastp -version >"$out/blast_version.txt" 2>&1
/home/tuatchenjh9703/miniconda3/bin/iqtree --version >"$out/iqtree_version.txt" 2>&1
pepstats -version >"$out/emboss_version.txt" 2>&1
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastdbcmd -db /lustre10/home/tuatchenjh9703/ph/07_homology/ABC/Bmori_db -info >"$out/Bmori_blastdb_info.txt"
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastdbcmd -db /lustre10/home/tuatchenjh9703/ph/07_homology/ABC/Spodo_db -info >"$out/Spodoptera_blastdb_info.txt"
timeout 20 /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/diamond dbinfo --db /lustre10/home/tuatchenjh9703/ph/db/uniprot/uniprot_sprot.dmnd >"$out/SwissProt_diamond_info.txt" 2>&1 || true
ls -lh /lustre10/home/tuatchenjh9703/tools/pfam/Pfam-A.hmm* >"$out/Pfam_files.txt"

for run in interproscan_20260819T181500JST interproscan_sanitized_20260819T184500JST interpro_pfam_20260819T191500JST reference_trees_20260819T203000JST; do
  source_dir=/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/$run
  target="$out/failed_run_logs/$run"
  mkdir -p "$target"
  find "$source_dir" -maxdepth 2 -type f \( -name '*.log' -o -name 'scheduler.*' -o -name 'input_sanitization.tsv' \) -exec cp -n {} "$target"/ \;
done
find "$out" -type f -printf '%P\t%s\n' | sort >"$out/output_inventory.tsv"
find "$out" -type f ! -name sha256.tsv -print0 | sort -z | xargs -0 sha256sum >"$out/sha256.tsv"
