from __future__ import annotations
import unittest


class MixtureTests(unittest.TestCase):
    def test_ac_dist_03_cdf_mixture_is_not_weighted_quantile_average(self) -> None:
        from volterra.distributions import DiscreteDistribution, cdf_mixture, weighted_quantile_average
        left = DiscreteDistribution(((0.0, 1.0),))
        right = DiscreteDistribution(((10.0, 1.0),))
        mixture = cdf_mixture(((0.5, left), (0.5, right)))
        self.assertEqual(mixture.cdf(0.0), 0.5)
        self.assertEqual(mixture.quantile(0.5), 0.0)
        self.assertEqual(weighted_quantile_average(((0.5, left), (0.5, right)), 0.5), 5.0)

    def test_ac_dist_04_empirical_crps_identity_matches_direct_enumeration(self) -> None:
        from volterra.distributions import DiscreteDistribution
        distribution = DiscreteDistribution(((0.0, 0.25), (2.0, 0.75)))
        self.assertAlmostEqual(distribution.crps(1.0), 0.625)

