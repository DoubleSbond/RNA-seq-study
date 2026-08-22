#!/usr/bin/env python3
"""Add conservative second-pass recommendations to domain-review candidates."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def gene_id(identifier: str) -> str:
    return re.sub(r"_i\d+(?:\.p\d+)?$", "", identifier)


def load_hits(paths: list[Path]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                fields = line.rstrip("\n").split("\t")
                if len(fields) >= 2:
                    hits.setdefault(gene_id(fields[0]), []).append(fields[-1])
    return hits


def recommendation(family: str, row: dict[str, str], annotations: list[str]) -> tuple[str, str]:
    text = " ".join(annotations).lower()
    reason = row["Reason"]
    historical = row["HistoricalFinal"].lower() == "yes"

    if family == "GST":
        return "exclude_from_canonical_detox_GST", "alternative protein family; no canonical cytosolic GST domain"
    if family == "UGT":
        return "exclude_from_canonical_UGT", "alternative domain architecture; PF00201/IPR002213 absent"
    if family == "SULT":
        return "exclude_from_cytosolic_SULT", "non-cytosolic sulfotransferase class; PF00685/IPR000863 absent"
    if family == "ABC":
        if "sub-family f" in text or "abcf" in text:
            return "retain_ABC_nontransporter", "ABCF proteins are soluble ABC-family ATPases and legitimately lack a TMD"
        if historical and reason != "no_family_defining_domain_in_current_core_table":
            return "retain_ABC_fragment_or_partial", "historical homology plus partial ABC architecture; inspect isoforms before nomenclature"
        if historical:
            return "hold_ABC_historical_review", "historical candidate lacks defining domains in the current representative sequence"
        if reason in {"NBD_only_or_TMD_not_detected", "TMD_only_or_NBD_not_detected"}:
            return "hold_ABC_fragment_review", "partial ABC architecture; requires isoform/homology inspection"
        return "exclude_from_current_ABC_rough_set", "no defining ABC domain in the current core table and no historical support"
    return "hold_review", "no family-specific second-pass rule"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True, choices=["GST", "UGT", "SULT", "ABC"])
    parser.add_argument("--domain-evidence", type=Path, required=True)
    parser.add_argument("--top-hit", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    hits = load_hits(args.top_hit)
    with args.domain_evidence.open(encoding="utf-8", newline="") as source:
        rows = [r for r in csv.DictReader(source, delimiter="\t") if r["DomainClassification"] == "review"]

    fields = list(rows[0]) + ["SecondPassRecommendation", "SecondPassReason", "TopHitAnnotations"] if rows else []
    args.output.parent.mkdir(parents=True, exist_ok=False)
    with args.output.open("x", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            annotations = hits.get(row["GeneID"], [])
            label, rationale = recommendation(args.family, row, annotations)
            row.update(
                SecondPassRecommendation=label,
                SecondPassReason=rationale,
                TopHitAnnotations=" | ".join(dict.fromkeys(annotations)) or "none_in_archived_top_hits",
            )
            writer.writerow(row)


if __name__ == "__main__":
    main()
