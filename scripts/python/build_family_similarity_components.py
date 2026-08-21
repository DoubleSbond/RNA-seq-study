#!/usr/bin/env python3
"""Build rough undirected components from filtered within-family BLAST edges."""

import argparse
import csv
from pathlib import Path


def fasta_ids(path: Path) -> list[str]:
    ids = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(">"):
                ids.append(line[1:].strip().split()[0])
    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise SystemExit(f"refusing existing output directory: {args.output_dir}")
    args.output_dir.mkdir(parents=True)

    overview = []
    for family in ("CarE", "GST", "UGT", "SULT", "ABC"):
        family_dir = args.input_root / family
        nodes = fasta_ids(family_dir / f"{family}_Phoenei_longest_per_gene.fa")
        adjacency = {node: set() for node in nodes}
        with (family_dir / f"{family}_edges_e1e5_cov50.tsv").open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                query, subject = row["qseqid"], row["sseqid"]
                adjacency.setdefault(query, set()).add(subject)
                adjacency.setdefault(subject, set()).add(query)

        components = []
        unseen = set(adjacency)
        while unseen:
            seed = min(unseen)
            stack = [seed]
            unseen.remove(seed)
            component = []
            while stack:
                node = stack.pop()
                component.append(node)
                neighbors = adjacency[node] & unseen
                unseen.difference_update(neighbors)
                stack.extend(sorted(neighbors, reverse=True))
            components.append(sorted(component))
        components.sort(key=lambda members: (-len(members), members[0]))

        output = args.output_dir / f"{family}_rough_components.tsv"
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow(["family", "component", "component_size", "representative_id"])
            for index, members in enumerate(components, 1):
                for member in members:
                    writer.writerow([family, f"{family}_C{index:03d}", len(members), member])
        overview.append((family, len(nodes), len(components), max(map(len, components))))

    with (args.output_dir / "component_summary.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["family", "representatives", "rough_components", "largest_component"])
        writer.writerows(overview)


if __name__ == "__main__":
    main()
