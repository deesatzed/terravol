"""VT01 distribution representation acceptance tests."""
from __future__ import annotations

import unittest


class DistributionContractTests(unittest.TestCase):
    def test_ac_dist_02_quantile_only_forecast_does_not_claim_tails_or_joint_paths(self) -> None:
        try:
            from volterra.contracts import ContractError, QuantileForecast
        except ImportError as exc:
            self.fail(f"VT01 distribution contracts are not implemented: {exc}")
        forecast = QuantileForecast.from_pairs(((0.1, 0.01), (0.5, 0.03), (0.9, 0.08)))
        self.assertFalse(forecast.has_full_cdf)
        self.assertFalse(forecast.has_joint_paths)
        with self.assertRaises(ContractError):
            QuantileForecast.from_pairs(((0.1, 0.01), (0.5, 0.08), (0.9, 0.03)))
        with self.assertRaises(ContractError):
            QuantileForecast.from_pairs(((0.0, 0.01), (0.5, 0.03)))


if __name__ == "__main__":
    unittest.main()
