import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/python/classify_gene_family_domain_evidence.py"
SPEC = importlib.util.spec_from_file_location("domain_classifier", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DomainClassificationTests(unittest.TestCase):
    def test_abc_requires_nbd_and_tmd_for_provisional_hq(self):
        self.assertEqual(MODULE.status("ABC", {"PF00005", "PF00664"})[0], "provisional_HQ_domain")
        self.assertEqual(MODULE.status("ABC", {"PF00005"})[0], "review")

    def test_ugt_core_domain(self):
        self.assertEqual(MODULE.status("UGT", {"PF00201"})[0], "provisional_HQ_domain")
        self.assertEqual(MODULE.status("UGT", {"PF05024"})[0], "review")


if __name__ == "__main__":
    unittest.main()
