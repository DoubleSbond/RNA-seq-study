#!/usr/bin/env python3
"""Compare archived group means with means recomputed from the six visible TPM columns."""

import argparse
import csv
import statistics
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing existing output file: {args.output}")
    with args.master.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    fields = [
        "Family", "GeneID", "Recalc_Dan_mean", "Archived_Dan_mean", "Dan_mean_difference",
        "Recalc_Mul_mean", "Archived_Mul_mean", "Mul_mean_difference", "Max_absolute_difference",
        "Interpretation",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            dan = statistics.mean(float(row[name]) for name in ("Dan_mg1", "Dan_mg2", "Dan_mg3"))
            mul = statistics.mean(float(row[name]) for name in ("Mul_mg1", "Mul_mg2", "Mul_mg3"))
            archived_dan = float(row["Archived_Dan_mean"])
            archived_mul = float(row["Archived_Mul_mean"])
            max_diff = max(abs(dan - archived_dan), abs(mul - archived_mul))
            writer.writerow({
                "Family": row["Family"], "GeneID": row["GeneID"],
                "Recalc_Dan_mean": dan, "Archived_Dan_mean": archived_dan,
                "Dan_mean_difference": dan - archived_dan,
                "Recalc_Mul_mean": mul, "Archived_Mul_mean": archived_mul,
                "Mul_mean_difference": mul - archived_mul,
                "Max_absolute_difference": max_diff,
                "Interpretation": "archived mean uses a different upstream/statistical basis; retain both",
            })


if __name__ == "__main__":
    main()
