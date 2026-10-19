from __future__ import annotations
import unittest
class QueryDedupTests(unittest.TestCase):
 def test_query_dedup_keeps_origin_target_identity(self):
  from volterra.cascades import dedup_queries
  self.assertEqual(len(dedup_queries((("episode","origin1","target1"),("episode","origin2","target2")))),2)
