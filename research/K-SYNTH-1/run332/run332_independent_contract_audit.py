"""Read-only, independent Run332 frozen-request/source/gate contract auditor.

Does not import either primary runner or the shared editor.
"""
import ast,hashlib,json,re,sys
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()

def main(root,out):
    meta=json.loads((out/'freeze.json').read_text())
    rows=json.loads((out/'candidates.json').read_text())
    gates=json.loads((out/'gate_candidates.json').read_text())
    assert meta['base']=='891d865044d27c229278f0fa20d84ba4007cb289'
    assert len(rows)==31 and len(gates)==2
    counts={'KW_ONLY':0,'POSITIONAL':0}; checked=[]
    for c in rows:
        data=(root/c['path']).read_bytes()
        assert sha(data)==meta['source_sha256'][c['path']]==c['source_sha256']
        tree=ast.parse(data.decode())
        qual=c['qual'].split('.')
        nodes=tree.body
        for name in qual:
            matches=[n for n in nodes if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name]
            assert len(matches)==1,(c['id'],qual)
            node=matches[0];nodes=node.body
        assert isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))
        arg=node.args
        if c['param'] in [x.arg for x in arg.kwonlyargs]:
            i=[x.arg for x in arg.kwonlyargs].index(c['param'])
            value=arg.kw_defaults[i];slot='KW_ONLY'
        else:
            pos=arg.posonlyargs+arg.args
            i=[x.arg for x in pos].index(c['param'])
            value=arg.defaults[i-(len(pos)-len(arg.defaults))];slot='POSITIONAL'
        assert isinstance(value,ast.Constant) and type(value.value) is bool
        assert str(value.value)==c['old_expr'] and slot==c['slot']
        counts[slot]+=1;checked.append(c['id'])
    assert counts=={'KW_ONLY':29,'POSITIONAL':2}
    for kind in ['GATE','REAL']:
        for arm in ['IR','PYTHON_AST']:
            name=f'{kind}_{arm}'
            request_path=out/f'request_{name}.json';req=json.loads(request_path.read_text())
            record=meta['requests'][name]
            assert sha(request_path.read_bytes())==record['request_sha256']
            prompt=req['messages'][0]['content']
            assert sha(prompt.encode())==record['prompt_sha256']
            assert req['seed']==3322026 and req['temperature']==0 and req['max_tokens']==768
            lines=[line for line in prompt.splitlines() if line.startswith('IR_DEFAULT ') or line.startswith('PY_AST_DEFAULT ')]
            target=gates if kind=='GATE' else rows
            assert len(lines)==len(target)
            for c,line in zip(target,lines):
                assert line.split()[1]==c['id'] and c['source_sha256'] not in line
                assert f"old={c['old_expr']} sha={c['old_sha256']}" in line
                assert 'CALLEE=UNKNOWN RUNTIME_EFFECT=UNKNOWN' in line
                if arm=='IR':assert f"SLOT={c['slot']}" in line
                else:
                    slot='ast.arguments.kw_defaults' if c['slot']=='KW_ONLY' else 'ast.arguments.defaults'
                    assert f'SLOT={slot}' in line
    assert len(set(checked))==31
    return {'passed':True,'source_candidate_count':len(rows),'slots':counts,
            'request_count':4,'gate_count':2,'candidate_ids_sha256':sha(json.dumps(checked).encode()),
            'original_source_sha256':meta['source_sha256'],
            'notes':'independent static source and request audit; no model inference'}

if __name__=='__main__':
    print(json.dumps(main(Path(sys.argv[1]),Path(sys.argv[2])),indent=2,sort_keys=True))
