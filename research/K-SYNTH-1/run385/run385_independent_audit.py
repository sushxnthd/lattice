#!/usr/bin/env python3
"""Independent Run385 audit: fresh CPython on frozen synthetic-only sources.

No generated model code is run. Frozen source is AST-validated against the
strict Run383 grammar before CPython execution, imports are stripped, and
builtins are empty. The independent ANF implementation uses exhaustive proper
subsets, not the implementation's in-place Moebius transform.
"""
import ast,hashlib,json,collections
from pathlib import Path
from run383_exact_counterfactual import parse

ROOT=Path(__file__).resolve().parent
INPUTS=((False,False),(False,True),(True,False),(True,True))
PRODUCER='def produce(x,y):\n    return x and y\n'

def reference_anf(values):
    out=[]
    for mask in range(16):
        prev=sum(out[s] for s in range(mask) if (s&mask)==s)%2
        out.append(int(values[mask])^prev)
    return out

def replay(src):
    # parse() admits only a small whitelisted AST. This is synthetic corpus code,
    # never untrusted model output; original import is not executed.
    parse(PRODUCER,src)
    tree=ast.parse(src)
    name=tree.body[0].names[0].asname or 'produce'
    safe=ast.fix_missing_locations(ast.Module(body=tree.body[1:],type_ignores=[]))
    code=compile(safe,'<frozen-synthetic-boolean>','exec')
    obs=[]
    for table in range(16):
        def producer(x,y,t=table):return bool((t>>(2*int(x)+int(y)))&1)
        namespace={'__builtins__':{},name:producer}
        exec(code,namespace,namespace)
        obs.append([bool(namespace['target'](*xy)) for xy in INPUTS])
    return obs

def main():
    rows=json.loads((ROOT/'run385_results.json').read_text())['records']
    original={r['id']:r for r in json.loads((ROOT/'prior/run374_raw.json').read_text())['records']}
    fresh={r['id']:r for r in json.loads((ROOT/'prior/run384_cross_input_raw.json').read_text())['records']}
    checked=0; support_checked=0; pair_checked=0; unknown=0
    for r in rows:
        if r['verdict']=='UNKNOWN':unknown+=1;continue
        src=(original if r['group']=='frozen1100' else fresh)[r['id']]['source']
        assert hashlib.sha256(src.encode()).hexdigest()==r['source_sha256']
        obs=replay(src)
        for t in range(16):
            for i in range(4):
                assert obs[t][i]==r['truth'][i][t],(r['id'],t,i)
                checked+=1
        for i in range(4):
            truth=[obs[t][i] for t in range(16)]
            coefficients=reference_anf(truth)
            assert coefficients==r['anf'][i],(r['id'],i,'anf')
            for bit in range(4):
                actual=any(truth[t]!=truth[t^(1<<bit)] for t in range(16))
                assert actual==r['support'][i][bit]
                support_checked+=1
            for j in range(4):
                for k in range(j+1,4):
                    actual=any(truth[t]^truth[t^(1<<j)]^truth[t^(1<<k)]^truth[t^(1<<j)^(1<<k)] for t in range(16))
                    assert actual==r['interaction'][i][j*(7-j)//2+(k-j-1)],(r['id'],i,j,k)
                    pair_checked+=1
    report={'experiment':'run385_independent_fresh_cpython_audit','programs_total':len(rows),
            'programs_replayed':len(rows)-unknown,'unknown':unknown,
            'fresh_cpython_observations':checked,'support_entries_checked':support_checked,
            'pairwise_interaction_entries_checked':pair_checked,
            'mismatches':0}
    (ROOT/'run385_audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
