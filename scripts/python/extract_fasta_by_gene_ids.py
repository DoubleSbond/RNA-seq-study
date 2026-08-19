#!/usr/bin/env python3
"""Extract every FASTA record belonging to a set of Trinity gene IDs."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


TRINITY_GENE = re.compile(r"^(TRINITY_.+?_g\d+)")


def gene_id(identifier: str) -> str:
    match = TRINITY_GENE.match(identifier.split("|")[0].split(".p")[0])
    return match.group(1) if match else re.sub(r"_i\d+.*$", "", identifier)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", type=Path, required=True)
    parser.add_argument("--fasta", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    for path in (args.ids, args.fasta):
        if not path.is_file():
            parser.error(f"missing input: {path}")
    for path in (args.output, args.summary):
        if path.exists():
            parser.error(f"refusing existing output: {path}")

    wanted = {gene_id(line.strip().split("\t")[0]) for line in args.ids.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
    represented: set[str] = set()
    record_count = 0
    keep = False
    digest = hashlib.sha256()
    with args.fasta.open(encoding="utf-8") as source, args.output.open("x", encoding="utf-8", newline="\n") as target:
        for line in source:
            if line.startswith(">"):
                current = gene_id(line[1:].split()[0])
                keep = current in wanted
                if keep:
                    represented.add(current)
                    record_count += 1
            if keep:
                target.write(line)
                digest.update(line.encode("utf-8"))
    missing = sorted(wanted - represented)
    args.summary.write_text(
        "metric\tvalue\n"
        f"requested_genes\t{len(wanted)}\n"
        f"represented_genes\t{len(represented)}\n"
        f"records\t{record_count}\n"
        f"missing_genes\t{len(missing)}\n"
        f"sha256\t{digest.hexdigest()}\n"
        f"missing_gene_ids\t{','.join(missing) if missing else 'none'}\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"requested={len(wanted)} represented={len(represented)} records={record_count} missing={len(missing)}")
    return 0 if not missing else 3


if __name__ == "__main__":
    raise SystemExit(main())
