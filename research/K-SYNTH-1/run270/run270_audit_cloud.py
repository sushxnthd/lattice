#!/usr/bin/env python3
"""K-SYNTH-1 Run270: independent no-execution audit of original Run268 cloud ZIP.
Usage: python run270_audit_cloud.py lattice_run268_qwen_artifact.zip
Does not execute untrusted model code or modify frozen completions.
"""
import ast, hashlib, json, sys, zipfile
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
MODEL='509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c'
ABSTAIN=b'```json\n{\n  "unable": true\n}\n```'
def main(path):
    z=zipfile.ZipFile(path); names=set(z.namelist())
    m=json.loads(z.read('SHA256_MANIFEST.json'))
    assert names==set(m)|{'SHA256_MANIFEST.json'}
    for n,sha in m.items():assert H(z.read(n))==sha,n
    rows=[]
    for task in ('flask_6096','urllib3_5071'):
        base=task+'/'
        freeze=json.loads(z.read(base+'freeze.json')); assert freeze['task']==task
        ff=[]
        for arm in freeze['arms']:
            p=base+arm['file'];raw=z.read(p);req=json.loads(raw)
            prompt=req['messages'][0]['content']
            assert H(raw)==arm['request_sha256']
            assert H(prompt.encode())==arm['prompt_sha256']
            assert req['seed']==268001 and req['temperature']==0 and req['max_tokens']==2048
            assert req['model_sha256']==freeze['model_sha256']==MODEL
            assert req['view']==arm['view'] and req['action']==arm['action']
            payload=prompt.split('FACTS_BEGIN\n',1)[1].rsplit('\nFACTS_END',1)[0]
            f=json.loads(payload) if req['view']=='graph_json' else ast.literal_eval(payload)
            ff.append(f)
            dest=base+'results/'+arm['file'].removesuffix('.json')+'/'
            completion=z.read(dest+'raw_completion.txt')
            resp=json.loads(z.read(dest+'raw_response.json'))
            meta=json.loads(z.read(dest+'result.json'))
            assert meta['request_sha256']==H(raw) and meta['model_sha256']==MODEL
            assert H(completion)==meta['completion_sha256']
            assert resp['choices'][0]['message']['content'].encode()==completion
            assert resp['usage']==meta['usage']
            assert resp['usage']['completion_tokens']==13
            assert resp['choices'][0]['finish_reason']=='stop'
            assert completion==ABSTAIN
            try:json.loads(completion)
            except json.JSONDecodeError:pass
            else:raise AssertionError('unexpected valid strict JSON')
            rows.append({'task':task,'view':req['view'],'action':req['action'],
                         'raw_sha256':H(completion),'strict_compiler':'REJECTED_INVALID_JSON',
                         'functional_oracle':'NOT_RUN_NO_ACCEPTED_PATCH',
                         'usage':resp['usage']})
        assert len(ff)==4 and all(x==ff[0] for x in ff)
        assert H(C(ff[0]).encode())==freeze['fact_sha256']
    print(json.dumps({'manifest_entries_verified':len(m),'arms':len(rows),
        'raw_identical':len(set(x['raw_sha256'] for x in rows))==1,
        'strict_accepted':0,'oracles_run':0,'rows':rows},indent=2))
if __name__=='__main__':main(sys.argv[1])
