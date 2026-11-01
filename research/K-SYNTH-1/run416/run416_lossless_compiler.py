#!/usr/bin/env python3
"""Bounded lossless Python RHS transaction compiler (K-SYNTH-1 Run416).

The representation-specific locator differs, but both semantic definition names
and ordinary AST statement indices use the same byte-preserving compiler.
Original-source UTF-8 byte spans are used, never AST-unparse of a whole module.
This guarantees only *syntactic* byte-frame preservation and AST equivalence
within the Run402 grammar. It is not a Python semantic noninterference proof.
"""
from __future__ import annotations
import ast
import copy
from dataclasses import dataclass
from typing import Any
import run402_dual_edit as base

SEMANTIC = 'SEMANTIC_DATAFLOW_EFFECT_AWARE'
ORDINARY = 'PYTHON_AST_ACTION'

@dataclass(frozen=True)
class Patch:
    path: str
    function: str
    index: int
    start: int
    end: int
    replacement: bytes


def _byte_span(source: str, node: ast.AST) -> tuple[int,int]:
    """CPython AST columns are UTF-8 byte offsets, not Unicode columns."""
    lines = source.encode('utf-8').splitlines(keepends=True)
    if not all(hasattr(node,k) for k in ('lineno','col_offset','end_lineno','end_col_offset')):
        raise base.Unknown('MISSING_EXPRESSION_LOCATION')
    if not (1 <= node.lineno <= node.end_lineno <= len(lines)):
        raise base.Unknown('INVALID_EXPRESSION_LOCATION')
    start=sum(map(len,lines[:node.lineno-1]))+node.col_offset
    end=sum(map(len,lines[:node.end_lineno-1]))+node.end_col_offset
    if not (0 <= start < end <= len(source.encode('utf-8'))):
        raise base.Unknown('INVALID_EXPRESSION_SPAN')
    return start,end


def compile_lossless(files: dict[str,str], expected_sha: dict[str,str],
                     authority: dict[str,list[str]], actions: list[dict[str,Any]],
                     language: str) -> tuple[dict[str,str],list[dict[str,Any]]]:
    if language not in (SEMANTIC,ORDINARY):
        raise base.InvalidEdit('UNKNOWN_LANGUAGE')
    if set(expected_sha)!=set(files) or any(base.sha(s)!=expected_sha[p] for p,s in files.items()):
        raise base.InvalidEdit('SOURCE_HASH_MISMATCH')
    trees={p:ast.parse(s,filename=p) for p,s in files.items()}
    expected={p:copy.deepcopy(t) for p,t in trees.items()}
    patches: dict[str,list[Patch]]={p:[] for p in files}
    seen=set()
    for a in actions:
        required={'path','function','definition','expression'} if language==SEMANTIC else {'path','function','statement_index','expression'}
        if not isinstance(a,dict) or set(a)!=required:
            raise base.InvalidEdit('BAD_ACTION_SCHEMA')
        p=a['path']; f=a['function']; expr_text=a['expression']
        if not isinstance(p,str) or not isinstance(f,str) or p not in files or p not in authority or f not in authority[p]:
            raise base.InvalidEdit('OUT_OF_AUTHORITY')
        if not isinstance(expr_text,str) or len(expr_text)>1024:
            raise base.InvalidEdit('BAD_EXPRESSION')
        try: expr=ast.parse(expr_text,mode='eval').body
        except SyntaxError as e: raise base.InvalidEdit('BAD_EXPRESSION') from e
        if not base._safe_expr(expr): raise base.Unknown('DYNAMIC_EDIT_EXPRESSION')
        fn=base._function(trees[p],f)
        graph=base._graph(fn)
        if language==SEMANTIC:
            name=a['definition']
            if not isinstance(name,str) or name not in graph['definitions']:
                raise base.InvalidEdit('UNKNOWN_DEFINITION')
            index=graph['definitions'][name]['index']
        else:
            index=a['statement_index']
            if type(index) is not int or index not in [d['index'] for d in graph['definitions'].values()]:
                raise base.InvalidEdit('UNKNOWN_AST_INDEX')
        key=(p,f,index)
        if key in seen: raise base.InvalidEdit('DUPLICATE_TARGET')
        seen.add(key)
        available=set(graph['arguments'])
        for prior in fn.body[:index]: available.add(prior.targets[0].id)
        if not base._names(expr)<=available:
            raise base.Unknown('NEW_UNBOUND_OR_FORWARD_REFERENCE')
        node=fn.body[index].value
        start,end=_byte_span(files[p],node)
        replacement=ast.unparse(expr).encode('utf-8')
        patches[p].append(Patch(p,f,index,start,end,replacement))
        # Build an independent AST expectation; do not trust a text-only parse.
        ef=base._function(expected[p],f)
        ef.body[index].value=copy.deepcopy(expr)
    for p,ps in patches.items():
        spans=sorted(ps,key=lambda x:x.start)
        if any(a.end>b.start for a,b in zip(spans,spans[1:])):
            raise base.InvalidEdit('OVERLAPPING_RHS_SPANS')
    out={}; receipts=[]
    for p,src in files.items():
        raw=src.encode('utf-8')
        for patch in sorted(patches[p],key=lambda x:x.start,reverse=True):
            raw=raw[:patch.start]+patch.replacement+raw[patch.end:]
        try: final=raw.decode('utf-8'); parsed=ast.parse(final,filename=p)
        except (UnicodeError,SyntaxError) as e: raise base.InvalidEdit('OUTPUT_INVALID_PYTHON') from e
        if ast.dump(parsed,include_attributes=False)!=ast.dump(expected[p],include_attributes=False):
            raise base.InvalidEdit('UNEXPECTED_AST_CHANGE')
        for f in authority.get(p,[]):
            base._graph(base._function(parsed,f))
        out[p]=final
        for patch in sorted(patches[p],key=lambda x:x.start):
            receipts.append({'path':p,'function':patch.function,'statement_index':patch.index,
                             'start_byte':patch.start,'end_byte':patch.end,
                             'old_rhs_sha256':base.sha(src.encode('utf-8')[patch.start:patch.end].decode('utf-8')),
                             'new_rhs_sha256':base.sha(patch.replacement.decode('utf-8'))})
    return out,receipts
