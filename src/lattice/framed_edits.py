"""Versioned rule DAG: protected outputs keep their prior meaning by construction.

Scope is a trusted caller input, not model-generated authority. This compiler
enforces a frame, not correctness of the requested changed behavior. It uses no
target oracle. Ordinary Python can call this compiler too; a new syntax is not
required to obtain the guarantee.
"""
from __future__ import annotations
from dataclasses import dataclass
import ast
import argparse
import json
import keyword
from pathlib import Path
from .semantic_edits import Program, InvalidProgram, expression, evaluate


@dataclass(frozen=True)
class BoundRule:
    source: str
    # Each reference captures a specific old/new version, not a mutable name.
    bindings: tuple[tuple[str, int], ...]

    def __post_init__(self):
        object.__setattr__(self, "bindings", tuple(tuple(b) for b in self.bindings))


@dataclass(frozen=True)
class FramedProgram:
    inputs: tuple[str, ...]
    nodes: tuple[BoundRule, ...]
    roots: tuple[tuple[str, int], ...]
    sources: tuple[tuple[str, str], ...]

    def __post_init__(self):
        # Serialized or directly constructed state must obey the same acyclic,
        # immutable representation invariant as compiler-created state.
        object.__setattr__(self, "inputs", tuple(self.inputs))
        object.__setattr__(self, "nodes", tuple(self.nodes))
        object.__setattr__(self, "roots", tuple(tuple(r) for r in self.roots))
        object.__setattr__(self, "sources", tuple(tuple(s) for s in self.sources))
        names = self.inputs + tuple(k for k, _ in self.roots)
        if len(set(names)) != len(names) or not all(type(n) is str and n.isidentifier() and not keyword.iskeyword(n) for n in names):
            raise InvalidProgram("invalid framed schema")
        if not self.roots or len(self.inputs) > 16:
            raise InvalidProgram("framed schema supports 1+ outputs and at most 16 Boolean inputs")
        for i, node in enumerate(self.nodes):
            if not isinstance(node, BoundRule): raise InvalidProgram("expected immutable bound rule")
            bindings = dict(node.bindings)
            if len(bindings) != len(node.bindings): raise InvalidProgram("duplicate binding")
            refs = {n.id for n in ast.walk(expression(node.source)) if isinstance(n, ast.Name)}
            if set(bindings) != refs - set(self.inputs): raise InvalidProgram("incomplete or extra binding")
            if any(type(j) is not int or not 0 <= j < i for j in bindings.values()):
                raise InvalidProgram("bindings must refer to earlier immutable nodes")
        if any(type(i) is not int or not 0 <= i < len(self.nodes) for _, i in self.roots):
            raise InvalidProgram("invalid output root")
        if tuple(k for k, _ in self.sources) != tuple(k for k, _ in self.roots):
            raise InvalidProgram("source/output schema mismatch")
        for (_, i), (_, s) in zip(self.roots, self.sources):
            if self.nodes[i].source != s: raise InvalidProgram("current source does not match bound root")

    @classmethod
    def from_program(cls, program: Program):
        sources = dict(program.rules)
        nodes = []
        ids = {}
        for name in program.order():
            refs = {n.id for n in ast.walk(expression(sources[name])) if isinstance(n, ast.Name)}
            bindings = tuple((ref, ids[ref]) for ref in sorted(refs) if ref in ids)
            ids[name] = len(nodes)
            nodes.append(BoundRule(sources[name], bindings))
        return cls(program.inputs, tuple(nodes), tuple((k, ids[k]) for k, _ in program.rules), program.rules)

    def run(self, values):
        if set(values) != set(self.inputs) or any(type(v) is not bool for v in values.values()):
            raise InvalidProgram("provide exactly the declared Boolean inputs")
        memo = {}
        def visit(idx):
            if idx not in memo:
                node = self.nodes[idx]
                env = dict(values)
                env.update((k, visit(j)) for k, j in node.bindings)
                memo[idx] = evaluate(expression(node.source), env)
            return memo[idx]
        return {k: visit(i) for k, i in self.roots}

    def edit(self, replacements: dict[str, str], allowed_outputs: set[str]):
        roots = dict(self.roots)
        if not replacements or not set(replacements) <= allowed_outputs <= set(roots):
            raise InvalidProgram("edit targets must be inside trusted output scope")
        sources = dict(self.sources)
        sources.update(replacements)
        dependencies = {}
        for k in allowed_outputs:
            refs = {n.id for n in ast.walk(expression(sources[k])) if isinstance(n, ast.Name)}
            if not refs <= set(self.inputs) | set(roots):
                raise InvalidProgram("unknown rule reference")
            dependencies[k] = refs
        # Protected references bind to prior roots. Authorized references bind to
        # the newly compiled version, including unchanged propagated outputs.
        nodes = list(self.nodes)
        ids = {k: i for k, i in self.roots if k not in allowed_outputs}
        done = set(self.inputs) | set(ids)
        ordered = [k for k, _ in self.roots if k in allowed_outputs]
        while any(k not in done for k in ordered):
            ready = [k for k in ordered if k not in done and dependencies[k] <= done]
            if not ready:
                raise InvalidProgram("cycle among changed output versions")
            for k in ready:
                bindings = tuple((ref, ids[ref]) for ref in sorted(dependencies[k]) if ref in ids)
                ids[k] = len(nodes)
                nodes.append(BoundRule(sources[k], bindings))
                done.add(k)
        return FramedProgram(self.inputs, tuple(nodes), tuple((k, ids[k]) for k, _ in self.roots),
                             tuple((k, sources[k]) for k, _ in self.sources))

    def lower_python(self):
        # Emit only the reachable closure; discarded versions do not inflate the
        # executable artifact. Node identities preserve captured dependencies.
        reachable = set()
        def visit(i):
            if i in reachable: return
            reachable.add(i)
            for _, j in self.nodes[i].bindings: visit(j)
        for _, i in self.roots: visit(i)
        # Use a prefix absent from input names to avoid generated-name capture.
        prefix = "_lattice_v"
        while any(n.startswith(prefix) for n in self.inputs): prefix = "_" + prefix
        lines = [f"def policy({', '.join(self.inputs)}):"]
        class Rewrite(ast.NodeTransformer):
            def __init__(self, bindings): self.bindings = dict(bindings)
            def visit_Name(self, node):
                if node.id in self.bindings:
                    return ast.copy_location(ast.Name(f"{prefix}{self.bindings[node.id]}", ast.Load()), node)
                return node
        for i in sorted(reachable):
            node = self.nodes[i]
            tree = Rewrite(node.bindings).visit(expression(node.source))
            lines.append(f"    {prefix}{i} = {ast.unparse(tree)}")
        values = ", ".join(f"{prefix}{i}" for _, i in self.roots)
        if len(self.roots) == 1: values += ","
        lines.append(f"    return ({values})")
        return "\n".join(lines) + "\n"

    def context(self):
        """Expose captured semantics rather than misleading unversioned sources."""
        return {"inputs": self.inputs, "roots": dict(self.roots),
                "nodes": [{"id": i, "expression": n.source, "references": dict(n.bindings)}
                          for i, n in enumerate(self.nodes)]}


def main():
    from .semantic_edits import parse_lattice_patch, cases
    parser = argparse.ArgumentParser(description="Compile a bounded Boolean policy edit with protected output versions")
    parser.add_argument("policy", type=Path, help="JSON containing inputs and rules")
    parser.add_argument("patch", type=Path, help="file of changed rule assignments")
    parser.add_argument("--allow", nargs="+", required=True, help="trusted authorized output names")
    parser.add_argument("--output", type=Path, required=True, help="generated Python file")
    args = parser.parse_args()
    raw = json.loads(args.policy.read_text())
    before = FramedProgram.from_program(Program(tuple(raw["inputs"]), tuple(raw["rules"].items())))
    after = before.edit(parse_lattice_patch(args.patch.read_text()), set(args.allow))
    pairs = 0
    for values in cases(before.inputs):
        old, new = before.run(values), after.run(values)
        for k in old:
            if k not in args.allow:
                assert old[k] == new[k]
                pairs += 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(after.lower_python())
    print(json.dumps({"output": str(args.output), "protected_pairs_checked": pairs,
                      "context": after.context()}, indent=2))


if __name__ == "__main__": main()
