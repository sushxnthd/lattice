"""Adversarial tests for the representation-independent Run206 diagnostics."""
import unittest
from safety_gate import legal_header, evidence, enforce

ORIGINAL = (
    b"# Copyright 2026 Example\n"
    b"# Licensed under the Apache License, Version 2.0\n"
    b"\n"
    b"def f(x):\n    return x\n"
)

class GateTests(unittest.TestCase):
    def test_detect_legal_header(self):
        self.assertIn("Copyright", legal_header(ORIGINAL.decode()))

    def test_reject_license_removal(self):
        with self.assertRaisesRegex(ValueError, "legal-header removal"):
            enforce({"a.py": ORIGINAL}, {"a.py": b"def f(x):\n    return x\n"})

    def test_ast_equivalent_comment_only_rejected_when_requested(self):
        with self.assertRaisesRegex(ValueError, "no Python AST delta"):
            enforce({"a.py": ORIGINAL}, {"a.py": ORIGINAL + b"# Comment\n"},
                    require_python_ast_delta=True)

    def test_real_ast_delta_preserving_license_accepted(self):
        changed = ORIGINAL.replace(b"return x", b"return x + 1")
        result = enforce({"a.py": ORIGINAL}, {"a.py": changed},
                         require_python_ast_delta=True)
        self.assertTrue(result[0].ast_changed)
        self.assertTrue(result[0].legal_header_preserved)

    def test_comment_only_accepted_when_ast_gate_disabled(self):
        result = enforce({"a.py": ORIGINAL}, {"a.py": ORIGINAL + b"# Documentation\n"})
        self.assertFalse(result[0].ast_changed)

    def test_new_files_need_separate_authority(self):
        with self.assertRaises(ValueError):
            enforce({}, {"new.py": b"x=1\n"})

    def test_nonpython_does_not_require_ast(self):
        result = enforce({"README.md": b"a"}, {"README.md": b"b"},
                         require_python_ast_delta=True)
        self.assertIsNone(result[0].ast_changed)

    def test_invalid_syntax_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid Python syntax"):
            enforce({"a.py": ORIGINAL}, {"a.py": ORIGINAL + b"if :\n"})

    def test_empty_is_valid(self):
        self.assertEqual(enforce({}, {}), [])

if __name__ == "__main__":
    unittest.main()
