#!/usr/bin/env python3
import ast,unittest
import run402_dual_edit as base
import run416_lossless_compiler as c

class LosslessTests(unittest.TestCase):
    def setUp(self):
        self.s='#!/usr/bin/env python3\n# Copyright retained\n# coding: utf-8\ndef f(x):\n    dead = (x + 1) # noqa: F841\n    live = x + 2\n    return live\n'
        self.files={'a.py':self.s}; self.h={'a.py':base.sha(self.s)}; self.auth={'a.py':['f']}
    def sem(self,expression='x + 3'):
        return [{'path':'a.py','function':'f','definition':'dead','expression':expression}]
    def py(self,expression='x + 3'):
        return [{'path':'a.py','function':'f','statement_index':0,'expression':expression}]
    def check_failure(self,exc,actions,lang=c.SEMANTIC,files=None,hashes=None,authority=None):
        with self.assertRaises(exc):
            c.compile_lossless(files if files is not None else self.files,
                               hashes if hashes is not None else self.h,
                               authority if authority is not None else self.auth,
                               actions,lang)
    def test_semantic_and_ast_byte_identical(self):
        a,rec=c.compile_lossless(self.files,self.h,self.auth,self.sem(),c.SEMANTIC)
        b,_=c.compile_lossless(self.files,self.h,self.auth,self.py(),c.ORDINARY)
        self.assertEqual(a,b);self.assertEqual(len(rec),1)
        self.assertIn('# Copyright retained',a['a.py']);self.assertIn('# noqa: F841',a['a.py'])
    def test_unchanged_outside_rhs(self):
        a,_=c.compile_lossless(self.files,self.h,self.auth,self.sem(),c.SEMANTIC)
        self.assertEqual(a['a.py'],self.s.replace('x + 1','x + 3'))
    def test_unmodified_file_exact(self):
        files=dict(self.files);files['b.py']='\n# immutable control\n'
        hashes={p:base.sha(s) for p,s in files.items()}
        a,_=c.compile_lossless(files,hashes,self.auth,self.sem(),c.SEMANTIC)
        self.assertEqual(a['b.py'],files['b.py'])
    def test_multibyte_columns(self):
        s=self.s.replace('dead =','dead =').replace('x + 1','(x + 1)')
        s=s.replace('    dead =','    dead =')
        s=s.replace('# Copyright retained','# 漢字 🧪')
        files={'a.py':s}
        a,_=c.compile_lossless(files,{'a.py':base.sha(s)},self.auth,self.sem(),c.SEMANTIC)
        self.assertIn('# 漢字 🧪',a['a.py'])
        self.assertEqual(ast.dump(ast.parse(a['a.py']),include_attributes=False),
                         ast.dump(ast.parse(s.replace('x + 1','x + 3')),include_attributes=False))
    def test_utf8_byte_column_same_line(self):
        s='def f(x):\n    π = x + 1\n    live = x + 2\n    return live\n'
        a=[{'path':'a.py','function':'f','definition':'π','expression':'x + 99'}]
        out,_=c.compile_lossless({'a.py':s},{'a.py':base.sha(s)},self.auth,a,c.SEMANTIC)
        self.assertEqual(out['a.py'],s.replace('x + 1','x + 99'))
    def test_multiline_parenthesized(self):
        s='def f(x):\n    dead = (\n       x\n       + 1\n    )\n    live = x + 2\n    return live\n'
        a,_=c.compile_lossless({'a.py':s},{'a.py':base.sha(s)},self.auth,self.sem(),c.SEMANTIC)
        self.assertIn('dead = (\n       x + 3\n    )',a['a.py'])
    def test_crlf_preserved(self):
        s=self.s.replace('\n','\r\n'); a,_=c.compile_lossless({'a.py':s},{'a.py':base.sha(s)},self.auth,self.sem(),c.SEMANTIC)
        self.assertEqual(a['a.py'].count('\r\n'),s.count('\r\n'))
    def test_source_hash_mismatch(self):
        self.check_failure(base.InvalidEdit,self.sem(),hashes={'a.py':'0'*64})
    def test_out_of_authority(self):
        a=self.sem();a[0]['function']='g';self.check_failure(base.InvalidEdit,a)
    def test_duplicate_target(self):
        self.check_failure(base.InvalidEdit,self.sem()+self.sem())
    def test_dynamic_call_rejected(self):
        self.check_failure(base.Unknown,self.sem('eval("1")'))
    def test_attribute_rejected(self):
        self.check_failure(base.Unknown,self.sem('x.__class__'))
    def test_unbound_name_rejected(self):
        self.check_failure(base.Unknown,self.sem('not_defined + 1'))
    def test_forward_name_rejected(self):
        self.check_failure(base.Unknown,self.sem('live + 1'))
    def test_ast_index_bool_rejected(self):
        a=self.py();a[0]['statement_index']=False;self.check_failure(base.InvalidEdit,a,c.ORDINARY)
    def test_unknown_definition(self):
        a=self.sem();a[0]['definition']='nope';self.check_failure(base.InvalidEdit,a)
    def test_schema_extra_field(self):
        a=self.sem();a[0]['extra']=True;self.check_failure(base.InvalidEdit,a)
    def test_bad_expression_syntax(self):
        self.check_failure(base.InvalidEdit,self.sem('x +'))
    def test_malicious_expr_rejected(self):
        self.check_failure(base.Unknown,self.sem('__import__("os").system("echo no")'))
    def test_unsupported_signature_rejected(self):
        s=self.s.replace('def f(x):','def f(x=1):')
        self.check_failure(base.Unknown,self.sem(),files={'a.py':s},hashes={'a.py':base.sha(s)})
    def test_empty_transaction_no_reformat(self):
        a,receipts=c.compile_lossless(self.files,self.h,self.auth,[],c.ORDINARY)
        self.assertEqual(a,self.files);self.assertEqual(receipts,[])
    def test_multiple_edits_same_file(self):
        a=self.sem()+[{'path':'a.py','function':'f','definition':'live','expression':'x + 17'}]
        out,receipts=c.compile_lossless(self.files,self.h,self.auth,a,c.SEMANTIC)
        self.assertEqual(out['a.py'],self.s.replace('x + 1','x + 3').replace('x + 2','x + 17'))
        self.assertEqual(len(receipts),2)

if __name__=='__main__':unittest.main(verbosity=2)
