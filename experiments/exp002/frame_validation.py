"""Validate frame compilation independently of LLM generation and intent oracle.

Conventional live-name graphs and framed graphs receive identical replacements.
This measures enforcement of an authorized output scope, not whether AI writes
correct requested features. A Python wrapper calling the framed compiler has
identical behavior and is an explicit equivalence control.
"""
from __future__ import annotations
import hashlib
import json
import random
from pathlib import Path
from lattice.semantic_edits import Program, cases
from lattice.framed_edits import FramedProgram

SEED = 202610021
CHAINS = 100
STEPS = 20


def main():
    rng = random.Random(SEED)
    rows = []
    for chain in range(CHAINS):
        base = Program(("auth", "owner", "blocked", "reviewed", "urgent", "paid"), (
            ("read", "auth and not blocked"),
            ("edit", "read and owner"),
            ("ship", "edit and reviewed"),
            ("export", "read and paid"),
            ("audit", "ship or export"),
        ))
        framed = FramedProgram.from_program(base)
        live = base
        for step in range(STEPS):
            # Acyclic but arbitrarily authorized single-output edits; effects
            # outside the authorized root must not silently propagate.
            output = rng.choice([k for k, _ in base.rules])
            index = [k for k, _ in base.rules].index(output)
            refs = list(base.inputs) + [k for k, _ in base.rules[:index]]
            x, y = rng.choice(refs), rng.choice(refs)
            source = f"({x} {rng.choice(['and', 'or'])} {y})"
            if rng.choice([False, True]): source = "not " + source
            replacement = {output: source}
            after_live = live.patched(replacement)
            after_framed = framed.edit(replacement, {output})
            # Same compiler called as a normal Python library: new syntax is
            # not necessary to obtain the preservation property.
            after_python_library = framed.edit(replacement, {output})
            scope = {"__builtins__": {}}
            lowered = after_framed.lower_python()
            exec(compile(lowered, "<trusted-lowering>", "exec"), scope)
            live_pairs = framed_pairs = lowering_mismatches = wrapper_mismatches = 0
            live_witness = None
            for values in cases(base.inputs):
                old_live, new_live = live.run(values), after_live.run(values)
                old_framed, new_framed = framed.run(values), after_framed.run(values)
                for k in old_live:
                    if k == output: continue
                    live_pairs += old_live[k] != new_live[k]
                    framed_pairs += old_framed[k] != new_framed[k]
                    if old_live[k] != new_live[k] and live_witness is None:
                        live_witness = {"input": values, "output": k,
                                        "old": old_live[k], "new": new_live[k]}
                lowering_mismatches += tuple(new_framed.values()) != scope["policy"](**values)
                wrapper_mismatches += new_framed != after_python_library.run(values)
            rows.append({"chain": chain, "step": step, "replacement": replacement,
                "allowed_outputs": [output], "live_graph_regression_pairs": live_pairs,
                "framed_regression_pairs": framed_pairs, "lowering_mismatches": lowering_mismatches,
                "python_library_mismatches": wrapper_mismatches, "live_witness": live_witness,
                "versioned_nodes": len(after_framed.nodes), "lowered_bytes": len(lowered.encode())})
            live, framed = after_live, after_framed
    summary = {
        "chains": CHAINS, "edits_per_chain": STEPS, "edits": len(rows),
        "inputs_per_edit": 64, "protected_output_pairs_per_edit": 256,
        "live_graph_edits_with_regressions": sum(r["live_graph_regression_pairs"] > 0 for r in rows),
        "live_graph_regression_pairs": sum(r["live_graph_regression_pairs"] for r in rows),
        "framed_edits_with_regressions": sum(r["framed_regression_pairs"] > 0 for r in rows),
        "framed_regression_pairs": sum(r["framed_regression_pairs"] for r in rows),
        "native_python_lowering_mismatches": sum(r["lowering_mismatches"] for r in rows),
        "python_library_mismatches": sum(r["python_library_mismatches"] for r in rows),
    }
    sources = [Path("src/lattice/framed_edits.py"), Path("experiments/exp002/frame_validation.py")]
    out = {"seed": SEED, "source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
           "summary": summary, "rows": rows,
           "claim_boundary": "Random bounded policy edits validate a scope-preserving compiler; not model-generated feature correctness or evidence for new-language superiority."}
    Path("artifacts/exp002/frame_validation.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
