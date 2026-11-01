#!/usr/bin/env python3
"""Conservative, *descriptive* intra-function MAY graph for Python source.

This graph never grants edit authority or proves noninterference. Its UNKNOWN
markers are explicit, because lexical def-use alone is not sound for dynamic
Python semantics. Cross-function effects are not resolved. In particular,
UNKNOWN is a barrier to an independence claim, not evidence of an effect.
"""
from __future__ import annotations
import ast, hashlib, json
from dataclasses import dataclass, asdict

DYNAMIC=(ast.Call,ast.Attribute,ast.Subscript,ast.BinOp,ast.UnaryOp,
         ast.BoolOp,ast.Compare,ast.Await,ast.Yield,ast.YieldFrom,
         ast.JoinedStr,ast.FormattedValue,ast.NamedExpr)
CONTROL=(ast.If,ast.For,ast.AsyncFor,ast.While,ast.Try,ast.With,
         ast.AsyncWith,ast.Match,ast.TryStar)
DEFERRED=(ast.Lambda,ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)
OPAQUE=(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)


def _walk_bounded(root):
    """Walk AST but do not falsely treat deferred code as eager execution."""
    todo=[root]
    while todo:
        node=todo.pop()
        yield node
        if node is not root and isinstance(node,(*DEFERRED,*OPAQUE)):
            continue
        todo.extend(reversed(list(ast.iter_child_nodes(node))))


def _statement_nodes(fn):
    # Traverse all lexical statement blocks; do not traverse nested def bodies.
    out=[]
    def descend(stmt):
        out.append(stmt)
        if isinstance(stmt,OPAQUE):return
        for _,value in ast.iter_fields(stmt):
            if isinstance(value,list):
                for child in value:
                    if isinstance(child,ast.stmt):descend(child)
            elif isinstance(value,ast.stmt):descend(value)
    for s in fn.body:descend(s)
    return out


def _stmt_facts(stmt):
    # Own expressions only; nested control bodies have separate nodes.
    fields=[]
    for _,v in ast.iter_fields(stmt):
        if isinstance(v,ast.stmt):continue
        if isinstance(v,list):fields.extend(x for x in v if isinstance(x,ast.AST) and not isinstance(x,ast.stmt))
        elif isinstance(v,ast.AST):fields.append(v)
    seen=[]
    for f in fields:seen.extend(_walk_bounded(f))
    reads=sorted({n.id for n in seen if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)})
    writes=sorted({n.id for n in seen if isinstance(n,ast.Name) and isinstance(n.ctx,(ast.Store,ast.Del))})
    reasons=set()
    if any(isinstance(n,DYNAMIC) for n in seen):reasons.add('UNKNOWN_DYNAMIC_DISPATCH_OR_EFFECT')
    if any(isinstance(n,DEFERRED) for n in seen):reasons.add('UNKNOWN_DEFERRED_EXECUTION')
    if isinstance(stmt,CONTROL):reasons.add('UNKNOWN_CONTROL_ORDER_OR_EXCEPTION')
    if isinstance(stmt,(ast.Import,ast.ImportFrom,ast.Raise,ast.Assert,ast.Delete,ast.Global,ast.Nonlocal,*OPAQUE)):
        reasons.add('UNKNOWN_STATEMENT_EFFECT')
    if isinstance(stmt,(ast.AugAssign,ast.AnnAssign)):
        reasons.add('UNKNOWN_AUGMENTED_OR_ANNOTATED_ASSIGNMENT')
    if isinstance(stmt,(ast.Assign,ast.AugAssign,ast.AnnAssign,ast.Delete)):
        # Attribute/subscript targets, unpacking and star targets can run arbitrary code.
        targets=[]
        if isinstance(stmt,ast.Assign):targets=stmt.targets
        elif isinstance(stmt,ast.AnnAssign):targets=[stmt.target]
        elif isinstance(stmt,ast.AugAssign):targets=[stmt.target]
        else:targets=stmt.targets
        if any(not isinstance(t,ast.Name) for t in targets):
            reasons.add('UNKNOWN_COMPLEX_TARGET_OR_ALIAS')
    return reads,writes,sorted(reasons)


def build_graph(source: str, function: ast.AST, file_id: str='unknown'):
    if not isinstance(function,(ast.FunctionDef,ast.AsyncFunctionDef)):
        raise TypeError('function required')
    statements=_statement_nodes(function)
    nodes=[]
    for i,s in enumerate(statements):
        reads,writes,reasons=_stmt_facts(s)
        nodes.append({'id':i,'type':type(s).__name__,'line':s.lineno,
                      'end_line':getattr(s,'end_lineno',s.lineno),
                      'reads':reads,'writes':writes,'unknown':reasons})
    edges=[]
    for i,a in enumerate(nodes):
        for j,b in enumerate(nodes):
            if i==j:continue
            shared=sorted(set(a['writes']) & set(b['reads']))
            if shared:
                edges.append({'from':i,'to':j,'kind':'LEXICAL_MAY_DEF_USE','names':shared})
            # Opaque unknown-effect coupling: potential side effects and aliases
            # can link apparently unrelated statements, including returns.
            if i<j and (a['unknown'] or b['unknown']):
                edges.append({'from':i,'to':j,'kind':'UNKNOWN_POSSIBLE_EFFECT_COUPLING'})
    return {'schema':'K-SYNTH-1/MAY-v1','file_id':file_id,'function':function.name,
            'function_line':function.lineno,'nodes':nodes,'edges':edges,
            'independence_certificate':False,'edit_authority_granted':False,
            'unknown_policy':'NO_ABSENCE_INFERENCE'}


def graph_digest(graph):
    return hashlib.sha256(json.dumps(graph,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def function_graphs(source: str, file_id: str='unknown'):
    tree=ast.parse(source,filename=file_id)
    return [build_graph(source,n,file_id) for n in ast.walk(tree)
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
