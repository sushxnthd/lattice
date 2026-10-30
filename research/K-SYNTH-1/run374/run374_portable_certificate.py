"""K-SYNTH-1 Run374: bounded, conservative Python two-module dependence certificate.

NO_DEPENDENCE is a sound noninterference certificate only for the admitted pure,
acyclic, total Boolean fragment. MAY_DEPEND is not a proof of causal effect.
UNKNOWN carries no guarantee. Never use on untrusted code as an execution gate.
"""
import ast


def _valid_function(node):
    if not isinstance(node, ast.FunctionDef):
        return False
    a = node.args
    return (not node.decorator_list and not a.posonlyargs and not a.kwonlyargs
            and not a.vararg and not a.kwarg and not a.defaults and not a.kw_defaults
            and len(a.args) == 2 and [v.arg for v in a.args] == ['x', 'y']
            and all(v.annotation is None for v in a.args) and node.returns is None
            and len(node.body) == 1 and isinstance(node.body[0], ast.Return))


def _calls(expr):
    if isinstance(expr, ast.Name):
        return set() if expr.id in ('x', 'y') else None
    if isinstance(expr, ast.Constant):
        return set() if type(expr.value) is bool else None
    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
        return _calls(expr.operand)
    if isinstance(expr, ast.BoolOp) and isinstance(expr.op, (ast.And, ast.Or)):
        parts = [_calls(v) for v in expr.values]
    elif isinstance(expr, ast.IfExp):
        parts = [_calls(v) for v in (expr.test, expr.body, expr.orelse)]
    elif isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name):
        # x/y are Boolean parameters, even if a module function shares the name.
        if expr.func.id in ('x', 'y'):
            return None
        if expr.keywords or len(expr.args) != 2 or any(
            not isinstance(v, ast.Name) or v.id not in ('x', 'y') for v in expr.args
        ):
            return None
        return {expr.func.id}
    else:
        return None
    return None if any(v is None for v in parts) else set().union(*parts)


def certificate(producer_source, consumer_source):
    """Return NO_DEPENDENCE / MAY_DEPEND / UNKNOWN, with explicit scope checks."""
    if len(producer_source) + len(consumer_source) > 65536:
        return 'UNKNOWN'
    try:
        p, c = ast.parse(producer_source), ast.parse(consumer_source)
    except (SyntaxError, ValueError, RecursionError):
        return 'UNKNOWN'
    if len(p.body) != 1 or not _valid_function(p.body[0]) or p.body[0].name != 'produce':
        return 'UNKNOWN'
    p_calls = _calls(p.body[0].body[0].value)
    if p_calls is None or p_calls:
        return 'UNKNOWN'
    if not c.body or not isinstance(c.body[0], ast.ImportFrom):
        return 'UNKNOWN'
    imp = c.body[0]
    if imp.module != 'producer' or imp.level or len(imp.names) != 1 or imp.names[0].name != 'produce':
        return 'UNKNOWN'
    aliases = {imp.names[0].asname or 'produce'}
    functions = {}
    for node in c.body[1:]:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Name) and node.value.id in aliases:
            name = node.targets[0].id
            if name in aliases or name in functions or name in ('x', 'y'):
                return 'UNKNOWN'
            aliases.add(name)
        elif _valid_function(node) and node.name not in aliases and node.name not in functions:
            functions[node.name] = node
        else:
            return 'UNKNOWN'
    if 'target' not in functions or len(functions) > 128:
        return 'UNKNOWN'
    edges = {}
    for name, fn in functions.items():
        calls = _calls(fn.body[0].value)
        if calls is None or any(v not in aliases and v not in functions for v in calls):
            return 'UNKNOWN'
        edges[name] = {'@producer' if v in aliases else v for v in calls}

    # CRITICAL: validate every edge before computing reachability. A boolean
    # `any(visit(child) ...)` short-circuits after @producer=True and can miss
    # recursion in a sibling branch. That would violate the totality lemma.
    state = {}
    def check_acyclic(name):
        if name == '@producer':
            return True
        if state.get(name) == 1:
            return False
        if state.get(name) == 2:
            return True
        state[name] = 1
        for child in sorted(edges[name]):
            if not check_acyclic(child):
                return False
        state[name] = 2
        return True
    try:
        if not all(check_acyclic(name) for name in sorted(edges)):
            return 'UNKNOWN'
    except RecursionError:
        return 'UNKNOWN'

    seen = set()
    pending = ['target']
    while pending:
        name = pending.pop()
        if name == '@producer':
            return 'MAY_DEPEND'
        if name not in seen:
            seen.add(name)
            pending.extend(sorted(edges[name]))
    return 'NO_DEPENDENCE'


if __name__ == '__main__':
    p = 'def produce(x,y):\n    return x and y\n'
    c = 'from producer import produce as p\ndef target(x,y):\n    return p(x,y) or target(x,y)\n'
    assert certificate(p,c) == 'UNKNOWN'
    assert certificate(p,'from producer import produce as p\ndef target(x,y):\n    return x or y\n') == 'NO_DEPENDENCE'
    assert certificate(p,'from producer import produce as p\ndef target(x,y):\n    return p(x,y)\n') == 'MAY_DEPEND'
    print('3/3 portable smoke checks passed')
