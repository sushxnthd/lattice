#!/usr/bin/env python3
"""Prospective Run335 minimal-delta reformulation, paired and reference-blind."""
import hashlib,json,sys
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
SUFFIX=(
 '\nMINIMAL-DELTA OUTPUT CONTRACT (applies equally to both representations):\n'
 'Return only actual changes: never output an edit whose new_expr is the same as its listed old value.\n'
 'Do not enumerate all authorized candidates. Select only edits justified by the issue.\n'
 'Use at most FOUR edit objects. Return syntactically complete JSON within the token budget.\n'
 'Use the exact opaque candidate IDs. Do not edit any function body.\n'
)
def freeze(root):
    before={};after={}
    for arm in ('IR','PYTHON_AST'):
        path=root/f'request_REAL_{arm}.json'
        raw=path.read_bytes();before[arm]=sha(raw)
        obj=json.loads(raw)
        assert len(obj['messages'])==1 and obj['messages'][0]['role']=='user'
        assert obj['max_tokens']==768
        assert 'MINIMAL-DELTA OUTPUT CONTRACT' not in obj['messages'][0]['content']
        obj['messages'][0]['content']+=SUFFIX
        path.write_bytes(canon(obj))
        after[arm]=sha(path.read_bytes())
    report={'schema':'run335-prospective-minimal-delta-v1',
        'classification':'post-Run333 exploratory intervention, not original Run333 rescore',
        'source_and_edit_authority_unchanged':True,'shared_compiler_oracle_unchanged':True,
        'gate_requests_unchanged':True,'intervention_identical_suffix':True,
        'suffix_sha256':sha(SUFFIX.encode()),'suffix_characters':len(SUFFIX),
        'before_real_request_sha256':before,'after_real_request_sha256':after,
        'gate_request_sha256':{arm:sha((root/f'request_GATE_{arm}.json').read_bytes()) for arm in ('IR','PYTHON_AST')},
        'candidate_sha256':sha((root/'candidates.json').read_bytes())}
    (root/'run335_freeze.json').write_bytes(canon(report))
    return report
def audit(root):
    d=json.loads((root/'run335_freeze.json').read_text())
    assert d['schema']=='run335-prospective-minimal-delta-v1'
    assert d['suffix_sha256']==sha(SUFFIX.encode())
    assert d['suffix_characters']==len(SUFFIX)
    assert d['candidate_sha256']==sha((root/'candidates.json').read_bytes())
    prompts={}
    for arm in ('IR','PYTHON_AST'):
        assert d['gate_request_sha256'][arm]==sha((root/f'request_GATE_{arm}.json').read_bytes())
        path=root/f'request_REAL_{arm}.json'
        assert d['after_real_request_sha256'][arm]==sha(path.read_bytes())
        obj=json.loads(path.read_bytes());p=obj['messages'][0]['content']
        assert p.endswith(SUFFIX) and p.count('MINIMAL-DELTA OUTPUT CONTRACT')==1
        assert obj['max_tokens']==768
        prompts[arm]=p
    assert prompts['IR'].split('MINIMAL-DELTA OUTPUT CONTRACT')[1]==prompts['PYTHON_AST'].split('MINIMAL-DELTA OUTPUT CONTRACT')[1]
    rows=json.loads((root/'candidates.json').read_text())
    for p in prompts.values():
        assert all(r['id'] in p for r in rows)
    return {'audited':True,'arms':2,'candidate_count':len(rows),'suffix_identical':True,'frozen':True,'source_reference_not_accessed':True}
if __name__=='__main__':
    cmd,root=sys.argv[1],Path(sys.argv[2])
    print(json.dumps({'freeze':freeze,'audit':audit}[cmd](root),sort_keys=True,indent=2))
