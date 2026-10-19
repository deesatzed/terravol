from __future__ import annotations
import unittest
class InteractionTests(unittest.TestCase):
 def test_declared_interactions_are_distinct(self):
  from volterra.cascades import interaction
  self.assertEqual(interaction("AND",True,True),True)
  self.assertEqual(interaction("INHIBIT",True,True),False)
