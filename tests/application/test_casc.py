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

