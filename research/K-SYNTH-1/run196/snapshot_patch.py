"""One-transaction immutable snapshot-reference compiler adapter.

Aliases bind directly to pre-edit node IDs, not mutable root names.
Both IR and Python SSA arms use this identical compiler. This is NOT
yet a persistent multi-transaction epoch ledger.
"""
from __future__ import annotations
import ast
import keyword
from lattice.framed_edits import FramedProgram, BoundRule
from lattice.semantic_edits import InvalidProgram, expression


def snapshot_edit(frame: FramedProgram, replacements: dict[str, str],
                  allowed_outputs: set[str], aliases: dict[str, str]) -> FramedProgram:
    old_roots = dict(frame.roots)
    if not replacements or not set(replacements) <= allowed_outputs <= set(old_roots):
        raise InvalidProgram("untrusted or empty edit scope")
    if any(not name.isidentifier() or keyword.iskeyword(name) for name in aliases):
        raise InvalidProgram("invalid snapshot alias")
    if set(aliases) & (set(old_roots) | set(frame.inputs)):
        raise InvalidProgram("snapshot alias shadows an existing identifier")
    if not set(aliases.values()) <= set(old_roots):
        raise InvalidProgram("unknown snapshot root")
    # A future epoch-ledger implementation must preserve historical aliases
    # across multiple edits. Reject this unsupported case rather than guess.
    for _, old_source in frame.sources:
        if {n.id for n in ast.walk(expression(old_source)) if isinstance(n, ast.Name)} & set(aliases):
            raise InvalidProgram("snapshot-bearing input requires epoch-ledger compiler")
    sources = dict(frame.sources)
    sources.update(replacements)
    dependencies = {}
    for root in allowed_outputs:
        refs = {n.id for n in ast.walk(expression(sources[root])) if isinstance(n, ast.Name)}
        if not refs <= set(frame.inputs) | set(old_roots) | set(aliases):
            raise InvalidProgram("unknown patch reference")
        dependencies[root] = refs
    nodes = list(frame.nodes)
    ids = {k: v for k, v in frame.roots if k not in allowed_outputs}
    ids.update({alias: old_roots[target] for alias, target in aliases.items()})
    done = set(frame.inputs) | set(ids)
    order = [root for root, _ in frame.roots if root in allowed_outputs]
    while any(root not in done for root in order):
        ready = [root for root in order if root not in done and dependencies[root] <= done]
        if not ready:
            raise InvalidProgram("cycle among changed output versions")
        for root in ready:
            binds = tuple((name, ids[name]) for name in sorted(dependencies[root]) if name in ids)
            ids[root] = len(nodes)
            nodes.append(BoundRule(sources[root], binds))
            done.add(root)
    return FramedProgram(frame.inputs, tuple(nodes),
                         tuple((root, ids[root]) for root, _ in frame.roots),
                         tuple((root, sources[root]) for root, _ in frame.sources))
