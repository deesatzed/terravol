from __future__ import annotations
import unittest
class JointArtifactTests(unittest.TestCase):
 def test_episode_and_path_must_agree(self):
  from volterra.cascades import joint_artifact
  with self.assertRaises(ValueError):joint_artifact(episode=True,variance_path=(0.0,0.0))
