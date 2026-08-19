#!/usr/bin/env python3
"""Select the longest peptide isoform per Trinity gene without altering input."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


GENE_RE = re.compile(r"^(TRINITY_.+?_g\d+)")


def records(path: Path):
    name = ""
    sequence: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    yield name, "".join(sequence)
                name, sequence = line[1:], []
            elif line:
                sequence.append(line)
    if name:
        yield name, "".join(sequence)


def gene_id(header: str) -> str:
    match = GENE_RE.match(header.split()[0])
    return match.group(1) if match else header.split()[0]


def select(path: Path) -> dict[str, tuple[str, str]]:
    best: dict[str, tuple[str, str]] = {}
    for header, sequence in records(path):
        gene = gene_id(header)
        if gene not in best or len(sequence) > len(best[gene][1]):
            best[gene] = (header, sequence)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"refusing existing output: {args.output}")
    best = select(args.input)
    with args.output.open("x", encoding="utf-8") as handle:
        for gene in sorted(best):
            header, sequence = best[gene]
            handle.write(f">{header}\n")
            for start in range(0, len(sequence), 80):
                handle.write(sequence[start:start + 80] + "\n")
    print(f"input_records={sum(1 for _ in records(args.input))} selected_genes={len(best)}")


if __name__ == "__main__":
    main()
