#!/usr/bin/env python3
"""Prospective scoped declaration/decorator contract tests."""
import unittest
from run236_descriptor_contract import (
    validate_declaration_and_decorators, DeclarationContractError
)


class DescriptorTests(unittest.TestCase):
    def setUp(self):
        self.before = "class C:\n    @property\n    def value(self):\n        return 1\n"
        self.target = {"kind": "FunctionDef", "name": "value",
                       "start_line": 2, "end_line": 4}

    def test_preserved(self):
        after = "class C:\n    @property\n    def value(self):\n        return 2\n"
        self.assertTrue(validate_declaration_and_decorators(
            self.target, self.before, after)["passes"])

    def test_decorator_erased(self):
        after = "class C:\n    def value(self):\n        return 2\n"
        with self.assertRaises(DeclarationContractError):
            validate_declaration_and_decorators(self.target, self.before, after)

    def test_explicit_decorator_authority(self):
        after = "class C:\n    def value(self):\n        return 2\n"
        result = validate_declaration_and_decorators(
            self.target, self.before, after, allow_decorator_change=True)
        self.assertFalse(result["decorators_preserved"])

    def test_declaration_erased(self):
        with self.assertRaises(DeclarationContractError):
            validate_declaration_and_decorators(
                self.target, self.before, "class C:\n    pass\n")

    def test_moved_scope_rejected(self):
        after = "class D:\n    @property\n    def value(self):\n        return 2\n"
        with self.assertRaises(DeclarationContractError):
            validate_declaration_and_decorators(self.target, self.before, after)


if __name__ == "__main__":
    unittest.main()
