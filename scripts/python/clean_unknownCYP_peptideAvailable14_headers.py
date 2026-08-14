from pathlib import Path

infile = Path("seqs/unknownCYP_peptide_available_14genes_17ORFs.raw.faa")
outfile = Path("seqs/unknownCYP_peptideAvailable14_17ORFs.clean_header.faa")
mapfile = Path("final_round/tables/unknownCYP_peptideAvailable14_17ORFs_header_mapping.tsv")

with infile.open() as fin, outfile.open("w") as fout, mapfile.open("w") as fmap:
    fmap.write("old_header\tnew_header\tgene_id\n")
    for line in fin:
        line = line.rstrip("\n")
        if line.startswith(">"):
            old = line[1:].strip()
            first = old.split()[0]

            if "_i" in first and ".p" in first:
                gene = first.split("_i")[0]
                new = f"PhUNK|{first}"
            else:
                gene = first
                new = f"PhUNK|{gene}"

            fout.write(f">{new}\n")
            fmap.write(f"{old}\t{new}\t{gene}\n")
        else:
            fout.write(line + "\n")
