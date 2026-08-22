#!/usr/bin/env python3
"""Create cautious P. hoenei–B. mori expression-context comparison tables."""

import argparse, csv, math
from collections import defaultdict
from pathlib import Path
from statistics import median

def read(path):
 with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))
def write(path,rows,fields):
 with path.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,delimiter="\t",fieldnames=fields); w.writeheader(); w.writerows(rows)
def stats(vals):
 return {"GeneCount":len(vals),"MeanGeneTPM":sum(vals)/len(vals),"MedianGeneTPM":median(vals),"MaxGeneTPM":max(vals),"GenesMeanTPM_GE10":sum(x>=10 for x in vals)}

ap=argparse.ArgumentParser(); ap.add_argument("--phoenei-panel",type=Path,required=True); ap.add_argument("--bmori-panel",type=Path,required=True); ap.add_argument("--phoenei-cyp",type=Path,required=True); ap.add_argument("--bmori-cyp",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); a=ap.parse_args(); a.output_dir.mkdir(parents=True,exist_ok=False)
p={r["Marker"]:r for r in read(a.phoenei_panel)}; b={r["Marker"]:r for r in read(a.bmori_panel)}
rows=[]
for marker in sorted(set(p)|set(b)):
 pr,br=p.get(marker),b.get(marker); pv=float(pr["MeanTPM"]) if pr else None; bv=float(br["MeanTPM"]) if br else None
 rows.append({"Marker":marker,"Group":(pr or br)["Group"],"PhoeneiRepresentative":pr["TranscriptID"] if pr else "","PhoeneiMeanTPM":pv,"BmoriRepresentative":br["TranscriptID"] if br else "","BmoriMeanTPM":bv,"Bmori_to_Phoenei_Ratio":bv/pv if pv and bv is not None else "","Log2_Bmori_over_Phoenei":math.log2(bv/pv) if pv and bv else "","ComparisonUse":"context_only_not_species_effect"})
write(a.output_dir/"Phoenei_Bmori_functional_context.tsv",rows,["Marker","Group","PhoeneiRepresentative","PhoeneiMeanTPM","BmoriRepresentative","BmoriMeanTPM","Bmori_to_Phoenei_Ratio","Log2_Bmori_over_Phoenei","ComparisonUse"])

# P. hoenei table is gene-level; first column has an empty header.
with a.phoenei_cyp.open(encoding="utf-8-sig",newline="") as f:
 rr=csv.reader(f,delimiter="\t"); head=next(rr); ps=[]
 for c in rr:
  if len(c)>=7: ps.append(sum(float(x) for x in c[1:7])/6)
# B. mori transcript TPM is summed within RefSeq gene annotation before summary.
bm=read(a.bmori_cyp); sample_cols=[c for c in bm[0] if c.startswith("SRR")]; bg=defaultdict(lambda:[0.0]*len(sample_cols))
for r in bm:
 key=r.get("gene") or r.get("cyp_symbol_guess") or r["Name_x"]
 for i,c in enumerate(sample_cols): bg[key][i]+=float(r[c])
bs=[sum(v)/len(v) for v in bg.values()]
cyp=[{"Species":"P. hoenei","Dataset":"current six-sample de novo gene-level matrix","Aggregation":"91 broad CYP genes",**stats(ps)}, {"Species":"B. mori","Dataset":"PRJNA729897 mulberry-fed midgut","Aggregation":"RefSeq transcripts summed by annotated gene",**stats(bs)}]
write(a.output_dir/"CYP_expression_context.tsv",cyp,["Species","Dataset","Aggregation","GeneCount","MeanGeneTPM","MedianGeneTPM","MaxGeneTPM","GenesMeanTPM_GE10"])

compat=[
 {"Dimension":"Tissue","P_hoenei":"Current experimental sample context; not matched here as isolated midgut","B_mori":"Midgut","Comparability":"limited"},
 {"Dimension":"Diet","P_hoenei":"Dan and Mul conditions","B_mori":"Mulberry leaf only","Comparability":"partial"},
 {"Dimension":"Replication","P_hoenei":"3 + 3","B_mori":"3 female + 3 male","Comparability":"descriptive"},
 {"Dimension":"Reference","P_hoenei":"de novo Trinity","B_mori":"RefSeq genome-guided transcripts","Comparability":"limited"},
 {"Dimension":"Expression unit","P_hoenei":"gene-level for detox; Trinity transcript for functional panel","B_mori":"RefSeq transcript; CYP summed by gene","Comparability":"mixed"},
 {"Dimension":"Valid inference","P_hoenei":"within-dataset expression layer","B_mori":"within-midgut expression layer","Comparability":"rank_and_layer_only"},
]
write(a.output_dir/"comparability_matrix.tsv",compat,["Dimension","P_hoenei","B_mori","Comparability"])
