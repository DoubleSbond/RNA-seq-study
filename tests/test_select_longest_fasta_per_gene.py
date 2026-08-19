import importlib.util
import pathlib
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).parents[1] / "scripts/python/select_longest_fasta_per_gene.py"
SPEC = importlib.util.spec_from_file_location("select_longest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SelectLongestTests(unittest.TestCase):
    def test_selects_longest_isoform_per_gene(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "input.fa"
            path.write_text(">TRINITY_DN1_c0_g1_i1.p1\nAAA\n>TRINITY_DN1_c0_g1_i2.p1\nAAAAA\n")
            best = MODULE.select(path)
        self.assertEqual(best["TRINITY_DN1_c0_g1"][0], "TRINITY_DN1_c0_g1_i2.p1")


if __name__ == "__main__":
    unittest.main()
