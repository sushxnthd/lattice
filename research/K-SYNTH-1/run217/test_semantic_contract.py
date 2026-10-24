import unittest
from semantic_contract import check_rename_contract

class ContractTests(unittest.TestCase):
    def test_valid_multifile_refactor(self):
        files={"pkg/a.py":b"def better(x):\n    return x + 1\n\ndef internal(y):\n    return better(y)\n",
               "pkg/b.py":b"from pkg.a import better\n\ndef call(x):\n    return better(x)\n"}
        result=check_rename_contract(files,definition_path="pkg/a.py",old="foo",new="better",
                                     required_calls={"pkg/a.py":"better","pkg/b.py":"better"})
        self.assertTrue(result.passed,result.failures)

    def test_dead_code_stale_reference_rejected(self):
        files={"pkg/a.py":b"def better(x):\n    return x + 1\n    return foo(x)\n"}
        result=check_rename_contract(files,definition_path="pkg/a.py",old="foo",new="better")
        self.assertFalse(result.passed)
        self.assertTrue(any("stale name" in f for f in result.failures))

    def test_wrong_public_name_rejected(self):
        files={"pkg/a.py":b"def new_foo(x):\n    return x + 1\n"}
        self.assertFalse(check_rename_contract(files,definition_path="pkg/a.py",old="foo",new="better").passed)

    def test_stale_import_and_attribute_rejected(self):
        files={"pkg/a.py":b"def better(x):\n    return x\n",
               "pkg/b.py":b"from pkg.a import foo\n\ndef call(x):\n    return foo(x)\n",
               "pkg/c.py":b"import pkg.a as a\n\ndef call(x):\n    return a.foo(x)\n"}
        result=check_rename_contract(files,definition_path="pkg/a.py",old="foo",new="better")
        self.assertFalse(result.passed)
        self.assertGreaterEqual(len(result.failures),3)

if __name__=="__main__": unittest.main()
