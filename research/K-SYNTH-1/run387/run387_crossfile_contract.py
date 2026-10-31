#!/usr/bin/env python3
"""Soundness-scoped static direct-call compatibility check for Rich #3176.

Checks only direct import binding, no rebinding, and concrete AST call arguments.
A COMPATIBLE verdict proves conditional Python signature binding only, not
importability, runtime reachability, semantic equivalence, or other failures. Unsupported shapes UNKNOWN.
"""
import ast, hashlib, inspect, json, pathlib, sys

class Unknown(Exception): pass

def source_sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def signature(fn):
    a=fn.args
    if a.posonlyargs or a.vararg or a.kwarg or a.kwonlyargs or a.kw_defaults:
        raise Unknown('UNSUPPORTED_SIGNATURE')
    params=[]
    mandatory=len(a.args)-len(a.defaults)
    for i,arg in enumerate(a.args):
        # Binding-only claim: annotations are deliberately outside this scope.
        # They may have definition-time effects; this does NOT certify importability.
        default=inspect.Parameter.empty if i<mandatory else None
        params.append(inspect.Parameter(arg.arg,inspect.Parameter.POSITIONAL_OR_KEYWORD,default=default))
    return inspect.Signature(params)

def audit(wrap_path,cells_path):
    wp=pathlib.Path(wrap_path);cp=pathlib.Path(cells_path)
    report={'wrap_sha256':source_sha(wp),'cells_sha256':source_sha(cp)}
    try:
        w=ast.parse(wp.read_text());c=ast.parse(cp.read_text())
        imports=[x for x in w.body if isinstance(x,ast.ImportFrom) and x.module=='cells' and x.level==1]
        if len(imports)!=1 or not any(a.name=='chop_cells' and a.asname is None for a in imports[0].names):
            raise Unknown('DIRECT_IMPORT_NOT_PROVEN')
        wf=[x for x in w.body if isinstance(x,ast.FunctionDef) and x.name=='divide_line']
        cf=[x for x in c.body if isinstance(x,ast.FunctionDef) and x.name=='chop_cells']
        if len(wf)!=1 or len(cf)!=1: raise Unknown('FUNCTION_NOT_UNIQUE')
        fn=wf[0];callee=cf[0]
        # Reject any local shadowing or module rebinding of the imported name.
        if any(isinstance(x,ast.Name) and isinstance(x.ctx,(ast.Store,ast.Del)) and x.id=='chop_cells'
               for x in ast.walk(fn)):
            raise Unknown('LOCAL_REBIND')
        for x in w.body:
            if x is fn or x is imports[0]: continue
            if isinstance(x,(ast.Assign,ast.AnnAssign,ast.AugAssign)) and any(
                isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id=='chop_cells'
                for n in ast.walk(x)):
                raise Unknown('MODULE_REBIND')
        calls=[x for x in ast.walk(fn) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name)
               and x.func.id=='chop_cells']
        if len(calls)!=1: raise Unknown('DIRECT_CALL_NOT_UNIQUE')
        call=calls[0]
        if any(isinstance(a,ast.Starred) for a in call.args) or any(k.arg is None for k in call.keywords):
            raise Unknown('DYNAMIC_ARGUMENT_UNPACKING')
        sig=signature(callee)
        names=[k.arg for k in call.keywords]
        report.update(signature=str(sig),annotations_ignored_for_binding=any(a.annotation is not None for a in callee.args.args),call_positional=len(call.args),call_keywords=names,
                      call_line=call.lineno)
        try:
            sig.bind(*([object()]*len(call.args)),**{k:object() for k in names})
        except TypeError as e:
            report.update(verdict='INCOMPATIBLE',reason=str(e))
        else:
            report.update(verdict='COMPATIBLE',reason='direct call arguments bind to declared signature')
    except (Unknown,SyntaxError,ValueError) as e:
        report.update(verdict='UNKNOWN',reason=str(e))
    return report

if __name__=='__main__':
    print(json.dumps(audit(sys.argv[1],sys.argv[2]),indent=2,sort_keys=True))
