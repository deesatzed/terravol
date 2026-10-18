from __future__ import annotations
import unittest
class PathTests(unittest.TestCase):
 def test_ac_dist_05_path_sum_and_annualized_volatility(self):
  from volterra.paths import VariancePath
  path=VariancePath((.01,.09))
  self.assertAlmostEqual(path.cumulative_variance,.10)
  self.assertLess(path.annualized_volatility(1),path.annualized_volatility(2))
 def test_ac_dist_06_marginal_adapter_rejects_joint_queries(self):
  from volterra.paths import MarginalOnlyError, MarginalPathAdapter
  with self.assertRaises(MarginalOnlyError): MarginalPathAdapter().joint_tail()
 def test_ac_dist_07_joint_mixture_preserves_world_path(self):
  from volterra.paths import JointPathMixture
  mixture=JointPathMixture(((.5,(0,0)),(.5,(1,1))))
  self.assertEqual(mixture.support(),{(0,0),(1,1)})
  self.assertNotIn((0,1),mixture.support())

