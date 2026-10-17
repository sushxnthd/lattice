"""Matched-information prompt generator and pre-inference token gate for Run79."""
import hashlib
import json
from pathlib import Path
from lattice.semantic_edits import Program
from lattice.framed_edits import FramedProgram
from research.run79.independent_scoring import load_tasks

TOKENIZER = "Qwen/Qwen2.5-Coder-7B-Instruct"

def prompt(task, arm):
    before = FramedProgram.from_program(Program(tuple(task["inputs"]), tuple(task["rules"].items())))
    facts = {"inputs": task["inputs"], "rules": task["rules"], "allowed": task["allowed"],
             "captured_dependencies": before.context()}
    common = ("Repair this bounded Boolean policy. Only the authorized output may change. "
              "The compiler and verifier are identical for all candidates.\n"
              "Policy facts: " + json.dumps(facts, sort_keys=True) + "\n"
              "Requested change: " + task["request"] + "\n")
    if arm == "python":
        suffix = ("Return exactly one Python dictionary expression of authorized output "
                  "to Boolean expression, e.g. {'read': a and b}. No commentary.")
    elif arm == "ir":
        suffix = ("Return exactly one semantic-IR assignment of authorized output "
                  "to Boolean expression, e.g. read = a and b. No commentary.")
    else:
        raise ValueError(arm)
    return common + suffix

def paired_prompts():
    return {task["id"]: {arm: prompt(task, arm) for arm in ("python", "ir")}
            for task in load_tasks()}

def gate(out):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(TOKENIZER)
    pairs = paired_prompts()
    counts = {}
    for task, pair in pairs.items():
        n = {}
        for arm, text in pair.items():
            chat = tok.apply_chat_template([{"role": "user", "content": text}],
                                          tokenize=False, add_generation_prompt=True)
            n[arm] = len(tok(chat, add_special_tokens=False).input_ids)
        gap = abs(n["python"] - n["ir"]) / max(n.values())
        counts[task] = {"tokens": n, "relative_gap": gap, "pass": gap <= .05}
    report = {"tokenizer": TOKENIZER, "counts": counts,
              "pass": all(x["pass"] for x in counts.values())}
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompts.json").write_text(json.dumps(pairs, sort_keys=True, indent=2))
    (out / "token_gate.json").write_text(json.dumps(report, sort_keys=True, indent=2))
    if not report["pass"]:
        raise RuntimeError("TOKEN_GATE_FAILED_BEFORE_MODEL_INFERENCE")
    return report
