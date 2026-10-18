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


if __name__ == "__main__":
    unittest.main()
