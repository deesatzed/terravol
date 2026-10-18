"""Application operational-boundary acceptance tests."""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class OperationsAcceptanceTests(unittest.TestCase):
    def test_ac_ops_05_donor_and_sensitive_runtime_paths_are_excluded(self) -> None:
        ignored = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/aXc-ace-forecaster/", ignored)
        self.assertIn(".env", ignored)
        self.assertIn("*.pkl", ignored)
        self.assertIn("/data/", ignored)

    def test_ac_ops_09_application_matrix_never_counts_scaffold_results(self) -> None:
        matrix = json.loads((ROOT / "config/acceptance_matrix.json").read_text())
        self.assertEqual(matrix["scope"], "APPLICATION_REQUIREMENTS_NOT_SCAFFOLD_TEST_RESULTS")
        scaffold = json.loads((ROOT / "reports/scaffold/verification.json").read_text())
        self.assertEqual(scaffold["application_acceptance_executed"], 0)
        self.assertTrue(all("reports/scaffold/" not in reference
                            for row in matrix["requirements"]
                            for reference in row["evidence_refs"]))


if __name__ == "__main__":
    unittest.main()
