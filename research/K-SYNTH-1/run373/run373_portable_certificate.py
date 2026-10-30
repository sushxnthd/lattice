"""Portable bounded two-module Python MAY-dependence certificate. UNKNOWN outside scope."""
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
        # Function parameters x/y shadow module-level function names and imports.
        # Calling them would raise TypeError for the admitted Boolean inputs.
        if expr.func.id in ('x', 'y'):
            return None
        if expr.keywords or len(expr.args) != 2 or any(not isinstance(v, ast.Name) or v.id not in ('x', 'y') for v in expr.args):
            return None
        return {expr.func.id}
    else:
        return None
    return None if any(v is None for v in parts) else set().union(*parts)


def certificate(producer_source, consumer_source):
    """Return NO_DEPENDENCE, MAY_DEPEND or UNKNOWN; only NO has a guarantee."""
    try:
        p, c = ast.parse(producer_source), ast.parse(consumer_source)
    except SyntaxError:
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
    if 'target' not in functions:
        return 'UNKNOWN'
    edges = {}
    for name, fn in functions.items():
        calls = _calls(fn.body[0].value)
        if calls is None or any(v not in aliases and v not in functions for v in calls):
            return 'UNKNOWN'
        edges[name] = {'@producer' if v in aliases else v for v in calls}
    visiting, done = set(), {}
    def visit(name):
        if name == '@producer':
            return True
        if name in visiting:
            raise ValueError('recursive')
        if name in done:
            return done[name]
        visiting.add(name)
        outcome = any(visit(child) for child in sorted(edges[name]))
        visiting.remove(name)
        done[name] = outcome
        return outcome
    try:
        return 'MAY_DEPEND' if visit('target') else 'NO_DEPENDENCE'
    except ValueError:
        return 'UNKNOWN'


if __name__ == '__main__':
    producer = 'def produce(x,y):\n    return x and y\n'
    direct = 'from producer import produce as p\ndef target(x,y):\n    return p(x,y)\n'
    unrelated = 'from producer import produce as p\ndef target(x,y):\n    return x or y\n'
    dynamic = 'from producer import produce as p\ndef target(x,y):\n    return globals()["p"](x,y)\n'
    assert certificate(producer, direct) == 'MAY_DEPEND'
    assert certificate(producer, unrelated) == 'NO_DEPENDENCE'
    assert certificate(producer, dynamic) == 'UNKNOWN'
    print('3/3 portable certificate smoke checks passed')
