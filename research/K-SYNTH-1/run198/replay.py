"""Independent exhaustive replay of unchanged Run186 frozen public contexts.

This is compiler correctness evidence, not new capable-model inference.
Run from repository root after installing lattice-research:
  python research/K-SYNTH-1/run198/replay.py --public /path/to/frozen/public.json
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path
from lattice.framed_edits import FramedProgram, BoundRule
from lattice.epoch_editor import EpochEditor

EXPECTED_PUBLIC_SHA = "75a29941a8802ab6b1c8a55e501d25e2273267839eb965fe303698d164c0cc94"


@lru_cache(maxsize=None)
def parsed(source):
    return ast.parse(source, mode="eval")


def independent_expr(source, env):
    def visit(n):
        if isinstance(n, ast.Expression):
            return visit(n.body)
        if isinstance(n, ast.Name):
            return env[n.id]
        if isinstance(n, ast.Constant) and type(n.value) is bool:
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return not visit(n.operand)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.And):
            return all(visit(v) for v in n.values)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
            return any(visit(v) for v in n.values)
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitXor):
            return visit(n.left) != visit(n.right)
        if isinstance(n, ast.IfExp):
            return visit(n.body) if visit(n.test) else visit(n.orelse)
        raise ValueError(type(n).__name__)
    return visit(parsed(source))


def independent_frame(frame, values):
    computed = []
    for node in frame.nodes:
        env = dict(values)
        env.update({name: computed[index] for name, index in node.bindings})
        computed.append(independent_expr(node.source, env))
    return {name: computed[index] for name, index in frame.roots}


def reconstruct(task):
    context = task["context"]
    nodes = tuple(BoundRule(n["expression"], tuple(sorted(n["references"].items())))
                  for n in context["nodes"])
    roots = tuple(context["roots"].items())
    sources = tuple((name, nodes[index].source) for name, index in roots)
    return FramedProgram(tuple(context["inputs"]), nodes, roots, sources)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("run198_raw.jsonl"))
    args = parser.parse_args()
    public = args.public.read_bytes()
    assert hashlib.sha256(public).hexdigest() == EXPECTED_PUBLIC_SHA
    tasks = json.loads(public)
    assert len(tasks) == 258
    comparisons = 0
    with args.out.open("w") as handle:
        for task in tasks:
            before = reconstruct(task)
            editor = EpochEditor(before)
            genesis = editor.tip
            editor.edit({"gate": "not h0_gate"}, {"gate", "endpoint"}, editor.tip)
            editor.edit({"gate": "h0_gate and h1_gate"}, {"gate", "endpoint"}, editor.tip)
            editor.edit({"gate": "h1_gate or h0_gate"}, {"gate", "endpoint"}, editor.tip)
            assert editor.verify(pinned_genesis=genesis, pinned_tip=editor.tip)
            for bits in itertools.product((False, True), repeat=len(before.inputs)):
                values = dict(zip(before.inputs, bits))
                original = independent_frame(before, values)
                for epoch in range(4):
                    frame = editor.at(epoch)
                    independent = independent_frame(frame, values)
                    if bits[0] == bits[1] == bits[2]:
                        assert frame.run(values) == independent
                    assert independent["audit"] == original["audit"]
                    assert independent["gate"] == (
                        original["gate"] if epoch == 0 else
                        not original["gate"] if epoch == 1 else
                        False if epoch == 2 else True)
                    assert independent["endpoint"] == (
                        original["endpoint"] if epoch == 0 else independent["gate"])
                    handle.write(json.dumps({
                        "task": task["id"], "epoch": epoch,
                        "input_bits": "".join("1" if x else "0" for x in bits),
                        "outputs": independent, "tip": editor.records[epoch].history
                    }, sort_keys=True) + "\n")
                    comparisons += len(frame.roots)
    summary = {
        "source_public_sha256": EXPECTED_PUBLIC_SHA, "tasks": len(tasks),
        "epoch_input_traces": len(tasks) * 4 * 64,
        "output_comparisons": comparisons,
        "raw_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
        "qualification": "synthetic compiler correctness, not model or independent-issue evidence"
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
