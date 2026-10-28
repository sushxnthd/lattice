from dataclasses import replace
import json
from pathlib import Path
from run316_structural_experiment import fixture
from run316_structural_compiler import compile_structural
from run315_multifile_compiler import PatchRejected
src,actions,_=fixture(0)
bad=[
    ([replace(actions[0],source_sha256='0'*64)],frozenset(src)),
    ([replace(actions[0],path='../escape.py')],frozenset(src)),
    ([actions[0]],frozenset({'b.py','c.py'})),
    ([actions[0],actions[0]],frozenset(src)),
    ([replace(actions[1],replacement='(')],frozenset(src)),
    ([replace(actions[2],replacement='return (')],frozenset(src)),
    ([replace(actions[3],replacement='return 9')],frozenset(src)),
    ([replace(actions[0],node_sha256='0'*64)],frozenset(src)),
]
result=[]
for j,(edits,allowed) in enumerate(bad):
    try:compile_structural(src,edits,allowed_paths=allowed)
    except PatchRejected as exc:result.append({'control':j,'status':'REJECT','reason':str(exc)})
    else:result.append({'control':j,'status':'UNEXPECTED_ACCEPT'})
assert len(result)==8 and all(r['status']=='REJECT' for r in result)
Path('structural_negative_controls.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({'rejected':len(result)}))
