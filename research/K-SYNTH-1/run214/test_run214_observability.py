"""Run214 observable-behavior regression cases. Executed under CPython 3.11/3.12."""
import unittest
from repo_transaction import Rejected
from semantic_refactor import compile_semantic_rename

CASES = {
    "decorator_registration": 'registry = []\ndef register(fn):\n    registry.append(repr(fn).split(" at ")[0])\n    return fn\n@register\ndef old():\n    return 7\ndef probe():\n    return registry\n',
    "generator_repr": 'def old():\n    yield 7\ndef probe():\n    return repr(old()).split(" at ")[0]\n',
    "nested_lambda_repr": 'def old():\n    return lambda: 7\ndef probe():\n    return repr(old()).split(" at ")[0]\n',
    "exception_traceback": 'import traceback\ndef old():\n    raise RuntimeError("boom")\ndef probe():\n    try:\n        old()\n    except RuntimeError:\n        return traceback.format_exc().splitlines()[-3].split("in ")[-1]\n',
    "logging_funcname": 'import logging\nimport io\nstream = io.StringIO()\nhandler = logging.StreamHandler(stream)\nhandler.setFormatter(logging.Formatter("%(funcName)s"))\nlogger = logging.getLogger("run214")\nlogger.addHandler(handler)\nlogger.setLevel(logging.INFO)\ndef old():\n    logger.info("event")\ndef probe():\n    old()\n    return stream.getvalue().strip()\n',
    "async_coroutine_repr": 'async def old():\n    return 7\ndef probe():\n    c = old()\n    name = repr(c).split(" at ")[0]\n    c.close()\n    return name\n',
}

def rename(source):
    snap={"target.py":source.encode("utf-8")}
    return compile_semantic_rename(snap,set(snap),module_map={"target.py":"target"},
        target_path="target.py",old="old",new="new",closed_world=True)

class Run214Tests(unittest.TestCase):
    def test_six_new_observation_counterexamples_rejected(self):
        for name,source in CASES.items():
            with self.subTest(name=name),self.assertRaises(Rejected):
                rename(source)

    def test_direct_call_positive_control(self):
        tx,_=rename('def old(x):\n    return x+1\ndef probe():\n    return old(3)\n')
        self.assertIn(b'def new(x)',tx.changes['target.py'])

    def test_nested_definition_rejected(self):
        with self.assertRaisesRegex(Rejected,"nested code"):
            rename('def old():\n    def nested(): return 1\n    return nested()\n')

if __name__=="__main__": unittest.main()
