#!/usr/bin/env python3
"""Bounded structural scope relation. UNKNOWN for unresolved/dynamic cases."""
from pathlib import PurePosixPath
from itertools import product
import json

def path_relation(fixture, test, *, normalized=True, symlinks_resolved=True, dynamic=False):
    if not normalized or not symlinks_resolved or dynamic:
        return "UNKNOWN"
    f=PurePosixPath(fixture).parts
    t=PurePosixPath(test).parts
    if not f or not t or any(x in (".","..") for x in f+t):
        return "UNKNOWN"
    return "APPLIES" if len(f)<=len(t) and t[:len(f)]==f else "NOT_APPLIES"

def exhaustive():
    tuples=[p for n in range(1,5) for p in product(("a","ab","b"),repeat=n)]
    checks=0
    false_positives=0
    witnesses=[]
    for a in tuples:
        for b in tuples:
            expected=len(a)<=len(b) and b[:len(a)]==a
            assert (path_relation("/".join(a),"/".join(b))=="APPLIES")==expected
            checks+=1
            if "/".join(b).startswith("/".join(a)) and not expected:
                false_positives+=1
                if len(witnesses)<5:
                    witnesses.append({"fixture":"/".join(a),"test":"/".join(b)})
    assert path_relation("a","a/b",symlinks_resolved=False)=="UNKNOWN"
    assert path_relation("a","a/b",dynamic=True)=="UNKNOWN"
    return {"pairs":checks,"lexical_false_positives":false_positives,
            "witnesses":witnesses,
            "empty_baseid_counterexample":{"fixture_dir":"tests/sdk/inner",
            "test":"tests/sdk/test_outer.py","unsafe_empty_baseid_applies":True,
            "component_ancestry_applies":False}}
if __name__=="__main__":
    print(json.dumps(exhaustive(),indent=2))
