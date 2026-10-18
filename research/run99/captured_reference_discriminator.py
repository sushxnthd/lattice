"""Run99: exact historical-capture collision, using Lattice's real compiler.

All eight instances have identical current unversioned sources and request.
Their captured historical versions differ. The full graph and lowered Python
both retain the distinguishing information. This is NOT a model comparison.
"""
from __future__ import annotations
import ast
import itertools
import json
from lattice.semantic_edits import Program
from lattice.framed_edits import FramedProgram

INPUTS = ("a", "b", "c")
OLD_MEMOS = (
    "a and b", "a and not b", "not a and b", "not (a and b)",
    "a or b", "a or not b", "not a or b", "not (a or b)",
)
REQUEST = "Set decision to the historical memo predicate captured by archive, preserving all other outputs."
AUTHORITY = ("decision",)


def evaluate(source, env):
    """Independent, no-eval Boolean interpreter."""
    def walk(n):
        if isinstance(n, ast.Name): return env[n.id]
        if isinstance(n, ast.Constant) and type(n.value) is bool: return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not): return not walk(n.operand)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.And): return all(map(walk, n.values))
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or): return any(map(walk, n.values))
        raise ValueError("unsupported")
    return walk(ast.parse(source, mode="eval").body)


def cases():
    for bits in itertools.product((False, True), repeat=3):
        yield dict(zip(INPUTS, bits))


def instance(old):
    before = FramedProgram.from_program(Program(INPUTS, (
        ("decision", "a"), ("memo", old),
        ("archive", "memo and c"), ("audit", "decision or c"),
    )))
    return before.edit({"memo": "a or b"}, {"memo"})


def witness():
    programs = [instance(old) for old in OLD_MEMOS]
    assert len({tuple(p.sources) for p in programs}) == 1
    assert len({p.lower_python() for p in programs}) == 8
    assert len({json.dumps(p.context(), sort_keys=True) for p in programs}) == 8
    truth_tables = [[evaluate(old, env) for env in cases()] for old in OLD_MEMOS]
    assert len({tuple(t) for t in truth_tables}) == 8
    matrix = []
    for proposal in OLD_MEMOS:
        row = []
        for old, p in zip(OLD_MEMOS, programs):
            changed = p.edit({"decision": proposal}, {"decision"})
            good = True
            for env in cases():
                prior, actual = p.run(env), changed.run(env)
                if actual["decision"] != evaluate(old, env): good = False
                if any(actual[k] != prior[k] for k in prior if k != "decision"):
                    raise AssertionError("protected output changed")
                if prior["archive"] != (evaluate(old, env) and env["c"]):
                    raise AssertionError("captured memo changed")
            row.append(good)
        matrix.append(row)
    assert all(sum(row) == 1 for row in matrix)
    # At c=False, archive masks every old memo despite distinct target values.
    mask = {"a": True, "b": True, "c": False}
    assert all(p.run(mask)["archive"] is False for p in programs)
    assert len({evaluate(old, mask) for old in OLD_MEMOS}) == 2
    return {
        "claim": "Unversioned current sources are non-injective with respect to captured historical semantics.",
        "request": REQUEST, "authority": list(AUTHORITY),
        "instances": 8, "oracle_evaluations": 512,
        "unversioned_source_signatures": 1,
        "distinct_graph_views": 8, "distinct_python_views": 8,
        "historical_truth_tables": dict(zip(OLD_MEMOS, truth_tables)),
        "single_blind_patch_success_upper_bound": 0.125,
        "success_matrix": matrix, "model_calls": 0,
        "representation_specific_advantage": False,
        "unseen_prediction": "The collision disappears when old captured versions are extensionally identical or no historical capture exists.",
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
