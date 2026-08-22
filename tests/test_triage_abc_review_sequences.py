import importlib.util
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).parents[1] / "scripts/python/triage_abc_review_sequences.py"
SPEC = importlib.util.spec_from_file_location("abc_triage", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ABCTriageTests(unittest.TestCase):
    def test_motifs_and_membrane_support_retain(self):
        row = {"HistoricalFinal": "no"}
        label, _ = MODULE.decision(row, "ABC transporter", True, True, 4)
        self.assertEqual(label, "retain_sequence_supported_ABC")

    def test_abcf_does_not_require_membrane(self):
        row = {"HistoricalFinal": "yes"}
        label, _ = MODULE.decision(row, "ATP-binding cassette sub-family F member 1", True, False, 0)
        self.assertEqual(label, "retain_ABC_nontransporter")

    def test_weak_nonhistorical_candidate_is_held(self):
        row = {"HistoricalFinal": "no"}
        label, _ = MODULE.decision(row, "none", False, False, 1)
        self.assertTrue(label.startswith("hold_"))


if __name__ == "__main__":
    unittest.main()
