#!/usr/bin/env python3
"""Prospective Run333 format-binding reformulation. Not a Run332 rescue.
Freezes two paired gate prompts before inference; no reference source access.
"""
import hashlib, json, sys
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(obj):return (json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()

def freeze(root):
    rows=json.loads((root/'gate_candidates.json').read_text())
    assert len(rows)==2 and {r['qual'] for r in rows}=={'probe_a','probe_b'}
    assert len({r['id'] for r in rows})==2
    assert all(r['id'].startswith('D') and r['id']!=r['qual'] for r in rows)
    original={}
    extra=('\nOUTPUT-ID BINDING CONTRACT (not an example solution):\n'
           'The `id` field MUST be the exact opaque ID in the authorized table, NOT the function name.\n'
           'Map the function name in the issue to its authorized ID as follows:\n')
    extra+=''.join(f'function {r["qual"]} -> JSON id {r["id"]}\n' for r in sorted(rows,key=lambda x:x['qual']))
    extra+='Any output with id `probe_a` or `probe_b` is INVALID, even if the new values are correct.\n'
    for arm in ('IR','PYTHON_AST'):
        p=root/f'request_GATE_{arm}.json'
        raw=p.read_bytes();original[arm]=sha(raw)
        obj=json.loads(raw)
        assert len(obj['messages'])==1 and obj['messages'][0]['role']=='user'
        assert 'OUTPUT-ID BINDING CONTRACT' not in obj['messages'][0]['content']
        obj['messages'][0]['content']+=extra
        p.write_bytes(canonical(obj))
    report={'schema':'run333-explicit-id-gate-v1','classification':'post-Run332 exploratory reformulation',
            'changed_fields':['gate prompt output-id binding only'],
            'original_request_sha256':original,
            'reformulated_request_sha256':{arm:sha((root/f'request_GATE_{arm}.json').read_bytes()) for arm in ('IR','PYTHON_AST')},
            'gate_candidate_sha256':sha((root/'gate_candidates.json').read_bytes()),
            'real_request_sha256':{arm:sha((root/f'request_REAL_{arm}.json').read_bytes()) for arm in ('IR','PYTHON_AST')},
            'source_issue_edit_authority_compiler_oracle_unchanged':True}
    (root/'run333_freeze.json').write_bytes(canonical(report))
    print(json.dumps(report,sort_keys=True))

def audit(root):
    rows=json.loads((root/'gate_candidates.json').read_text())
    report=json.loads((root/'run333_freeze.json').read_text())
    assert sha((root/'gate_candidates.json').read_bytes())==report['gate_candidate_sha256']
    for arm in ('IR','PYTHON_AST'):
        p=root/f'request_GATE_{arm}.json';raw=p.read_bytes()
        assert sha(raw)==report['reformulated_request_sha256'][arm]
        prompt=json.loads(raw)['messages'][0]['content']
        assert prompt.count('OUTPUT-ID BINDING CONTRACT')==1
        assert all(f'function {r["qual"]} -> JSON id {r["id"]}' in prompt for r in rows)
        assert sha((root/f'request_REAL_{arm}.json').read_bytes())==report['real_request_sha256'][arm]
    assert report['classification']=='post-Run332 exploratory reformulation'
    print(json.dumps({'audited':True,'gates':2,'real_requests_unchanged':2},sort_keys=True))

if __name__=='__main__':
    cmd,root=sys.argv[1],Path(sys.argv[2])
    {'freeze':freeze,'audit':audit}[cmd](root)
