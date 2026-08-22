#!/usr/bin/env python3
"""Build an auditable expression-reference panel from TPM and Swiss-Prot hits."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path
from statistics import median


SAMPLES = ["Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3"]

PANELS = [
    ("Housekeeping", "Ribosomal protein eL32 (RP49-like)", r"\b(?:rpl32|rp49)\b|ribosomal subunit protein el32|ribosomal protein l32"),
    ("Housekeeping", "Actin", r"\bactin(?:\b|-)") ,
    ("Housekeeping", "Alpha/Beta tubulin", r"\b(?:alpha|beta)[ -]tubulin\b|\btubulin (?:alpha|beta)"),
    ("Housekeeping", "Elongation factor 1-alpha", r"elongation factor 1[- ]alpha|\bef-?1[- ]alpha\b"),
    ("Housekeeping", "GAPDH", r"glyceraldehyde-3-phosphate dehydrogenase|\bgapdh\b"),
    ("Energy", "ATP synthase", r"atp synthase subunit"),
    ("Digestion", "Trypsin", r"\btrypsin\b"),
    ("Digestion", "Chymotrypsin", r"\bchymotrypsin\b"),
    ("Digestion", "Aminopeptidase N", r"aminopeptidase n\b"),
    ("Digestion", "Carboxypeptidase", r"\bcarboxypeptidase\b"),
    ("Digestion", "Alpha-amylase", r"alpha-amylase|\bamylase\b"),
    ("Digestion", "Digestive lipase", r"pancreatic lipase|gastric lipase|triacylglycerol lipase|neutral lipase"),
    ("Immunity", "Lysozyme", r"\blysozyme\b"),
    ("Immunity", "Cecropin", r"\bcecropin\b"),
    ("Immunity", "Defensin", r"\bdefensin\b"),
    ("Immunity", "PGRP", r"peptidoglycan-recognition protein|peptidoglycan recognition protein"),
    ("Immunity", "Prophenoloxidase", r"\bprophenoloxidase\b|phenoloxidase subunit"),
    ("Development", "Juvenile hormone-binding protein", r"juvenile hormone-binding protein"),
    ("Development", "Juvenile hormone esterase", r"juvenile hormone esterase"),
    ("Development", "Ecdysone receptor", r"ecdysone receptor"),
    ("Development", "Broad-complex", r"broad-complex|broad isoform"),
    ("Development", "Ecdysis-triggering hormone receptor", r"ecdysis-triggering hormone receptor"),
]


def f(x: str) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def quantile(values: list[float], q: float) -> float:
    if not values:
        return math.nan
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    return s[lo] if lo == hi else s[lo] + (s[hi] - s[lo]) * (pos - lo)


def write_tsv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tpm", type=Path, required=True)
    ap.add_argument("--annotation", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=20260822)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)

    expression: dict[str, dict] = {}
    with args.tpm.open(encoding="utf-8", newline="") as src:
        for row in csv.DictReader(src, delimiter="\t"):
            vals = [f(row[s]) for s in SAMPLES]
            expression[row["GeneID"]] = {
                "TranscriptID": row["GeneID"],
                **{s: vals[i] for i, s in enumerate(SAMPLES)},
                "MeanTPM": sum(vals) / len(vals),
                "DanMean": sum(vals[:3]) / 3,
                "MulMean": sum(vals[3:]) / 3,
                "CV": (math.sqrt(sum((v - sum(vals)/6) ** 2 for v in vals) / 5) / (sum(vals)/6)) if sum(vals) else math.nan,
            }

    annotations: dict[str, dict] = {}
    with args.annotation.open(encoding="utf-8", newline="") as src:
        reader = csv.reader(src, delimiter="\t")
        for cols in reader:
            if len(cols) < 14:
                continue
            tid = cols[1]
            if tid not in expression or tid in annotations:
                continue
            annotations[tid] = {
                "SwissProtID": cols[2], "IdentityPct": f(cols[3]), "AlignmentLength": int(f(cols[4])),
                "QueryLength": int(f(cols[5])), "SubjectLength": int(f(cols[6])), "Evalue": f(cols[11]),
                "Bitscore": f(cols[12]), "Annotation": cols[13],
            }

    joined = []
    for tid, ann in annotations.items():
        row = {**expression[tid], **ann}
        row["QueryCoveragePct"] = 100 * row["AlignmentLength"] / row["QueryLength"] if row["QueryLength"] else 0
        joined.append(row)

    panel_rows, family_rows = [], []
    for group, marker, pattern in PANELS:
        rx = re.compile(pattern, re.I)
        hits = [r for r in joined if rx.search(r["Annotation"])]
        hits.sort(key=lambda r: (r["MeanTPM"], r["Bitscore"]), reverse=True)
        if not hits:
            family_rows.append({"Group": group, "Marker": marker, "CandidateCount": 0})
            continue
        vals = [r["MeanTPM"] for r in hits]
        rep = hits[0]
        panel_rows.append({"SelectionType": "Functional_panel_top_expressed", "Group": group, "Marker": marker, **rep})
        family_rows.append({
            "Group": group, "Marker": marker, "CandidateCount": len(hits),
            "MedianMeanTPM": median(vals), "P25MeanTPM": quantile(vals, .25), "P75MeanTPM": quantile(vals, .75),
            "MaxMeanTPM": max(vals), "RepresentativeTranscript": rep["TranscriptID"],
            "RepresentativeMeanTPM": rep["MeanTPM"], "RepresentativeAnnotation": rep["Annotation"],
        })

    # Fixed-seed stratified random background: four annotated transcripts per expression quintile.
    eligible = sorted([r for r in joined if r["MeanTPM"] > 0], key=lambda r: r["MeanTPM"])
    rng = random.Random(args.seed)
    random_rows = []
    for q in range(5):
        lo, hi = round(len(eligible) * q / 5), round(len(eligible) * (q + 1) / 5)
        bucket = eligible[lo:hi]
        for r in rng.sample(bucket, min(4, len(bucket))):
            random_rows.append({"SelectionType": f"Random_expression_quintile_{q+1}", "Group": "Random background", "Marker": "Fixed-seed random", **r})

    fields = ["SelectionType", "Group", "Marker", "TranscriptID", *SAMPLES, "DanMean", "MulMean", "MeanTPM", "CV",
              "SwissProtID", "IdentityPct", "QueryCoveragePct", "Evalue", "Bitscore", "Annotation"]
    write_tsv(args.output_dir / "functional_reference_panel.tsv", panel_rows, fields)
    write_tsv(args.output_dir / "random_background_panel.tsv", random_rows, fields)
    write_tsv(args.output_dir / "functional_family_distribution.tsv", family_rows,
              ["Group", "Marker", "CandidateCount", "MedianMeanTPM", "P25MeanTPM", "P75MeanTPM", "MaxMeanTPM",
               "RepresentativeTranscript", "RepresentativeMeanTPM", "RepresentativeAnnotation"])
    metadata = {
        "seed": args.seed, "tpm_rows": len(expression), "annotated_expression_rows": len(joined),
        "functional_markers_requested": len(PANELS), "functional_markers_recovered": len(panel_rows),
        "random_background_n": len(random_rows), "selection_note": "Top-expressed annotated representative per predefined function; random background stratified across expression quintiles.",
        "tpm_source": str(args.tpm), "annotation_source": str(args.annotation),
    }
    (args.output_dir / "run_summary.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
