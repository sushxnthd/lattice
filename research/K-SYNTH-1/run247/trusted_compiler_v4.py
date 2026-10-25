#!/usr/bin/env python3
"""Lattice Run247 trusted transactional compiler hardening.

Provides a *syntactic* declaration-ownership guarantee, not semantic
noninterference. Rejects duplicate declarations shadowing existing methods,
read-only target text changes, stale input snapshots, and malformed paths.
"""
from __future__ import annotations
import ast
from collections import Counter
from typing import Any
import run240


def declaration_counts(source: str) -> Counter[tuple[str,str,str]]:
    """Count declarations by lexical scope, kind and name; preserve duplicates."""
    root=ast.parse(source)
    counts=Counter()
    def visit(node: ast.AST,scope:tuple[str,...]):
        for child in ast.iter_child_nodes(node):
            if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                key=('.'.join(scope),type(child).__name__,child.name)
                counts[key]+=1
                visit(child,scope+(child.name,))
            else:
                visit(child,scope)
    visit(root,())
    return counts


def scope_writes_to_existing_declarations(source:str)->Counter[tuple[str,str]]:
    """Count lexical writes/deletions to names that are declared in that scope.

    Includes class-body assignments that shadow an existing method.
    Does not claim to detect dynamic setattr/exec.
    """
    root=ast.parse(source)
    declarations=declaration_counts(source)
    declared={(scope,name) for (scope,kind,name),n in declarations.items() if n}
    writes=Counter()
    def walk(node:ast.AST,scope:tuple[str,...]):
        for child in ast.iter_child_nodes(node):
            if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                walk(child,scope+(child.name,))
            elif isinstance(child,ast.Name) and isinstance(child.ctx,(ast.Store,ast.Del)):
                key=('.'.join(scope),child.id)
                if key in declared:writes[key]+=1
            else:walk(child,scope)
    walk(root,())
    return writes


def compile_checked(facts:dict, files:dict[str,bytes], output:dict)->tuple[dict,list[dict]]:
    """Call existing compiler, then enforce transaction-safety invariants."""
    expected=facts.get('file_sha256')
    if not isinstance(expected,dict) or set(files)!=set(expected):
        raise ValueError('incomplete or unexpected input files')
    for path,raw in files.items():
        if not isinstance(raw,bytes) or run240.sha(raw)!=expected[path]:
            raise ValueError('stale or mismatched input snapshot: '+path)
    after,traces=run240.compile_actions(facts,files,output)
    for path in files:
        if path not in after:raise ValueError('compiler omitted input file')
        if after[path]==files[path]:continue
        before_counts=declaration_counts(files[path].decode('utf-8'))
        after_counts=declaration_counts(after[path].decode('utf-8'))
        for key,count in before_counts.items():
            if after_counts[key]>count:
                raise ValueError('shadowing existing declaration: '+repr(key))
        before_writes=scope_writes_to_existing_declarations(files[path].decode('utf-8'))
        after_writes=scope_writes_to_existing_declarations(after[path].decode('utf-8'))
        for key,count in after_writes.items():
            if count>before_writes[key]:
                raise ValueError('write shadows existing declaration: '+repr(key))
        for block in facts['blocks']:
            if block['path']!=path or block['authority']!='read_only':continue
            anchor=block['code'].encode('utf-8')
            if files[path].count(anchor)!=1 or after[path].count(anchor)!=1:
                raise ValueError('read-only anchor missing, duplicated or altered')
    return after,traces
