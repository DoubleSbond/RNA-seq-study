#!/usr/bin/env python3
"""Build an append-only, portable broad-pool package for one gene family.

The script never replaces an existing output directory. It joins historical
broad candidate IDs to transcript-level TPM and DESeq2 tables, emits both
transcript- and gene-level summaries, subsets candidate peptide FASTA, and
records provenance plus SHA256 checksums.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


TRINITY_GENE = re.compile(r"^(TRINITY_.+?_g\d+)")


def gene_id(identifier: str) -> str:
    clean = identifier.split("|")[0].split(".p")[0]
    match = TRINITY_GENE.match(clean)
    return match.group(1) if match else re.sub(r"_i\d+.*$", "", clean)


def read_ids(path: Path) -> list[str]:
    values = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            value = line.strip().split("\t")[0]
            if value and not value.startswith("#"):
                values.append(gene_id(value))
    return sorted(set(values))


def dialect_for(path: Path) -> str:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        first = handle.readline()
    return "," if first.count(",") > first.count("\t") else "\t"


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=dialect_for(path))
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def write_table(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def numeric(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def subset_fasta(source: Path, target: Path, genes: set[str]) -> tuple[int, set[str]]:
    count = 0
    represented: set[str] = set()
    keep = False
    with source.open(encoding="utf-8") as src, target.open("x", encoding="utf-8") as dst:
        for line in src:
            if line.startswith(">"):
                identifier = line[1:].split()[0]
                current = gene_id(identifier)
                keep = current in genes
                if keep:
                    count += 1
                    represented.add(current)
            if keep:
                dst.write(line)
    return count, represented


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--candidate-ids", type=Path, required=True)
    parser.add_argument("--final-ids", type=Path)
    parser.add_argument("--tpm", type=Path, required=True)
    parser.add_argument("--deseq2", type=Path, required=True)
    parser.add_argument("--candidate-peptides", type=Path)
    parser.add_argument("--evidence-table", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    required = [args.candidate_ids, args.tpm, args.deseq2]
    optional = [args.final_ids, args.candidate_peptides, args.evidence_table]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        parser.error("missing required input(s): " + ", ".join(missing))
    if args.output_dir.exists():
        parser.error(f"refusing to reuse existing output directory: {args.output_dir}")
    args.output_dir.mkdir(parents=True)

    candidates = read_ids(args.candidate_ids)
    candidate_set = set(candidates)
    final = read_ids(args.final_ids) if args.final_ids and args.final_ids.is_file() else []
    final_set = set(final)

    tpm_fields, tpm_rows = read_table(args.tpm)
    de_fields, de_rows = read_table(args.deseq2)
    if not tpm_fields or not de_fields:
        parser.error("TPM or DESeq2 table has no header")
    tpm_id = tpm_fields[0]
    de_id = de_fields[0]
    de_by_tx = {row[de_id]: row for row in de_rows}

    transcript_rows: list[dict[str, object]] = []
    sample_fields = [f for f in tpm_fields[1:] if re.search(r"^(Dan|Mul)_", f, re.I)]
    joined_de_fields = [f for f in de_fields[1:] if f not in tpm_fields]
    for row in tpm_rows:
        transcript = row[tpm_id]
        gene = gene_id(transcript)
        if gene not in candidate_set:
            continue
        out: dict[str, object] = {"Family": args.family, "GeneID": gene, "TranscriptID": transcript, "HistoricalFinal": "yes" if gene in final_set else "no"}
        # Keep the normalized gene-level ID. The TPM table's first column is
        # named GeneID but actually contains transcript IDs; copying it would
        # silently replace GeneID with TranscriptID.
        out.update({field: value for field, value in row.items() if field != tpm_id})
        de = de_by_tx.get(transcript, {})
        out.update({field: de.get(field, "") for field in joined_de_fields})
        transcript_rows.append(out)

    transcript_fields = ["Family", "GeneID", "TranscriptID", "HistoricalFinal"] + [f for f in tpm_fields if f != tpm_id] + joined_de_fields
    write_table(args.output_dir / f"{args.family}_broad_master_by_transcript.tsv", transcript_fields, transcript_rows)

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in transcript_rows:
        grouped[str(row["GeneID"])].append(row)
    unexpected = set(grouped) - candidate_set
    if unexpected:
        raise RuntimeError(f"normalized expression IDs escaped candidate set: {sorted(unexpected)[:5]}")
    gene_rows: list[dict[str, object]] = []
    for gene in candidates:
        rows = grouped.get(gene, [])
        out: dict[str, object] = {"Family": args.family, "GeneID": gene, "HistoricalFinal": "yes" if gene in final_set else "no", "TranscriptCount": len(rows)}
        for field in sample_fields:
            out[field] = sum(numeric(str(row.get(field, ""))) for row in rows)
        dan = [numeric(str(out[f])) for f in sample_fields if f.lower().startswith("dan_")]
        mul = [numeric(str(out[f])) for f in sample_fields if f.lower().startswith("mul_")]
        out["Dan_mean"] = sum(dan) / len(dan) if dan else ""
        out["Mul_mean"] = sum(mul) / len(mul) if mul else ""
        out["Delta_Mul_minus_Dan"] = (out["Mul_mean"] - out["Dan_mean"]) if dan and mul else ""
        padj_values = [numeric(str(row.get("padj", ""))) for row in rows if str(row.get("padj", "")) not in ("", "NA", "nan")]
        out["Best_padj"] = min(padj_values) if padj_values else "NA"
        gene_rows.append(out)
    gene_fields = ["Family", "GeneID", "HistoricalFinal", "TranscriptCount"] + sample_fields + ["Dan_mean", "Mul_mean", "Delta_Mul_minus_Dan", "Best_padj"]
    write_table(args.output_dir / f"{args.family}_broad_master_by_gene.tsv", gene_fields, gene_rows)

    write_table(args.output_dir / f"{args.family}_candidate_ids.tsv", ["Family", "GeneID", "HistoricalFinal"], [{"Family": args.family, "GeneID": g, "HistoricalFinal": "yes" if g in final_set else "no"} for g in candidates])

    peptide_count = 0
    peptide_genes: set[str] = set()
    if args.candidate_peptides and args.candidate_peptides.is_file():
        peptide_count, peptide_genes = subset_fasta(args.candidate_peptides, args.output_dir / f"{args.family}_broad_peptides.fasta", candidate_set)
    if args.evidence_table and args.evidence_table.is_file():
        shutil.copyfile(args.evidence_table, args.output_dir / f"{args.family}_source_evidence{args.evidence_table.suffix}")

    summary = {
        "family": args.family,
        "phase": args.phase,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_gene_count": len(candidates),
        "historical_final_gene_count": len(final),
        "candidate_genes_with_expression": len(grouped),
        "candidate_transcript_count": len(transcript_rows),
        "candidate_peptide_count": peptide_count,
        "candidate_genes_with_peptide": len(peptide_genes),
        "inputs": {name: str(path) for name, path in {"candidate_ids": args.candidate_ids, "final_ids": args.final_ids, "tpm": args.tpm, "deseq2": args.deseq2, "candidate_peptides": args.candidate_peptides, "evidence_table": args.evidence_table}.items() if path},
    }
    with (args.output_dir / "run_summary.json").open("x", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    outputs = sorted(p for p in args.output_dir.iterdir() if p.is_file())
    write_table(args.output_dir / "sha256.tsv", ["sha256", "bytes", "file"], [{"sha256": sha256(p), "bytes": p.stat().st_size, "file": p.name} for p in outputs])
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
