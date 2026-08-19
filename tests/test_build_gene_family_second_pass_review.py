import importlib.util
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).parents[1] / "scripts/python/build_gene_family_second_pass_review.py"
SPEC = importlib.util.spec_from_file_location("second_pass", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SecondPassTests(unittest.TestCase):
    def test_abcf_is_retained_without_tmd(self):
        row = {"Reason": "NBD_only_or_TMD_not_detected", "HistoricalFinal": "yes"}
        label, _ = MODULE.recommendation("ABC", row, ["ATP-binding cassette sub-family F member 1"])
        self.assertEqual(label, "retain_ABC_nontransporter")

    def test_noncanonical_ugt_is_excluded(self):
        row = {"Reason": "no_family_defining_domain_in_current_core_table", "HistoricalFinal": "no"}
        label, _ = MODULE.recommendation("UGT", row, [])
        self.assertEqual(label, "exclude_from_canonical_UGT")


if __name__ == "__main__":
    unittest.main()
