#!/usr/bin/env python3
"""Run304: correct lexical provenance for undecorated user function definitions.

This is a bounded MAY-call analysis, not runtime identity inference.
The only trusted builtins in this kernel are len and sum. Assumptions and
unsupported effects are inherited from Run293/301; UNKNOWN remains explicit.
"""
import ast
from run301_decorator_transfer import CorrectedTransfer
from run293_conservative_transfer import NON_TARGET

class ShadowingAwareTransfer(CorrectedTransfer):
    def stmt(self, node, env):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Evaluate definition-time expressions and scan deferred body
            # with the exact inherited bounded transfer policy.
            for decorator in node.decorator_list:
                self.expr(decorator, env)
            for default in node.args.defaults:
                self.expr(default, env)
            for default in node.args.kw_defaults:
                self.expr(default, env)
            for body_stmt in node.body:
                self.deferred_stmt(body_stmt, env.copy())
            if node.decorator_list:
                # A decorator can return an arbitrary callable, including len.
                from run293_conservative_transfer import UNKNOWN
                env[node.name] = UNKNOWN
            else:
                # A fresh Python function is not the pre-existing builtin,
                # even if its lexical name is exactly 'len' or 'sum'.
                env[node.name] = NON_TARGET
        else:
            super().stmt(node, env)

def extract(source):
    return ShadowingAwareTransfer(source).run()
