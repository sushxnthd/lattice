#!/usr/bin/env python3
"""Freeze model requests prospectively and test shared compiler before inference."""
import hashlib,json,sys,tempfile
from pathlib import Path
import run301_shared_adapter as adapter
import run295_compiler_v2 as compiler
h=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)

def main(root,out):
    freeze=json.loads((out/'freeze.json').read_text())
    assert len(freeze['arms'])==2 and {a['arm'] for a in freeze['arms']}=={'IR','PYTHON_AST'}
    for entry in freeze['arms']:
        p=out/entry['request_file'];req=json.loads(p.read_text())
        assert req['seed']==299001 and req['max_tokens']==768
        prompt=req['messages'][0]['content']
        marker='SOURCE_CONTEXT_BEGIN'
        assert prompt.count(marker)==1
        prompt=prompt.replace(marker,'One optional outer JSON Markdown fence is permitted. No extra text.\n'+marker)
        req['messages'][0]['content']=prompt
        req['seed']=301001
        raw=(canon(req)+'\n').encode()
        p.write_bytes(raw)
        entry['request_sha256']=h(raw)
        entry['prompt_sha256']=h(prompt.encode())
        entry['prompt_characters']=len(prompt)
    freeze['protocol']='RUN301_PROSPECTIVE_SHARED_ADAPTER_V1'
    freeze['seed']=301001
    freeze['adapter_contract']='exact old/new preimage; one optional outer JSON fence; same Run295 compiler both arms'
    freeze['original_run299_immutable']=True
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
    (out/'run301_freeze.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
    old='def maybe_read_from_IDLE_client(buf):\n'
    new=old+'    # inert prospective paired contract marker\n'
    raw=canon({'edits':[{'path':'h11/_readers.py','old':old,'new':new}]})
    results=[]
    with tempfile.TemporaryDirectory() as tmp:
        for label,text in [('bare',raw),('fenced','```json\n'+raw+'\n```')]:
            ir,py=adapter.to_views(text,root)
            a=compiler.compile_to_isolated_stage(root,ir,Path(tmp)/('ir-'+label))
            b=compiler.compile_to_isolated_stage(root,py,Path(tmp)/('py-'+label))
            assert a['canonical_sha256']==b['canonical_sha256']
            assert a['files']==b['files']
            results.append({'case':label,'accepted':True,'canonical_sha256':a['canonical_sha256']})
    try:
        adapter.to_views(canon({'edits':[{'path':'../bad.py','old':old,'new':new}]}),root)
    except compiler.Rejected as e:assert e.code=='EDIT_AUTHORITY'
    else:raise AssertionError('negative contract gate failed')
    (out/'run301_contract_gate.json').write_text(json.dumps({'passed':True,'positive':2,'negative':1,'results':results},indent=2,sort_keys=True)+'\n')
    print(canon({'freeze_sha256':h((out/'freeze.json').read_bytes()),'contract_gate':'PASS','arms':freeze['arms']}))

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
