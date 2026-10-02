"""Frozen representation microbenchmark for Experiment 001.

Exploratory gate: same model + same semantic facts, representation changes only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
FORMATS = ("code", "prose", "graph", "lattice")
BATCH_SIZE = 16

DOMAINS = [
    ("Document", "draft", "published", "owner", "viewer", "document", "revision"),
    ("Order", "pending", "paid", "merchant", "guest", "order", "amount"),
    ("Report", "private", "released", "author", "reader", "report", "version"),
    ("Ticket", "open", "closed", "agent", "visitor", "ticket", "priority"),
    ("Dataset", "staged", "approved", "curator", "anonymous", "dataset", "records"),
]

def build_tasks():
    tasks = []
    for i, (entity, s0, s1, owner, outsider, resource, metric) in enumerate(DOMAINS):
        spec = {
            "commitment": f"{resource}_protected",
            "entity": entity, "transition": [s0, s1],
            "owner": owner, "outsider": outsider, "resource": resource,
            "metric": metric, "min_metric": 0,
            "dependency": [f"{resource}_publish", "authorization"],
        }
        proposals = [
            ("valid_transition", "A", {"transition": [s0, s1], "metric": i + 1}),
            ("valid_owner_write", "A", {"permission": [owner, "write", resource], "metric": i}),
            ("valid_metric", "A", {"metric": i + 2}),
            ("drop_commitment", "R", {"drop": spec["commitment"], "metric": i}),
            ("illegal_transition", "R", {"transition": [s1, s0], "metric": i}),
            ("permission_broadening", "R", {"permission": [outsider, "write", resource], "metric": i}),
            ("dependency_removal", "R", {"remove_dependency": spec["dependency"], "metric": i}),
            ("invariant_failure", "R", {"metric": -1}),
        ]
        for kind, label, proposal in proposals:
            tasks.append({
                "id": f"{i:02d}-{kind}", "domain": i, "label": label,
                "kind": kind, "spec": spec, "proposal": proposal,
            })
    return tasks

def render(task, fmt):
    s, p = task["spec"], task["proposal"]
    if fmt == "code":
        context = f"""PROTECTED = {{\"{s['commitment']}\"}}
TRANSITIONS = {{(\"{s['entity']}\", \"{s['transition'][0]}\", \"{s['transition'][1]}\")}}
PERMISSIONS = {{(\"{s['owner']}\", \"write\", \"{s['resource']}\")}}
FORBIDDEN_PERMISSIONS = {{(\"{s['outsider']}\", \"write\", \"{s['resource']}\")}}
PROTECTED_DEPENDENCIES = {{(\"{s['dependency'][0]}\", \"{s['dependency'][1]}\")}}
MINIMUM = {{\"{s['metric']}\": {s['min_metric']}}}
proposal = {json.dumps(p, sort_keys=True)}"""
    elif fmt == "prose":
        context = " ".join([
            f"The commitment {s['commitment']} is protected and must not be removed.",
            f"{s['entity']} may transition from {s['transition'][0]} to {s['transition'][1]}, but not in reverse.",
            f"Only {s['owner']} may write {s['resource']}; {s['outsider']} must not be granted write access.",
            f"{s['dependency'][0]} must retain its dependency on {s['dependency'][1]}.",
            f"{s['metric']} must always be at least {s['min_metric']}.",
            "Proposed change: " + json.dumps(p, sort_keys=True),
        ])
    elif fmt == "graph":
        context = json.dumps({
            "nodes": [
                {"id": s["commitment"], "type": "protected_commitment"},
                {"id": s["entity"], "type": "state_machine"},
                {"id": s["owner"], "type": "role"},
                {"id": s["outsider"], "type": "role"},
                {"id": s["resource"], "type": "resource"},
                {"id": s["metric"], "type": "metric", "minimum": s["min_metric"]},
            ],
            "edges": [
                {"type": "legal_transition", "source": s["transition"][0], "target": s["transition"][1]},
                {"type": "may_write", "source": s["owner"], "target": s["resource"]},
                {"type": "may_not_write", "source": s["outsider"], "target": s["resource"]},
                {"type": "must_depend_on", "source": s["dependency"][0], "target": s["dependency"][1]},
            ],
            "proposal": p,
        }, sort_keys=True)
    elif fmt == "lattice":
        lines = []
        if "drop" in p: lines.append(f"drop commitment {p['drop']}")
        if "transition" in p: lines.append(f"transition {s['entity']} {p['transition'][0]} -> {p['transition'][1]}")
        if "permission" in p: lines.append(f"grant {p['permission'][0]} {p['permission'][1]} {p['permission'][2]}")
        if "remove_dependency" in p: lines.append(f"remove dependency {p['remove_dependency'][0]} -> {p['remove_dependency'][1]}")
        lines.append(f"set {s['metric']} = {p.get('metric', s['min_metric'])}")
        context = f"""commit {s['commitment']} protected
state {s['entity']} {{ {s['transition'][0]} -> {s['transition'][1]} }}
permit {s['owner']} write {s['resource']}
forbid {s['outsider']} write {s['resource']}
require {s['dependency'][0]} -> {s['dependency'][1]}
invariant {s['metric']} >= {s['min_metric']}
change {{
  """ + "\n  ".join(lines) + "\n}"
    else:
        raise ValueError(fmt)

    return (
        "Review this proposed software change against all binding project requirements. "
        "Output exactly A if every requirement is preserved, or R if any requirement is violated. "
        "Do not output anything else.\n\n" + context
    )

def score_prompts(model, tokenizer, prompts):
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    a_ids = tokenizer("A", add_special_tokens=False).input_ids
    r_ids = tokenizer("R", add_special_tokens=False).input_ids
    if len(a_ids) != 1 or len(r_ids) != 1:
        raise RuntimeError(f"Expected single-token labels, got A={a_ids}, R={r_ids}")
    a_id, r_id = a_ids[0], r_ids[0]
    outputs = []
    for start in range(0, len(prompts), BATCH_SIZE):
        batch = prompts[start:start+BATCH_SIZE]
        rendered = [
            tokenizer.apply_chat_template(
                [{"role": "user", "content": p}],
                tokenize=False, add_generation_prompt=True,
            )
            for p in batch
        ]
        toks = tokenizer(rendered, padding=True, return_tensors="pt", add_special_tokens=False)
        with torch.inference_mode():
            logits = model(**toks).logits[:, -1, :]
        pair = logits[:, [a_id, r_id]]
        probs = torch.softmax(pair, dim=-1)
        preds = torch.argmax(pair, dim=-1).tolist()
        lengths = toks["attention_mask"].sum(dim=1).tolist()
        for j, pred in enumerate(preds):
            outputs.append({
                "pred": "A" if pred == 0 else "R",
                "confidence": float(probs[j, pred].item()),
                "prompt_tokens": int(lengths[j]),
            })
    return outputs

def summarize(rows, domains):
    result = {}
    for fmt in FORMATS:
        subset = [r for r in rows if r["format"] == fmt and r["domain"] in domains]
        result[fmt] = {
            "n": len(subset),
            "correct": sum(r["correct"] for r in subset),
            "accuracy": sum(r["correct"] for r in subset) / len(subset),
            "mean_prompt_tokens": sum(r["prompt_tokens"] for r in subset) / len(subset),
            "mean_confidence": sum(r["confidence"] for r in subset) / len(subset),
        }
    return result

def main():
    torch.set_num_threads(2)
    tasks = build_tasks()
    manifest = json.dumps(tasks, sort_keys=True, separators=(",", ":")).encode()
    manifest_sha256 = hashlib.sha256(manifest).hexdigest()

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    model.eval()

    rows = []
    for fmt in FORMATS:
        prompts = [render(task, fmt) for task in tasks]
        scored = score_prompts(model, tokenizer, prompts)
        for task, result in zip(tasks, scored):
            rows.append({
                "format": fmt, "task_id": task["id"], "domain": task["domain"],
                "kind": task["kind"], "gold": task["label"],
                **result, "correct": result["pred"] == task["label"],
            })

    dev = summarize(rows, {0, 1, 2})
    holdout = summarize(rows, {3, 4})
    selected = max(
        FORMATS,
        key=lambda f: (dev[f]["accuracy"], -dev[f]["mean_prompt_tokens"], f),
    )

    by_kind = {}
    for fmt in FORMATS:
        by_kind[fmt] = {}
        for kind in sorted({r["kind"] for r in rows}):
            sub = [r for r in rows if r["format"] == fmt and r["kind"] == kind]
            by_kind[fmt][kind] = sum(r["correct"] for r in sub) / len(sub)

    out = {
        "model": MODEL,
        "deterministic": True,
        "task_manifest_sha256": manifest_sha256,
        "task_count": len(tasks),
        "development_domains": [0, 1, 2],
        "holdout_domains": [3, 4],
        "development": dev,
        "holdout": holdout,
        "selected_on_development": selected,
        "selected_holdout_accuracy": holdout[selected]["accuracy"],
        "by_kind": by_kind,
        "rows": rows,
        "claim_boundary": (
            "Exploratory representation-comprehension microbenchmark. "
            "Selection is among four hand-designed encodings. "
            "This does not establish repository-level coding superiority."
        ),
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/representation_microbench.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "manifest": manifest_sha256,
        "development": dev,
        "holdout": holdout,
        "selected_on_development": selected,
        "selected_holdout_accuracy": holdout[selected]["accuracy"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
