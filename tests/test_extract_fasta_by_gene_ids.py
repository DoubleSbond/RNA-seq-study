import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/python/extract_fasta_by_gene_ids.py"


class FastaExtractionTests(unittest.TestCase):
    def test_extracts_all_isoforms_for_requested_gene(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ids.txt").write_text("TRINITY_DN1_c0_g1\n", encoding="utf-8")
            (root / "all.fa").write_text(">TRINITY_DN1_c0_g1_i1\nAAA\n>TRINITY_DN1_c0_g1_i2.p1 note\nBBB\n>TRINITY_DN2_c0_g1_i1\nCCC\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "--ids", str(root / "ids.txt"), "--fasta", str(root / "all.fa"), "--output", str(root / "subset.fa"), "--summary", str(root / "summary.tsv")], check=True, capture_output=True, text=True)
            self.assertIn("records=2", result.stdout)
            subset = (root / "subset.fa").read_text(encoding="utf-8")
            self.assertIn("TRINITY_DN1", subset)
            self.assertNotIn("TRINITY_DN2", subset)


if __name__ == "__main__":
    unittest.main()
