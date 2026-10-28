#!/usr/bin/env python3
"""Conservative correction: decorated def bindings are UNKNOWN, not NON_TARGET.

Bounded source-only lexical provenance, not runtime identity or general soundness.
"""
import ast
from run293_conservative_transfer import Transfer, Abstract, NON_TARGET, UNKNOWN, TARGETS

class CorrectedTransfer(Transfer):
    def stmt(self,node,env):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            for d in node.decorator_list:self.expr(d,env)
            for d in node.args.defaults:self.expr(d,env)
            for d in node.args.kw_defaults:self.expr(d,env)
            for s in node.body:self.deferred_stmt(s,env.copy())
            if node.decorator_list:
                env[node.name]=UNKNOWN
            else:
                env[node.name]=(Abstract(frozenset({node.name}))
                                if node.name in TARGETS else NON_TARGET)
        else:
            super().stmt(node,env)

def extract(source):
    return CorrectedTransfer(source).run()
