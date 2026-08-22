#!/usr/bin/env python3
"""Apply the P. hoenei expression-background design to B. mori RefSeq data."""

from __future__ import annotations

import argparse, csv, json, math, random, re
from pathlib import Path
from statistics import median

PANELS = [
 ("Housekeeping","Ribosomal protein eL32 (RP49-like)",r"ribosomal (?:subunit )?protein (?:e?l32|49)|\brpl32\b"),
 ("Housekeeping","Actin",r"\bactin\b"),
 ("Housekeeping","Alpha/Beta tubulin",r"(?:alpha|beta)[ -]tubulin|tubulin (?:alpha|beta)"),
 ("Housekeeping","Elongation factor 1-alpha",r"elongation factor 1[- ]alpha"),
 ("Housekeeping","GAPDH",r"glyceraldehyde-3-phosphate dehydrogenase|\bgapdh\b"),
 ("Energy","ATP synthase",r"atp synthase subunit"),
 ("Digestion","Trypsin",r"\btrypsin\b"), ("Digestion","Chymotrypsin",r"\bchymotrypsin\b"),
 ("Digestion","Aminopeptidase N",r"aminopeptidase n\b"),
 ("Digestion","Carboxypeptidase",r"\bcarboxypeptidase\b"),
 ("Digestion","Alpha-amylase",r"alpha-amylase|\bamylase\b"),
 ("Digestion","Digestive lipase",r"pancreatic lipase|gastric lipase|triacylglycerol lipase|neutral lipase"),
 ("Immunity","Lysozyme",r"\blysozyme\b"), ("Immunity","Cecropin",r"\bcecropin\b"),
 ("Immunity","Defensin",r"\bdefensin\b"),
 ("Immunity","PGRP",r"peptidoglycan[- ]recognition protein"),
 ("Immunity","Prophenoloxidase",r"\bprophenoloxidase\b|phenoloxidase subunit"),
 ("Development","Juvenile hormone-binding protein",r"juvenile hormone-binding protein"),
 ("Development","Juvenile hormone esterase",r"juvenile hormone esterase"),
 ("Development","Ecdysone receptor",r"ecdysone receptor"),
 ("Development","Broad-complex",r"broad-complex|broad isoform"),
 ("Development","Ecdysis-triggering hormone receptor",r"ecdysis-triggering hormone receptor"),
]

def qtile(v,q):
 s=sorted(v); p=(len(s)-1)*q; lo=int(p); hi=math.ceil(p)
 return s[lo] if lo==hi else s[lo]+(s[hi]-s[lo])*(p-lo)

def write(path, rows, fields):
 with path.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,delimiter="\t",fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--tpm",type=Path,required=True); ap.add_argument("--tx2gene",type=Path,required=True); ap.add_argument("--gene-annotation",type=Path,required=True); ap.add_argument("--sample-info",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); ap.add_argument("--seed",type=int,default=20260822); a=ap.parse_args()
 a.output_dir.mkdir(parents=True,exist_ok=False)
 with a.sample_info.open(encoding="utf-8") as f: samples=[r["Run"] for r in csv.DictReader(f,delimiter="\t")]
 gene_ann={}
 with a.gene_annotation.open(encoding="utf-8") as f:
  for c in csv.reader(f,delimiter="\t"):
   if len(c)>=3: gene_ann[c[0]]={"GeneSymbol":c[1],"Annotation":c[2]}
 tx_gene={}
 with a.tx2gene.open(encoding="utf-8") as f:
  for c in csv.reader(f,delimiter="\t"):
   if len(c)>=2: tx_gene[c[0]]=c[1]
 rows=[]
 with a.tpm.open(encoding="utf-8") as f:
  for r in csv.DictReader(f,delimiter="\t"):
   tid=r["Name"]; gid=tx_gene.get(tid,""); ann=gene_ann.get(gid)
   if not ann: continue
   vals=[float(r[s]) for s in samples]; mean=sum(vals)/len(vals)
   rows.append({"TranscriptID":tid,"GeneID":gid,**ann,**{s:vals[i] for i,s in enumerate(samples)},"MeanTPM":mean,"MaxTPM":max(vals),"CV":(math.sqrt(sum((x-mean)**2 for x in vals)/(len(vals)-1))/mean if mean else None)})
 panel=[]; dist=[]
 for group,marker,pat in PANELS:
  hits=[r for r in rows if re.search(pat,r["Annotation"],re.I)]; hits.sort(key=lambda r:r["MeanTPM"],reverse=True)
  if not hits: dist.append({"Group":group,"Marker":marker,"CandidateCount":0}); continue
  v=[r["MeanTPM"] for r in hits]; rep=hits[0]
  panel.append({"SelectionType":"Functional_panel_top_expressed","Group":group,"Marker":marker,**rep})
  dist.append({"Group":group,"Marker":marker,"CandidateCount":len(hits),"MedianMeanTPM":median(v),"P25MeanTPM":qtile(v,.25),"P75MeanTPM":qtile(v,.75),"MaxMeanTPM":max(v),"RepresentativeTranscript":rep["TranscriptID"],"RepresentativeMeanTPM":rep["MeanTPM"],"RepresentativeAnnotation":rep["Annotation"]})
 eligible=sorted([r for r in rows if r["MeanTPM"]>0],key=lambda r:r["MeanTPM"]); rng=random.Random(a.seed); random_rows=[]
 for q in range(5):
  bucket=eligible[round(len(eligible)*q/5):round(len(eligible)*(q+1)/5)]
  for r in rng.sample(bucket,min(4,len(bucket))): random_rows.append({"SelectionType":f"Random_expression_quintile_{q+1}","Group":"Random background","Marker":"Fixed-seed random",**r})
 fields=["SelectionType","Group","Marker","TranscriptID","GeneID","GeneSymbol",*samples,"MeanTPM","MaxTPM","CV","Annotation"]
 write(a.output_dir/"functional_reference_panel.tsv",panel,fields); write(a.output_dir/"random_background_panel.tsv",random_rows,fields)
 write(a.output_dir/"functional_family_distribution.tsv",dist,["Group","Marker","CandidateCount","MedianMeanTPM","P25MeanTPM","P75MeanTPM","MaxMeanTPM","RepresentativeTranscript","RepresentativeMeanTPM","RepresentativeAnnotation"])
 summary={"species":"Bombyx mori","project":"PRJNA729897","tissue":"midgut","diet":"mulberry leaf","samples":samples,"tpm_rows_with_annotation":len(rows),"functional_markers_requested":len(PANELS),"functional_markers_recovered":len(panel),"random_background_n":len(random_rows),"seed":a.seed,"unit":"transcript-level TPM"}
 (a.output_dir/"run_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")

if __name__=="__main__": main()
