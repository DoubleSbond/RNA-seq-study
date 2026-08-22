#!/bin/bash
set -euo pipefail
out=/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/environment_snapshot_20260819T224500JST
test ! -e "$out"
mkdir -p "$out/failed_run_logs"

{
  date -Is
  hostname
  uname -a
  df -h /lustre10/home/tuatchenjh9703
} >"$out/system.txt"

{
  /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/diamond version
  /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastp -version
  /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/hmmscan -h | head -4
  /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/mafft --version
  /home/tuatchenjh9703/miniconda3/envs/busco_env/bin/FastTree 2>&1 | head -3
  /home/tuatchenjh9703/miniconda3/bin/iqtree --version
  pepstats -version
  tmap -version
} >"$out/software_versions.txt" 2>&1

/home/tuatchenjh9703/miniconda3/bin/conda list --prefix /home/tuatchenjh9703/miniconda3/envs/busco_env >"$out/busco_env_conda_list.txt"
/home/tuatchenjh9703/miniconda3/bin/conda list --prefix /home/tuatchenjh9703/miniconda3/envs/interproscan >"$out/interproscan_env_conda_list.txt"
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastdbcmd -db /lustre10/home/tuatchenjh9703/ph/07_homology/ABC/Bmori_db -info >"$out/Bmori_blastdb_info.txt"
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/blastdbcmd -db /lustre10/home/tuatchenjh9703/ph/07_homology/ABC/Spodo_db -info >"$out/Spodoptera_blastdb_info.txt"
/home/tuatchenjh9703/miniconda3/envs/busco_env/bin/diamond dbinfo --db /lustre10/home/tuatchenjh9703/ph/db/uniprot/uniprot_sprot.dmnd >"$out/SwissProt_diamond_info.txt" 2>&1
ls -lh /lustre10/home/tuatchenjh9703/tools/pfam/Pfam-A.hmm* >"$out/Pfam_files.txt"

for run in interproscan_20260819T181500JST interproscan_sanitized_20260819T184500JST interpro_pfam_20260819T191500JST reference_trees_20260819T203000JST; do
  source_dir=/lustre10/home/tuatchenjh9703/ph/07_family_analysis/_automation_runs/$run
  target="$out/failed_run_logs/$run"
  mkdir -p "$target"
  find "$source_dir" -maxdepth 2 -type f \( -name '*.log' -o -name 'scheduler.*' -o -name 'input_sanitization.tsv' \) -exec cp -n {} "$target"/ \;
done

find "$out" -type f -printf '%P\t%s\n' | sort >"$out/output_inventory.tsv"
sha256sum "$out"/*.txt "$out"/failed_run_logs/*/* >"$out/sha256.tsv"
