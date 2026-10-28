#!/usr/bin/env python3
"""Bounded soundness repair: unknown calls invalidate module alias provenance.

This is NOT a general sound Python analyzer. Assumptions: trusted module-level
subset, source-only MAY candidates, no mutation except through explicit Call
expressions; dynamic attributes/descriptors/import hooks/threads excluded.
"""
import ast
from run305_annotation_transfer import AnnotationAwareTransfer
from run293_conservative_transfer import UNKNOWN

class EffectAwareTransfer(AnnotationAwareTransfer):
    def expr(self, node, env, deferred=False):
        if not isinstance(node, ast.Call):
            return super().expr(node, env, deferred)
        # Evaluate function expression and arguments before the call side effect.
        # Child calls may themselves invalidate the environment.
        v=self.expr(node.func,env,deferred)
        for arg in node.args:
            self.expr(arg,env,deferred)
        for kw in node.keywords:
            self.expr(kw.value,env,deferred)
        self.calls.append(dict(
            name=ast.unparse(node.func),line=node.lineno,column=node.col_offset,
            provenance=v.data(),classification=(
                'UNKNOWN_DEFERRED' if deferred else
                'UNKNOWN_DYNAMIC' if v.unknown else
                'MAY_TARGET' if v.candidates else 'NOT_KNOWN_TARGET')))
        if not deferred:
            for name in list(env):
                env[name]=UNKNOWN
        return UNKNOWN

def extract(src):
    return EffectAwareTransfer(src).run()
