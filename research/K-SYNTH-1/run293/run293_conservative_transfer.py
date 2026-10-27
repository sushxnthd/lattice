#!/usr/bin/env python3
"""A bounded, conservative source-only alias candidate transfer.

Candidate names are NOT runtime identities. No general Python soundness claim:
only trusted module-level assignments, simple If/IfExp, BoolOp, NamedExpr and
calls under an explicit no-unmodeled-mutation assumption are supported.
Unsupported operations propagate UNKNOWN instead of silently dropping MAY edges.
"""
import ast
import hashlib
from dataclasses import dataclass

TARGETS=frozenset(('len','sum'))

@dataclass(frozen=True)
class Abstract:
    candidates:frozenset=frozenset()
    unknown:bool=False
    def join(self,other):
        return Abstract(self.candidates|other.candidates,self.unknown or other.unknown)
    def data(self):
        return dict(candidates=sorted(self.candidates),unknown=self.unknown,runtime_identity='UNKNOWN')
UNKNOWN=Abstract(unknown=True)
NON_TARGET=Abstract()

def join_env(a,b):
    return {k:a.get(k,UNKNOWN).join(b.get(k,UNKNOWN)) for k in a.keys()|b.keys()}

class Transfer:
    def __init__(self,src):
        self.src=src
        self.calls=[]
        self.env={'len':Abstract(frozenset({'len'})), 'sum':Abstract(frozenset({'sum'}))}
        self.dynamic=False
    def bind(self,target,v,env):
        if isinstance(target,ast.Name):env[target.id]=v
        else:
            self.dynamic=True
            for k in list(env):env[k]=UNKNOWN
    def expr(self,node,env,deferred=False):
        if node is None:return NON_TARGET
        if isinstance(node,ast.Name):return env.get(node.id,UNKNOWN)
        if isinstance(node,ast.Constant):return NON_TARGET
        if isinstance(node,ast.IfExp):
            self.expr(node.test,env,deferred)
            yes=env.copy();no=env.copy()
            v1=self.expr(node.body,yes,deferred);v2=self.expr(node.orelse,no,deferred)
            env.update(join_env(yes,no));return v1.join(v2)
        if isinstance(node,ast.BoolOp):
            # Each operand may be the returned operand of short-circuit and/or.
            # Analyze both paths; joining side effects is conservative.
            accumulated=NON_TARGET
            path_env=env.copy(); possible_env=env.copy()
            for child in node.values:
                v=self.expr(child,path_env,deferred)
                accumulated=accumulated.join(v)
                possible_env=join_env(possible_env,path_env)
            env.update(possible_env)
            return accumulated
        if isinstance(node,ast.NamedExpr):
            v=self.expr(node.value,env,deferred)
            self.bind(node.target,v,env)
            return v
        if isinstance(node,ast.Call):
            v=self.expr(node.func,env,deferred)
            name=ast.unparse(node.func)
            self.calls.append(dict(name=name,line=node.lineno,column=node.col_offset,
                provenance=v.data(),classification=('UNKNOWN_DEFERRED' if deferred else 'UNKNOWN_DYNAMIC' if v.unknown else 'MAY_TARGET' if v.candidates else 'NOT_KNOWN_TARGET')))
            for arg in node.args:self.expr(arg,env,deferred)
            for kw in node.keywords:self.expr(kw.value,env,deferred)
            # Dynamic mutation is possible for arbitrary calls. This kernel
            # deliberately uses the trusted no-unmodeled-mutation assumption.
            return UNKNOWN
        if isinstance(node,ast.Lambda):
            for d in node.args.defaults:self.expr(d,env,deferred)
            for d in node.args.kw_defaults:self.expr(d,env,deferred)
            self.expr(node.body,env.copy(),True)
            return NON_TARGET
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.Not):
            self.expr(node.operand,env,deferred);return NON_TARGET
        if isinstance(node,(ast.Tuple,ast.List,ast.Set,ast.Dict)):
            for child in ast.iter_child_nodes(node):self.expr(child,env,deferred)
            return NON_TARGET
        # Any other expression might produce a target callable dynamically.
        for child in ast.iter_child_nodes(node):self.expr(child,env,deferred)
        return UNKNOWN
    def stmt(self,node,env):
        if isinstance(node,ast.Assign):
            v=self.expr(node.value,env)
            for t in node.targets:self.bind(t,v,env)
        elif isinstance(node,ast.Expr):
            self.expr(node.value,env)
        elif isinstance(node,ast.If):
            self.expr(node.test,env)
            yes=env.copy();no=env.copy()
            for s in node.body:self.stmt(s,yes)
            for s in node.orelse:self.stmt(s,no)
            env.update(join_env(yes,no))
        elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            for d in node.decorator_list:self.expr(d,env)
            for d in node.args.defaults:self.expr(d,env)
            for d in node.args.kw_defaults:self.expr(d,env)
            for s in node.body:self.deferred_stmt(s,env.copy())
            env[node.name]=Abstract(frozenset({node.name})) if node.name in TARGETS else NON_TARGET
        elif isinstance(node,ast.Import):
            for alias in node.names:env[alias.asname or alias.name.split('.')[0]]=UNKNOWN
        elif isinstance(node,ast.ImportFrom):
            for alias in node.names:
                env[alias.asname or alias.name]=Abstract(frozenset({alias.name})) if node.module=='builtins' and alias.name in TARGETS else UNKNOWN
        else:
            self.dynamic=True
            for child in ast.walk(node):
                if isinstance(child,ast.Call):self.expr(child,env.copy(),True)
            for k in list(env):env[k]=UNKNOWN
    def deferred_stmt(self,node,env):
        if isinstance(node,ast.Return):self.expr(node.value,env,True)
        else:
            for child in ast.walk(node):
                if isinstance(child,ast.Call):self.expr(child,env.copy(),True)
    def run(self):
        tree=ast.parse(self.src)
        for node in tree.body:self.stmt(node,self.env)
        return dict(schema='ksynth1-run293-conservative-transfer-v1',source_sha256=hashlib.sha256(self.src.encode()).hexdigest(),calls=sorted(self.calls,key=lambda c:(c['line'],c['column'])),runtime_identity='UNKNOWN',assumptions=['trusted module-level supported subset','no unmodeled mutation between source operations','candidate-name provenance only'],unsupported_effect_seen=self.dynamic)

def extract(src):return Transfer(src).run()

def equal_views(facts):
    canon={k:v for k,v in facts.items() if k!='schema'}
    return {'representation':'SEMANTIC_IR','facts':canon},{'representation':'ORDINARY_PYTHON_AST_ACTIONS','facts':canon}
