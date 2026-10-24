"""Prospective tests for Run210 bounded-context selection and transport parity."""
import json
import unittest
from paired_repo_pilot_210 import ARMS, CONTROL, FLAT_KEYS, compact_facts, compile_arm, prompt
from repo_transaction import Rejected


class BoundedViewTests(unittest.TestCase):
    def test_identical_information_all_arms(self):
        issue={'problem_statement':'Change compute(x) to return x + 2'}
        suffix=[prompt(issue,CONTROL,a).split('SOURCE AND STRUCTURAL FACTS (bounded shared view):\n',1)[1] for a in ARMS]
        self.assertEqual(suffix[0],suffix[1])
        self.assertEqual(suffix[1],suffix[2])
        self.assertLess(len(suffix[0]),26_000)

    def test_exact_preimage_vs_short_id_compile_equivalence(self):
        issue={'problem_statement':'Change compute(x) to return x + 2'}
        facts=compact_facts(CONTROL,issue)
        target=next(t for t in facts['src/a.py']['targets'] if 'def compute' in t['old_text'])
        after=[]
        for arm in ARMS:
            act={k:'' for k in FLAT_KEYS}
            act.update(op='replace',path='src/a.py',file_sha256=facts['src/a.py']['file_sha256'],
                       selector=target['old_text'] if arm=='python_text' else target['target_id'],
                       replacement='def compute(x):\n    return x + 2\n')
            tx=compile_arm(CONTROL,{'actions':[act]},set(CONTROL),arm)
            after.append(tx.changes['src/a.py'])
        self.assertEqual(after,[b'def compute(x):\n    return x + 2\n']*3)

    def test_long_non_python_file_has_local_line_targets(self):
        body=('irrelevant line of background\n'*700)+'important setting = False\n'
        files={'docs/large.md':body.encode()}
        issue={'problem_statement':'Change important setting in docs/large.md'}
        facts=compact_facts(files,issue)
        self.assertLess(len(json.dumps(facts)),26_000)
        self.assertTrue(any('important setting' in t['old_text'] for t in facts['docs/large.md']['targets']))
        self.assertIn('important setting',facts['docs/large.md']['source_excerpt'])

    def test_long_python_file_target_after_old_8kb_limit(self):
        src=''.join(f'def filler_{i}():\n    return {i}\n\n' for i in range(700))
        src+='def important_feature():\n    return "old"\n'
        self.assertGreater(len(src),8000)
        files={'pkg/large.py':src.encode()}
        issue={'problem_statement':'Change important_feature to return new'}
        facts=compact_facts(files,issue)
        self.assertTrue(any('important_feature' in t['old_text'] for t in facts['pkg/large.py']['targets']))
        self.assertLess(len(json.dumps(facts)),26_000)

    def test_stale_hash_rejected_in_every_arm(self):
        facts=compact_facts(CONTROL,{'problem_statement':'compute'})
        t=facts['src/a.py']['targets'][0]
        for arm in ARMS:
            a={k:'' for k in FLAT_KEYS}
            a.update(op='replace',path='src/a.py',file_sha256='0'*64,
                     selector=t['old_text'] if arm=='python_text' else t['target_id'],
                     replacement='def compute(x):\n    return x + 2\n')
            with self.assertRaises(Rejected):
                compile_arm(CONTROL,{'actions':[a]},set(CONTROL),arm)

if __name__=='__main__':
    unittest.main()
