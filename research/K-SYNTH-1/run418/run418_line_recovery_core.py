#!/usr/bin/env python3
"""Run418 bounded line-preserving lowering, not full trace equivalence.

Both semantic IR and ordinary AST actions pass through the same Run416
schema/authority/AST verifier. Preserves outside-span bytes and ordered EOLs
inside RHS spans; refuses in-span comments. No untrusted model code executes.
"""
import ast
import hashlib
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "run416"))
import run402_dual_edit as base
import run416_lossless_compiler as shared

EOLS=re.compile(rb"\r\n|\r|\n")

class UnknownComment(base.Unknown):
    pass

def compile_line_recovered(files, expected_sha, authority, actions, language):
    original_out, _=shared.compile_lossless(
        files, expected_sha, authority, actions, language
    )
    trees={p:ast.parse(s,filename=p) for p,s in files.items()}
    expected={p:ast.parse(s,filename=p) for p,s in original_out.items()}
    patches={p:[] for p in files}
    for action in actions:
        path=action["path"]; fn_name=action["function"]
        fn=base._function(trees[path],fn_name)
        graph=base._graph(fn)
        idx=(graph["definitions"][action["definition"]]["index"]
             if language==shared.SEMANTIC else action["statement_index"])
        start,end=shared._byte_span(files[path],fn.body[idx].value)
        old_rhs=files[path].encode("utf-8")[start:end]
        if b"#" in old_rhs:
            raise UnknownComment("UNKNOWN_COMMENT_IN_RHS")
        expr=ast.unparse(ast.parse(action["expression"],mode="eval").body).encode("utf-8")
        endings=tuple(EOLS.findall(old_rhs))
        replacement=(b"("+expr+b"".join(endings)+b")") if endings else expr
        assert tuple(EOLS.findall(replacement))==endings
        patches[path].append((start,end,replacement))
    output={}
    for path,source in files.items():
        ordered=sorted(patches[path])
        if any(a[1]>b[0] for a,b in zip(ordered,ordered[1:])):
            raise base.InvalidEdit("OVERLAPPING_RHS_SPANS")
        data=source.encode("utf-8")
        for start,end,replacement in reversed(ordered):
            data=data[:start]+replacement+data[end:]
        try:
            result=data.decode("utf-8")
            tree=ast.parse(result,filename=path)
        except (UnicodeError,SyntaxError) as exc:
            raise base.InvalidEdit("OUTPUT_INVALID_PYTHON") from exc
        if ast.dump(tree,include_attributes=False)!=ast.dump(expected[path],include_attributes=False):
            raise base.InvalidEdit("UNEXPECTED_AST_CHANGE")
        for fn_name in authority.get(path,[]):
            before=base._function(trees[path],fn_name).body
            after=base._function(tree,fn_name).body
            if [(x.lineno,x.end_lineno) for x in before]!=[(x.lineno,x.end_lineno) for x in after]:
                raise base.Unknown("UNKNOWN_LINE_MAP_SHIFT")
        output[path]=result
    return output

if __name__=="__main__":
    s="def f(x):\n    dead = (\n        x\n        + 1\n    )\n    live = x + 2\n    return live\n"
    files={"a.py":s};sha={"a.py":base.sha(s)};auth={"a.py":["f"]}
    sem=[{"path":"a.py","function":"f","definition":"dead","expression":"x + 3"}]
    py=[{"path":"a.py","function":"f","statement_index":0,"expression":"x + 3"}]
    a=compile_line_recovered(files,sha,auth,sem,shared.SEMANTIC)
    b=compile_line_recovered(files,sha,auth,py,shared.ORDINARY)
    assert a==b and a["a.py"].count("\n")==s.count("\n")
    print("RUN418_LINE_RECOVERY_BOUNDED_PASS")
