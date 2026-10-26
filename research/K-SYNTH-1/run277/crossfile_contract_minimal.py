#!/usr/bin/env python3
"""Bounded, fail-closed cross-file declaration/use witness, not Python soundness."""
import ast,hashlib,json,pathlib,argparse
def sha(b):return hashlib.sha256(b).hexdigest()
def inspect(m,r):
    mt,rt=ast.parse(m),ast.parse(r)
    state=next(x for x in mt.body if isinstance(x,ast.ClassDef) and x.name=='State')
    part=next(x for x in rt.body if isinstance(x,ast.ClassDef) and x.name=='RulePart')
    fields={x.target.id for x in part.body if isinstance(x,ast.AnnAssign) and isinstance(x.target,ast.Name)}
    dynamic=next(x for x in state.body if isinstance(x,ast.AnnAssign) and isinstance(x.target,ast.Name) and x.target.id=='dynamic')
    typed='Tuple[RulePart,' in ast.unparse(dynamic.annotation)
    imported=any(isinstance(x,ast.ImportFrom) and x.level==1 and x.module=='rules' and any(y.name=='RulePart' for y in x.names) for x in mt.body)
    parents={c:p for p in ast.walk(mt) for c in ast.iter_child_nodes(p)}
    sites=[]
    for loop in ast.walk(mt):
        if not isinstance(loop,ast.For) or not isinstance(loop.iter,ast.Attribute) or loop.iter.attr!='dynamic' or not isinstance(loop.iter.value,ast.Name):continue
        if not isinstance(loop.target,ast.Tuple) or not isinstance(loop.target.elts[0],ast.Name):continue
        variable=loop.target.elts[0].id; statevar=loop.iter.value.id
        owner=parents.get(loop)
        while owner is not None and not isinstance(owner,(ast.FunctionDef,ast.AsyncFunctionDef)):owner=parents.get(owner)
        scoped=bool(owner and any(a.arg==statevar and isinstance(a.annotation,ast.Name) and a.annotation.id=='State' for a in owner.args.args))
        rebound=any(isinstance(n,ast.Name) and n.id==variable and isinstance(n.ctx,(ast.Store,ast.Del)) for s in loop.body for n in ast.walk(s))
        for stmt in loop.body:
            for n in ast.walk(stmt):
                if isinstance(n,ast.Attribute) and isinstance(n.ctx,ast.Load) and isinstance(n.value,ast.Name) and n.value.id==variable:
                    status=('DECLARED' if n.attr in fields else 'UNDECLARED_RUNTIME_UNKNOWN') if typed and imported and scoped and not rebound else 'UNKNOWN'
                    sites.append({'line':n.lineno,'attribute':n.attr,'status':status,'scope':owner.name if owner else 'UNKNOWN'})
    return {'matcher_sha256':sha(m),'rules_sha256':sha(r),'declared_fields':sorted(fields),'sites':sites}
p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--ref',required=True);p.add_argument('--out',required=True);a=p.parse_args()
path='src/werkzeug/routing/'
s={v:{f:(pathlib.Path(root)/path/f).read_bytes() for f in ('matcher.py','rules.py')} for v,root in [('base',a.base),('ref',a.ref)]}
variants={'base':('base','base'),'matcher_only':('ref','base'),'rules_only':('base','ref'),'full':('ref','ref')}
out={k:inspect(s[x]['matcher.py'],s[y]['rules.py']) for k,(x,y) in variants.items()}
def has(k,status):return any(n['attribute']=='suffixed' and n['status']==status for n in out[k]['sites'])
assert has('matcher_only','UNDECLARED_RUNTIME_UNKNOWN')
assert has('full','DECLARED')
assert not any(n['attribute']=='suffixed' for n in out['base']['sites'])
assert not any(n['attribute']=='suffixed' for n in out['rules_only']['sites'])
pathlib.Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
