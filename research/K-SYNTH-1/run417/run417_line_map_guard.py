#!/usr/bin/env python3
"""Run417: source-line-stable preflight for the shared Run416 atomic compiler.

Only guarantees that edited RHS spans do not change the exact physical
line-ending sequence. It does NOT guarantee Python semantic or trace equivalence.
Both IR and ordinary AST actions use the same authority and compiler.
"""
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "run416"))
import run402_dual_edit as base
import run416_lossless_compiler as compiler

class UnknownLineMap(base.Unknown):
    pass

def endings(raw):
    return tuple(m.group() for m in re.finditer(rb"\r\n|\r|\n", raw))

def compile_line_stable(files, expected_sha, authority, actions, language):
    # Run416 validates the entire transaction, all source hashes, authority,
    # graph restrictions, AST equivalence and byte-preserving patch receipts.
    # No files are written by the compiler.
    out, receipts = compiler.compile_lossless(
        files, expected_sha, authority, actions, language
    )
    trees = {p: ast.parse(source, filename=p) for p, source in files.items()}
    for action in actions:
        path = action["path"]
        fn = base._function(trees[path], action["function"])
        graph = base._graph(fn)
        index = (graph["definitions"][action["definition"]]["index"]
                 if language == compiler.SEMANTIC
                 else action["statement_index"])
        start, end = compiler._byte_span(files[path], fn.body[index].value)
        old_rhs = files[path].encode("utf-8")[start:end]
        new_rhs = ast.unparse(
            ast.parse(action["expression"], mode="eval").body
        ).encode("utf-8")
        if endings(old_rhs) != endings(new_rhs):
            raise UnknownLineMap("UNKNOWN_LINE_MAP_SHIFT")
    return out, receipts
