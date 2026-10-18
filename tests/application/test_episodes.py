from __future__ import annotations
import unittest
class EpisodeTests(unittest.TestCase):
 def test_ac_time_06_confirmation_and_right_censoring(self):
  from volterra.episodes import derive_episode
  state=derive_episode((.9,1.1,1.2,1.3),upper=1.0,lower=.5)
  self.assertEqual(state.started_at,1)
  self.assertTrue(state.right_censored)
