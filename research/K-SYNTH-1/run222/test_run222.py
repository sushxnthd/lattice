"""Deterministic pre-inference Run222 tests; no network or model required."""
import json, pathlib, subprocess, sys, tempfile, unittest
from unittest.mock import patch
import run220, run222, paired_repo_pilot as prior, run217_matched_pilot as view

class Run222Tests(unittest.TestCase):
    def test_frozen_three_discovery_issues(self):
        self.assertEqual(run222.INDICES,(2,6,7))
        rows=json.loads(pathlib.Path('cohort.json').read_text())
        self.assertEqual(tuple(r['instance_id'] for r in rows),run220.COHORT_IDS)
        self.assertTrue(all(rows[i]['split']=='discovery' for i in run222.INDICES))
    def test_lexical_preflight_counterexample(self):
        issue={'problem_statement':'Fix `_get_metadata` in refresh_utils.py.'}
        self.assertIn('_get_metadata',issue['problem_statement'])
        self.assertNotIn('_get_metadata',run220.issue_names(issue))
    def test_lossless_control_views_and_reference_functionality(self):
        issue={'problem_statement':'In sample.py change scale(x) to return x + 2.'}
        files={'sample.py':b'def scale(x):\n    return x + 1\n'}
        f=run220.facts(files,issue)
        self.assertEqual(json.loads(json.dumps(f)),view.parse_python_view(view.python_view(f)))
        t=next(t for t in f['sample.py']['targets'] if t['name']=='scale')
        patch={'actions':[{'op':'replace','path':'sample.py','file_sha256':f['sample.py']['file_sha256'],
            'selector':t['target_id'],'replacement':'def scale(x):\n    return x + 2\n','content':''}]}
        tx=prior.compile_arm(files,patch,{'sample.py'},'python_short_id')
        ns={};exec(compile(tx.changes['sample.py'],'sample.py','exec'),ns)
        self.assertEqual([ns['scale'](x) for x in (-3,0,2)],[-1,2,4])
    def test_compiler_acceptance_not_equivalent_to_functional_control(self):
        def fake(endpoint,folder,issue,facts,files,authority,arm):
            t=next(t for t in facts['sample.py']['targets'] if t['name']=='scale')
            patch={'actions':[{'op':'replace','path':'sample.py',
                'file_sha256':facts['sample.py']['file_sha256'],'selector':t['target_id'],
                'replacement':'def scale(x):\n    return x + 9\n','content':''}]}
            (folder/'mock-response.json').write_text(json.dumps({'choices':[{'message':{'content':json.dumps(patch)}}]}))
            return {'accepted':True}
        with tempfile.TemporaryDirectory() as d,patch.object(run220,'invoke',fake):
            self.assertFalse(run222.control('unused',pathlib.Path(d),'semantic_ir_json')['independent_functional_control'])
    def test_freeze_no_functional_claim(self):
        with tempfile.TemporaryDirectory() as d:
            for i in run222.INDICES:
                subprocess.run([sys.executable,'run222.py','--cohort','cohort.json',
                    '--out',str(pathlib.Path(d)/str(i)),'--task-index',str(i),'--freeze-only'],check=True)
                f=json.loads((pathlib.Path(d)/str(i)/'freeze.json').read_text())
                self.assertEqual(f['functional_issue_resolution'],'NOT_EVALUATED')
                self.assertTrue(f['boundary_untouched'])

if __name__=='__main__':unittest.main()
