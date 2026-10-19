from __future__ import annotations
import unittest
class WorkbenchTests(unittest.TestCase):
 def test_ac_ui_01_card_exposes_context(self):
  from volterra.workbench import NumericalCard
  c=NumericalCard('t','conditional',5,'v1','SYNTHETIC',.2);self.assertEqual(c.status,'AVAILABLE')
 def test_ac_ui_02_branch_changes_validated_assumption(self):
  from volterra.workbench import ScenarioBranch
  b=ScenarioBranch('base',{'lag':1});n=b.edit('lag',2);self.assertNotEqual(n.branch_id,b.branch_id)
 def test_ac_ui_03_empty_states_do_not_invent_probability(self):
  from volterra.workbench import NumericalCard
  self.assertIsNone(NumericalCard('t','c',1,'v','SYNTHETIC',None,'UNAVAILABLE').value)
 def test_ac_ui_04_05_coverage_and_lineage_labels(self):
  from volterra.workbench import ArbitrationView,CoverageView
  self.assertEqual(CoverageView(.2).label,'RESEARCH_MONITORING_COVERAGE');self.assertEqual(ArbitrationView(('a',),(),{'a':1},.1).actual_runs,('a',))

 def test_ac_ui_06_workbench_cli_is_reproducible(self):
  import os,subprocess,sys,json
  r=subprocess.run([sys.executable,'-B','-m','volterra','workbench','inspect'],capture_output=True,text=True,env=dict(os.environ,PYTHONPATH='src'))
  self.assertEqual(r.returncode,0);self.assertEqual(json.loads(r.stdout)['status'],'UNAVAILABLE')
