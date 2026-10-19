from pathlib import Path
import unittest
class ReleaseTests(unittest.TestCase):
 def test_release_record_separates_engineering_from_scientific_and_live_claims(self):
  report=Path('docs/RELEASE_REPORT.md').read_text()
  for state in ('VERIFIED_LOCAL','BLOCKED','NOT_EVALUATED','PENDING','NOT_ASSESSED','NOT_RELEASED'):
   self.assertIn(state,report)
