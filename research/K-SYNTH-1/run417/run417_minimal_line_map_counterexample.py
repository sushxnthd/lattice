#!/usr/bin/env python3
"""Run417 minimal counterexample: AST-equivalent RHS edit shifts line trace."""
import ast
import json
import subprocess
import sys

SOURCE = """# coding: utf-8
def f(x):
    dead = (
        x
        + 1
    )
    live = x + 2
    return live
"""
EDITED = SOURCE.replace("x\n        + 1", "x + 3")
TRACER = """import json,sys
lines=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=="f" and event=="line": lines.append(frame.f_lineno)
 return trace
sys.settrace(trace)
value=f(7)
sys.settrace(None)
print(json.dumps({"value":value,"lines":lines},sort_keys=True))
"""
def run(source):
    cp=subprocess.run([sys.executable,"-I","-S","-c",source+"\n"+TRACER],
                      text=True,capture_output=True,timeout=5,check=True)
    return json.loads(cp.stdout)
def suffix_lines(source):
    f=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef))
    return [n.lineno for n in f.body[1:]]
if __name__=="__main__":
    original=run(SOURCE)
    edited=run(EDITED)
    assert original["value"]==edited["value"]==9
    assert suffix_lines(SOURCE)!=suffix_lines(EDITED)
    assert original["lines"][-1]!=edited["lines"][-1]
    print(json.dumps({"original":original,"edited":edited,
                      "original_suffix_lines":suffix_lines(SOURCE),
                      "edited_suffix_lines":suffix_lines(EDITED)},sort_keys=True))
