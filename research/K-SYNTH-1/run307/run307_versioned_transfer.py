#!/usr/bin/env python3
"""Bounded source-only annotation-effect timing analysis.

This is deliberately not a Python-wide abstract interpreter. It handles only
module-level function definitions, lambda shadowing of len, direct annotation
attribute reads, simple function aliases and a final len(...) observation.
Unknown mutation is classified UNKNOWN, never as definitely absent.
"""
import ast
import hashlib

MODES = {'3.13': 'EAGER', '3.14': 'DEFERRED'}


def classify(source: str, version: str):
    if version not in MODES:
        return {'schema': 'run307-v1', 'status': 'UNSUPPORTED_RUNTIME_UNKNOWN',
                'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                'final_len': 'UNKNOWN', 'events': []}
    tree = ast.parse(source)
    future = any(isinstance(s, ast.ImportFrom) and s.module == '__future__' and
                 any(a.name == 'annotations' for a in s.names) for s in tree.body)
    mode = 'STRINGIFIED' if future else MODES[version]
    env = {'len': 'UNKNOWN'}
    functions = {}
    aliases = {}
    events = []
    unsupported = False

    def unknown_effect(where):
        env['len'] = 'UNKNOWN'
        events.append({'event': 'UNKNOWN_ANNOTATION_EFFECT', 'site': where})

    def annotated_calls(node):
        args = node.args
        anns = [a.annotation for a in args.posonlyargs + args.args + args.kwonlyargs]
        anns += [a.annotation for a in (args.vararg, args.kwarg) if a is not None]
        anns += [node.returns]
        return any(any(isinstance(x, ast.Call) for x in ast.walk(a))
                   for a in anns if a is not None)

    def access_expr(expr):
        nonlocal unsupported
        # Supported direct or aliased __annotations__ read. The same function
        # identity is tracked across aliases, including a cached first access.
        if isinstance(expr, ast.Attribute) and expr.attr == '__annotations__' and isinstance(expr.value, ast.Name):
            name = expr.value.id
            fid = aliases.get(name)
            if fid is None or fid not in functions:
                unsupported = True
                env['len'] = 'UNKNOWN'
                events.append({'event': 'UNKNOWN_REFLECTION', 'site': name})
                return
            entry = functions[fid]
            if mode == 'DEFERRED' and entry['has_effect'] and not entry['cached']:
                unknown_effect(fid + '.__annotations__')
                entry['cached'] = True
            elif mode == 'DEFERRED' and not entry['cached']:
                entry['cached'] = True
            events.append({'event': 'ANNOTATION_READ', 'site': name,
                           'cache_filled': entry['cached']})
        elif isinstance(expr, ast.Call):
            # Unknown arbitrary calls can mutate module bindings. Do not infer
            # a negative identity from any unsupported dynamic call.
            env['len'] = 'UNKNOWN'
            unsupported = True
            events.append({'event': 'UNKNOWN_CALL', 'site': ast.unparse(expr.func)})
        elif isinstance(expr, (ast.Constant, ast.Name)):
            pass
        else:
            unsupported = True
            env['len'] = 'UNKNOWN'
            events.append({'event': 'UNKNOWN_EXPRESSION', 'site': type(expr).__name__})

    final = None
    for stmt in tree.body:
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Restricted fixture functions have no decorators/defaults. Refuse
            # otherwise rather than assume no definition-time effects.
            if stmt.decorator_list or stmt.args.defaults or any(x is not None for x in stmt.args.kw_defaults):
                unsupported = True
                env['len'] = 'UNKNOWN'
                events.append({'event': 'UNSUPPORTED_DEF_EFFECT', 'site': stmt.name})
            effect = annotated_calls(stmt)
            functions[stmt.name] = {'has_effect': effect, 'cached': False}
            aliases[stmt.name] = stmt.name
            if mode == 'EAGER' and effect:
                unknown_effect(stmt.name + ':definition')
        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            name = stmt.targets[0].id
            val = stmt.value
            if name == 'len' and isinstance(val, ast.Lambda):
                env['len'] = 'NON_TARGET'
            elif name == 'events' and isinstance(val, ast.List) and not val.elts:
                pass
            elif name == 'observed' and isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id == 'len':
                final = ('NOT_KNOWN_TARGET' if env['len'] == 'NON_TARGET' else
                         'MAY_TARGET' if env['len'] == 'BUILTIN' else 'UNKNOWN_DYNAMIC')
                events.append({'event': 'FINAL_LEN_CALL', 'classification': final})
                break  # Ignore trusted observation instrumentation after the final call.
            elif isinstance(val, ast.Name) and val.id in aliases:
                aliases[name] = aliases[val.id]
            else:
                access_expr(val)
        elif isinstance(stmt, ast.Expr):
            access_expr(stmt.value)
        elif isinstance(stmt, ast.Pass):
            pass
        else:
            unsupported = True
            env['len'] = 'UNKNOWN'
            events.append({'event': 'UNSUPPORTED_STATEMENT', 'site': type(stmt).__name__})
    return {'schema': 'run307-v1', 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'mode': mode, 'final_len': final or 'UNKNOWN_DYNAMIC',
            'events': events, 'unsupported': unsupported,
            'status': 'BOUNDED' if not unsupported else 'PARTIAL_UNKNOWN'}
