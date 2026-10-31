#!/usr/bin/env python3
"""Run387: conservative annotation preflight for bounded effect certificates.

This is a standalone executable guard, not an unrestricted Python verifier.
Call it before a finite effect certificate; UNKNOWN must not be promoted.
"""
import ast

def guard(source):
    try:
        tree=ast.parse(source)
    except SyntaxError:
        return ('UNKNOWN','SYNTAX')
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.Lambda)):
            args=node.args
            if any(a.annotation is not None for a in
                   [*args.posonlyargs,*args.args,*args.kwonlyargs]):
                return ('UNKNOWN','DEFINITION_TIME_ANNOTATION')
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.returns is not None:
                return ('UNKNOWN','RETURN_ANNOTATION')
    return ('PASS_ANNOTATION_PREFLIGHT','NO_ANNOTATIONS')

if __name__=='__main__':
    good='from producer import produce as p\ndef target(x,y):\n    return p(x,y)\n'
    bad='from producer import produce as p\ndef target(x: missing,y):\n    return p(x,y)\n'
    effect='from producer import produce as p\ndef target(x: emit("defined",True),y):\n    return p(x,y)\n'
    assert guard(good)[0]=='PASS_ANNOTATION_PREFLIGHT'
    assert guard(bad)==('UNKNOWN','DEFINITION_TIME_ANNOTATION')
    assert guard(effect)==('UNKNOWN','DEFINITION_TIME_ANNOTATION')
    print('PASS: 3 definition-time annotation preflight checks')
