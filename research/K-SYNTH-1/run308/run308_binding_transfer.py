#!/usr/bin/env python3
"""Bounded module-binding transfer for K-SYNTH-1, not a general Python analyzer.

Scope: trusted module-level import/delete/assignment/definition statements;
no monkeypatching of builtins, import hooks, arbitrary runtime effects, or
reflection. Every unsupported statement or effect invalidates definite-negative
knowledge about the builtin len identity.
"""
import ast,hashlib

BUILTIN='BUILTIN_LEN'
NON='NON_TARGET'
UNKNOWN='UNKNOWN'


def classify(source: str, version: str='3.13'):
    digest=hashlib.sha256(source.encode()).hexdigest()
    if version not in ('3.13','3.14'):
        return {'schema':'run308-binding-v1','source_sha256':digest,
                'status':'UNSUPPORTED_RUNTIME_UNKNOWN','final_len':'UNKNOWN_DYNAMIC','events':[]}
    tree=ast.parse(source)
    bindings={'len':BUILTIN}
    events=[]
    status='BOUNDED'
    final='UNKNOWN_DYNAMIC'

    def invalidate(site,reason):
        nonlocal status
        bindings['len']=UNKNOWN
        status='PARTIAL_UNKNOWN'
        events.append({'event':'INVALIDATE','site':site,'reason':reason})

    def value_of(node):
        if isinstance(node,ast.Lambda):
            if node.args.defaults or any(x is not None for x in node.args.kw_defaults):
                return UNKNOWN
            return NON
        if isinstance(node,ast.Name):
            return bindings.get(node.id,UNKNOWN)
        if isinstance(node,ast.Constant):
            return NON
        return UNKNOWN

    for stmt in tree.body:
        if isinstance(stmt,ast.Import):
            # These two modules are pinned trusted modules in the frozen cases.
            if all(x.name in ('builtins','json') for x in stmt.names):
                for x in stmt.names:
                    bindings[x.asname or x.name]=NON
            else:
                invalidate('import','unsupported import side effects')
        elif isinstance(stmt,ast.ImportFrom):
            if stmt.module=='__future__':
                continue
            if stmt.module!='builtins' or stmt.level!=0:
                invalidate('importfrom','unsupported import source')
                for alias in stmt.names:
                    if alias.name!='*': bindings[alias.asname or alias.name]=UNKNOWN
                continue
            for alias in stmt.names:
                if alias.name=='*':
                    invalidate('importfrom','wildcard import may rebind aliases')
                    break
                name=alias.asname or alias.name
                bindings[name]=BUILTIN if alias.name=='len' else NON
                events.append({'event':'IMPORT_BIND','name':name,'identity':bindings[name]})
        elif isinstance(stmt,ast.Delete):
            for target in stmt.targets:
                if isinstance(target,ast.Name):
                    # In the trusted module-level subset, deleting a global
                    # binding exposes the unmodified builtin in name lookup.
                    bindings.pop(target.id,None)
                    if target.id=='len': bindings['len']=BUILTIN
                    events.append({'event':'DELETE_BIND','name':target.id})
                else:
                    invalidate('delete','dynamic delete target')
        elif isinstance(stmt,ast.Assign):
            if len(stmt.targets)!=1 or not isinstance(stmt.targets[0],ast.Name):
                invalidate('assign','complex assignment target')
                continue
            name=stmt.targets[0].id
            if name=='observed' and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Name) and stmt.value.func.id=='len':
                state=bindings.get('len',BUILTIN)
                final={'BUILTIN_LEN':'MAY_TARGET','NON_TARGET':'NOT_KNOWN_TARGET',
                       'UNKNOWN':'UNKNOWN_DYNAMIC'}[state]
                events.append({'event':'FINAL_LEN_CALL','classification':final})
                break
            if isinstance(stmt.value,(ast.Call,ast.Await,ast.Yield,ast.YieldFrom)):
                invalidate(name,'potentially effectful assignment')
                bindings[name]=UNKNOWN
            else:
                bindings[name]=value_of(stmt.value)
                if name=='len' and isinstance(stmt.value,ast.Lambda) and bindings[name]==UNKNOWN:
                    invalidate(name,'lambda default may have side effects')
                events.append({'event':'ASSIGN_BIND','name':name,'identity':bindings[name]})
        elif isinstance(stmt,(ast.FunctionDef,ast.AsyncFunctionDef)):
            if stmt.decorator_list or stmt.args.defaults or any(x is not None for x in stmt.args.kw_defaults):
                invalidate(stmt.name,'definition-time dynamic effect')
                bindings[stmt.name]=UNKNOWN
            else:
                # Annotations with executable expressions can change globals.
                annotations=[a.annotation for a in stmt.args.posonlyargs+stmt.args.args+stmt.args.kwonlyargs]
                annotations += [a.annotation for a in (stmt.args.vararg,stmt.args.kwarg) if a]
                annotations.append(stmt.returns)
                if any(isinstance(x,ast.Call) for a in annotations if a for x in ast.walk(a)):
                    invalidate(stmt.name,'annotation effect')
                bindings[stmt.name]=NON
        elif isinstance(stmt,ast.Expr):
            invalidate('expression','unknown expression side effect')
        elif isinstance(stmt,ast.Pass):
            pass
        else:
            invalidate(type(stmt).__name__,'unsupported statement')
    return {'schema':'run308-binding-v1','source_sha256':digest,'status':status,
            'final_len':final,'events':events,'final_identity':bindings.get('len',BUILTIN)}
