#!/usr/bin/env python3
"""Run263 regression: ast.parse acceptance is weaker than CPython compilability.

First run RESTORE_COMPILABLE_EDITOR.py from repository root, then execute this
test with the resulting atomic_span_editor_v3.py on PYTHONPATH.
"""
import ast, json, unittest
from atomic_span_editor_v3 import apply_transaction, digest

class CompilerValidity(unittest.TestCase):
    def test_ast_parse_is_not_compilability(self):
        path = "src/example.py"
        original = b"pass\n"
        invalid = [
            "return 1\n", "break\n", "continue\n",
            "nonlocal x\n", "yield 1\n", "await f()\n",
            "def f(x,x):\n    pass\n",
        ]
        for candidate in invalid:
            with self.subTest(candidate=candidate):
                ast.parse(candidate, filename=path)
                with self.assertRaises(SyntaxError):
                    compile(candidate, path, "exec", dont_inherit=True)
                tx = {
                    "schema": "lattice.atomic_span.v1",
                    "files": {path: digest(original)},
                    "edits": [{
                        "path": path, "start": 0, "end": len(original),
                        "old_sha256": digest(original),
                        "replacement": candidate,
                    }],
                }
                with self.assertRaises(ValueError):
                    apply_transaction(json.dumps(tx), {path: original}, {path})

    def test_compilation_does_not_execute(self):
        path, original = "src/example.py", b"pass\n"
        replacement = "raise RuntimeError('must not execute')\n"
        tx = {"schema": "lattice.atomic_span.v1",
              "files": {path: digest(original)},
              "edits": [{"path": path, "start": 0, "end": len(original),
                         "old_sha256": digest(original), "replacement": replacement}]}
        updated, audit = apply_transaction(json.dumps(tx), {path: original}, {path})
        self.assertEqual(updated[path], replacement.encode())
        self.assertEqual(len(audit), 1)

if __name__ == "__main__":
    unittest.main()
