"""Minimal read-only Run351 cloud evidence gate; no model code execution.
Usage: python run352_cloud_gate.py ORIGINAL_ACTIONS_ZIP PARENT_RUN351_ZIP
"""
import ast, hashlib, json, sys, zipfile

def h(b): return hashlib.sha256(b).hexdigest()
def j(z,p): return json.loads(z.read(p))
def check(cloud,parent):
    with zipfile.ZipFile(cloud) as z, zipfile.ZipFile(parent) as p:
        manifest=j(z,'SHA256_MANIFEST.json')
        assert len(manifest)==46
        for name,digest in manifest.items(): assert h(z.read(name))==digest,name
        frozen=j(z,'RUN351_FREEZE.json')
        baseline=p.read('source_httpx_baseline/_api.py')
        assert h(baseline)==frozen['source_sha256']['_api.py']
        candidates={c['id']:c for c in j(z,'candidates.json')}
        outputs={}
        for arm in ('IR','PYTHON_AST'):
            request=j(z,'request_REAL_'+arm+'.json')
            prompt=request['messages'][0]['content'].encode()
            assert h(prompt)==frozen['augmented'][arm]['prompt_sha256']
            assert h(json.dumps(request,sort_keys=True,separators=(',',':')).encode())==frozen['augmented'][arm]['request_sha256']
            raw=j(z,'raw_REAL_'+arm+'.json')
            completion=raw['choices'][0]['message']['content']
            assert completion.encode()==z.read('completion_REAL_'+arm+'.txt')
            actions=json.loads(completion)['edits']
            assert len(actions)==4 and len({a['id'] for a in actions})==4
            edits=[(candidates[a['id']]['qual'],candidates[a['id']]['old_expr'],a['new_expr']) for a in actions]
            assert sum(old!=new for _,old,new in edits)==1
            assert [(qual,old,new) for qual,old,new in edits if old!=new]==[('head','False','True')]
            stage=z.read('stages/'+arm+'/httpx/_api.py')
            assert h(stage)==j(z,'compile_REAL_'+arm+'.json')['patched_sha256']['httpx/_api.py']
            assert z.read('stages/'+arm+'/httpx/_client.py')==p.read('source_httpx_baseline/_client.py')
            cases=j(z,'oracle_'+arm+'.json')['cases']
            assert len(cases)==9
            assert all(c['passed']==(c['expected']==c['observed']) and c['error'] is None for c in cases)
            outputs[arm]={'prompt_tokens':raw['usage']['prompt_tokens'],'edits':edits,
                          'source_sha256':h(stage),'passed':[c['id'] for c in cases if c['passed']]}
        assert outputs['IR']['source_sha256']==outputs['PYTHON_AST']['source_sha256']
        assert outputs['IR']['passed']==outputs['PYTHON_AST']['passed']
        assert outputs['PYTHON_AST']['prompt_tokens']-outputs['IR']['prompt_tokens']==279
        return outputs
if __name__=='__main__': print(json.dumps(check(sys.argv[1],sys.argv[2]),indent=2,sort_keys=True))
