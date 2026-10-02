"""Finite Boolean semantic edits with exact regression checking.

This is a bounded research language, not a verifier for arbitrary applications.
The trusted contract is supplied separately from the untrusted model response.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import keyword
from dataclasses import dataclass
from typing import Mapping


class InvalidProgram(ValueError):
    pass


def expression(source: str) -> ast.expr:
    if len(source) > 4096:
        raise InvalidProgram("expression too long")
    try:
        node = ast.parse(source, mode="eval").body
    except (SyntaxError, RecursionError) as exc:
        raise InvalidProgram("invalid expression") from exc
    allowed = (ast.Expression, ast.Name, ast.Load, ast.Constant, ast.BoolOp,
               ast.And, ast.Or, ast.UnaryOp, ast.Not)
    for part in ast.walk(node):
        if not isinstance(part, allowed):
            raise InvalidProgram(f"unsupported expression: {type(part).__name__}")
        if isinstance(part, ast.Constant) and type(part.value) is not bool:
            raise InvalidProgram("only Boolean constants are supported")
    return node


def evaluate(node: ast.expr, env: Mapping[str, bool]) -> bool:
    if isinstance(node, ast.Name):
        try:
            return env[node.id]
        except KeyError as exc:
            raise InvalidProgram(f"unknown name: {node.id}") from exc
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp):
        return not evaluate(node.operand, env)
    if isinstance(node, ast.BoolOp):
        values = [evaluate(n, env) for n in node.values]
        return all(values) if isinstance(node.op, ast.And) else any(values)
    raise InvalidProgram("unsupported expression")


@dataclass(frozen=True)
class Program:
    inputs: tuple[str, ...]
    # Tuple prevents caller mutation of an admitted program.
    rules: tuple[tuple[str, str], ...]

    def __post_init__(self):
        names = self.inputs + tuple(k for k, _ in self.rules)
        if len(set(names)) != len(names) or not all(
            n.isidentifier() and not keyword.iskeyword(n) for n in names
        ):
            raise InvalidProgram("names must be unique non-keyword identifiers")
        if len(self.inputs) > 16:
            raise InvalidProgram("exact checker supports at most 16 Boolean inputs")
        if not self.rules or len(self.rules) > 256:
            raise InvalidProgram("provide between 1 and 256 rules")
        self.order()  # Check unknown references and cycles before evaluation.

    def order(self) -> tuple[str, ...]:
        rules = dict(self.rules)
        deps = {k: {n.id for n in ast.walk(expression(s)) if isinstance(n, ast.Name)}
                for k, s in self.rules}
        known = set(self.inputs) | set(rules)
        if any(not d <= known for d in deps.values()):
            raise InvalidProgram("unknown rule reference")
        done = set(self.inputs)
        ordered = []
        while len(ordered) < len(rules):
            ready = [k for k in rules if k not in done and deps[k] <= done]
            if not ready:
                raise InvalidProgram("cyclic rule dependency")
            ordered.extend(ready)
            done.update(ready)
        return tuple(ordered)

    def run(self, values: Mapping[str, bool]) -> dict[str, bool]:
        if set(values) != set(self.inputs) or any(type(v) is not bool for v in values.values()):
            raise InvalidProgram("provide exactly the declared Boolean inputs")
        env = dict(values)
        rules = dict(self.rules)
        for k in self.order():
            env[k] = evaluate(expression(rules[k]), env)
        return {k: env[k] for k, _ in self.rules}

    def digest(self) -> str:
        payload = json.dumps([self.inputs, self.rules], separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

    def patched(self, replacements: Mapping[str, str]) -> Program:
        if not replacements or not set(replacements) <= set(dict(self.rules)):
            raise InvalidProgram("patch must replace existing rules")
        return Program(self.inputs, tuple((k, replacements.get(k, s)) for k, s in self.rules))

    def lower_python(self, function_name: str = "policy") -> str:
        if not function_name.isidentifier() or keyword.iskeyword(function_name):
            raise InvalidProgram("invalid function name")
        rules = dict(self.rules)
        lines = [f"def {function_name}({', '.join(self.inputs)}):"]
        lines.extend(f"    {k} = {ast.unparse(expression(rules[k]))}" for k in self.order())
        output = ", ".join(k for k, _ in self.rules)
        if len(self.rules) == 1:
            output += ","
        lines.append(f"    return ({output})")
        return "\n".join(lines) + "\n"


def parse_lattice_patch(source: str) -> dict[str, str]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise InvalidProgram("expected rule = Boolean expression") from exc
    patch = {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            raise InvalidProgram("expected rule = Boolean expression")
        name = node.targets[0].id
        if name in patch:
            raise InvalidProgram("duplicate patch target")
        rhs = ast.unparse(node.value)
        expression(rhs)
        patch[name] = rhs
    return patch


def parse_python_patch(source: str) -> dict[str, str]:
    """Strong baseline: a conventional Python dictionary of rule expressions."""
    try:
        node = ast.parse(source, mode="eval").body
    except SyntaxError as exc:
        raise InvalidProgram("expected a Python expression dictionary") from exc
    if not isinstance(node, ast.Dict):
        raise InvalidProgram("expected a Python expression dictionary")
    patch = {}
    for k, v in zip(node.keys, node.values):
        if not isinstance(k, ast.Constant) or type(k.value) is not str or k.value in patch:
            raise InvalidProgram("invalid or duplicate dictionary key")
        rhs = ast.unparse(v)
        expression(rhs)
        patch[k.value] = rhs
    return patch


def cases(inputs: tuple[str, ...]):
    for bits in itertools.product((False, True), repeat=len(inputs)):
        yield dict(zip(inputs, bits))


def verify(before: Program, after: Program, target: Program,
           allowed_outputs: set[str]) -> dict:
    """Check all input combinations, including propagated dependency effects.

    Frame check: outputs outside allowed_outputs equal the prior program.
    Intent check: every output equals the independently supplied target.
    No state is committed on rejection. The model cannot edit this contract.
    """
    schemas = lambda p: (p.inputs, tuple(k for k, _ in p.rules))
    if schemas(before) != schemas(after) or schemas(before) != schemas(target):
        raise InvalidProgram("schema changes require a separate contract")
    if not allowed_outputs <= set(dict(before.rules)):
        raise InvalidProgram("unknown allowed output")
    checked = 0
    for values in cases(before.inputs):
        old, new, expected = before.run(values), after.run(values), target.run(values)
        checked += 1
        for k in old:
            kind = None
            if k not in allowed_outputs and new[k] != old[k]:
                kind = "regression"
            elif new[k] != expected[k]:
                kind = "intent_mismatch"
            if kind:
                return {"ok": False, "checked_inputs": checked,
                        "witness": {"kind": kind, "input": values, "output": k,
                                    "old": old[k], "got": new[k], "expected": expected[k]}}
    return {"ok": True, "checked_inputs": checked, "witness": None,
            "before_sha256": before.digest(), "after_sha256": after.digest(),
            "contract_sha256": target.digest()}


def admit(before: Program, proposed: Program, target: Program,
          allowed_outputs: set[str]) -> tuple[Program, dict]:
    result = verify(before, proposed, target, allowed_outputs)
    return (proposed if result["ok"] else before), result
