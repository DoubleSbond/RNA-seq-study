#!/usr/bin/env python3
"""Classify broad candidates by family-defining domain evidence without deletion."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path


GENE_RE = re.compile(r"^(TRINITY_.+?_g\d+)")
DOMAIN_RE = re.compile(r"(?:PF\d{5}|IPR\d{6})")
RULES = {
    "CarE": {"core": {"PF00135", "IPR002018"}},
    "GST": {"core": {"PF00043", "PF02798", "PF13417", "PF14497", "PF13410", "IPR004045", "IPR004046"}},
    "UGT": {"core": {"PF00201", "IPR002213"}},
    "SULT": {"core": {"PF00685", "IPR000863"}},
    "ABC": {"nbd": {"PF00005", "IPR003439"}, "tmd": {"PF00664", "PF01061", "IPR011527", "IPR013525"}},
}


def gene_id(value: str) -> str:
    match = GENE_RE.match(value)
    return match.group(1) if match else re.sub(r"_i\d+.*$", "", value)


def status(family: str, domains: set[str]) -> tuple[str, str]:
    rule = RULES[family]
    if family == "ABC":
        nbd = bool(domains & rule["nbd"])
        tmd = bool(domains & rule["tmd"])
        if nbd and tmd:
            return "provisional_HQ_domain", "NBD_and_TMD_evidence"
        if nbd:
            return "review", "NBD_only_or_TMD_not_detected"
        if tmd:
            return "review", "TMD_only_or_NBD_not_detected"
        return "review", "no_family_defining_domain_in_current_core_table"
    if domains & rule["core"]:
        return "provisional_HQ_domain", "family_defining_domain_detected"
    return "review", "no_family_defining_domain_in_current_core_table"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=sorted(RULES), required=True)
    parser.add_argument("--candidate-ids", type=Path, required=True)
    parser.add_argument("--historical-final-ids", type=Path)
    parser.add_argument("--interpro-core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"refusing existing output: {args.output}")
    candidates = {gene_id(x.split("\t")[0]) for x in args.candidate_ids.read_text().splitlines() if x.strip()}
    historical = {gene_id(x.split("\t")[0]) for x in args.historical_final_ids.read_text().splitlines() if x.strip()} if args.historical_final_ids and args.historical_final_ids.is_file() else set()
    domains: dict[str, set[str]] = defaultdict(set)
    descriptions: dict[str, set[str]] = defaultdict(set)
    with args.interpro_core.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            gene = gene_id(fields[0])
            if gene not in candidates:
                continue
            domains[gene].update(DOMAIN_RE.findall(line))
            for index in (5, 12):
                if len(fields) > index and fields[index] not in ("", "-"):
                    descriptions[gene].add(fields[index])
    rows = []
    for gene in sorted(candidates):
        classification, reason = status(args.family, domains[gene])
        rows.append({"Family": args.family, "GeneID": gene, "DomainClassification": classification, "Reason": reason, "HistoricalFinal": "yes" if gene in historical else "no", "Domains": ";".join(sorted(domains[gene])) or "none", "DomainDescriptions": ";".join(sorted(descriptions[gene])) or "none"})
    with args.output.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    hq = sum(row["DomainClassification"] == "provisional_HQ_domain" for row in rows)
    print(f"family={args.family} candidates={len(rows)} provisional_hq={hq} review={len(rows)-hq}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
