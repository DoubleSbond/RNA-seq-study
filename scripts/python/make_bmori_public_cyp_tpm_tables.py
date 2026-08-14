import re
import math
import argparse
import pandas as pd
from pathlib import Path
from urllib.parse import unquote

parser = argparse.ArgumentParser(
    description="Build B. mori midgut CYP TPM tables from public Salmon quantification outputs."
)
parser.add_argument(
    "--base-dir",
    default=".",
    help="Directory containing sample_info.tsv and quant/<Run>/quant.sf. Default: current directory.",
)
parser.add_argument(
    "--gff",
    required=True,
    help="B. mori GFF/GFF3 annotation file used to extract CYP transcript annotations.",
)
parser.add_argument(
    "--sample-info",
    default=None,
    help="Sample metadata TSV. Default: <base-dir>/sample_info.tsv.",
)
args = parser.parse_args()

BASE = Path(args.base_dir)
GFF = Path(args.gff)
sample_info_file = Path(args.sample_info) if args.sample_info else BASE / "sample_info.tsv"

# -----------------------------
# Quadrant gene lists from Ph vs Bm no-rep result
# -----------------------------
quadrants = {
    "Q1_Bm_Mulberry": [
        "CYP12A2", "CYP332A1", "CYP9A21", "CYP9A20", "CYP6AU1", "CYP6B2", "CYP6AB4"
    ],
    "Q2": [
        "CYP4M5", "CYP6AU1", "CYP306A1", "CYP6AB4", "CYP6B2", "CYP49A1"
    ],
    "Q3": [
        "CYP6B2", "CYP303A1", "CYP6B29", "CYP12A2", "CYP9A21", "CYP4M5",
        "CYP9A20", "CYP6K1", "CYP332A1", "CYP6B1"
    ],
    "Q4": [
        "CYP303A1", "CYP6B29", "CYP6B2", "CYP6B1", "CYP332A1", "CYP12A2",
        "CYP6K1", "CYP9A21", "CYP4M5", "CYP9A20", "CYP9E2"
    ]
}

target_order = []
for q, genes in quadrants.items():
    for g in genes:
        if g not in target_order:
            target_order.append(g)

def normalize_symbol(s):
    if s is None or pd.isna(s):
        return ""
    s = str(s).strip()
    s = s.replace("cytochrome P450 ", "")
    s = s.replace("cytochrome p450 ", "")
    s = s.replace("monooxygenase ", "")
    s = s.replace(" ", "")
    s = s.replace("-", "-")
    if s.lower().startswith("cyp"):
        return "CYP" + s[3:].upper()
    return s.upper()

def parse_attr(attr):
    d = {}
    for part in attr.strip().split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k] = unquote(v)
    return d

def extract_cyp_symbol(row):
    texts = [
        str(row.get("gene", "")),
        str(row.get("product", "")),
        str(row.get("Name", "")),
        str(row.get("ID", "")),
        str(row.get("raw_attr", "")),
    ]
    text = " ".join(texts)

    # Direct Cyp/CYP symbols: Cyp6b29, CYP12A2, CYP9A21 etc.
    m = re.search(r"\bCYP\s*[-_ ]*([0-9]+[A-Z]+[0-9]+[A-Z0-9]*(?:-[A-Z]+)?)\b", text, flags=re.I)
    if m:
        return normalize_symbol("CYP" + m.group(1))

    m = re.search(r"\bCyp\s*[-_ ]*([0-9]+[A-Za-z]+[0-9]+[A-Za-z0-9]*(?:-[A-Za-z]+)?)\b", text, flags=re.I)
    if m:
        return normalize_symbol("CYP" + m.group(1))

    # product strings like "cytochrome P450 6B2-like" or "probable cytochrome P450 303a1"
    m = re.search(r"cytochrome\s+P450\s+([0-9]+[A-Za-z]+[0-9]+[A-Za-z0-9]*(?:-like)?)", text, flags=re.I)
    if m:
        return normalize_symbol("CYP" + m.group(1))

    # Last fallback: any P450-like token after whitespace
    m = re.search(r"\b([0-9]+[A-Za-z]+[0-9]+[A-Za-z0-9]*(?:-like)?)\b", text)
    if m and re.search(r"cytochrome\s+P450|CYP|Cyp", text, flags=re.I):
        return normalize_symbol("CYP" + m.group(1))

    return ""

def quadrant_membership(symbol):
    memberships = []
    base = symbol.replace("-LIKE", "")
    for q, genes in quadrants.items():
        if symbol in genes or base in genes:
            memberships.append(q)
    return ";".join(memberships)

# -----------------------------
# 1. Parse CYP transcript annotations from GFF
# -----------------------------
rows = []
with open(GFF) as f:
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 9:
            continue

        seqid, source, ftype, start, end, score, strand, phase, attr = parts

        # RefSeq transcript features usually mRNA
        if ftype not in ["mRNA", "transcript", "lnc_RNA", "ncRNA"]:
            continue

        a = parse_attr(attr)
        product = a.get("product", "")
        gene = a.get("gene", "")
        name = a.get("Name", "")
        transcript_id = a.get("transcript_id", "")
        ID = a.get("ID", "")
        parent = a.get("Parent", "")
        dbxref = a.get("Dbxref", "")
        gbkey = a.get("gbkey", "")

        text = " ".join([product, gene, name, transcript_id, ID, attr])
        if not re.search(r"cytochrome\s+P450|CYP|Cyp", text, flags=re.I):
            continue

        r = {
            "seqid": seqid,
            "start": int(start),
            "end": int(end),
            "strand": strand,
            "feature_type": ftype,
            "ID": ID,
            "Parent": parent,
            "Name": name,
            "transcript_id": transcript_id,
            "gene": gene,
            "product": product,
            "Dbxref": dbxref,
            "gbkey": gbkey,
            "raw_attr": attr,
        }
        r["cyp_symbol"] = extract_cyp_symbol(r)
        if not r["cyp_symbol"]:
            r["cyp_symbol"] = "UNPARSED_CYP"

        # Gene-level grouping ID
        # Prefer explicit gene symbol if available, otherwise Parent/gene locus.
        if gene and not gene.startswith("LOC"):
            gene_group = normalize_symbol(gene)
        else:
            gene_group = gene if gene else parent.replace("gene-", "")
        r["gene_group"] = gene_group
        r["quadrant_membership"] = quadrant_membership(r["cyp_symbol"])

        rows.append(r)

ann = pd.DataFrame(rows).drop_duplicates(subset=["Name", "transcript_id", "ID"])
ann.to_csv("Bmori_all_CYP_transcripts_from_GFF.tsv", sep="\t", index=False)

# Long annotation table for matching Salmon transcript names
ann_long_rows = []
for _, r in ann.iterrows():
    for col in ["Name", "transcript_id"]:
        val = str(r.get(col, ""))
        if val and val != "nan":
            rr = r.to_dict()
            rr["match_id"] = val
            rr["match_source"] = col
            ann_long_rows.append(rr)
ann_long = pd.DataFrame(ann_long_rows).drop_duplicates(subset=["match_id", "ID"])

# -----------------------------
# 2. Read Salmon quant.sf files
# -----------------------------
sample_info = pd.read_csv(sample_info_file, sep="\t")
sample_order = sample_info["Run"].tolist()

expr_rows = []
for run in sample_order:
    q = BASE / "quant" / run / "quant.sf"
    if not q.exists():
        raise FileNotFoundError(f"Missing quant.sf: {q}")
    df = pd.read_csv(q, sep="\t")
    df["Run"] = run
    expr_rows.append(df[["Run", "Name", "Length", "EffectiveLength", "TPM", "NumReads"]])

expr = pd.concat(expr_rows, ignore_index=True)

# -----------------------------
# 3. Merge CYP annotation + TPM
# -----------------------------
m = expr.merge(ann_long, left_on="Name", right_on="match_id", how="inner")

# After merge, pandas renames duplicated Name columns to Name_x and Name_y.
# Name_x is the Salmon transcript ID; Name_y is the GFF transcript Name.
if "Name_x" in m.columns:
    m["salmon_transcript_id"] = m["Name_x"]
elif "Name" in m.columns:
    m["salmon_transcript_id"] = m["Name"]
else:
    raise KeyError("Cannot find Salmon transcript ID column after merge.")

# Transcript-level TPM matrix
tpm_wide = m.pivot_table(index=[
    "salmon_transcript_id", "cyp_symbol", "gene_group", "gene", "product", "seqid", "start", "end", "strand",
    "quadrant_membership"
], columns="Run", values="TPM", aggfunc="sum").reset_index()

# Ensure all sample columns exist and ordered
for s in sample_order:
    if s not in tpm_wide.columns:
        tpm_wide[s] = 0.0

female_samples = sample_info.loc[sample_info["Sex"] == "female", "Run"].tolist()
male_samples = sample_info.loc[sample_info["Sex"] == "male", "Run"].tolist()

tpm_wide["Female_mean_TPM"] = tpm_wide[female_samples].mean(axis=1)
tpm_wide["Female_sd_TPM"] = tpm_wide[female_samples].std(axis=1)
tpm_wide["Male_mean_TPM"] = tpm_wide[male_samples].mean(axis=1)
tpm_wide["Male_sd_TPM"] = tpm_wide[male_samples].std(axis=1)
tpm_wide["All6_mean_TPM"] = tpm_wide[sample_order].mean(axis=1)
tpm_wide["All6_sd_TPM"] = tpm_wide[sample_order].std(axis=1)
tpm_wide["All6_max_TPM"] = tpm_wide[sample_order].max(axis=1)

tpm_wide = tpm_wide.sort_values(["All6_mean_TPM", "cyp_symbol"], ascending=[False, True])
tpm_wide.to_csv("Bm_ML_midgut_ALL_CYP_transcript_level_TPM.tsv", sep="\t", index=False)

# -----------------------------
# 4. Gene/symbol-level summary
#    Sum TPM over transcript variants belonging to the same gene_group/symbol/product block.
# -----------------------------
# Make a cleaner gene key: gene_group + cyp_symbol
m["gene_key"] = m["gene_group"].astype(str) + "|" + m["cyp_symbol"].astype(str)

gene_meta_cols = ["gene_key", "gene_group", "cyp_symbol", "gene", "product", "quadrant_membership"]
gene_meta = (
    m[gene_meta_cols]
    .drop_duplicates()
    .groupby("gene_key", as_index=False)
    .agg({
        "gene_group": "first",
        "cyp_symbol": "first",
        "gene": lambda x: ";".join(sorted(set(map(str, x)))),
        "product": lambda x: "; ".join(sorted(set(map(str, x))))[:1000],
        "quadrant_membership": lambda x: ";".join(sorted(set([v for v in x.astype(str) if v and v != "nan"])))
    })
)

gene_expr = (
    m.groupby(["gene_key", "Run"], as_index=False)["TPM"]
    .sum()
    .pivot_table(index="gene_key", columns="Run", values="TPM", aggfunc="sum")
    .reset_index()
)

for s in sample_order:
    if s not in gene_expr.columns:
        gene_expr[s] = 0.0

gene_out = gene_meta.merge(gene_expr, on="gene_key", how="left")

gene_out["Female_mean_TPM"] = gene_out[female_samples].mean(axis=1)
gene_out["Female_sd_TPM"] = gene_out[female_samples].std(axis=1)
gene_out["Male_mean_TPM"] = gene_out[male_samples].mean(axis=1)
gene_out["Male_sd_TPM"] = gene_out[male_samples].std(axis=1)
gene_out["All6_mean_TPM"] = gene_out[sample_order].mean(axis=1)
gene_out["All6_sd_TPM"] = gene_out[sample_order].std(axis=1)
gene_out["All6_max_TPM"] = gene_out[sample_order].max(axis=1)

gene_out = gene_out.sort_values(["All6_mean_TPM", "cyp_symbol"], ascending=[False, True])
gene_out.to_csv("Bm_ML_midgut_ALL_CYP_gene_symbol_level_TPM.tsv", sep="\t", index=False)

# -----------------------------
# 5. Quadrant target subset
# -----------------------------
def is_target_symbol(sym):
    sym = str(sym)
    base = sym.replace("-LIKE", "")
    return sym in target_order or base in target_order

target_transcript = tpm_wide[tpm_wide["cyp_symbol"].apply(is_target_symbol)].copy()
target_gene = gene_out[gene_out["cyp_symbol"].apply(is_target_symbol)].copy()

target_transcript.to_csv("Bm_ML_midgut_QUADRANT_CYP_transcript_level_TPM.tsv", sep="\t", index=False)
target_gene.to_csv("Bm_ML_midgut_QUADRANT_CYP_gene_symbol_level_TPM.tsv", sep="\t", index=False)

# -----------------------------
# 6. Optional Excel workbook
# -----------------------------
try:
    with pd.ExcelWriter("Bm_ML_midgut_CYP_TPM_full_tables.xlsx", engine="openpyxl") as writer:
        sample_info.to_excel(writer, sheet_name="sample_info", index=False)
        ann.to_excel(writer, sheet_name="all_CYP_GFF_annotation", index=False)
        tpm_wide.to_excel(writer, sheet_name="ALL_CYP_transcript_TPM", index=False)
        gene_out.to_excel(writer, sheet_name="ALL_CYP_gene_symbol_TPM", index=False)
        target_transcript.to_excel(writer, sheet_name="quadrant_CYP_transcript", index=False)
        target_gene.to_excel(writer, sheet_name="quadrant_CYP_gene_symbol", index=False)
    excel_msg = "Bm_ML_midgut_CYP_TPM_full_tables.xlsx"
except Exception as e:
    excel_msg = f"Excel not generated: {e}"

# -----------------------------
# 7. Console summary
# -----------------------------
print("Saved:")
print("  Bmori_all_CYP_transcripts_from_GFF.tsv")
print("  Bm_ML_midgut_ALL_CYP_transcript_level_TPM.tsv")
print("  Bm_ML_midgut_ALL_CYP_gene_symbol_level_TPM.tsv")
print("  Bm_ML_midgut_QUADRANT_CYP_transcript_level_TPM.tsv")
print("  Bm_ML_midgut_QUADRANT_CYP_gene_symbol_level_TPM.tsv")
print(" ", excel_msg)

print("\nCYP transcript count:", len(tpm_wide))
print("CYP gene/symbol group count:", len(gene_out))

print("\nTop 20 CYP gene/symbol groups by All6_mean_TPM:")
show_cols = ["gene_group", "cyp_symbol", "gene", "All6_mean_TPM", "All6_sd_TPM",
             "Female_mean_TPM", "Male_mean_TPM", "quadrant_membership", "product"]
print(gene_out[show_cols].head(20).to_string(index=False))

print("\nQuadrant CYP gene/symbol summary:")
show_cols2 = ["gene_group", "cyp_symbol", "All6_mean_TPM", "All6_sd_TPM",
              "Female_mean_TPM", "Male_mean_TPM", "quadrant_membership", "product"]
print(target_gene[show_cols2].to_string(index=False))
