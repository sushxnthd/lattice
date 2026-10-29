"""K-SYNTH-1 Run348: assumption-scoped, branch-aware reaching local definitions.

This is deliberately a finite CPython 3.13 lexical/dataflow analysis, NOT a
runtime-callee or cross-file semantic guarantee. Unknowns are first-class.
Only straightline/if/return/expr/pass and simple Name assignments are admitted.
"""
from __future__ import annotations
import ast, dis, hashlib, json, types
from typing import Any

VERSION='K-SYNTH-1/run348/branch-reaching-v1'
UNBOUND=('UNBOUND',-1,-1)
EXCLUDE=(ast.NamedExpr,ast.Lambda,ast.ListComp,ast.SetComp,ast.DictComp,
         ast.GeneratorExp,ast.Yield,ast.YieldFrom,ast.Global,
         ast.Nonlocal,ast.Delete,ast.AugAssign,ast.AnnAssign,ast.Match,
         ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def source_code_objects(code):
    for v in code.co_consts:
        if isinstance(v,types.CodeType):
            yield v
            yield from source_code_objects(v)

def valid_stmt(s):
    if isinstance(s,ast.If):
        return (not any(isinstance(n,EXCLUDE) for n in ast.walk(s.test))
                and all(valid_stmt(t) for t in s.body+s.orelse))
    if isinstance(s,ast.Assign):
        return (len(s.targets)==1 and isinstance(s.targets[0],ast.Name)
                and not any(isinstance(n,EXCLUDE) for n in ast.walk(s.value)))
    if isinstance(s,(ast.Return,ast.Expr)):
        v=s.value
        return v is None or not any(isinstance(n,EXCLUDE) for n in ast.walk(v))
    return isinstance(s,ast.Pass)

def read_nodes(expr):
    if expr is None: return []
    return sorted((n for n in ast.walk(expr) if isinstance(n,ast.Name)
                   and isinstance(n.ctx,ast.Load)),key=lambda n:(n.lineno,n.col_offset,n.id))

def params(f):
    a=f.args
    return [x.arg for x in a.posonlyargs+a.args+a.kwonlyargs]+([a.vararg.arg] if a.vararg else [])+([a.kwarg.arg] if a.kwarg else [])

def analyze(path,src):
    tree=ast.parse(src,filename=path)
    code=compile(src,path,'exec',dont_inherit=True)
    cs=list(source_code_objects(code))
    out={'version':VERSION,'path':path,'source_sha256':sha(src.encode()),'functions_total':0,
         'functions_eligible':0,'certificates':[],'unknowns':[],'calls':[]}
    for f in ast.walk(tree):
        if not isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef)): continue
        out['functions_total']+=1
        fid=f'{f.name}@{f.lineno}'
        if not all(valid_stmt(s) for s in f.body):
            out['unknowns'].append({'function':fid,'reason':'UNSUPPORTED_CONTROL_OR_SCOPE'})
            continue
        matches=[c for c in cs if c.co_name==f.name and c.co_firstlineno in
                 (f.lineno,*[d.lineno for d in f.decorator_list])]
        if len(matches)!=1:
            out['unknowns'].append({'function':fid,'reason':'AMBIGUOUS_CODE_OBJECT'})
            continue
        instructions=list(dis.get_instructions(matches[0],show_caches=False))
        out['functions_eligible']+=1
        init={n:frozenset({('PARAM',f.lineno,-1)}) for n in params(f)}
        def record_expr(expr, state):
            if expr is None: return
            for c in ast.walk(expr):
                if isinstance(c,ast.Call):
                    out['calls'].append({'function':fid,'location':[c.lineno,c.col_offset],
                                         'callee_syntax':ast.unparse(c.func),'runtime_target':'UNKNOWN'})
            for n in read_nodes(expr):
                defs=state.get(n.id,frozenset({UNBOUND}))
                loads=[i for i in instructions if i.opname in ('LOAD_FAST','LOAD_FAST_CHECK')
                       and i.argval==n.id and i.positions and i.positions.lineno==n.lineno
                       and i.positions.col_offset==n.col_offset]
                if len(loads)!=1:
                    out['unknowns'].append({'function':fid,'read':[n.lineno,n.col_offset],
                                            'name':n.id,'reason':'BYTECODE_LOAD_UNVERIFIED'})
                    continue
                if UNBOUND in defs:
                    out['unknowns'].append({'function':fid,'read':[n.lineno,n.col_offset],
                                            'name':n.id,'reason':'POSSIBLY_UNBOUND',
                                            'reaching':[list(d) for d in sorted(defs)]})
                    continue
                stores_valid=True
                for kind,line,col in defs:
                    if kind=='PARAM': continue
                    stores=[i for i in instructions if i.opname=='STORE_FAST' and i.argval==n.id
                            and i.positions and i.positions.lineno==line
                            and i.positions.col_offset==col]
                    if len(stores)!=1:
                        stores_valid=False
                if not stores_valid:
                    out['unknowns'].append({'function':fid,'read':[n.lineno,n.col_offset],
                                            'name':n.id,'reason':'BYTECODE_STORE_UNVERIFIED'})
                    continue
                out['certificates'].append({'function':fid,'read':[n.lineno,n.col_offset],
                     'name':n.id,'reaching':[list(d) for d in sorted(defs)],
                     'modality':'MUST_UNIQUE_ON_REACH' if len(defs)==1 else 'MAY_SET_ON_REACH',
                     'assumptions':['standard_cpython_local_semantics',
                       'no_external_frame_local_mutation','original_function_body_executed'],
                     'runtime_callee':'UNKNOWN','load_opcode':loads[0].opname})
        def merge(a,b):
            if a is None: return b
            if b is None: return a
            return {k:a.get(k,frozenset({UNBOUND}))|b.get(k,frozenset({UNBOUND}))
                    for k in a.keys()|b.keys()}
        def walk(stmts,st):
            if st is None: return None
            for s in stmts:
                if st is None: break
                if isinstance(s,ast.If):
                    record_expr(s.test,st)
                    st=merge(walk(s.body,dict(st)),walk(s.orelse,dict(st)))
                elif isinstance(s,ast.Assign):
                    record_expr(s.value,st)
                    target=s.targets[0]
                    st=dict(st)
                    st[target.id]=frozenset({('ASSIGN',target.lineno,target.col_offset)})
                elif isinstance(s,ast.Expr): record_expr(s.value,st)
                elif isinstance(s,ast.Return):
                    record_expr(s.value,st)
                    st=None
            return st
        walk(f.body,init)
    out['certificates'].sort(key=lambda c:(c['function'],c['read'],c['name']))
    out['unknowns'].sort(key=lambda c:(c['function'],c.get('read',[-1,-1]),c['reason']))
    out['calls'].sort(key=lambda c:(c['function'],c['location']))
    return out

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('sources',nargs='+');p.add_argument('--out',required=True)
    a=p.parse_args()
    data=[analyze(x.split('/')[-1],open(x,encoding='utf-8').read()) for x in a.sources]
    with open(a.out,'w') as f:json.dump(data,f,indent=2,sort_keys=True)
    print(json.dumps([{k:v for k,v in r.items() if k in ('path','functions_total','functions_eligible')}
       |{'must':sum(c['modality']=='MUST_UNIQUE_ON_REACH' for c in r['certificates']),
          'may':sum(c['modality']=='MAY_SET_ON_REACH' for c in r['certificates']),
          'unknowns':len(r['unknowns'])} for r in data],indent=2))
