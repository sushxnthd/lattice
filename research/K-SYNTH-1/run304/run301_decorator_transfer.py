#!/usr/bin/env python3
"""Conservative Run301 correction of decorator-rebound lexical call provenance.

No general Python soundness claim. A decorated function's post-definition
binding may be *any* decorator return value; it cannot be certified non-target.
"""
import ast
from run293_conservative_transfer import Transfer, Abstract, NON_TARGET, UNKNOWN, TARGETS

class CorrectedTransfer(Transfer):
    def stmt(self,node,env):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            # The expressions are evaluated at definition time, and the
            # resulting decorator call(s) can rebind the function name.
            for d in node.decorator_list:self.expr(d,env)
            for d in node.args.defaults:self.expr(d,env)
            for d in node.args.kw_defaults:self.expr(d,env)
            for s in node.body:self.deferred_stmt(s,env.copy())
            if node.decorator_list:
                # Explicit UNKNOWN, not a claim that the name is never len/sum.
                env[node.name]=UNKNOWN
            else:
                env[node.name]=(Abstract(frozenset({node.name}))
                                if node.name in TARGETS else NON_TARGET)
        else:
            super().stmt(node,env)

def extract(source):
    return CorrectedTransfer(source).run()
