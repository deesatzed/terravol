"""Application control acceptance tests."""
from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ControlAcceptanceTests(unittest.TestCase):
    def test_ac_ctrl_01_canonical_goal_and_archive_are_identifiable(self) -> None:
        self.assertIn("GOAL_UPD.md", (ROOT / "GOAL.md").read_text())
        self.assertTrue((ROOT / "GOAL_UPD.md").is_file())
        self.assertTrue((ROOT / "docs/archive/spec-v1/GOAL.md").is_file())
        self.assertTrue((ROOT / "docs/archive/spec-v1/MANIFEST.json").is_file())

    def test_ac_ctrl_05_rejects_overflow_and_nested_nonfinite_numbers(self) -> None:
        try:
            from volterra.contracts import ContractError, canonical_json
        except ImportError as exc:
            self.fail(f"VT01 safe serialization is not implemented: {exc}")
        with self.assertRaises(ContractError):
            canonical_json({"nested": [1.0, float("inf")]})
        with self.assertRaises(ContractError):
            canonical_json({"overflow": float("1e999")})

    def test_ac_ctrl_06_student_t_rejects_invalid_scale_and_required_variance(self) -> None:
        try:
            from volterra.contracts import ContractError, StudentTSpec
        except ImportError as exc:
            self.fail(f"VT01 distribution parameter contracts are not implemented: {exc}")
        with self.assertRaises(ContractError):
            StudentTSpec(degrees_of_freedom=5, location=0.0, scale=-1.0)
        with self.assertRaises(ContractError):
            StudentTSpec(degrees_of_freedom=2, location=0.0, scale=1.0).require_finite_variance()
        StudentTSpec(degrees_of_freedom=3, location=0.0, scale=1.0).require_finite_variance()

    def test_ac_ctrl_07_missing_snapshot_or_artifact_reference_is_rejected(self) -> None:
        try:
            from volterra.storage import EvidenceLedger, LedgerError
        except ImportError as exc:
            self.fail(f"VT02 integrity references are not implemented: {exc}")
        import tempfile
        with tempfile.TemporaryDirectory(prefix="volterra-artifact-") as directory:
            ledger = EvidenceLedger(Path(directory) / "ledger.sqlite")
            self.addCleanup(ledger.close)
            with self.assertRaises(LedgerError):
                ledger.get_snapshot("missing")
            digest = ledger.put_artifact(b"synthetic artifact")
            self.assertEqual(ledger.read_artifact(digest), b"synthetic artifact")
            with self.assertRaises(LedgerError):
                ledger.read_artifact("0" * 64)


if __name__ == "__main__":
    unittest.main()
