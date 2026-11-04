#!/usr/bin/env python3
"""Run477: deterministic canonicalization/expressibility audit. No untrusted execution."""
import ast, json, hashlib
CASES = [
 ("3",3,True), ("0x3",3,False), ("+3",3,False),
 ("3 ",3,False), ("3 # note",3,False), ("(3)",3,False),
 ("-3",-3,True), ("- 3",-3,False), ("-0x3",-3,False),
 ("'a'","a",True), ('"a"',"a",False),
 ("03",None,False), ("3;4",None,False),
 ("f()",None,False), ("True",None,False)
]
def literal_value(s):
    try:
        t=ast.parse(s,mode="eval").body
        if isinstance(t,ast.Constant) and type(t.value) in (int,str): return t.value
        if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.USub) and isinstance(t.operand,ast.Constant) and type(t.operand.value) is int: return -t.operand.value
    except (SyntaxError,ValueError): pass
    return None
def canonical(s,v):
    return s == repr(v) if type(v) in (int,str) else False
def main():
    rows=[]
    for source,expected,expected_canonical in CASES:
        actual=literal_value(source)
        assert actual == expected, (source,actual,expected)
        accepted=canonical(source,actual)
        assert accepted == expected_canonical,(source,accepted)
        rows.append(dict(source=source,parsed_value=actual,canonical_accepted=accepted))
    assert sum(x["canonical_accepted"] for x in rows)==3
    assert sum(x["parsed_value"] is not None and not x["canonical_accepted"] for x in rows)==8
    payload=json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    print(json.dumps(dict(cases=len(rows),canonical_accepted=3,valid_noncanonical=8,invalid=4,rows=rows,sha256=hashlib.sha256(payload.encode()).hexdigest()),indent=2))
if __name__=="__main__": main()
