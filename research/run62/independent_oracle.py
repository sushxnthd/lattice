"""Three-way finite Boolean consistency oracle (experimental).

Independent bound-node evaluation, production run(), and lowered Python are
compared on the same complete finite input domain. No intent guarantee.
"""
import ast
import hashlib
import itertools


class OracleError(ValueError):
    pass


def eval_bool(node, env):
    if isinstance(node, ast.Constant) and type(node.value) is bool:
        return node.value
    if isinstance(node, ast.Name) and node.id in env and type(env[node.id]) is bool:
        return env[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not eval_bool(node.operand, env)
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
        return all(eval_bool(x, env) for x in node.values)
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        return any(eval_bool(x, env) for x in node.values)
    raise OracleError("unsupported Boolean expression")


def bound_values(frame, values):
    if set(values) != set(frame.inputs) or any(type(v) is not bool for v in values.values()):
        raise OracleError("invalid Boolean inputs")
    memo = {}

    def visit(index):
        if index in memo:
            return memo[index]
        if type(index) is not int or not 0 <= index < len(frame.nodes):
            raise OracleError("invalid node index")
        node = frame.nodes[index]
        expr = ast.parse(node.source, mode="eval").body
        bindings = dict(node.bindings)
        refs = {part.id for part in ast.walk(expr) if isinstance(part, ast.Name)}
        if len(bindings) != len(node.bindings) or set(bindings) != refs - set(frame.inputs):
            raise OracleError("invalid immutable bindings")
        env = dict(values)
        for name, prior in bindings.items():
            if name in env or type(prior) is not int or not 0 <= prior < index:
                raise OracleError("invalid version reference")
            env[name] = visit(prior)
        memo[index] = eval_bool(expr, env)
        return memo[index]

    return {name: visit(index) for name, index in frame.roots}


def lowered_values(source, inputs, values):
    tree = ast.parse(source)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise OracleError("expected one function")
    fn = tree.body[0]
    if (fn.name != "policy" or fn.decorator_list or fn.args.posonlyargs
            or fn.args.kwonlyargs or fn.args.vararg or fn.args.kwarg
            or fn.args.defaults or fn.args.kw_defaults
            or tuple(arg.arg for arg in fn.args.args) != tuple(inputs)):
        raise OracleError("invalid function signature")
    env = dict(values)
    result = None
    for pos, stmt in enumerate(fn.body):
        if isinstance(stmt, ast.Assign):
            if result is not None or len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
                raise OracleError("invalid lowering assignment")
            name = stmt.targets[0].id
            if name in env:
                raise OracleError("lowering overwrites a binding")
            env[name] = eval_bool(stmt.value, env)
        elif isinstance(stmt, ast.Return) and pos == len(fn.body) - 1:
            if not isinstance(stmt.value, ast.Tuple):
                raise OracleError("expected tuple return")
            result = tuple(eval_bool(x, env) for x in stmt.value.elts)
        else:
            raise OracleError("unexpected lowered statement")
    if result is None:
        raise OracleError("missing return")
    return result


def audit_three_way(before, after, allowed_outputs, max_inputs=12):
    if (before.inputs != after.inputs or
            tuple(name for name, _ in before.roots) != tuple(name for name, _ in after.roots)):
        raise OracleError("schema mismatch")
    outputs = tuple(name for name, _ in after.roots)
    if not set(allowed_outputs) <= set(outputs):
        raise OracleError("invalid authorized outputs")
    if not 0 <= max_inputs <= 16 or len(before.inputs) > max_inputs:
        raise OracleError("exhaustive audit bound exceeded")
    source = after.lower_python()
    counts = dict(protected_regressions=0, production_before_mismatches=0,
                  production_after_mismatches=0, lowering_mismatches=0)
    witness = None
    checked = 0
    for bits in itertools.product((False, True), repeat=len(before.inputs)):
        values = dict(zip(before.inputs, bits))
        old = bound_values(before, values)
        new = bound_values(after, values)
        old_prod = before.run(values)
        new_prod = after.run(values)
        lowered = lowered_values(source, after.inputs, values)
        if set(old_prod) != set(outputs) or set(new_prod) != set(outputs) or len(lowered) != len(outputs):
            raise OracleError("output schema mismatch")
        checked += 1
        for pos, name in enumerate(outputs):
            conditions = {
                "protected_regressions": name not in allowed_outputs and old[name] != new[name],
                "production_before_mismatches": old_prod[name] != old[name],
                "production_after_mismatches": new_prod[name] != new[name],
                "lowering_mismatches": lowered[pos] != new[name],
            }
            for kind, flag in conditions.items():
                counts[kind] += int(flag)
                if flag and witness is None:
                    witness = {"kind": kind, "input": values, "output": name,
                               "old": old[name], "new": new[name],
                               "production_before": old_prod[name],
                               "production_after": new_prod[name],
                               "lowered": lowered[pos]}
    return {
        "ok": all(x == 0 for x in counts.values()), "cases": checked,
        "protected_pairs": checked * (len(outputs) - len(allowed_outputs)),
        **counts, "first_witness": witness,
        "lowered_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "claim_boundary": "Exact bounded consistency audit, not a model improvement or an intent oracle."
    }
