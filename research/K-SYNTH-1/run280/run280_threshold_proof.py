#!/usr/bin/env python3
"""Independent CPython enumeration of the exact finite Boolean-count mechanism."""
import hashlib, itertools, json, pathlib

def enumerate_trace(out:pathlib.Path, max_n:int=12):
    digest=hashlib.sha256()
    ncases=0;discordances=0;counterexample=None
    per_n=[]
    for n in range(max_n+1):
        nd=0;nv=0
        for values in itertools.product((False,True),repeat=n):
            idle=sum(values)
            for limit in range(n+2):
                baseline=(len([v for v in values])>limit)
                corrected=(sum(v for v in values)>limit)
                expected=(idle<=limit<n)
                assert (baseline != corrected)==expected
                assert not(corrected and not baseline)
                record=[n,limit,idle,int(baseline),int(corrected)]
                digest.update((json.dumps(record,separators=(',',':'))+'\n').encode())
                ncases+=1;nv+=1;discordances+=int(expected);nd+=int(expected)
                if expected and counterexample is None:counterexample={'n':n,'idle':idle,'limit':limit,'flags':values}
        per_n.append({'n':n,'cases':nv,'discordant':nd})
    nonboolean=[2,2]
    assert sum(nonboolean)>3 and len([v for v in nonboolean])<=3
    out.mkdir(parents=True,exist_ok=True)
    result={'scope':'finite stable exact Boolean vector and integer limit >=0',
            'cases':ncases,'discordances':discordances,'raw_trace_sha256':digest.hexdigest(),
            'per_n':per_n,'first_counterexample':counterexample,
            'outside_scope_counterexample':{'predicate_outputs':nonboolean,'limit':3,'baseline':False,'corrected':True},
            'claim':'For n elements, i true, and threshold k, len([p(x) for x in C])>k differs from sum(p(x) for x in C)>k iff i<=k<n, under stated purity/Boolean/stability assumptions.'}
    (out/'threshold_proof.json').write_text(json.dumps(result,indent=2,sort_keys=True,default=list)+'\n')
    return result
if __name__=='__main__':
    print(json.dumps(enumerate_trace(pathlib.Path(__file__).resolve().parent),sort_keys=True,default=list))
