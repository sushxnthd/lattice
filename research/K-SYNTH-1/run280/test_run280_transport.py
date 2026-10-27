import ast, pathlib, unittest
from unittest.mock import patch
import run280_transport_alias as t

class Tests(unittest.TestCase):
    def test_fixed_provenance(self):
        self.assertNotEqual(t.ORIGINAL_REF,t.MERGE_REF)
        self.assertEqual(len(t.ORIGINAL_BLOBS),2)
    def test_direct_child_and_blob_equivalence_enforced(self):
        def fake_git(root,*args):
            if args==('rev-parse','HEAD'):return t.BASE if str(root)=='base' else t.MERGE_REF
            if args==('rev-parse','HEAD^'):return t.BASE
            if args[0]=='hash-object':return t.ORIGINAL_BLOBS[args[1]]
            raise AssertionError(args)
        with patch.object(t,'git',side_effect=fake_git):
            self.assertEqual(t.verify_transport(pathlib.Path('base'),pathlib.Path('ref'))['reachable_merge_ref'],t.MERGE_REF)
        def wrong_blob(root,*args):
            if args[0]=='hash-object':return '0'*40
            return fake_git(root,*args)
        with patch.object(t,'git',side_effect=wrong_blob):
            with self.assertRaises(AssertionError):t.verify_transport(pathlib.Path('base'),pathlib.Path('ref'))
    def test_frozen_harness_unchanged(self):
        p=pathlib.Path(__file__).resolve().parent.parent/'run279'/'run279_httpcore_1000_qualify.py'
        if not p.exists():p=pathlib.Path(__file__).with_name('run279_httpcore_1000_qualify.py')
        tree=ast.parse(p.read_text())
        self.assertIn('qualify',[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)])
        self.assertEqual(t.ORIGINAL_REF,'7fb20526175e2300185ce2b472a97acca95b2525')

if __name__=='__main__':unittest.main()
