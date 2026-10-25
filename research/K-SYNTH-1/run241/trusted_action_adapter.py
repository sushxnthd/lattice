"""Trusted action adapter for Lattice Run241.

Models emit only selector and content. Paths and source hashes are derived
from immutable facts, not copied from model-generated strings.

Post-hoc use on Run240 completions is diagnostic, not model success.
"""
from __future__ import annotations

import ast
import textwrap


class ContractError(ValueError):
    pass


def declarations(source: str):
    tree = ast.parse("class _Container:\n" + textwrap.indent(textwrap.dedent(source), "    "))
    return [(node.name, type(node).__name__) for node in tree.body[0].body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]


def project_and_validate(facts: dict, output: dict):
    known = {b["selector"]: b for b in facts["blocks"]}
    if set(output) != {"actions"} or not isinstance(output["actions"], list):
        raise ContractError("bad envelope")
    if not 1 <= len(output["actions"]) <= 3:
        raise ContractError("bad action count")
    result = []
    seen = set()
    for index, action in enumerate(output["actions"]):
        if not {"selector", "content"} <= set(action):
            raise ContractError(f"action {index}: missing selector/content")
        selector = action["selector"]
        if selector in seen:
            raise ContractError(f"action {index}: duplicate selector")
        seen.add(selector)
        target = known.get(selector)
        if target is None or target["authority"] != "editable":
            raise ContractError(f"action {index}: unauthorized selector")
        if target["kind"] == "method":
            try:
                before = declarations(target["code"])
                after = declarations(action["content"])
            except SyntaxError as exc:
                raise ContractError(f"action {index}: invalid syntax: {exc}") from exc
            if not all(name in after for name in before):
                raise ContractError(f"action {index}: declaration erased")
        elif target["kind"] == "assignment":
            try:
                parsed = ast.parse(action["content"])
            except SyntaxError as exc:
                raise ContractError(f"action {index}: invalid syntax: {exc}") from exc
            if not any(isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == target["name"]
                               for t in n.targets)
                       for n in parsed.body):
                raise ContractError(f"action {index}: assignment erased")
        result.append({"selector": selector, "content": action["content"],
                       "path": target["path"],
                       "file_sha256": facts["file_sha256"][target["path"]]})
    return {"actions": result}
