from __future__ import annotations
import unittest
class PruningTests(unittest.TestCase):
 def test_pruning_preserves_remainder_and_no_event_mass(self):
  from volterra.cascades import preserved_mass
  self.assertEqual(preserved_mass(retained=.2,remainder=.3,no_event=.5),1.0)
