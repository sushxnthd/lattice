"""Regression tests for Run241 trusted-selector adapter."""
import unittest

from trusted_action_adapter import ContractError, project_and_validate


PATH = "pkg/example.py"
METHOD = "    def old(self):\n        return 1\n"
LEXER = "TOKENS = []\n"
FACTS = {
    "blocks": [
        {"selector": "m", "path": PATH, "name": "old",
         "kind": "method", "authority": "editable", "code": METHOD},
        {"selector": "r", "path": PATH, "name": "read_only",
         "kind": "method", "authority": "read_only",
         "code": "    def read_only(self):\n        pass\n"},
        {"selector": "l", "path": "pkg/lexer.py", "name": "TOKENS",
         "kind": "assignment", "authority": "editable", "code": LEXER},
    ],
    "file_sha256": {PATH: "trusted-hash", "pkg/lexer.py": "lexer-hash"},
}


class TrustedActionAdapterTests(unittest.TestCase):
    def test_injects_trusted_hash_and_path(self):
        out = project_and_validate(FACTS, {"actions": [
            {"selector": "m", "content": METHOD}]})
        self.assertEqual(out["actions"][0]["file_sha256"], "trusted-hash")
        self.assertEqual(out["actions"][0]["path"], PATH)

    def test_rejects_method_rename(self):
        with self.assertRaisesRegex(ContractError, "declaration erased"):
            project_and_validate(FACTS, {"actions": [
                {"selector": "m", "content": "    def new(self):\n        pass\n"}]})

    def test_rejects_readonly(self):
        with self.assertRaisesRegex(ContractError, "unauthorized selector"):
            project_and_validate(FACTS, {"actions": [
                {"selector": "r", "content": "    def read_only(self):\n        pass\n"}]})

    def test_rejects_duplicate(self):
        with self.assertRaisesRegex(ContractError, "duplicate selector"):
            project_and_validate(FACTS, {"actions": [
                {"selector": "m", "content": METHOD},
                {"selector": "m", "content": METHOD}]})

    def test_rejects_erased_assignment(self):
        with self.assertRaisesRegex(ContractError, "assignment erased"):
            project_and_validate(FACTS, {"actions": [
                {"selector": "l", "content": "OTHER = []\n"}]})

    def test_preserves_assignment(self):
        out = project_and_validate(FACTS, {"actions": [
            {"selector": "l", "content": "TOKENS = ['ELIF']\n"}]})
        self.assertEqual(out["actions"][0]["file_sha256"], "lexer-hash")


if __name__ == "__main__":
    unittest.main()
