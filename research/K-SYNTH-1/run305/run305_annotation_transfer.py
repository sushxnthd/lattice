#!/usr/bin/env python3
"""Run305 bounded fix: inspect function annotation expressions at definition time.

Explicitly accounts for `from __future__ import annotations`, where source
annotations are postponed. Does not claim Python-wide soundness: dynamic
mutation, descriptors, nested execution and class metaclasses are excluded.
"""
import ast
from run304_shadowing_transfer import ShadowingAwareTransfer
from run293_conservative_transfer import NON_TARGET, UNKNOWN

class AnnotationAwareTransfer(ShadowingAwareTransfer):
    def __init__(self, src):
        super().__init__(src)
        tree=ast.parse(src)
        self.postponed_annotations=any(
            isinstance(s,ast.ImportFrom) and s.module=='__future__'
            and any(a.name=='annotations' for a in s.names)
            for s in tree.body
        )
    def stmt(self,node,env):
        if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            return super().stmt(node,env)
        for d in node.decorator_list:self.expr(d,env)
        for d in node.args.defaults:self.expr(d,env)
        for d in node.args.kw_defaults:self.expr(d,env)
        if not self.postponed_annotations:
            args=node.args
            for a in args.posonlyargs+args.args+args.kwonlyargs:
                if a.annotation is not None:self.expr(a.annotation,env)
            for a in (args.vararg,args.kwarg):
                if a is not None and a.annotation is not None:self.expr(a.annotation,env)
            if node.returns is not None:self.expr(node.returns,env)
        for s in node.body:self.deferred_stmt(s,env.copy())
        env[node.name]=UNKNOWN if node.decorator_list else NON_TARGET

def extract(source):return AnnotationAwareTransfer(source).run()
