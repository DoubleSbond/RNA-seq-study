#!/usr/bin/env python3
"""Reconstruct broad CYP/P450 candidate filtering from a tabular annotation file.

This utility is intentionally schema-tolerant: it scans selected annotation columns,
or all non-ID columns by default, for common CYP/P450 evidence terms. It is a public
reconstruction of the candidate-screening logic, not the unrecovered original HPC
one-command script.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


DEFAULT_PATTERNS = [
    r"\bCYP\b",
    r"cytochrome\s+P450",
    r"\bP450\b",
    r"PF00067",
    r"IPR001128",
    r"GO:0004497",
    r"GO:0005506",
    r"GO:0016705",
    r"GO:0020037",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter CYP/P450 candidate rows from an annotation TSV."
    )
    parser.add_argument("--input", required=True, help="Input annotation TSV.")
    parser.add_argument("--output", required=True, help="Output candidate TSV.")
    parser.add_argument(
        "--gene-id-output",
        help="Optional output text file containing one unique gene ID per line.",
    )
    parser.add_argument(
        "--gene-id-column",
        default="GeneID",
        help="Gene ID column name. Default: GeneID.",
    )
    parser.add_argument(
        "--scan-columns",
        nargs="*",
        help="Specific columns to scan. Default: all columns except the gene ID column.",
    )
    parser.add_argument(
        "--patterns",
        nargs="*",
        default=DEFAULT_PATTERNS,
        help="Regex evidence patterns. Defaults cover CYP/P450, PF00067, IPR001128, and related GO terms.",
    )
    return parser.parse_args()


def row_has_evidence(row: dict[str, str], columns: list[str], regex: re.Pattern[str]) -> bool:
    haystack = " ".join(row.get(column, "") for column in columns)
    return bool(regex.search(haystack))


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    gene_id_output = Path(args.gene_id_output) if args.gene_id_output else None

    regex = re.compile("|".join(f"(?:{pattern})" for pattern in args.patterns), re.IGNORECASE)

    with input_path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter="\t")
        if not reader.fieldnames:
            raise SystemExit(f"No header found in {input_path}")

        if args.gene_id_column not in reader.fieldnames:
            raise SystemExit(
                f"Gene ID column '{args.gene_id_column}' not found. "
                f"Available columns: {', '.join(reader.fieldnames)}"
            )

        scan_columns = args.scan_columns or [
            column for column in reader.fieldnames if column != args.gene_id_column
        ]
        missing = [column for column in scan_columns if column not in reader.fieldnames]
        if missing:
            raise SystemExit(f"Scan columns not found: {', '.join(missing)}")

        rows = [row for row in reader if row_has_evidence(row, scan_columns, regex)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    if gene_id_output:
        gene_ids = sorted({row[args.gene_id_column] for row in rows if row[args.gene_id_column]})
        gene_id_output.parent.mkdir(parents=True, exist_ok=True)
        gene_id_output.write_text("\n".join(gene_ids) + "\n", encoding="utf-8")

    print(f"Wrote {len(rows)} candidate rows to {output_path}")


if __name__ == "__main__":
    main()
