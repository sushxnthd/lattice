"""Independent, non-executing semantic-rename contract evaluator (Run217).

This is a *necessary* static contract, not a proof of behavioral equivalence.
Never replace functional tests with this evaluator. It rejects stale references,
including references in unreachable code that ordinary smoke tests miss.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class ContractResult:
    passed: bool
    failures: tuple[str, ...]

def check_rename_contract(files: Mapping[str, bytes], *,
                          definition_path: str, old: str, new: str,
                          required_calls: Mapping[str, str] | None = None) -> ContractResult:
    failures: list[str] = []
    if definition_path not in files:
        return ContractResult(False, ("definition file missing",))
    trees: dict[str, ast.AST] = {}
    for path, source in sorted(files.items()):
        if not path.endswith(".py"):
            continue
        try:
            trees[path] = ast.parse(source.decode("utf-8"), filename=path)
        except (UnicodeError, SyntaxError) as exc:
            failures.append(f"{path}: invalid source: {exc}")
    if definition_path not in trees:
        failures.append("definition file not parseable")
    else:
        definitions = [node.name for node in trees[definition_path].body
                       if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        if new not in definitions:
            failures.append("new public definition absent")
        if old in definitions:
            failures.append("old public definition still exported")
    for path, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == old:
                failures.append(f"{path}:{node.lineno}: stale name {old}")
            elif isinstance(node, ast.Attribute) and node.attr == old:
                failures.append(f"{path}:{node.lineno}: stale attribute {old}")
            elif isinstance(node, ast.ImportFrom):
                if any(alias.name == old for alias in node.names):
                    failures.append(f"{path}:{node.lineno}: stale import {old}")
    for path, target in (required_calls or {}).items():
        tree = trees.get(path)
        if tree is None:
            failures.append(f"{path}: required consumer absent")
            continue
        found = any(isinstance(node, ast.Call) and
                    ((isinstance(node.func, ast.Name) and node.func.id == target) or
                     (isinstance(node.func, ast.Attribute) and node.func.attr == target))
                    for node in ast.walk(tree))
        if not found:
            failures.append(f"{path}: required call {target} absent")
    return ContractResult(not failures, tuple(failures))
