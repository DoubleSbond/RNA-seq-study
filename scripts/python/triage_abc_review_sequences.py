#!/usr/bin/env python3
"""Sequence-aware triage for ABC candidates left after domain screening."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


HYDROPHOBIC = set("AILMFWVY")


def normalize_gene(identifier: str) -> str:
    return re.sub(r"_i\d+(?:\.p\d+)?$", "", identifier.split()[0])


def read_fasta(path: Path) -> dict[str, list[tuple[str, str]]]:
    result: dict[str, list[tuple[str, str]]] = {}
    name = ""
    chunks: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    result.setdefault(normalize_gene(name), []).append((name, "".join(chunks)))
                name, chunks = line[1:].split()[0], []
            else:
                chunks.append(line)
    if name:
        result.setdefault(normalize_gene(name), []).append((name, "".join(chunks)))
    return result


def hydrophobic_windows(sequence: str, width: int = 19, threshold: int = 14) -> int:
    """Count separated strongly hydrophobic windows as a conservative TMD proxy."""
    starts = [i for i in range(max(0, len(sequence) - width + 1)) if sum(a in HYDROPHOBIC for a in sequence[i:i+width]) >= threshold]
    count, last = 0, -width
    for start in starts:
        if start - last >= width:
            count += 1
            last = start
    return count


def sequence_metrics(sequence: str) -> tuple[bool, bool, int]:
    walker_a = bool(re.search(r"G....GK[ST]", sequence))
    abc_signature = "LSGGQ" in sequence
    return walker_a, abc_signature, hydrophobic_windows(sequence)


def decision(row: dict[str, str], annotation: str, walker: bool, signature: bool, tmd_proxy: int) -> tuple[str, str]:
    text = annotation.lower()
    historical = row["HistoricalFinal"].lower() == "yes"
    if "sub-family f" in text or "abcf" in text:
        return "retain_ABC_nontransporter", "ABCF homology; soluble ABC ATPase architecture"
    if walker and signature and tmd_proxy >= 2:
        return "retain_sequence_supported_ABC", "Walker A, ABC signature, and hydrophobic segments co-occur in one isoform"
    if historical and (walker or signature or tmd_proxy >= 2):
        return "retain_historical_partial_ABC", "historical support plus partial sequence-level ABC evidence"
    return "hold_for_targeted_homology_or_assembly_review", "current isoforms do not unite sufficient sequence and architecture evidence"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--peptides", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sequences = read_fasta(args.peptides)
    with args.review.open(encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle, delimiter="\t") if not r["SecondPassRecommendation"].startswith("exclude_")]
    fields = list(rows[0]) + ["RepresentativePeptide", "PeptideLength", "WalkerA", "ABCSignatureLSGGQ", "HydrophobicSegmentProxy", "ABCTriage", "ABCTriageReason"]
    args.output.parent.mkdir(parents=True, exist_ok=False)
    with args.output.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            candidates = sequences.get(row["GeneID"], [])
            scored = []
            for identifier, sequence in candidates:
                walker, signature, tmd_proxy = sequence_metrics(sequence)
                scored.append(((walker + signature, tmd_proxy, len(sequence)), identifier, sequence, walker, signature, tmd_proxy))
            if scored:
                _, identifier, sequence, walker, signature, tmd_proxy = max(scored)
            else:
                identifier, sequence, walker, signature, tmd_proxy = "none", "", False, False, 0
            label, rationale = decision(row, row["TopHitAnnotations"], walker, signature, tmd_proxy)
            row.update(RepresentativePeptide=identifier, PeptideLength=len(sequence), WalkerA=str(walker).lower(),
                       ABCSignatureLSGGQ=str(signature).lower(), HydrophobicSegmentProxy=tmd_proxy,
                       ABCTriage=label, ABCTriageReason=rationale)
            writer.writerow(row)


if __name__ == "__main__":
    main()
