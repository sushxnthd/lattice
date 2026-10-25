import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest

from prospective_symbol_gate import validate_replacement, DeclarationContractError


class Tests(unittest.TestCase):
    def test_decorator_and_scope_positive(self):
        before = '@staticmethod\ndef wait():\n    return 1\n'
        after = '@staticmethod\ndef wait():\n    return 2\n'
        target = {'kind':'FunctionDef','name':'wait','start_line':1,'end_line':3}
        self.assertTrue(validate_replacement(target,before,after)['passes'])

    def test_class_method_positive(self):
        before = 'class C:\n    def run(self):\n        return 1\n'
        after = 'class C:\n    def run(self):\n        return 2\n'
        target = {'kind':'FunctionDef','name':'run','start_line':2,'end_line':3}
        self.assertTrue(validate_replacement(target,before,after)['passes'])

    def test_move_to_other_class_rejected(self):
        before = 'class C:\n    def run(self):\n        return 1\n'
        after = 'class D:\n    def run(self):\n        return 2\n'
        target = {'kind':'FunctionDef','name':'run','start_line':2,'end_line':3}
        with self.assertRaises(DeclarationContractError):
            validate_replacement(target,before,after)

    def test_real_artifacts_reversed_patches(self):
        root = pathlib.Path(__file__).parent
        for name,issue in [('repo1','benchopt__benchopt-697'),
                           ('repo3','bluesky__bluesky-1850')]:
            d = root/name
            if not d.exists():
                self.skipTest('original cloud artifact not present')
            facts = json.loads((d/'facts.json').read_text())
            for arm in ('python_annotated','semantic_ir_json'):
                prefix = d/'raw'/f'{issue}-{arm}'
                rec = json.loads(pathlib.Path(str(prefix)+'-verifier.json').read_text())
                after = json.loads(pathlib.Path(str(prefix)+'-after.json').read_text())
                patch = pathlib.Path(str(prefix)+'-patch.diff').read_text()
                with tempfile.TemporaryDirectory() as tmp:
                    tmp = pathlib.Path(tmp)
                    for path,src in after.items():
                        p = tmp/path
                        p.parent.mkdir(parents=True,exist_ok=True)
                        p.write_text(src)
                    check = subprocess.run(['git','apply','--reverse','-'],
                                           input=patch,text=True,cwd=tmp,capture_output=True)
                    self.assertEqual(check.returncode,0,check.stderr)
                    for path,src in after.items():
                        before = (tmp/path).read_text()
                        self.assertEqual(hashlib.sha256(before.encode()).hexdigest(),
                                         rec['before'][path])
                        response = json.loads(pathlib.Path(str(prefix)+'-response.json').read_text())
                        acts = json.loads(response['choices'][0]['message']['content'])['actions']
                        for act in acts:
                            if act['op'] != 'replace' or act['path'] != path:
                                continue
                            t = next(t for t in facts[path]['targets']
                                     if t['target_id'] == act['selector'])
                            with self.assertRaises(DeclarationContractError):
                                validate_replacement(t,before,src)


if __name__ == '__main__':
    unittest.main()
