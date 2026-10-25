"""Independent local checks for the frozen paired Run234 experiment."""
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import run234 as r
from repo_transaction import Rejected,digest

ROOT=pathlib.Path(__file__).parent

class Run234Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public=(ROOT/'public/public.json').read_bytes()
        cls.prereg=json.loads((ROOT/'frozen_run234.json').read_bytes())
        cls.cohort=r.freeze_public(cls.public,cls.prereg)
        cls.files={'src/a.py':b'def compute(x):\n    return x + 1\n',
                   'src/b.py':b'from .a import compute\n\ndef run(x):\n    return compute(x)\n'}
        cls.issue={'problem_statement':'Please modify compute(x) and run(x) in both files, with complete function replacements.'}

    def test_public_sha(self):
        self.assertEqual(r.sha(self.public),r.PUBLIC_SHA)
    def test_selection_repositories(self):
        self.assertEqual(len(self.cohort),12)
        self.assertEqual(len({x['repo'] for x in self.cohort}),12)
        self.assertTrue(all(x['split']=='discovery' for x in self.cohort))
    def test_reject_changed_prereg(self):
        bad=dict(self.prereg);bad['cohort']=[dict(x) for x in bad['cohort']]
        bad['cohort'][0]['issue_sha256']='0'*64
        with self.assertRaises(ValueError):r.freeze_public(self.public,bad)
    def test_roundtrip_shared_facts(self):
        f=r.facts(self.files,self.issue)
        self.assertEqual(json.loads(r.canonical(f)),r.parse_python_view(r.python_view(f)))
        self.assertIn('compute',r.python_view(f))
    def test_prompt_info_equivalence(self):
        f=r.facts(self.files,self.issue)
        ir=r.prompt(self.issue,f,r.ARMS[0]);py=r.prompt(self.issue,f,r.ARMS[1])
        self.assertEqual(json.loads(ir.split('SOURCE_FACTS:\n',1)[1]),
                         r.parse_python_view(py.split('SOURCE_FACTS:\n',1)[1]))
        self.assertNotEqual(ir,py)
    def test_positive_two_file_functional_control(self):
        self.assertEqual(r.positive_controls()['positive_two_file_result'],8)
    def test_same_compiler_valid_edit(self):
        f=r.facts(self.files,self.issue)
        t=next(t for t in f['src/a.py']['targets'] if t['name']=='compute')
        action={'op':'replace','path':'src/a.py','file_sha256':digest(self.files['src/a.py']),
                'selector':t['target_id'],'content':'def compute(x):\n    return x + 5\n'}
        tx=r.compile_common(self.files,{'actions':[action]},set(self.files))
        self.assertIn(b'return x + 5',tx.changes['src/a.py'])
    def test_stale_hash_rejected(self):
        f=r.facts(self.files,self.issue)
        t=next(t for t in f['src/a.py']['targets'] if t['name']=='compute')
        action={'op':'replace','path':'src/a.py','file_sha256':'0'*64,
                'selector':t['target_id'],'content':'def compute(x):\n    return x + 5\n'}
        with self.assertRaises(Rejected):r.compile_common(self.files,{'actions':[action]},set(self.files))
    def test_unknown_selector_rejected(self):
        action={'op':'replace','path':'src/a.py','file_sha256':digest(self.files['src/a.py']),
                'selector':'0'*24,'content':'def compute(x):\n    return x + 5\n'}
        with self.assertRaises(Rejected):r.compile_common(self.files,{'actions':[action]},set(self.files))
    def test_bad_unused_field_rejected(self):
        action={'op':'create','path':'src/c.py','file_sha256':'stale','selector':'','content':'x=1\n'}
        with self.assertRaises(Rejected):r.compile_common(self.files,{'actions':[action]},set(self.files))
    def test_out_of_authority_rejected(self):
        f=r.facts(self.files,self.issue)
        t=next(t for t in f['src/a.py']['targets'] if t['name']=='compute')
        action={'op':'replace','path':'src/a.py','file_sha256':digest(self.files['src/a.py']),
                'selector':t['target_id'],'content':'def compute(x):\n    return x + 5\n'}
        with self.assertRaises(Rejected):r.compile_common(self.files,{'actions':[action]},set())
    def test_no_hidden_gold_fields(self):
        for x in self.cohort:
            self.assertFalse({'patch','test_patch','FAIL_TO_PASS','PASS_TO_PASS','gold_changed_files'}&set(x))
    def test_git_apply_patch(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td);(root/'src').mkdir()
            for p,b in self.files.items():
                dest=root/p;dest.write_bytes(b)
            subprocess.run(['git','init','-q',str(root)],check=True)
            subprocess.run(['git','-C',str(root),'add','.'],check=True)
            f=r.facts(self.files,self.issue)
            t=next(t for t in f['src/a.py']['targets'] if t['name']=='compute')
            action={'op':'replace','path':'src/a.py','file_sha256':digest(self.files['src/a.py']),
                    'selector':t['target_id'],'content':'def compute(x):\n    return x + 5\n'}
            tx=r.compile_common(self.files,{'actions':[action]},set(self.files))
            diff=r.patch_text(self.files,tx)
            proc=subprocess.run(['git','-C',str(root),'apply','--check','-'],
                                input=diff,text=True,capture_output=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
    def test_schema_digest(self):
        self.assertEqual(r.sha(r.canonical(r.schema())),self.prereg['schema_sha256'])

if __name__=='__main__':unittest.main()
