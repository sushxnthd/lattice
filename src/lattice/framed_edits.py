"""Versioned rule DAG: protected outputs keep their prior meaning by construction.

Scope is a trusted caller input, not model-generated authority. This compiler
enforces a frame, not correctness of the requested changed behavior. It uses no
target oracle. Ordinary Python can call this compiler too; a new syntax is not
required to obtain the guarantee.
"""
from __future__ import annotations
from dataclasses import dataclass
import ast
from .semantic_edits import Program, InvalidProgram, expression, evaluate


@dataclass(frozen=True)
class BoundRule:
    source: str
    # Each reference captures a specific old/new version, not a mutable name.
    bindings: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class FramedProgram:
    inputs: tuple[str, ...]
    nodes: tuple[BoundRule, ...]
    roots: tuple[tuple[str, int], ...]
    sources: tuple[tuple[str, str], ...]

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
