"""Run212 adversarial regressions against Run211 semantic refactor."""
import unittest
from repo_transaction import Rejected
from semantic_refactor import compile_semantic_rename

def rename(sources):
    data = {p: s.encode() for p, s in sources.items()}
    return compile_semantic_rename(data, set(data),
        module_map={p: p[:-3] for p in data},
        target_path="target.py", old="old", new="new", closed_world=True)

class Run212AdversarialTests(unittest.TestCase):
    def test_match_capture(self):
        source = {"target.py": "def old():\n    return 7\ndef probe(x):\n    match x:\n        case old:\n            return old\n"}
        with self.assertRaisesRegex(Rejected, "pattern capture"):
            rename(source)

    def test_star_capture(self):
        source = {"target.py": "def old():\n    return 7\ndef probe(x):\n    match x:\n        case [*old]:\n            return old\n"}
        with self.assertRaisesRegex(Rejected, "pattern capture"):
            rename(source)

    def test_mapping_capture(self):
        source = {"target.py": "def old():\n    return 7\ndef probe(x):\n    match x:\n        case {**old}:\n            return old\n"}
        with self.assertRaisesRegex(Rejected, "pattern rest capture"):
            rename(source)

    def test_aliased_getattr(self):
        source = {"target.py": "def old():\n    return 7\n",
                  "consumer.py": 'import target as t\nimport builtins as b\ndef probe():\n    key = "o" + "ld"\n    return b.getattr(t, key)()\n'}
        with self.assertRaisesRegex(Rejected, "reflection"):
            rename(source)

    def test_from_import_getattr_alias(self):
        source = {"target.py": "def old():\n    return 7\n",
                  "consumer.py": 'from builtins import getattr as g\nimport target as t\ndef probe():\n    return g(t, "o" + "ld")()\n'}
        with self.assertRaisesRegex(Rejected, "reflection"):
            rename(source)

    def test_name_introspection(self):
        source = {"target.py": "def old():\n    return 7\ndef probe():\n    return old.__name__\n"}
        with self.assertRaisesRegex(Rejected, "introspection"):
            rename(source)

    def test_module_alias_escape(self):
        source = {"target.py": "def old():\n    return 7\n",
                  "consumer.py": "import target as t\nalias = t\ndef probe():\n    return alias.old()\n"}
        with self.assertRaisesRegex(Rejected, "module alias escapes"):
            rename(source)

    def test_attribute_rebinding(self):
        source = {"target.py": "def old():\n    return 7\n",
                  "consumer.py": "import target as t\nt.old = lambda: 12\n"}
        with self.assertRaisesRegex(Rejected, "attribute rebinding"):
            rename(source)

    def test_normal_cross_module_rename(self):
        source = {"target.py": "def old():\n    return 7\ndef probe():\n    return old()\n",
                  "consumer.py": "from target import old\ndef probe():\n    return old()\n"}
        txn, _ = rename(source)
        self.assertIn(b"def new()", txn.changes["target.py"])
        self.assertIn(b"from target import new", txn.changes["consumer.py"])

if __name__ == "__main__":
    unittest.main()
