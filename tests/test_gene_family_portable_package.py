import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/python/build_gene_family_portable_package.py"
SPEC = importlib.util.spec_from_file_location("family_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GeneFamilyPackageTests(unittest.TestCase):
    def test_gene_id_normalizes_transcript_and_peptide_ids(self):
        self.assertEqual(MODULE.gene_id("TRINITY_DN12_c0_g3_i17"), "TRINITY_DN12_c0_g3")
        self.assertEqual(MODULE.gene_id("TRINITY_DN12_c0_g3_i17.p1"), "TRINITY_DN12_c0_g3")

    def test_tpm_geneid_field_does_not_overwrite_normalized_gene(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ids.txt").write_text("TRINITY_DN12_c0_g3\n", encoding="utf-8")
            (root / "final.txt").write_text("TRINITY_DN12_c0_g3\n", encoding="utf-8")
            (root / "tpm.tsv").write_text(
                "GeneID\tDan_1\tMul_1\nTRINITY_DN12_c0_g3_i17\t2\t5\n",
                encoding="utf-8",
            )
            (root / "de.tsv").write_text(
                "GeneID\tlog2FoldChange\tpadj\nTRINITY_DN12_c0_g3_i17\t1.2\t0.04\n",
                encoding="utf-8",
            )
            output = root / "output"
            command = [
                sys.executable,
                str(SCRIPT),
                "--family", "GST",
                "--phase", "II",
                "--candidate-ids", str(root / "ids.txt"),
                "--final-ids", str(root / "final.txt"),
                "--tpm", str(root / "tpm.tsv"),
                "--deseq2", str(root / "de.tsv"),
                "--output-dir", str(output),
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            summary = json.loads((output / "run_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["candidate_genes_with_expression"], 1)
            lines = (output / "GST_broad_master_by_transcript.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[1].split("\t")[1:3], ["TRINITY_DN12_c0_g3", "TRINITY_DN12_c0_g3_i17"])
            self.assertFalse(lines[1].endswith("\t"))


if __name__ == "__main__":
    unittest.main()
