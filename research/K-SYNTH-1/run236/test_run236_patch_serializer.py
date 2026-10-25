#!/usr/bin/env python3
"""Prospective byte-faithful patch serializer regression tests (no model/GPU required)."""
import unittest
from run236_patch_serializer import byte_faithful_patch


class PatchTests(unittest.TestCase):
    def test_missing_terminal_newline(self):
        patch = byte_faithful_patch(
            {"x.py": b"def f():\n    pass\n"},
            {"x.py": b"def f():\n    return 2"},
        )
        self.assertIn(b"\\ No newline at end of file", patch)

    def test_new_file(self):
        patch = byte_faithful_patch({"new.py": None}, {"new.py": b"x=1"})
        self.assertIn(b"new file mode", patch)

    def test_delete_file(self):
        patch = byte_faithful_patch({"old.py": b"x=1\n"}, {"old.py": None})
        self.assertIn(b"deleted file mode", patch)

    def test_two_files(self):
        patch = byte_faithful_patch(
            {"a.py": b"a=1\n", "b.py": b"b=2\n"},
            {"a.py": b"a=2\n", "b.py": b"b=3\n"},
        )
        self.assertEqual(patch.count(b"diff --git"), 2)

    def test_binary(self):
        patch = byte_faithful_patch(
            {"image.bin": b"\0\1\2\3"},
            {"image.bin": b"\0\1\2\3\4"},
        )
        self.assertTrue(patch)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            byte_faithful_patch({"../bad": b"a"}, {"../bad": b"b"})


if __name__ == "__main__":
    unittest.main()
