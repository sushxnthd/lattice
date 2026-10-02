"""Prospective diagnostic after exp002 0.5B hit a floor in every condition.

Frozen 2x2 prompt ablation. Same held-out first edits and same model; not a new
held-out estimate of Lattice superiority. No adaptive task exclusion.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path

spec = importlib.util.spec_from_file_location("exp002", Path(__file__).parents[1] / "exp002/sequential_edits.py")
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
CONDITIONS = ("original", "request_last", "alias_example", "both")
MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"


def change_prompt(original, request, names, condition):
    p = original
    if condition in ("request_last", "both"):
        p = p.replace(f"REQUEST:\n{request}\n", "")
        p += f"\nCURRENT EDIT REQUEST (implement this change):\n{request}\nReturn only the updated code in the specified format.\n"
    if condition in ("alias_example", "both"):
        p = p.replace("auth and not blocked", f"{names[0]} and not {names[2]}")
    return p


def main():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(min(4, os.cpu_count() or 2))
    tok = AutoTokenizer.from_pretrained(MODEL); tok.padding_side = "left"
    if tok.pad_token_id is None: tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
    tasks = E.ALIASES[2:5]  # Every semantic family, fixed before this run.
    manifest = {"conditions": CONDITIONS, "tasks": tasks, "arms": E.ARMS,
                "model": MODEL, "max_new_tokens": E.MAX_NEW_TOKENS, "attempts": 1,
                "diagnostic_only": True,
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    prepared = []
    for condition in CONDITIONS:
        for arm in E.ARMS:
            for row in tasks:
                split, domain, current, steps, family = E.scenario(row)
                brief = f"Initial rules: {dict(current.rules)}. Rules describe output values, with dependency references evaluated using current values."
                if arm == "python_full": current = E.PythonPolicy(current.lower_python(), current.inputs)
                request, _, allowed = steps[0]
                p = E.prompt(arm, current, brief, request)
                p = change_prompt(p, request, current.inputs, condition)
                t = {"arm": arm, "split": split, "domain": domain,
                     "current": current, "family": family, "allowed": allowed}
                prepared.append((condition, t, p))
    rows = []
    for start in range(0, len(prepared), 4):
        batch = prepared[start:start+4]
        results = E.generate_batch(model, tok, [p for _, _, p in batch])
        for (condition, t, p), (raw, it, ot, seconds) in zip(batch, results):
            _, result = E.assess(t, raw, 1)
            rows.append({"condition": condition, "arm": t["arm"], "domain": t["domain"],
                         "prompt": p, "raw": raw, "input_tokens": it, "output_tokens": ot,
                         "generation_seconds": seconds, **result})
        print(f"batch={start//4+1}/9", flush=True)
    summary = {c: {a: {"correct": sum(r["ok"] for r in rows if r["condition"] == c and r["arm"] == a),
                      "total": 3, "invalid": sum("error" in r for r in rows if r["condition"] == c and r["arm"] == a)}
                   for a in E.ARMS} for c in CONDITIONS}
    out = {"manifest": manifest, "manifest_sha256": digest, "summary": summary, "rows": rows,
           "claim_boundary": "Post-pilot prospective prompt diagnostic on previously evaluated tasks; not untouched holdout or a general language comparison."}
    Path("artifacts/exp003").mkdir(parents=True, exist_ok=True)
    Path("artifacts/exp003/prompt_order.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("RESULT_SUMMARY " + json.dumps(summary), flush=True)


if __name__ == "__main__": main()
