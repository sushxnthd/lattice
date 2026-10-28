"""Prospectively frozen 512-case correlated fixture experiment, seed 321028."""
from __future__ import annotations
import ast, json, random, hashlib
from pathlib import Path
from run315_multifile_compiler import PatchRejected, node_digest
from run320_hardened_compiler import Action, compile_structural
from run321_ast_guard import compile_ast_congruent, expected_tree

SEED=321028
N=64
OUT=Path(__file__).resolve().parent
FAMILIES=('multiply','addition','boolean','conditional','inline_comment','unicode','crlf','nested_call')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def make_case(family: str, j: int):
    value=100+j
    expressions={
      'multiply': f'result = 3 * {value}',
      'addition': f'result = 3 + {value}',
      'boolean': f'result = True and {value}',
      'conditional': f'result = {value} if True else -1',
      'inline_comment': f'result = {value} + 2 # original comment',
      'unicode': f'π = {value}\n    result = π + 3',
      'crlf': f'result = 3 * {value}',
      'nested_call': f'result = max(0, {value}) + 1',
    }
    source=f'def probe():\n    {expressions[family]}\n    return result\n'
    if family=='crlf':source=source.replace('\n','\r\n')
    data=source.encode('utf-8')
    tree=ast.parse(source)
    hits=[n for n in ast.walk(tree) if isinstance(n,ast.Constant) and type(n.value) is int and n.value==value]
    assert len(hits)==1
    target=hits[0]
    choices=(str(value+5),'1 + 2','1 #','1 if True else 2')
    replacement=choices[j%4]
    action=Action('pkg/repair.py',sha(data),node_digest(target),type(target).__name__,target.lineno,target.col_offset,target.end_lineno,target.end_col_offset,'replace_expr',replacement)
    return data, action

def main():
    rng=random.Random(SEED)
    cases=[(fam,j) for fam in FAMILIES for j in range(N)]
    rng.shuffle(cases)
    records=[]
    for i,(family,j) in enumerate(cases):
        data,action=make_case(family,j)
        sources={action.path:data}
        expected=expected_tree(data,action)
        expected_dump=ast.dump(expected,include_attributes=False)
        record={'case':i,'family':family,'j':j,'source':data.decode('utf-8'),'source_sha256':sha(data),
                'replacement':action.replacement,'action':vars(action),'expected_ast_dump':expected_dump}
        try:
            original=compile_structural(sources,[action],allowed_paths=frozenset(sources))
            patch=original[action.path]
            actual_dump=ast.dump(ast.parse(patch.decode('utf-8')),include_attributes=False)
            record.update(original_status='accepted',original_patch=patch.decode('utf-8'),original_patch_sha256=sha(patch),
                          original_ast_dump=actual_dump,original_congruent=(actual_dump==expected_dump))
        except (PatchRejected,SyntaxError,ValueError) as exc:
            record.update(original_status='rejected',original_error=f'{type(exc).__name__}: {exc}',original_congruent=None)
        try:
            guarded=compile_ast_congruent(sources,[action],allowed_paths=frozenset(sources))
            patch=guarded[action.path]
            record.update(guard_status='accepted',guard_patch=patch.decode('utf-8'),guard_patch_sha256=sha(patch))
        except (PatchRejected,SyntaxError,ValueError) as exc:
            record.update(guard_status='rejected',guard_error=f'{type(exc).__name__}: {exc}')
        records.append(record)
    p=OUT/'run321_primary_traces.jsonl'
    p.write_text(''.join(json.dumps(x,sort_keys=True,ensure_ascii=False)+'\n' for x in records),encoding='utf-8')
    summary={
      'protocol_commit':'9d5fba4fc090c55b28925c74c52fdb7df9754dd7',
      'seed':SEED,'n':len(records),
      'original_accepted':sum(x['original_status']=='accepted' for x in records),
      'original_ast_mismatch':sum(x['original_congruent'] is False for x in records),
      'guard_accepted':sum(x['guard_status']=='accepted' for x in records),
      'guard_accepted_mismatch':sum(x['guard_status']=='accepted' and x['original_congruent'] is not True for x in records),
      'guard_missed_original_mismatch':sum(x['original_congruent'] is False and x['guard_status']!='rejected' for x in records),
      'guard_rejected_safe_original':sum(x['original_congruent'] is True and x['guard_status']=='rejected' for x in records),
      'per_family':{fam:{'original_accepted':sum(x['family']==fam and x['original_status']=='accepted' for x in records),
                         'original_mismatch':sum(x['family']==fam and x['original_congruent'] is False for x in records),
                         'guard_accepted':sum(x['family']==fam and x['guard_status']=='accepted' for x in records)} for fam in FAMILIES},
      'traces_sha256':sha(p.read_bytes())}
    (OUT/'run321_primary_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))
    assert summary['guard_accepted_mismatch']==0
    assert summary['guard_missed_original_mismatch']==0
    assert summary['guard_accepted']>=128

if __name__=='__main__':main()
