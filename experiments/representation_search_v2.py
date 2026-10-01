"""Representation Search v2: balanced four-way semantic-choice benchmark.

The representation is selected using opened development domains only. The
holdout domains were frozen before this script was executed. Every question has
four options, exactly one semantics-preserving choice, and balanced answer
positions to remove binary class-prior shortcuts exposed by v0/v1.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
CANDIDATES = ("prose", "explicit_nl", "decision_table", "violation_normal")
BATCH_SIZE = 24
LABELS = ("1", "2", "3", "4")

DEV = [
    ("Document", "draft", "published", "owner", "viewer", "document", "revision"),
    ("Order", "pending", "paid", "merchant", "guest", "order", "amount"),
    ("Report", "private", "released", "author", "reader", "report", "version"),
    ("Ticket", "open", "closed", "agent", "visitor", "ticket", "priority"),
    ("Dataset", "staged", "approved", "curator", "anonymous", "dataset", "records"),
    ("Shipment", "queued", "dispatched", "courier", "guest", "shipment", "packages"),
    ("Account", "unverified", "verified", "admin", "anonymous", "account", "quota"),
    ("Experiment", "planned", "running", "scientist", "observer", "experiment", "samples"),
]

# Frozen before v2 execution; none appeared in v0/v1.
HOLDOUT = [
    ("Pipeline", "created", "validated", "maintainer", "guest", "pipeline", "retries"),
    ("Workspace", "private", "shared", "owner", "viewer", "workspace", "seats"),
    ("Invoice", "draft", "sent", "accountant", "guest", "invoice", "total"),
    ("Release", "candidate", "stable", "releaser", "anonymous", "release", "version"),
]


def domain_spec(row):
    entity, s0, s1, owner, outsider, resource, metric = row
    return {
        "commitment": f"{resource}_protected",
        "entity": entity,
        "s0": s0,
        "s1": s1,
        "owner": owner,
        "outsider": outsider,
        "resource": resource,
        "metric": metric,
        "minimum": 0,
        "dependency": [f"{resource}_publish", "authorization"],
    }


def action_pool(s):
    valid = {
        "legal_transition": f"transition {s['entity']} from {s['s0']} to {s['s1']}",
        "owner_write": f"grant {s['owner']} write access to {s['resource']}",
        "positive_metric": f"set {s['metric']} to 2",
        "boundary_metric": f"set {s['metric']} to {s['minimum']}",
    }
    invalid = {
        "reverse_transition": f"transition {s['entity']} from {s['s1']} to {s['s0']}",
        "outsider_write": f"grant {s['outsider']} write access to {s['resource']}",
        "drop_commitment": f"remove protected commitment {s['commitment']}",
        "remove_dependency": f"remove dependency {s['dependency'][0]} -> {s['dependency'][1]}",
        "negative_metric": f"set {s['metric']} to -1",
    }
    return valid, invalid


TEMPLATES = [
    ("legal_transition", ("reverse_transition", "outsider_write", "negative_metric")),
    ("owner_write", ("drop_commitment", "remove_dependency", "reverse_transition")),
    ("positive_metric", ("outsider_write", "drop_commitment", "remove_dependency")),
    ("boundary_metric", ("negative_metric", "outsider_write", "drop_commitment")),
    ("legal_transition", ("drop_commitment", "remove_dependency", "outsider_write")),
    ("owner_write", ("negative_metric", "reverse_transition", "drop_commitment")),
    ("positive_metric", ("reverse_transition", "outsider_write", "negative_metric")),
    ("boundary_metric", ("remove_dependency", "reverse_transition", "outsider_write")),
]


def make_tasks(domains, split):
    rows = []
    for d_i, raw in enumerate(domains):
        s = domain_spec(raw)
        valid, invalid = action_pool(s)
        for q_i, (good_key, bad_keys) in enumerate(TEMPLATES):
            good = valid[good_key]
            bad = [invalid[k] for k in bad_keys]
            answer_pos = (d_i * len(TEMPLATES) + q_i) % 4
            options = bad.copy()
            options.insert(answer_pos, good)
            rows.append({
                "id": f"{split}-{d_i:02d}-{q_i:02d}",
                "split": split,
                "domain_index": d_i,
                "question_kind": good_key,
                "answer": str(answer_pos + 1),
                "spec": s,
                "options": options,
            })
    return rows


def render_rules(s, candidate):
    if candidate == "prose":
        return " ".join([
            f"The commitment {s['commitment']} is protected and may not be removed.",
            f"The only permitted {s['entity']} state transition is {s['s0']} to {s['s1']}; the reverse is forbidden.",
            f"{s['owner']} may write {s['resource']}, but {s['outsider']} may not write it.",
            f"{s['dependency'][0]} must keep its dependency on {s['dependency'][1]}.",
            f"{s['metric']} must never be less than {s['minimum']}.",
        ])
    if candidate == "explicit_nl":
        return "\n".join([
            f"MUST KEEP commitment: {s['commitment']}",
            f"ONLY LEGAL transition: {s['entity']} {s['s0']} -> {s['s1']}",
            f"PERMIT: {s['owner']} write {s['resource']}",
            f"FORBID: {s['outsider']} write {s['resource']}",
            f"MUST KEEP dependency: {s['dependency'][0]} -> {s['dependency'][1]}",
            f"INVARIANT: {s['metric']} >= {s['minimum']}",
        ])
    if candidate == "decision_table":
        return "\n".join([
            "RULE | DECISION",
            f"drop({s['commitment']}) | INVALID",
            f"transition({s['entity']},{s['s0']},{s['s1']}) | VALID",
            f"transition({s['entity']},anything_else) | INVALID",
            f"write({s['owner']},{s['resource']}) | VALID",
            f"write(any_other_role,{s['resource']}) | INVALID",
            f"remove_dependency({s['dependency'][0]},{s['dependency'][1]}) | INVALID",
            f"{s['metric']} < {s['minimum']} | INVALID",
            "otherwise | VALID",
        ])
    if candidate == "violation_normal":
        return "\n".join([
            "A change violates the program iff ANY predicate below is true:",
            f"V1 := drops({s['commitment']})",
            f"V2 := changes {s['entity']} state except {s['s0']} -> {s['s1']}",
            f"V3 := grants write({s['resource']}) to role != {s['owner']}",
            f"V4 := removes dependency {s['dependency'][0]} -> {s['dependency'][1]}",
            f"V5 := {s['metric']} < {s['minimum']}",
            "A change is valid iff NOT(V1 OR V2 OR V3 OR V4 OR V5).",
        ])
    raise ValueError(candidate)


def render_prompt(task, candidate):
    rules = render_rules(task["spec"], candidate)
    choices = "\n".join(f"{i + 1}. {x}" for i, x in enumerate(task["options"]))
    return (
        "Exactly one proposed software change below preserves every binding project rule. "
        "Choose it. Reply with exactly one digit: 1, 2, 3, or 4. No explanation.\n\n"
        f"PROJECT RULES:\n{rules}\n\nPROPOSED CHANGES:\n{choices}"
    )


def score(model, tokenizer, prompts):
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    label_ids = [tokenizer(x, add_special_tokens=False).input_ids for x in LABELS]
    if any(len(x) != 1 for x in label_ids):
        raise RuntimeError(f"Expected single-token choice labels, got {label_ids}")
    ids = [x[0] for x in label_ids]

    results = []
    for start in range(0, len(prompts), BATCH_SIZE):
        batch = prompts[start:start + BATCH_SIZE]
        rendered = [
            tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
            for prompt in batch
        ]
        toks = tokenizer(rendered, padding=True, return_tensors="pt", add_special_tokens=False)
        with torch.inference_mode():
            logits = model(**toks).logits[:, -1, :]
        choices = logits[:, ids]
        probabilities = torch.softmax(choices, dim=-1)
        pred_idx = torch.argmax(choices, dim=-1).tolist()
        token_lengths = toks["attention_mask"].sum(dim=1).tolist()
        for row_i, idx in enumerate(pred_idx):
            results.append({
                "pred": LABELS[idx],
                "confidence": float(probabilities[row_i, idx].item()),
                "prompt_tokens": int(token_lengths[row_i]),
            })
    return results


def aggregate(rows, split, candidate):
    selected = [r for r in rows if r["split"] == split and r["candidate"] == candidate]
    return {
        "n": len(selected),
        "correct": sum(r["correct"] for r in selected),
        "accuracy": sum(r["correct"] for r in selected) / len(selected),
        "mean_prompt_tokens": sum(r["prompt_tokens"] for r in selected) / len(selected),
        "mean_confidence": sum(r["confidence"] for r in selected) / len(selected),
    }


def exact_mcnemar(a_rows, b_rows):
    paired = list(zip(
        sorted(a_rows, key=lambda x: x["task_id"]),
        sorted(b_rows, key=lambda x: x["task_id"]),
    ))
    a_only = sum(a["correct"] and not b["correct"] for a, b in paired)
    b_only = sum(b["correct"] and not a["correct"] for a, b in paired)
    n = a_only + b_only
    if n == 0:
        return {"selected_only": 0, "baseline_only": 0, "two_sided_p": 1.0}
    k = min(a_only, b_only)
    tail = sum(math.comb(n, j) for j in range(k + 1)) / (2 ** n)
    return {
        "selected_only": a_only,
        "baseline_only": b_only,
        "two_sided_p": min(1.0, 2 * tail),
    }


def main():
    torch.set_num_threads(min(4, os.cpu_count() or 2))
    dev_tasks = make_tasks(DEV, "dev")
    holdout_tasks = make_tasks(HOLDOUT, "holdout")
    all_tasks = dev_tasks + holdout_tasks

    manifest = json.dumps(all_tasks, sort_keys=True, separators=(",", ":")).encode()
    manifest_sha256 = hashlib.sha256(manifest).hexdigest()

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    model.eval()

    rows = []
    for candidate in CANDIDATES:
        prompts = [render_prompt(task, candidate) for task in all_tasks]
        scored = score(model, tokenizer, prompts)
        for task, result in zip(all_tasks, scored):
            rows.append({
                "candidate": candidate,
                "task_id": task["id"],
                "split": task["split"],
                "question_kind": task["question_kind"],
                "gold": task["answer"],
                **result,
                "correct": result["pred"] == task["answer"],
            })

    development = {c: aggregate(rows, "dev", c) for c in CANDIDATES}
    holdout = {c: aggregate(rows, "holdout", c) for c in CANDIDATES}

    selected = max(
        CANDIDATES,
        key=lambda c: (
            development[c]["accuracy"],
            -development[c]["mean_prompt_tokens"],
            c,
        ),
    )

    selected_holdout = [r for r in rows if r["split"] == "holdout" and r["candidate"] == selected]
    prose_holdout = [r for r in rows if r["split"] == "holdout" and r["candidate"] == "prose"]

    answer_counts = {
        split: {
            label: sum(
                1 for task in (dev_tasks if split == "dev" else holdout_tasks)
                if task["answer"] == label
            )
            for label in LABELS
        }
        for split in ("dev", "holdout")
    }

    output = {
        "model": MODEL,
        "benchmark": "representation-search-v2-balanced-four-choice",
        "manifest_sha256": manifest_sha256,
        "chance_accuracy": 0.25,
        "answer_position_counts": answer_counts,
        "development_domains": [x[0] for x in DEV],
        "holdout_domains": [x[0] for x in HOLDOUT],
        "development": development,
        "holdout": holdout,
        "selected_on_development": selected,
        "selected_holdout_accuracy": holdout[selected]["accuracy"],
        "selected_vs_prose_holdout": exact_mcnemar(selected_holdout, prose_holdout),
        "rows": rows,
        "claim_boundary": (
            "Balanced semantic-comprehension benchmark over four hand-specified representations. "
            "Fresh domain holdout is opened once. A positive result is mechanistic evidence, not yet "
            "repository-level software-engineering superiority or a general programming-language result."
        ),
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/representation_search_v2.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "manifest_sha256": manifest_sha256,
        "answer_position_counts": answer_counts,
        "development": development,
        "holdout": holdout,
        "selected_on_development": selected,
        "selected_holdout_accuracy": holdout[selected]["accuracy"],
        "selected_vs_prose_holdout": output["selected_vs_prose_holdout"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
