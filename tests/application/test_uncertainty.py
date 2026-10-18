from __future__ import annotations
import unittest

class UncertaintyTests(unittest.TestCase):
    def test_ac_prob_09_parameter_and_monte_carlo_intervals_are_not_predictive(self) -> None:
        from volterra.distributions import Interval, UncertaintyError
        parameter = Interval(0.1, 0.2, kind="PARAMETER")
        monte_carlo = Interval(0.1, 0.2, kind="MONTE_CARLO_ERROR")
        self.assertFalse(parameter.is_predictive_outcome)
        self.assertFalse(monte_carlo.is_predictive_outcome)
        with self.assertRaises(UncertaintyError): parameter.as_predictive_outcome()

