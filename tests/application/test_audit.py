"""VT00 application-boundary audit tests, separate from scaffold checks."""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class VT00AuditTests(unittest.TestCase):
    def test_synthetic_target_declarations_are_explicit_and_finite(self) -> None:
        path = ROOT / "config" / "synthetic_targets.json"
        self.assertTrue(path.is_file(), "VT00 must freeze a synthetic target declaration")
        document = json.loads(path.read_text())
        self.assertEqual(document["schema_version"], "1.0")
        self.assertEqual(document["data_mode"], "SYNTHETIC_ONLY")
        self.assertEqual(document["targets"]["equity_variance"]["measurement_status"], "SYNTHETIC_PROXY")
        self.assertEqual(document["targets"]["equity_variance"]["annualization_sessions"], 252)

    def test_feasibility_matrix_keeps_external_evidence_unverified(self) -> None:
        path = ROOT / "config" / "feasibility_matrix.json"
        self.assertTrue(path.is_file(), "VT00 must record its external feasibility boundary")
        document = json.loads(path.read_text())
        self.assertEqual(document["schema_version"], "1.0")
        self.assertEqual(document["data_mode"], "SYNTHETIC_ONLY")
        statuses = {entry["status"] for entry in document["external_dependencies"]}
        self.assertTrue(statuses <= {"UNVERIFIED", "BLOCKED", "NOT_APPLICABLE"})
        self.assertNotIn("VERIFIED", statuses)

    def test_vt00_validator_reports_the_frozen_offline_boundary(self) -> None:
        try:
            from volterra.audit import validate_vt00
        except ImportError as exc:
            self.fail(f"VT00 audit validator is not implemented: {exc}")
        report = validate_vt00(ROOT)
        self.assertEqual(report["status"], "PASSED")
        self.assertEqual(report["data_mode"], "SYNTHETIC_ONLY")
        self.assertEqual(report["external_dependencies"]["UNVERIFIED"], 5)
        self.assertEqual(report["external_dependencies"]["BLOCKED"], 1)


if __name__ == "__main__":
    unittest.main()
