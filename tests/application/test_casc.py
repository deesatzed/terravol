"""VT03 exact cascade reference tests."""
from __future__ import annotations

import unittest


class ExactCascadeTests(unittest.TestCase):
    def test_ac_casc_01_three_independent_precursors_have_exact_any_mass(self) -> None:
        try:
            from volterra.cascades import independent_any_probability
        except ImportError as exc:
            self.fail(f"VT03 exact cascade reference is not implemented: {exc}")
        self.assertAlmostEqual(independent_any_probability((0.30, 0.30, 0.30)), 0.657)

    def test_ac_casc_03_and_04_coincident_and_exclusive_mass_are_not_independent(self) -> None:
        try:
            from volterra.cascades import coincident_any_probability, exclusive_any_probability
        except ImportError as exc:
            self.fail(f"VT03 dependence-specific reference is not implemented: {exc}")
        self.assertAlmostEqual(coincident_any_probability((0.30, 0.30, 0.30)), 0.30)
        self.assertAlmostEqual(exclusive_any_probability((0.30, 0.30, 0.30)), 0.90)
        with self.assertRaises(ValueError):
            exclusive_any_probability((0.60, 0.60))

    def test_ac_casc_06_two_marginals_return_joint_bounds_without_independence(self) -> None:
        try:
            from volterra.cascades import joint_probability_bounds
        except ImportError as exc:
            self.fail(f"VT03 joint-bounds reference is not implemented: {exc}")
        self.assertEqual(joint_probability_bounds(0.85, 0.85), (0.70, 0.85))

