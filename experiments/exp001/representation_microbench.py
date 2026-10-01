"""Frozen representation microbenchmark for Experiment 001.

This is an exploratory gate, not the final long-horizon benchmark. It holds the
model and semantic facts fixed while changing only their representation.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
FORMATS = ("code", "prose", "graph", "lattice")

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
            "entity": entity,
            "transition": [s0, s1],
            "owner": owner,
            "outsider": outsider,
            "resource": resource,
            "metric": metric,
            "min_metric": 0,
            "dependency": [f"{resource}_publish", "authorization"],
        }
        proposals = [
            ("valid_transition", "ALLOW", {"transition": [s0, s1], "metric": i + 1}),
            ("valid_owner_write", "ALLOW", {"permission": [owner, "write", resource], "metric": i}),
            ("valid_metric", "ALLOW", {"metric": i + 2}),
            ("drop_commitment", "REJECT", {"drop": spec["commitment"], "metric": i}),
            ("illegal_transition", "REJECT", {"transition": [s1, s0], "metric": i}),
            ("permission_broadening", "REJECT", {"permission": [outsider, "write", resource], "metric": i}),
            ("dependency_removal", "REJECT", {"remove_dependency": spec["dependency"], "metric": i}),
            ("invariant_failure", "REJECT", {"metric": -1}),
        ]
        for kind, label, proposal in proposals:
            tasks.append({
                "id": f"{i:02d}-{kind}",
                "label": label,
                "kind": kind,
                "spec": spec,
                "proposal": proposal,
            })
    return tasks

def render(task, fmt):
    s, p = task["spec"], task["proposal"]
    if fmt == "code":
        context = f"""PROTECTED = {{\"{s['commitment']}\"}}
TRANSITIONS = {{(\"{s['entity']}\", \"{s['transition'][0]}\", \"{s['transition'][1]}\")}}
PERMISSIONS = {{(\"{s['owner']}\", \"write\", \"{s['resource']}\")}}
PROTECTED_DEPENDENCIES = {{(\"{s['dependency'][0]}\", \"{s['dependency'][1]}\")}}
MINIMUM = {{\"{s['metric']}\": {s['min_metric']}}}
proposal = {json.dumps(p, sort_keys=True)}
"""
    elif fmt == "prose":
        bits = [
            f"The commitment {s['commitment']} is protected and must not be removed.",
            f"{s['entity']} may transition from {s['transition'][0]} to {s['transition'][1]}, but not in reverse.",
            f"Only {s['owner']} may write {s['resource']}; {s['outsider']} may not be granted write access.",
            f"{s['dependency'][0]} must retain its dependency on {s['dependency'][1]}.",
            f"{s['metric']} must always be at least {s['min_metric']}.",
            "Proposed change: " + json.dumps(p, sort_keys=True),
        ]
        context = " ".join(bits)
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
                {"type": "must_depend_on", "source": s["dependency"][0], "target": s["dependency"][1]},
            ],
            "proposal": p,
        }, sort_keys=True)
    elif fmt == "lattice":
        proposal_lines = []
        if "drop" in p:
            proposal_lines.append(f"drop commitment {p['drop']}")
        if "transition" in p:
            proposal_lines.append(f"transition {s['entity']} {p['transition'][0]} -> {p['transition'][1]}")
        if "permission" in p:
            proposal_lines.append(f"grant {p['permission'][0]} {p['permission'][1]} {p['permission'][2]}")
        if "remove_dependency" in p:
            proposal_lines.append(f"remove dependency {p['remove_dependency'][0]} -> {p['remove_dependency'][1]}")
        proposal_lines.append(f"set {s['metric']} = {p.get('metric', s['min_metric'])}")
        context = f"""commit {s['commitment']} protected
state {s['entity']} {{ {s['transition'][0]} -> {s['transition'][1]} }}
permit {s['owner']} write {s['resource']}
forbid {s['outsider']} write {s['resource']}
require {s['dependency'][0]} -> {s['dependency'][1]}
invariant {s['metric']} >= {s['min_metric']}
change {{
  """ + "\n  ".join(proposal_lines) + "\n}"
    else:
        raise ValueError(fmt)

    return (
        "You are reviewing a software change against the project's existing requirements. "
        "All listed requirements are binding. Decide whether the proposed change preserves every requirement. "
        "Answer exactly ALLOW or REJECT and nothing else.\n\n" + context
    )

def label_score(model, tokenizer, prompt, label):
    rendered = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=False,
        add_generation_prompt=True,
    )
    prompt_ids = tokenizer(rendered, add_special_tokens=False, return_tensors="pt").input_ids
    label_ids = tokenizer(label, add_special_tokens=False, return_tensors="pt").input_ids
    ids = torch.cat([prompt_ids, label_ids], dim=1)
    with torch.no_grad():
        logits = model(ids).logits
    start = prompt_ids.shape[1] - 1
    lp = torch.log_softmax(logits[:, start:start + label_ids.shape[1], :], dim=-1)
    score = lp.gather(2, label_ids.unsqueeze(-1)).sum().item()
    return score, prompt_ids.shape[1]

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
        for task in tasks:
            prompt = render(task, fmt)
            allow, n_tokens = label_score(model, tokenizer, prompt, "ALLOW")
            reject, _ = label_score(model, tokenizer, prompt, "REJECT")
            pred = "ALLOW" if allow > reject else "REJECT"
            rows.append({
                "format": fmt,
                "task_id": task["id"],
                "kind": task["kind"],
                "gold": task["label"],
                "pred": pred,
                "correct": pred == task["label"],
                "prompt_tokens": n_tokens,
                "margin": abs(allow - reject),
            })

    summary = {}
    for fmt in FORMATS:
        subset = [r for r in rows if r["format"] == fmt]
        correct = sum(r["correct"] for r in subset)
        summary[fmt] = {
            "n": len(subset),
            "accuracy": correct / len(subset),
            "correct": correct,
            "mean_prompt_tokens": sum(r["prompt_tokens"] for r in subset) / len(subset),
            "mean_margin": sum(r["margin"] for r in subset) / len(subset),
            "by_kind": {},
        }
        for kind in sorted({r["kind"] for r in subset}):
            kr = [r for r in subset if r["kind"] == kind]
            summary[fmt]["by_kind"][kind] = {
                "n": len(kr),
                "accuracy": sum(r["correct"] for r in kr) / len(kr),
            }

    out = {
        "model": MODEL,
        "deterministic": True,
        "task_manifest_sha256": manifest_sha256,
        "task_count": len(tasks),
        "summary": summary,
        "rows": rows,
        "claim_boundary": (
            "Exploratory representation-comprehension microbenchmark only. "
            "It does not establish long-horizon repository-level coding superiority."
        ),
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/representation_microbench.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"manifest": manifest_sha256, "summary": summary}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
