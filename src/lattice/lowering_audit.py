"""Independent, non-executing audit of the bounded framed Boolean compiler.

This checks the generated Python's semantics with a separate AST interpreter,
rather than executing compiler output or calling the production evaluator for
the lowering side. It is an exact finite-domain check, NOT an arbitrary-Python
verifier, model benchmark, or proof of representation superiority.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
from typing import Any

from .framed_edits import FramedProgram
from .semantic_edits import InvalidProgram


def _boolean(node: ast.AST, env: dict[str, bool]) -> bool:
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise InvalidProgram("unbound name in lowered code")
        return env[node.id]
    if isinstance(node, ast.Constant) and type(node.value) is bool:
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _boolean(node.operand, env)
    if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
        values = [_boolean(item, env) for item in node.values]
        return all(values) if isinstance(node.op, ast.And) else any(values)
    raise InvalidProgram("unsupported lowered expression")


def _interpret_lowering(source: str, inputs: tuple[str, ...], values: dict[str, bool]) -> tuple[bool, ...]:
    """Deliberately independent of semantic_edits.evaluate and Python exec."""
    tree = ast.parse(source)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise InvalidProgram("lowering must contain one function")
    fn = tree.body[0]
    if (fn.name != "policy" or fn.decorator_list or fn.args.posonlyargs
            or fn.args.kwonlyargs or fn.args.vararg or fn.args.kwarg
            or fn.args.defaults or fn.args.kw_defaults
            or tuple(arg.arg for arg in fn.args.args) != inputs):
        raise InvalidProgram("unexpected lowering function signature")
    env = dict(values)
    result = None
    for index, statement in enumerate(fn.body):
        if isinstance(statement, ast.Assign):
            if result is not None or len(statement.targets) != 1 or not isinstance(statement.targets[0], ast.Name):
                raise InvalidProgram("invalid lowering assignment")
            name = statement.targets[0].id
            if name in env:
                raise InvalidProgram("duplicate or overwritten lowering binding")
            env[name] = _boolean(statement.value, env)
        elif isinstance(statement, ast.Return) and index == len(fn.body) - 1:
            if not isinstance(statement.value, ast.Tuple):
                raise InvalidProgram("lowering must return a tuple")
            result = tuple(_boolean(element, env) for element in statement.value.elts)
        else:
            raise InvalidProgram("unexpected lowering statement")
    if result is None:
        raise InvalidProgram("lowering missing return")
    return result


def audit_framed_lowering(
    before: FramedProgram,
    after: FramedProgram,
    allowed_outputs: set[str],
    *,
    max_inputs: int = 12,
) -> dict[str, Any]:
    """Check frame preservation and lowered Python over every Boolean input.

    The caller supplies trusted edit scope. The target/intent is deliberately
    absent: this checks preservation and compiler fidelity, NOT desired edits.
    max_inputs limits the exhaustive audit to at most 2**12 cases by default.
    """
    if before.inputs != after.inputs or tuple(k for k, _ in before.roots) != tuple(k for k, _ in after.roots):
        raise InvalidProgram("before/after schema mismatch")
    outputs = tuple(k for k, _ in after.roots)
    if not allowed_outputs <= set(outputs):
        raise InvalidProgram("unknown authorized output")
    if len(before.inputs) > max_inputs or max_inputs > 16 or max_inputs < 0:
        raise InvalidProgram("exhaustive audit input bound exceeded")
    source = after.lower_python()
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    changed = {name: 0 for name in outputs}
    protected_regressions = 0
    lowering_mismatches = 0
    first_witness = None
    checked = 0
    for bits in itertools.product((False, True), repeat=len(before.inputs)):
        values = dict(zip(before.inputs, bits))
        old = before.run(values)
        new = after.run(values)
        lowered = _interpret_lowering(source, after.inputs, values)
        if len(lowered) != len(outputs):
            raise InvalidProgram("lowering output arity mismatch")
        checked += 1
        for index, name in enumerate(outputs):
            changed[name] += old[name] != new[name]
            regression = name not in allowed_outputs and old[name] != new[name]
            mismatch = lowered[index] != new[name]
            protected_regressions += regression
            lowering_mismatches += mismatch
            if first_witness is None and (regression or mismatch):
                first_witness = {
                    "input": values, "output": name,
                    "prior": old[name], "framed": new[name],
                    "lowered": lowered[index],
                    "kind": "protected_regression" if regression else "lowering_mismatch",
                }
    return {
        "ok": protected_regressions == 0 and lowering_mismatches == 0,
        "cases": checked,
        "protected_pairs": checked * (len(outputs) - len(allowed_outputs)),
        "changed_pairs": changed,
        "semantic_churn_pairs": sum(changed.values()),
        "protected_regressions": protected_regressions,
        "lowering_mismatches": lowering_mismatches,
        "first_witness": first_witness,
        "lowered_python_sha256": digest,
        "claim_boundary": "Exact bounded Boolean frame/lowering audit; does not check target intent or establish model gains.",
    }
