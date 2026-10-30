#!/usr/bin/env python3
"""Independent read-only source graph and CPython replay auditor for Run374.

Does not import the candidate analyzer or the experiment runner.
"""
import ast
import hashlib
import json
import sys
import types
from pathlib import Path

INPUTS=[(False,False),(False,True),(True,False),(True,True)]


def has_cycle(source):
    tree=ast.parse(source)
    funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    edges={}
    for name,fn in funcs.items():
        edges[name]={n.func.id for n in ast.walk(fn) if isinstance(n,ast.Call)
                     and isinstance(n.func,ast.Name) and n.func.id in funcs}
    # Independent iterative reachability: a node reaches itself along >=1 edge.
    for start in funcs:
        seen=set()
        stack=list(edges[start])
        while stack:
            n=stack.pop()
            if n==start:
                return True
            if n not in seen:
                seen.add(n)
                stack.extend(edges[n])
    return False


def producer(bits):
    values=[bool(bits & (1<<i)) for i in range(4)]
    return ('def produce(x,y):\n'
            f'    return ({values[3]} if y else {values[2]}) if x else '
            f'({values[1]} if y else {values[0]})\n')


def replay(psrc,csrc):
    saved=sys.modules.get('producer')
    pm=types.ModuleType('producer')
    cm=types.ModuleType('consumer')
    try:
        sys.modules['producer']=pm
        exec(compile(psrc,'producer.py','exec'),pm.__dict__)
        exec(compile(csrc,'consumer.py','exec'),cm.__dict__)
        result=[]
        for a,b in INPUTS:
            try:
                value=cm.target(a,b)
                result.append('T' if value is True else 'F' if value is False else 'NONBOOL')
            except RecursionError:
                result.append('RecursionError')
            except Exception as e:
                result.append(type(e).__name__)
        return result
    except Exception as e:
        return [f'MODULE:{type(e).__name__}']*4
    finally:
        if saved is None:
            sys.modules.pop('producer',None)
        else:
            sys.modules['producer']=saved


def audit(path):
    data=json.loads(Path(path).read_text())
    assert data['experiment']=='run374_cycle_short_circuit'
    assert len(data['records'])==data['summary']['programs']==1100
    saved=sys.getrecursionlimit()
    sys.setrecursionlimit(160)
    try:
        counts={'records':0,'observations':0,'cycles':0,'fixed_accepted_cycles':0,
                'fixed_accepted_nontotal':0,'fixed_no_dependence_counterexamples':0,
                'raw_trace_mismatches':0,'sha_mismatches':0}
        for record in data['records']:
            counts['records']+=1
            src=record['source']
            counts['sha_mismatches']+=int(hashlib.sha256(src.encode()).hexdigest()!=record['source_sha256'])
            cyc=has_cycle(src)
            counts['cycles']+=int(cyc)
            counts['fixed_accepted_cycles']+=int(cyc and record['fixed']!='UNKNOWN')
            observations=[]
            for bits in range(16):
                result=replay(producer(bits),src)
                observations.append(result)
                counts['observations']+=len(result)
            counts['raw_trace_mismatches']+=int(observations!=record['truth_tables'])
            non_total=any(v not in ('T','F') for vals in observations for v in vals)
            counts['fixed_accepted_nontotal']+=int(non_total and record['fixed']!='UNKNOWN')
            counts['fixed_no_dependence_counterexamples']+=int(
                record['fixed']=='NO_DEPENDENCE' and any(v!=observations[0] for v in observations[1:]))
        assert counts['observations']==70400
        assert counts['cycles']>0
        assert not any(counts[k] for k in ('fixed_accepted_cycles','fixed_accepted_nontotal',
                 'fixed_no_dependence_counterexamples','raw_trace_mismatches','sha_mismatches'))
        return counts
    finally:
        sys.setrecursionlimit(saved)


if __name__=='__main__':
    result=audit(sys.argv[1] if len(sys.argv)>1 else 'run374_raw.json')
    Path('run374_independent_audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
