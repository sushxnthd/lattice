"""K-SYNTH-1 Run375: target-scoped, conservative two-module Boolean noninterference.

NO_DEPENDENCE is guaranteed only for the admitted, bounded pure Boolean grammar
with an acyclic call graph *reachable from target*. Unreachable recursive helper
functions are permitted; their bodies are not executed during module import.
MAY_DEPEND does not establish causal effect; UNKNOWN makes no claim.
Do not use this certificate to authorize execution of untrusted code.
"""
import ast

MAX_SOURCE = 65536
MAX_AST_NODES = 4096
MAX_AST_DEPTH = 256
MAX_FUNCTIONS = 128


def _bounded_tree(tree):
    """Iterative shape check: no recursive visitor before bounding depth."""
    stack = [(tree, 0)]
    count = 0
    while stack:
        node, depth = stack.pop()
        count += 1
        if count > MAX_AST_NODES or depth > MAX_AST_DEPTH:
            return False
        stack.extend((child, depth + 1) for child in ast.iter_child_nodes(node))
    return True


def _valid_function(node):
    if not isinstance(node, ast.FunctionDef):
        return False
    a = node.args
    return (not node.decorator_list and not getattr(node, 'type_params', ())
            and not node.type_comment
            and not a.posonlyargs and not a.kwonlyargs and not a.vararg
            and not a.kwarg and not a.defaults and not a.kw_defaults
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
        if expr.func.id in ('x', 'y'):
            return None
        if expr.keywords or len(expr.args) != 2 or any(
            not isinstance(v, ast.Name) or v.id not in ('x', 'y')
            for v in expr.args
        ):
            return None
        return {expr.func.id}
    else:
        return None
    return None if any(v is None for v in parts) else set().union(*parts)


def certificate(producer_source, consumer_source):
    if not isinstance(producer_source, str) or not isinstance(consumer_source, str):
        return 'UNKNOWN'
    if len(producer_source) + len(consumer_source) > MAX_SOURCE:
        return 'UNKNOWN'
    try:
        p = ast.parse(producer_source)
        c = ast.parse(consumer_source)
        if not _bounded_tree(p) or not _bounded_tree(c):
            return 'UNKNOWN'
        if len(p.body) != 1 or not _valid_function(p.body[0]) or p.body[0].name != 'produce':
            return 'UNKNOWN'
        p_calls = _calls(p.body[0].body[0].value)
        if p_calls is None or p_calls:
            return 'UNKNOWN'
        if not c.body or not isinstance(c.body[0], ast.ImportFrom):
            return 'UNKNOWN'
        imp = c.body[0]
        if (imp.module != 'producer' or imp.level or len(imp.names) != 1
                or imp.names[0].name != 'produce'):
            return 'UNKNOWN'
        aliases = {imp.names[0].asname or 'produce'}
        functions = {}
        for node in c.body[1:]:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Name) and node.value.id in aliases):
                name = node.targets[0].id
                if name in aliases or name in functions or name in ('x', 'y'):
                    return 'UNKNOWN'
                aliases.add(name)
            elif (_valid_function(node) and node.name not in aliases
                  and node.name not in functions):
                functions[node.name] = node
            else:
                return 'UNKNOWN'
        if 'target' not in functions or len(functions) > MAX_FUNCTIONS:
            return 'UNKNOWN'
        edges = {}
        for name, fn in functions.items():
            calls = _calls(fn.body[0].value)
            if calls is None or any(v not in aliases and v not in functions for v in calls):
                return 'UNKNOWN'
            edges[name] = {'@producer' if v in aliases else v for v in calls}
        # Only target-reachable cycles can affect the target's totality. Unused
        # functions are defined but never invoked and have no side effects.
        state = {}
        def visit(name):
            if name == '@producer':
                return True
            if state.get(name) == 1:
                return False
            if state.get(name) == 2:
                return True
            state[name] = 1
            for child in sorted(edges[name]):
                if not visit(child):
                    return False
            state[name] = 2
            return True
        if not visit('target'):
            return 'UNKNOWN'
        seen = set()
        pending = ['target']
        while pending:
            name = pending.pop()
            if name == '@producer':
                return 'MAY_DEPEND'
            if name not in seen:
                seen.add(name)
                pending.extend(edges[name])
        return 'NO_DEPENDENCE'
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        return 'UNKNOWN'


if __name__ == '__main__':
    P = 'def produce(x,y):\n    return x and y\n'
    pre = 'from producer import produce as p\n'
    assert certificate(P, pre+'def target(x,y):\n    return x\ndef f(x,y):\n    return f(x,y)\n') == 'NO_DEPENDENCE'
    assert certificate(P, pre+'def target(x,y):\n    return p(x,y)\ndef f(x,y):\n    return f(x,y)\n') == 'MAY_DEPEND'
    assert certificate(P, pre+'def target(x,y):\n    return f(x,y)\ndef f(x,y):\n    return f(x,y)\n') == 'UNKNOWN'
    assert certificate(P, pre+'def target(x,y):\n    return '+'not '*1000+'x\n') == 'UNKNOWN'
    print('4/4 portable smoke checks passed')
