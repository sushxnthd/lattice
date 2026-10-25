"""Regression tests for Run247 authority-boundary hardening.

Requires run240.py and trusted_compiler_v4.py on PYTHONPATH.
"""
import unittest
import run240
from trusted_compiler_v4 import compile_checked, declaration_counts

SOURCE='''class Service:
    def protected(self):
        return "ORIGINAL"

    def editable(self):
        return 1
'''
OLD='''    def editable(self):
        return 1
'''
PATH='service.py'
SELECTOR=run240.target_id(PATH,OLD)
FILES={PATH:SOURCE.encode()}
FACTS={'file_sha256':{PATH:run240.sha(FILES[PATH])},
       'blocks':[{'path':PATH,'name':'editable','kind':'method',
                  'authority':'editable','selector':SELECTOR,'code':OLD},
                 {'path':PATH,'name':'protected','kind':'method',
                  'authority':'read_only','selector':'a'*24,
                  'code':'    def protected(self):\n        return "ORIGINAL"\n'}]}
def action(code):
    return {'actions':[{'path':PATH,'file_sha256':FACTS['file_sha256'][PATH],
                        'selector':SELECTOR,'content':code}]}

class AuthorityTests(unittest.TestCase):
    def test_original_compiler_accepts_duplicate_shadow(self):
        malicious=OLD+'\n    def protected(self):\n        return "OVERRIDDEN"\n'
        after,_=run240.compile_actions(FACTS,FILES,action(malicious))
        scope={};exec(after[PATH],scope)
        self.assertEqual(scope['Service']().protected(),'OVERRIDDEN')
    def test_hardened_compiler_rejects_duplicate_shadow(self):
        malicious=OLD+'\n    def protected(self):\n        return "OVERRIDDEN"\n'
        with self.assertRaisesRegex(ValueError,'shadowing'):
            compile_checked(FACTS,FILES,action(malicious))
    def test_hardened_compiler_rejects_assignment_shadow(self):
        malicious=OLD+'\n    protected = lambda self: "OVERRIDDEN"\n'
        after,_=run240.compile_actions(FACTS,FILES,action(malicious))
        scope={};exec(after[PATH],scope)
        self.assertEqual(scope['Service']().protected(),'OVERRIDDEN')
        with self.assertRaisesRegex(ValueError,'write shadows'):
            compile_checked(FACTS,FILES,action(malicious))
    def test_benign_replacement(self):
        after,_=compile_checked(FACTS,FILES,action(OLD.replace('return 1','return 2')))
        scope={};exec(after[PATH],scope)
        self.assertEqual(scope['Service']().protected(),'ORIGINAL')
        self.assertEqual(scope['Service']().editable(),2)
    def test_unique_helper_allowed(self):
        after,_=compile_checked(FACTS,FILES,action(OLD+'\n    def helper(self):\n        return 5\n'))
        scope={};exec(after[PATH],scope)
        self.assertEqual(scope['Service']().helper(),5)
    def test_stale_source(self):
        with self.assertRaisesRegex(ValueError,'stale'):
            compile_checked(FACTS,{PATH:FILES[PATH]+b'\n'},action(OLD))
    def test_missing_source(self):
        with self.assertRaisesRegex(ValueError,'incomplete'):
            compile_checked(FACTS,{},action(OLD))
    def test_extra_source(self):
        with self.assertRaisesRegex(ValueError,'unexpected'):
            compile_checked(FACTS,{**FILES,'extra.py':b''},action(OLD))
    def test_duplicate_inventory(self):
        self.assertEqual(declaration_counts(SOURCE)[('Service','FunctionDef','protected')],1)

if __name__=='__main__':
    unittest.main()
