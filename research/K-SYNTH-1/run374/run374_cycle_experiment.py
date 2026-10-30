#!/usr/bin/env python3
"""Deterministic exhaustive grammar audit; executes only self-authored synthetic code."""
import hashlib
import itertools
import json
import sys
import types
from pathlib import Path
from run374_portable_certificate import certificate as fixed
from prior.run373_portable_certificate import certificate as old

INPUTS = ((False,False),(False,True),(True,False),(True,True))


def producer(bits):
    b = [('True' if bits >> i & 1 else 'False') for i in range(4)]
    return f'def produce(x,y):\n    return ({b[3]} if y else {b[2]}) if x else ({b[1]} if y else {b[0]})\n'


def expressions(names):
    # Deterministic finite grammar, including source-order-sensitive cycles.
    others = [n for n in names if n != 'target']
    return ['True','False','x and y','p(x,y)','target(x,y)',
            'p(x,y) or target(x,y)','target(x,y) or p(x,y)',
            'p(x,y) and target(x,y)',
            f'{others[0]}(x,y)',f'p(x,y) or {others[0]}(x,y)']


def consumers():
    for names in [('target','f'),('target','f','g')]:
        exprs=expressions(names)
        for indices in itertools.product(range(len(exprs)),repeat=len(names)):
            lines=['from producer import produce as p']
            for name,index in zip(names,indices):
                lines += [f'def {name}(x,y):',f'    return {exprs[index]}']
            yield '-'.join(map(str,indices)), '\n'.join(lines)+'\n'


def run(p_src,c_src):
    original=sys.modules.get('producer')
    pm=types.ModuleType('producer')
    cm=types.ModuleType('consumer')
    try:
        sys.modules['producer']=pm
        exec(compile(p_src,'producer.py','exec'),pm.__dict__)
        exec(compile(c_src,'consumer.py','exec'),cm.__dict__)
        outcomes=[]
        for x,y in INPUTS:
            try:
                result=cm.target(x,y)
                outcomes.append('T' if result is True else 'F' if result is False else 'NONBOOL')
            except RecursionError:
                outcomes.append('RecursionError')
            except Exception as e:
                outcomes.append(type(e).__name__)
        return outcomes
    except Exception as e:
        return [f'MODULE:{type(e).__name__}']*4
    finally:
        if original is None:
            sys.modules.pop('producer',None)
        else:
            sys.modules['producer']=original


def main():
    oldlimit=sys.getrecursionlimit()
    sys.setrecursionlimit(160)
    try:
        ps=[producer(i) for i in range(16)]
        records=[]
        s={'programs':0,'functional_observations':0,'old':{'NO_DEPENDENCE':0,'MAY_DEPEND':0,'UNKNOWN':0},
           'fixed':{'NO_DEPENDENCE':0,'MAY_DEPEND':0,'UNKNOWN':0},
           'old_accepted_nontotal':0,'fixed_accepted_nontotal':0,
           'old_accepted_recursion':0,'fixed_false_noninterference':0,
           'old_may_to_unknown':0,'old_no_to_unknown':0}
        for i,(label,c_src) in enumerate(consumers()):
            old_v=old(ps[0],c_src)
            fixed_v=fixed(ps[0],c_src)
            obs=[run(p,c_src) for p in ps]
            nontotal=any(v not in ('T','F') for vals in obs for v in vals)
            recursion=any('RecursionError' in vals for vals in obs)
            false_no=(fixed_v=='NO_DEPENDENCE' and any(vals!=obs[0] for vals in obs[1:]))
            s['programs']+=1
            s['functional_observations']+=64
            s['old'][old_v]+=1
            s['fixed'][fixed_v]+=1
            s['old_accepted_nontotal']+=int(old_v!='UNKNOWN' and nontotal)
            s['fixed_accepted_nontotal']+=int(fixed_v!='UNKNOWN' and nontotal)
            s['old_accepted_recursion']+=int(old_v!='UNKNOWN' and recursion)
            s['fixed_false_noninterference']+=int(false_no)
            s['old_may_to_unknown']+=int(old_v=='MAY_DEPEND' and fixed_v=='UNKNOWN')
            s['old_no_to_unknown']+=int(old_v=='NO_DEPENDENCE' and fixed_v=='UNKNOWN')
            records.append({'index':i,'id':label,'source':c_src,
                            'source_sha256':hashlib.sha256(c_src.encode()).hexdigest(),
                            'old':old_v,'fixed':fixed_v,'nontotal':nontotal,
                            'recursion':recursion,'truth_tables':obs})
        assert s['old_accepted_recursion']>0,s
        assert s['fixed_accepted_nontotal']==0,s
        assert s['fixed_false_noninterference']==0,s
        assert s['old_may_to_unknown']>0,s
        result={'experiment':'run374_cycle_short_circuit','producer_truth_tables':16,
                'inputs_per_table':4,'expression_grammar':expressions(('target','f')),
                'summary':s,'records':records}
        Path('run374_raw.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps(s,indent=2,sort_keys=True))
    finally:
        sys.setrecursionlimit(oldlimit)


if __name__=='__main__':
    main()
