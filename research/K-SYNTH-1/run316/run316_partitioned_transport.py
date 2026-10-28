"""Postfreeze transport-only partition: execute frozen fixture/compiler/oracle unchanged."""
import json,sys
from pathlib import Path
from hashlib import sha256
from run316_structural_experiment import fixture,oracle
from run316_structural_compiler import compile_structural
start=int(sys.argv[1]);end=int(sys.argv[2]);traces=[]
for i in range(start,end):
    src,actions,expected=fixture(i)
    out=compile_structural(src,actions,allowed_paths=frozenset(src))
    assert out==expected
    oracle(out,i)
    traces.append({'case':i,'source_hashes':{p:sha256(b).hexdigest() for p,b in src.items()},
                   'output_hashes':{p:sha256(b).hexdigest() for p,b in out.items()},
                   'functional':'PASS'})
Path(f'structural_part_{start:03d}_{end:03d}.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in traces))
print(json.dumps({'start':start,'end':end,'passed':len(traces)}))
