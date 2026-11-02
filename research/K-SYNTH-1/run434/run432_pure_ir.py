#!/usr/bin/env python3
"""Soundness-scoped adjacent-assignment commutation for an exact-int, pure Python fragment.

Not a general Python effect analysis, not a model benchmark, not a repair certificate.
The certificate is conditional on exact built-in int arguments, normal termination,
and no resource exhaustion. Both IR and AST action compile through one validator.
"""
from __future__ import annotations
import ast, copy, hashlib, json

class Unknown(ValueError): pass

def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def _reads(expr: ast.AST) -> set[str]:
    if isinstance(expr, ast.Constant) and type(expr.value) is int:
        return set()
    if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
        return {expr.id}
    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op,(ast.UAdd,ast.USub)):
        return _reads(expr.operand)
    if isinstance(expr, ast.BinOp) and isinstance(expr.op,(ast.Add,ast.Sub,ast.Mult)):
        return _reads(expr.left) | _reads(expr.right)
    raise Unknown('UNKNOWN_EXPRESSION_EFFECT_OR_TYPE')

def inspect(source: bytes) -> dict:
    try: root=ast.parse(source.decode('utf-8'))
    except (UnicodeError,SyntaxError) as exc: raise Unknown('UNKNOWN_PARSE') from exc
    if len(root.body)!=1 or not isinstance(root.body[0],ast.FunctionDef):
        raise Unknown('UNKNOWN_MODULE_SHAPE')
    f=root.body[0]
    if f.decorator_list or f.returns is not None or f.type_comment is not None or getattr(f,'type_params',None):
        raise Unknown('UNKNOWN_FUNCTION_METADATA')
    a=f.args
    if a.posonlyargs or a.vararg or a.kwarg or a.kwonlyargs or a.defaults or a.kw_defaults:
        raise Unknown('UNKNOWN_ARGUMENT_SHAPE')
    if not a.args or any(x.annotation is not None for x in a.args):
        raise Unknown('UNKNOWN_ARGUMENT_TYPE_OR_ANNOTATION')
    names=[x.arg for x in a.args]
    if len(set(names))!=len(names): raise Unknown('UNKNOWN_DUPLICATE_ARGUMENT')
    if len(f.body)<3 or not isinstance(f.body[-1],ast.Return) or f.body[-1].value is None:
        raise Unknown('UNKNOWN_CONTROL_SHAPE')
    defined=set(names); rows=[]
    for s in f.body[:-1]:
        if not isinstance(s,ast.Assign) or len(s.targets)!=1 or not isinstance(s.targets[0],ast.Name) or s.type_comment:
            raise Unknown('UNKNOWN_STATEMENT_EFFECT')
        w=s.targets[0].id; r=_reads(s.value)
        if not r<=defined:raise Unknown('UNKNOWN_UNBOUND_LOCAL')
        rows.append({'writes':[w],'reads':sorted(r),'line':s.lineno})
        defined.add(w)
    if not _reads(f.body[-1].value)<=defined: raise Unknown('UNKNOWN_RETURN_DEPENDENCY')
    return {'schema':'K-SYNTH-1/PURE-INT-ASSIGNMENT-SCOPE-v1',
            'source_sha256':sha(source),'function':f.name,'args':names,
            'rows':rows,'return_reads':sorted(_reads(f.body[-1].value)),
            'scope':'exact built-in int arguments; pure +,-,*; normal termination; no resource failure',
            'unknown_outside_scope':True,'general_python_soundness':False}

def eligible(table: dict) -> list[int]:
    out=[];rs=table['rows']
    for i in range(len(rs)-1):
        a,b=rs[i],rs[i+1]
        wa=set(a['writes']);wb=set(b['writes']);ra=set(a['reads']);rb=set(b['reads'])
        if not (wa & (wb|rb) or wb & (wa|ra)):out.append(i)
    return out

def transact(source: bytes, expected_sha: str, action: dict, mode: str) -> tuple[bytes,dict]:
    """Both action views use exactly the same compiler, validator and edit authority."""
    if sha(source)!=expected_sha: raise Unknown('SOURCE_HASH_MISMATCH')
    if mode not in ('ir','ast'):raise Unknown('UNKNOWN_ACTION_MODE')
    if set(action)!= {'adjacent_index','source_sha256'}:raise Unknown('UNKNOWN_ACTION_FIELDS')
    if action['source_sha256']!=expected_sha:raise Unknown('ACTION_HASH_MISMATCH')
    t=inspect(source); i=action['adjacent_index']
    if type(i) is not int or i not in eligible(t):raise Unknown('UNKNOWN_OR_DEPENDENT_SWAP')
    root=ast.parse(source.decode()); f=root.body[0]
    f.body[i],f.body[i+1]=f.body[i+1],f.body[i]
    ast.fix_missing_locations(root)
    out=(ast.unparse(root)+'\n').encode()
    inspect(out)
    receipt={'schema':'K-SYNTH-1/PURE-COMMUTE-v1','input_sha256':expected_sha,
             'output_sha256':sha(out),'adjacent_index':i,'mode':mode,
             'proof_scope':t['scope'],'reads_writes':[t['rows'][i],t['rows'][i+1]],
             'no_general_python_claim':True}
    return out,receipt

def paired(source:bytes,index:int):
    h=sha(source);action={'adjacent_index':index,'source_sha256':h}
    ir,ri=transact(source,h,action,'ir');py,rp=transact(source,h,action,'ast')
    assert ir==py and {k:v for k,v in ri.items() if k!='mode'}=={k:v for k,v in rp.items() if k!='mode'}
    return ir,ri,rp
