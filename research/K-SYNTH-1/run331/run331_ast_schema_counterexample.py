#!/usr/bin/env python3
"""Run331 independent AST-field check. Input: extracted ORIGINAL Run330 cloud ZIP directory.
Static AST parsing only; never imports or executes staged/model code.
"""
import ast,hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1])
candidates=json.loads((root/'candidates.json').read_text())
freeze=json.loads((root/'freeze.json').read_text())
prompt=json.loads((root/'request_REAL_PYTHON_AST.json').read_text())['messages'][0]['content']
def qualified(t):
    out={}
    def visit(body,prefix=''):
        for n in body:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                out[prefix+n.name]=n
            if isinstance(n,ast.ClassDef):visit(n.body,prefix+n.name+'.')
    visit(t.body)
    return out
results=[]
for path in sorted(set(c['path'] for c in candidates)):
    source=(root/'stages/IR'/path).read_text()
    if path=='httpx/_api.py':
        n=qualified(ast.parse(source))['head']
        d=next(d for a,d in zip(n.args.kwonlyargs,n.args.kw_defaults) if a.arg=='allow_redirects')
        lines=source.splitlines(keepends=True)
        line=lines[d.lineno-1]
        assert line[d.col_offset:d.end_col_offset]=='True'
        lines[d.lineno-1]=line[:d.col_offset]+'False'+line[d.end_col_offset:]
        source=''.join(lines)
    assert hashlib.sha256(source.encode()).hexdigest()==freeze['source_sha256'][path]
    funcs=qualified(ast.parse(source))
    for c in (c for c in candidates if c['path']==path):
        f=funcs[c['qual']]
        pos={a.arg:ast.unparse(d) for a,d in zip(f.args.posonlyargs+f.args.args,[None]*(len(f.args.posonlyargs)+len(f.args.args)-len(f.args.defaults))+f.args.defaults) if d is not None}
        kw={a.arg:ast.unparse(d) for a,d in zip(f.args.kwonlyargs,f.args.kw_defaults) if d is not None}
        actual='kw_defaults' if c['param'] in kw else 'defaults'
        assert (kw if actual=='kw_defaults' else pos)[c['param']]==c['old_expr']
        line=[s for s in prompt.splitlines() if s.startswith('PY_AST_DEFAULT '+c['id']+' ')]
        assert len(line)==1
        declared='kw_defaults' if 'ast.FunctionDef.args.kw_defaults[' in line[0] else 'defaults'
        results.append(dict(id=c['id'],qual=c['qual'],actual=actual,declared=declared,mismatch=actual!=declared))
assert len(results)==31
assert sum(r['mismatch'] for r in results)==29
print(json.dumps({'total':31,'mismatches':29,'rows':results},indent=2))
