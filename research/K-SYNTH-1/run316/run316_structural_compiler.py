"""Bounded, SHA-preconditioned, pure multi-file structural Python patch compiler.

Engineering prototype: supports replacing an AST expression or statement,
inserting one statement before another, and deleting a statement. Does not
execute model-generated code. Does not guarantee preservation of comments or
semantic soundness. The same compiler must serve IR and Python/AST frontends.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping, Sequence
from run315_multifile_compiler import PatchRejected, checked_path, node_digest

@dataclass(frozen=True)
class Action:
    path: str
    source_sha256: str
    node_sha256: str
    node_type: str
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    operation: str
    replacement: str = ''


def _offset(lines: list[bytes], line: int, col: int) -> int:
    if not (1 <= line <= len(lines) and 0 <= col <= len(lines[line-1])):
        raise PatchRejected('invalid byte span')
    return sum(map(len,lines[:line-1]))+col


def _snippet(action: Action, original_indent: bytes) -> bytes:
    if '\x00' in action.replacement or len(action.replacement.encode('utf-8')) > 32768:
        raise PatchRejected('invalid replacement size')
    if action.operation == 'delete_stmt':
        if action.replacement:
            raise PatchRejected('deletion with replacement')
        return b''
    replacement=action.replacement.encode('utf-8')
    if not replacement.strip() or replacement.endswith(b'\n'):
        raise PatchRejected('empty or trailing-newline replacement')
    if action.operation == 'replace_expr':
        try:ast.parse(action.replacement,mode='eval')
        except (SyntaxError,ValueError) as exc:raise PatchRejected('invalid expression replacement') from exc
        return replacement
    if action.operation in ('replace_stmt','insert_before'):
        # Dedented input: continuation lines are indented to the target scope.
        if replacement[:1] in (b' ',b'\t'):
            raise PatchRejected('statement replacement must start dedented')
        return replacement.replace(b'\n',b'\n'+original_indent)
    raise PatchRejected('unsupported operation')


def compile_structural(sources: Mapping[str,bytes], actions: Sequence[Action], *,
                       allowed_paths: frozenset[str]) -> dict[str,bytes]:
    if not actions or len(actions)>64 or len(sources)>64:
        raise PatchRejected('invalid transaction size')
    if any(checked_path(p)!=p for p in allowed_paths):
        raise PatchRejected('invalid authority')
    out={}
    trees={}
    for path,data in sources.items():
        if checked_path(path)!=path or type(data) is not bytes or len(data)>1000000:
            raise PatchRejected('invalid source')
        try:
            text=data.decode('utf-8')
            tree=ast.parse(text)
        except (UnicodeError,SyntaxError,ValueError) as exc:raise PatchRejected('invalid source AST') from exc
        out[path]=data
        trees[path]=tree
    spans={}
    for a in actions:
        if not isinstance(a,Action) or a.path not in allowed_paths or a.path not in out:
            raise PatchRejected('unauthorized action')
        data=out[a.path]
        if sha256(data).hexdigest()!=a.source_sha256:
            raise PatchRejected('stale source SHA')
        hits=[n for n in ast.walk(trees[a.path]) if type(n).__name__==a.node_type
              and hasattr(n,'lineno') and
              (n.lineno,n.col_offset,n.end_lineno,n.end_col_offset)==
              (a.lineno,a.col_offset,a.end_lineno,a.end_col_offset)
              and node_digest(n)==a.node_sha256]
        if len(hits)!=1:
            raise PatchRejected('missing or ambiguous node')
        node=hits[0]
        is_stmt=isinstance(node,ast.stmt)
        if (a.operation in ('replace_stmt','delete_stmt','insert_before')) != is_stmt:
            raise PatchRejected('node kind/operation mismatch')
        if a.operation=='replace_expr' and not isinstance(node,ast.expr):
            raise PatchRejected('not an expression')
        lines=data.splitlines(keepends=True)
        start=_offset(lines,a.lineno,a.col_offset)
        stop=_offset(lines,a.end_lineno,a.end_col_offset)
        if not (0<=start<stop<=len(data)):
            raise PatchRejected('empty or invalid node span')
        indent=lines[a.lineno-1][:a.col_offset]
        if is_stmt and (indent.strip() or any(c not in (32,9) for c in indent)):
            raise PatchRejected('non-standalone statement')
        replacement=_snippet(a,indent)
        if a.operation=='insert_before':
            if getattr(node,'decorator_list',[]):
                raise PatchRejected('cannot insert between decorators')
            # Must be a standalone statement starting at line indentation.
            start-=len(indent)
            stop=start
            replacement=indent+replacement+b'\n'
        elif a.operation=='delete_stmt':
            # Delete entire physical line only if the remainder is whitespace.
            suffix=lines[a.end_lineno-1][a.end_col_offset:]
            if suffix.strip():raise PatchRejected('trailing content on deleted line')
            start-=len(indent)
            stop=_offset(lines,a.end_lineno,len(lines[a.end_lineno-1]))
        elif a.operation=='replace_stmt':
            suffix=lines[a.end_lineno-1][a.end_col_offset:]
            if suffix.strip():raise PatchRejected('trailing content on replaced line')
        spans.setdefault(a.path,[]).append((start,stop,replacement))
    for path,edits in spans.items():
        edits.sort(key=lambda x:(x[0],x[1]))
        if any(b[0]<a[1] or b[0]==a[0] for a,b in zip(edits,edits[1:])):
            raise PatchRejected('overlapping or colliding actions')
        data=out[path]
        for start,stop,replacement in reversed(edits):
            data=data[:start]+replacement+data[stop:]
        try:
            tree=ast.parse(data.decode('utf-8'))
            compile(tree,path,'exec',dont_inherit=True)  # compile only; NEVER exec
        except (UnicodeError,SyntaxError,ValueError,TypeError) as exc:
            raise PatchRejected('invalid compiled Python') from exc
        out[path]=data
    return out
