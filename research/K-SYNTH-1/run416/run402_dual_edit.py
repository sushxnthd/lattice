#!/usr/bin/env python3
"""Run402: two genuinely different edit action languages with one atomic compiler.

Semantic IR selects a unique reaching definition in a restricted acyclic SSA-like
function. AST actions select the corresponding statement by ordinal. The IR
extractor is deliberately fail-closed for all Python features outside this scope.
No claims of whole-Python soundness, behavioral preservation, or model advantage.
"""
from __future__ import annotations
import ast
import copy
import dataclasses
import hashlib
import json
from typing import Any

class Unknown(Exception):
    """Cannot establish a unique, soundness-scoped static target."""

class InvalidEdit(Exception):
    """Malformed edit, source mismatch, or violated authority."""


def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _function(tree: ast.Module, name: str) -> ast.FunctionDef:
    matches=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
    if len(matches)!=1:
        raise Unknown('FUNCTION_NOT_UNIQUE')
    return matches[0]


def _names(expr: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(expr) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}


def _safe_expr(expr: ast.AST) -> bool:
    # Deliberately disallow calls, attributes, subscripts, lambdas, comprehensions,
    # assignment expressions, f-strings and any dynamic dispatch.
    if isinstance(expr,ast.Name): return isinstance(expr.ctx,ast.Load)
    if isinstance(expr,ast.Constant): return type(expr.value) in (int,float,bool,type(None))
    if isinstance(expr,ast.UnaryOp): return isinstance(expr.op,(ast.UAdd,ast.USub)) and _safe_expr(expr.operand)
    if isinstance(expr,ast.BinOp): return isinstance(expr.op,(ast.Add,ast.Sub,ast.Mult)) and _safe_expr(expr.left) and _safe_expr(expr.right)
    return False


def _graph(fn: ast.FunctionDef) -> dict[str,Any]:
    if fn.decorator_list or fn.returns or fn.type_comment or fn.args.posonlyargs or fn.args.kwonlyargs or fn.args.vararg or fn.args.kwarg or fn.args.defaults or fn.args.kw_defaults:
        raise Unknown('UNSUPPORTED_SIGNATURE')
    if any(not isinstance(a,ast.arg) or a.annotation for a in fn.args.args):
        raise Unknown('UNSUPPORTED_ARGUMENT')
    args=[a.arg for a in fn.args.args]
    if len(set(args))!=len(args): raise Unknown('DUPLICATE_ARGUMENT')
    if not fn.body or not isinstance(fn.body[-1],ast.Return) or fn.body[-1].value is None:
        raise Unknown('NO_TERMINAL_RETURN')
    defs={}; available=set(args)
    for index,node in enumerate(fn.body[:-1]):
        if not isinstance(node,ast.Assign) or len(node.targets)!=1 or not isinstance(node.targets[0],ast.Name):
            raise Unknown('NON_STRAIGHT_LINE')
        name=node.targets[0].id
        if name in available: raise Unknown('NOT_SINGLE_ASSIGNMENT')
        if not _safe_expr(node.value): raise Unknown('DYNAMIC_RHS')
        used=_names(node.value)
        if not used <= available: raise Unknown('UNBOUND_RHS')
        defs[name]={'index':index,'uses':sorted(used),'ast':ast.unparse(node.value)}
        available.add(name)
    ret=fn.body[-1].value
    if not _safe_expr(ret): raise Unknown('DYNAMIC_RETURN')
    if not _names(ret) <= available: raise Unknown('UNBOUND_RETURN')
    reach=set(_names(ret)); pending=list(reach)
    while pending:
        cur=pending.pop()
        if cur in defs:
            for dep in defs[cur]['uses']:
                if dep not in reach:
                    reach.add(dep);pending.append(dep)
    return {'arguments':args,'definitions':defs,'return_uses':sorted(_names(ret)),
            'reaching_return':sorted(reach),'return_ast':ast.unparse(ret)}


def analyze(files: dict[str,str], authority: dict[str,list[str]]) -> dict[str,Any]:
    result={}
    for path,fnames in sorted(authority.items()):
        if path not in files: raise InvalidEdit('MISSING_AUTHORIZED_SOURCE')
        tree=ast.parse(files[path],filename=path)
        result[path]={}
        for fn in fnames:
            try: result[path][fn]={'status':'PROVEN_BOUNDED','graph':_graph(_function(tree,fn))}
            except Unknown as e: result[path][fn]={'status':'UNKNOWN','reason':str(e)}
    return result


def compile_transaction(files:dict[str,str], expected_sha:dict[str,str],
                        authority:dict[str,list[str]], actions:list[dict[str,Any]],
                        language:str) -> dict[str,str]:
    """All-or-nothing transaction; returns new sources, never mutates inputs."""
    if language not in ('SEMANTIC_DATAFLOW','PYTHON_AST_ACTION'):
        raise InvalidEdit('UNKNOWN_LANGUAGE')
    if set(expected_sha)!=set(files) or any(sha(files[p])!=h for p,h in expected_sha.items()):
        raise InvalidEdit('SOURCE_HASH_MISMATCH')
    trees={p:ast.parse(src,filename=p) for p,src in files.items()}
    modified=set()
    for action in actions:
        if not isinstance(action,dict) or set(action)!=({'path','function','definition','expression'} if language=='SEMANTIC_DATAFLOW' else {'path','function','statement_index','expression'}):
            raise InvalidEdit('BAD_ACTION_SCHEMA')
        p=action['path']; f=action['function']; expr_text=action['expression']
        if p not in trees or p not in authority or f not in authority[p]:
            raise InvalidEdit('OUT_OF_AUTHORITY')
        if not isinstance(expr_text,str) or len(expr_text)>1024:
            raise InvalidEdit('BAD_EXPRESSION')
        try: expr=ast.parse(expr_text,mode='eval').body
        except SyntaxError as e: raise InvalidEdit('BAD_EXPRESSION') from e
        if not _safe_expr(expr): raise Unknown('DYNAMIC_EDIT_EXPRESSION')
        fn=_function(trees[p],f)
        graph=_graph(fn)  # Reject unsupported Python even for AST baseline.
        if language=='SEMANTIC_DATAFLOW':
            name=action['definition']
            if not isinstance(name,str) or name not in graph['definitions'] or name not in graph['reaching_return']:
                raise Unknown('DEFINITION_NOT_UNIQUE_AND_REACHING_RETURN')
            index=graph['definitions'][name]['index']
        else:
            index=action['statement_index']
            if type(index) is not int or index<0 or index>=len(fn.body)-1:
                raise InvalidEdit('BAD_AST_INDEX')
        target=fn.body[index]
        if not isinstance(target,ast.Assign) or not isinstance(target.targets[0],ast.Name):
            raise Unknown('UNSUPPORTED_TARGET')
        name=target.targets[0].id
        # Preserve the SSA-like graph domain after editing, including absence
        # of new unbound dependencies or forward references.
        available=set(graph['arguments'])
        for prior in fn.body[:index]: available.add(prior.targets[0].id)
        if not _names(expr) <= available:
            raise Unknown('NEW_UNBOUND_OR_FORWARD_REFERENCE')
        if (p,f,index) in modified: raise InvalidEdit('DUPLICATE_TARGET')
        modified.add((p,f,index))
        target.value=expr
        ast.fix_missing_locations(trees[p])
        _graph(fn)
    out={p:(ast.unparse(t)+'\n' if any(x[0]==p for x in modified) else files[p]) for p,t in trees.items()}
    for p in out: ast.parse(out[p])
    return out


def matching_ast_action(files:dict[str,str], semantic:dict[str,Any]) -> dict[str,Any]:
    """Independent ordinary AST locator from the original source, not IR decoding."""
    path=semantic['path'];fn=_function(ast.parse(files[path]),semantic['function'])
    target=semantic['definition']; matches=[]
    for i,n in enumerate(fn.body[:-1]):
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==target:
            matches.append(i)
    if len(matches)!=1: raise Unknown('AST_TARGET_NOT_UNIQUE')
    return {'path':path,'function':semantic['function'],'statement_index':matches[0],
            'expression':semantic['expression']}


def equivalence_certificate(files:dict[str,str], authority:dict[str,list[str]], semantic:list[dict[str,Any]]) -> dict[str,Any]:
    """Proves byte-level compiler parity for a specific fixed transaction only."""
    hashes={p:sha(s) for p,s in files.items()}
    ast_actions=[matching_ast_action(files,a) for a in semantic]
    ir=compile_transaction(files,hashes,authority,semantic,'SEMANTIC_DATAFLOW')
    ordinary=compile_transaction(files,hashes,authority,ast_actions,'PYTHON_AST_ACTION')
    if ir!=ordinary: raise AssertionError('COMPILER_PARITY_FAILURE')
    return {'source_sha256':hashes,'semantic_actions':semantic,'ast_actions':ast_actions,
            'output_sha256':{p:sha(s) for p,s in ir.items()},'equal_sources':True}
