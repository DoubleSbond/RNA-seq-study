#!/usr/bin/env python3
"""Integrate detox-family TPM and annotation evidence into auditable TSV tables."""

import argparse
import csv
import hashlib
import math
import re
from collections import defaultdict
from pathlib import Path

FAMILIES = ("CarE", "GST", "UGT", "SULT", "ABC")
SAMPLES = ("Dan_mg1", "Dan_mg2", "Dan_mg3", "Mul_mg1", "Mul_mg2", "Mul_mg3")


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def gene_id(identifier: str) -> str:
    return re.sub(r"_i\d+.*$", "", identifier)


def fasta_lengths(path: Path):
    lengths = {}
    current = None
    size = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(">"):
                if current is not None:
                    lengths[gene_id(current)] = (current, size)
                current = line[1:].strip().split()[0]
                size = 0
            else:
                size += len(line.strip())
    if current is not None:
        lengths[gene_id(current)] = (current, size)
    return lengths


def prosite_counts(path: Path):
    counts = defaultdict(int)
    current = None
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("# Sequence:"):
                current = gene_id(line.split()[2])
            elif line.startswith("Motif =") and current:
                counts[current] += 1
    return counts


def best_swiss(path: Path):
    best = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 15:
                continue
            gene = gene_id(parts[0])
            item = {
                "id": parts[1], "pident": parts[2], "length": parts[3], "qlen": parts[8],
                "slen": parts[11], "evalue": parts[12], "bitscore": parts[13], "title": parts[14],
            }
            rank = (float(item["evalue"]), -float(item["bitscore"]))
            if gene not in best or rank < best[gene][0]:
                best[gene] = (rank, item)
    return {key: value[1] for key, value in best.items()}


def best_reference(path: Path):
    best = {}
    for row in read_tsv(path):
        gene = gene_id(row["qseqid"])
        rank = (float(row["evalue"]), -float(row["bitscore"]))
        if gene not in best or rank < best[gene][0]:
            best[gene] = (rank, row)
    return {key: value[1] for key, value in best.items()}


def safe_float(value):
    if value in (None, "", "NA", "NaN"):
        return None
    return float(value)


def write_tsv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise SystemExit(f"refusing existing output directory: {args.output_dir}")
    args.output_dir.mkdir(parents=True)

    runs = args.repo / "results_manifest" / "gene_family_runs"
    broad = runs / "20260819_broad_pool"
    swiss = best_swiss(runs / "20260821_proteome_swissprot_top5" / "Phoenei_longest_vs_sprot_top5.tsv")
    source_files = [runs / "20260821_proteome_swissprot_top5" / "Phoenei_longest_vs_sprot_top5.tsv"]
    master_rows, long_rows = [], []

    fields = [
        "Family", "GeneID", "HistoricalFinal", "TranscriptCount", *SAMPLES,
        "Archived_Dan_mean", "Archived_Mul_mean", "Archived_Delta_Mul_minus_Dan", "Best_padj",
        "RepresentativePeptide", "PeptideLength", "DomainClassification", "DomainReason", "Domains",
        "DomainDescriptions", "SecondPassRecommendation", "SecondPassReason", "ABCTriage", "ABCTriageReason",
        "ProfileHMMHit", "NovelProfileHMMHit", "ReferenceHit_E1e3", "ReferenceHit_E1e5_Cov40",
        "BestFamilyReference", "BestFamilyReferenceEvalue", "BestFamilyReferenceBitscore",
        "BestFamilyReferenceIdentity", "BestFamilyReferenceQcov", "BestFamilyReferenceScov",
        "SwissProtTopID", "SwissProtTopTitle", "SwissProtTopEvalue", "SwissProtTopBitscore",
        "SwissProtTopIdentity", "SwissProtTopQcov", "SwissProtTopScov",
        "PROSITE_Pruned_Count", "PROSITE_Full_Count", "SimilarityComponent", "SimilarityComponentSize",
    ]

    for family in FAMILIES:
        family_dir = broad / family
        master_path = family_dir / f"{family}_broad_master_by_gene.tsv"
        domain_path = family_dir / f"{family}_domain_evidence.tsv"
        source_files += [master_path, domain_path]
        domains = {row["GeneID"]: row for row in read_tsv(domain_path)}

        review = {}
        review_path = family_dir / "second_pass_20260819" / f"{family}_second_pass_review.tsv"
        if review_path.exists():
            review = {row["GeneID"]: row for row in read_tsv(review_path)}
            source_files.append(review_path)

        abc_triage = {}
        triage_path = family_dir / "sequence_triage_20260819" / "ABC_sequence_triage.tsv"
        if family == "ABC" and triage_path.exists():
            abc_triage = {row["GeneID"]: row for row in read_tsv(triage_path)}
            source_files.append(triage_path)

        hmm_dir = runs / "20260820_profile_hmm_expansion" / family
        hmm_all_path = hmm_dir / "all_hit_genes.txt"
        hmm_novel_path = hmm_dir / "novel_profile_hit_genes.txt"
        hmm_all = set(hmm_all_path.read_text(encoding="utf-8").split())
        hmm_novel = set(hmm_novel_path.read_text(encoding="utf-8").split())
        source_files += [hmm_all_path, hmm_novel_path]

        ref_dir = runs / "20260821_proteome_vs_family_references" / family
        ref_loose_path = ref_dir / f"{family}_hit_genes_e1e3.txt"
        ref_strict_path = ref_dir / f"{family}_hit_genes_e1e5_cov40.txt"
        ref_table_path = ref_dir / f"{family}_proteome_vs_references.with_coverage.tsv"
        ref_loose = set(ref_loose_path.read_text(encoding="utf-8").split())
        ref_strict = set(ref_strict_path.read_text(encoding="utf-8").split())
        ref_best = best_reference(ref_table_path)
        source_files += [ref_loose_path, ref_strict_path, ref_table_path]

        tree_dir = runs / "20260820_representative_iqtree_results" / "model_finder" / family
        fasta_path = tree_dir / f"{family}_Phoenei_longest_per_gene.fa"
        lengths = fasta_lengths(fasta_path)
        source_files.append(fasta_path)

        prosite_dir = runs / "20260820_prosite_motifs" / family
        pruned_path = prosite_dir / f"{family}.prosite_pruned"
        full_path = prosite_dir / f"{family}.prosite_full_patterns"
        pruned = prosite_counts(pruned_path)
        full = prosite_counts(full_path)
        source_files += [pruned_path, full_path]

        comp_path = runs / "20260821_representative_all_vs_all" / "derived_clusters_20260821" / f"{family}_rough_components.tsv"
        components = {gene_id(row["representative_id"]): row for row in read_tsv(comp_path)}
        source_files.append(comp_path)

        for row in read_tsv(master_path):
            gene = row["GeneID"]
            domain = domains.get(gene, {})
            rev = review.get(gene, {})
            triage = abc_triage.get(gene, {})
            ref = ref_best.get(gene, {})
            sw = swiss.get(gene, {})
            peptide, length = lengths.get(gene, ("", None))
            comp = components.get(gene, {})
            output = {
                "Family": family, "GeneID": gene, "HistoricalFinal": row["HistoricalFinal"],
                "TranscriptCount": int(row["TranscriptCount"]),
                **{sample: safe_float(row[sample]) for sample in SAMPLES},
                "Archived_Dan_mean": safe_float(row.get("Dan_mean")),
                "Archived_Mul_mean": safe_float(row.get("Mul_mean")),
                "Archived_Delta_Mul_minus_Dan": safe_float(row.get("Delta_Mul_minus_Dan")),
                "Best_padj": safe_float(row.get("Best_padj")),
                "RepresentativePeptide": peptide, "PeptideLength": length,
                "DomainClassification": domain.get("DomainClassification", ""),
                "DomainReason": domain.get("Reason", ""), "Domains": domain.get("Domains", ""),
                "DomainDescriptions": domain.get("DomainDescriptions", ""),
                "SecondPassRecommendation": rev.get("SecondPassRecommendation", ""),
                "SecondPassReason": rev.get("SecondPassReason", ""),
                "ABCTriage": triage.get("ABCTriage", ""), "ABCTriageReason": triage.get("ABCTriageReason", ""),
                "ProfileHMMHit": gene in hmm_all, "NovelProfileHMMHit": gene in hmm_novel,
                "ReferenceHit_E1e3": gene in ref_loose, "ReferenceHit_E1e5_Cov40": gene in ref_strict,
                "BestFamilyReference": ref.get("sseqid", ""),
                "BestFamilyReferenceEvalue": safe_float(ref.get("evalue")),
                "BestFamilyReferenceBitscore": safe_float(ref.get("bitscore")),
                "BestFamilyReferenceIdentity": safe_float(ref.get("pident")),
                "BestFamilyReferenceQcov": safe_float(ref.get("qcov")),
                "BestFamilyReferenceScov": safe_float(ref.get("scov")),
                "SwissProtTopID": sw.get("id", ""), "SwissProtTopTitle": sw.get("title", ""),
                "SwissProtTopEvalue": safe_float(sw.get("evalue")), "SwissProtTopBitscore": safe_float(sw.get("bitscore")),
                "SwissProtTopIdentity": safe_float(sw.get("pident")),
                "SwissProtTopQcov": (100 * float(sw["length"]) / float(sw["qlen"])) if sw else None,
                "SwissProtTopScov": (100 * float(sw["length"]) / float(sw["slen"])) if sw else None,
                "PROSITE_Pruned_Count": pruned.get(gene, 0), "PROSITE_Full_Count": full.get(gene, 0),
                "SimilarityComponent": comp.get("component", ""),
                "SimilarityComponentSize": int(comp["component_size"]) if comp else None,
            }
            master_rows.append(output)
            for sample in SAMPLES:
                condition, replicate = sample.split("_mg")
                long_rows.append({"Family": family, "GeneID": gene, "Condition": condition,
                                  "Replicate": int(replicate), "Sample": sample, "TPM": output[sample]})

    master_rows.sort(key=lambda row: (FAMILIES.index(row["Family"]), row["GeneID"]))
    write_tsv(args.output_dir / "detox_gene_tpm_annotation_master.tsv", fields, master_rows)
    write_tsv(args.output_dir / "detox_gene_tpm_long.tsv",
              ["Family", "GeneID", "Condition", "Replicate", "Sample", "TPM"], long_rows)

    with (args.output_dir / "source_manifest.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["sha256", "bytes", "repo_relative_path"])
        for path in sorted(set(source_files)):
            writer.writerow([hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_size,
                             path.relative_to(args.repo).as_posix()])

    counts = defaultdict(int)
    for row in master_rows:
        counts[row["Family"]] += 1
    with (args.output_dir / "build_summary.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["family", "broad_candidate_genes", "tpm_rows"])
        for family in FAMILIES:
            writer.writerow([family, counts[family], counts[family] * len(SAMPLES)])
        writer.writerow(["TOTAL", len(master_rows), len(long_rows)])


if __name__ == "__main__":
    main()
