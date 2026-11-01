#!/usr/bin/env python3
"""Run418: executable witness that Run416 cannot edit qualified PR syntax."""
import ast
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "run416"))
import run402_dual_edit as base
import run416_lossless_compiler as editor

def compile_rhs(source, expression="x + 3", language=editor.SEMANTIC):
    files={"a.py":source}
    action=({"path":"a.py","function":"f","definition":"dead","expression":expression}
            if language==editor.SEMANTIC else
            {"path":"a.py","function":"f","statement_index":0,"expression":expression})
    return editor.compile_lossless(files,{"a.py":base.sha(source)},{"a.py":["f"]},[action],language)

def check():
    positive="def f(x):\n    dead = x + 1\n    return dead\n"
    conditional="def f(x):\n    dead = x + 1\n    if x:\n        return dead\n    return x\n"
    nested="def f(x):\n    if x:\n        dead = x + 1\n    return x\n"
    call="def f(x):\n    dead = x + 1\n    print(dead)\n    return dead\n"
    for language in (editor.SEMANTIC, editor.ORDINARY):
        out,_=compile_rhs(positive,language=language)
        assert "dead = x + 3" in out["a.py"]
        for source in (conditional,nested,call):
            try: compile_rhs(source,language=language)
            except (base.Unknown,base.InvalidEdit): pass
            else: raise AssertionError("unexpectedly accepted unsupported edit")
        try: compile_rhs(positive,"urlsplit(x).hostname",language)
        except (base.Unknown,base.InvalidEdit): pass
        else: raise AssertionError("unexpectedly accepted dynamic expression")
        source="from urllib.parse import quote\n"+positive
        out,_=compile_rhs(source,language=language)
        assert ast.dump(ast.parse(out["a.py"]).body[0])==ast.dump(ast.parse(source).body[0])
    print("RUN418_COMPILER_CAPABILITY_GATE_PASS")
if __name__=="__main__": check()
