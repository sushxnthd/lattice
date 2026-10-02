"""Frozen sequential edit experiment; no API key, GPU, or remote inference.

Run on a GitHub Linux CPU runner with an open-weight model. The model generates
actual edits. The exhaustive oracle and trusted contract never enter its context
except for one identical counterexample-feedback opportunity per condition.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import os
import re
import time
from pathlib import Path
import sys

from lattice.semantic_edits import (Program, InvalidProgram, cases, evaluate,
    expression, parse_lattice_patch, parse_python_patch)

ARMS = ("python_full", "python_patch", "lattice_patch")
MODELS = ("Qwen/Qwen2.5-Coder-0.5B-Instruct", "Qwen/Qwen2.5-Coder-1.5B-Instruct")
MAX_NEW_TOKENS = 220
OUTPUTS = ("read", "edit", "ship")
ALIASES = [
    ("dev", "Document", ("auth", "owner", "blocked", "reviewed", "urgent", "paid"), 0),
    ("dev", "Dataset", ("login", "curator", "locked", "checked", "override", "licensed"), 1),
    ("holdout", "Release", ("signed_in", "maintainer", "suspended", "tested", "emergency", "subscriber"), 0),
    ("holdout", "Ticket", ("member", "agent", "frozen", "triaged", "priority", "funded"), 1),
    ("holdout", "Model", ("authenticated", "admin", "disabled", "validated", "hotfix", "approved"), 2),
    ("holdout", "Case", ("identified", "analyst", "sealed", "audited", "expedited", "authorized"), 0),
    ("holdout", "Job", ("connected", "operator", "paused", "inspected", "critical", "provisioned"), 1),
    ("holdout", "Session", ("verified", "host", "banned", "moderated", "exceptional", "registered"), 2),
]


def scenario(row):
    split, domain, names, family = row
    a, o, b, r, u, p = names
    base = {
        "read": f"{a} and not {b}",
        "edit": f"{a} and {o} and not {b}",
        "ship": f"edit and {r}",
    }
    if family == 1:
        base["read"] = f"not {b} and ({a} or {p})"
    if family == 2:
        base["edit"] = f"read and {o}"
    if family == 0:
        steps = [
            (f"Allow read when {r} is true even if {a} is false; {b} must still deny read. Keep edit and ship unchanged.",
             {"read": f"not {b} and ({a} or {r})"}, {"read"}),
            (f"For edit, allow {u} as an alternative to {o}. Still require {a} and forbid {b}. Ship must inherit this expanded edit permission and still require {r}. Preserve read.",
             {"edit": f"{a} and not {b} and ({o} or {u})"}, {"edit", "ship"}),
            (f"Ship now also requires {p} unless {u} is true. Keep the existing edit and {r} requirements for ship. Preserve read and edit.",
             {"ship": f"edit and {r} and ({p} or {u})"}, {"ship"}),
        ]
    elif family == 1:
        steps = [
            (f"Read must now require {a}; {p} cannot bypass it. Still forbid {b}. Keep edit and ship unchanged.",
             {"read": f"{a} and not {b}"}, {"read"}),
            (f"Edit must now additionally require {p} unless {u} is true. It still requires {a}, {o}, and not {b}. Ship inherits this restriction and still requires {r}. Preserve read.",
             {"edit": f"{a} and {o} and not {b} and ({p} or {u})"}, {"edit", "ship"}),
            (f"Ship is now forbidden when {u} is true, even if edit is allowed. Keep all existing ship requirements. Preserve read and edit.",
             {"ship": f"edit and {r} and not {u}"}, {"ship"}),
        ]
    else:
        steps = [
            (f"Read should also allow {p} when {a} is false, but {b} must still deny it. IMPORTANT: edit and ship must remain exactly as before; the new read permission must not expand edit.",
             {"read": f"not {b} and ({a} or {p})", "edit": f"{a} and {o} and not {b}"}, {"read"}),
            (f"Edit should now allow {r} as an alternative to {o}, but still require {a} and forbid {b}. Ship inherits this expanded edit permission and still requires {r}. Preserve read.",
             {"edit": f"{a} and not {b} and ({o} or {r})"}, {"edit", "ship"}),
            (f"Ship now requires {p}, and {u} may substitute for {r}. Ship must still require edit. Preserve read and edit.",
             {"ship": f"edit and {p} and ({r} or {u})"}, {"ship"}),
        ]
    return split, domain, Program(tuple(names), tuple(base.items())), steps, family


def oracle(family, stage, values):
    """Independent hand-written behavior oracle; does not interpret DSL rules."""
    a, o, b, r, u, p = values
    rd = a and not b
    ed = a and o and not b
    sh = ed and r
    if family == 0:
        if stage >= 1: rd = not b and (a or r)
        if stage >= 2: ed = a and not b and (o or u)
        sh = ed and r
        if stage >= 3: sh = sh and (p or u)
    elif family == 1:
        if stage == 0: rd = not b and (a or p)
        if stage >= 2: ed = a and o and not b and (p or u)
        sh = ed and r
        if stage >= 3: sh = sh and not u
    else:
        if stage >= 1: rd = not b and (a or p)
        if stage >= 2: ed = a and not b and (o or r)
        sh = ed and r
        if stage >= 3: sh = ed and p and (r or u)
    return rd, ed, sh


class PythonPolicy:
    """Bounded interpreter for real Python straight-line / if-return functions.

    Never executes imports, calls, loops, attributes, or arbitrary model code.
    This evaluator is distinct from the rule graph interpreter.
    """
    def __init__(self, source, inputs):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            raise InvalidProgram("invalid Python") from exc
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
            raise InvalidProgram("return one policy function")
        self.fn = tree.body[0]
        args = self.fn.args
        if (self.fn.name != "policy" or tuple(a.arg for a in args.args) != inputs
            or self.fn.decorator_list or args.defaults or args.kwonlyargs
            or args.vararg or args.kwarg or args.posonlyargs):
            raise InvalidProgram("function signature mismatch")
        self.inputs = inputs
        self.source = source
        self.validate(self.fn.body)

    def validate(self, body):
        for n in body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                expression(ast.unparse(n.value))
            elif isinstance(n, ast.If):
                expression(ast.unparse(n.test))
                self.validate(n.body); self.validate(n.orelse)
            elif isinstance(n, ast.Return):
                if not isinstance(n.value, (ast.Tuple, ast.List)) or len(n.value.elts) != 3:
                    raise InvalidProgram("return a 3-tuple of Boolean expressions")
                for e in n.value.elts: expression(ast.unparse(e))
            else:
                raise InvalidProgram(f"unsupported Python statement: {type(n).__name__}")

    def run(self, values):
        env = dict(values)
        def block(body):
            for n in body:
                if isinstance(n, ast.Assign):
                    env[n.targets[0].id] = evaluate(n.value, env)
                elif isinstance(n, ast.If):
                    answer = block(n.body if evaluate(n.test, env) else n.orelse)
                    if answer is not None: return answer
                elif isinstance(n, ast.Return):
                    return tuple(evaluate(e, env) for e in n.value.elts)
            return None
        answer = block(self.fn.body)
        if answer is None or any(type(x) is not bool for x in answer):
            raise InvalidProgram("function did not return Boolean tuple")
        return dict(zip(OUTPUTS, answer))


def clean(raw):
    match = re.search(r"```[^\n]*\n(.*?)```", raw, re.S)
    return match.group(1).strip() if match else raw.strip()


def propose(arm, previous, raw):
    source = clean(raw)
    if arm == "python_full":
        return PythonPolicy(source, previous.inputs)
    parser = parse_python_patch if arm == "python_patch" else parse_lattice_patch
    return previous.patched(parser(source))


def prompt(arm, current, brief, request):
    common = (
        "Update this Boolean permission policy. All inputs are independent Booleans. "
        "Preserve every earlier requirement except the requested change. "
        "Use only input names, local rule names, True, False, and/or/not, and parentheses. "
        "No calls, comparisons, imports, loops, annotations, or explanatory text.\n"
        f"PERSISTENT REQUIREMENTS:\n{brief}\nREQUEST:\n{request}\n"
    )
    if arm == "python_full":
        source = current.source if isinstance(current, PythonPolicy) else current.lower_python()
        return common + (
            f"CURRENT PYTHON:\n{source}\nReturn the complete Python function policy"
            f"({', '.join(current.inputs)}) with assignments, optional if statements, and a return "
            "3-tuple (read, edit, ship).\nOUTPUT ONLY THE FUNCTION:\n"
        )
    source = "\n".join(f"{k} = {s}" for k, s in current.rules)
    syntax = (
        'Return only a Python expression dictionary of changed rules, e.g. '
        '{"read": auth and not blocked}. Values are Boolean expressions, not strings.'
        if arm == "python_patch" else
        "Return only assignments for changed rules, e.g. read = auth and not blocked."
    )
    return common + (
        f"INPUTS: {', '.join(current.inputs)}\nCURRENT RULES:\n{source}\n"
        "Omitted rules stay unchanged. Rules referencing changed rules inherit their new values; "
        "rewrite dependent rules if needed to preserve protected behavior. " + syntax + "\nOUTPUT:\n"
    )


def check(previous, candidate, family, stage, allowed):
    regression_pairs = 0
    correct_pairs = 0
    witness = None
    for values in cases(previous.inputs):
        actual = candidate.run(values)
        old = previous.run(values)
        expected = dict(zip(OUTPUTS, oracle(family, stage, tuple(values.values()))))
        for k in OUTPUTS:
            correct_pairs += actual[k] == expected[k]
            # Preserve a prior output only if it already meets the cumulative
            # contract. A previously rejected requirement may still be repaired.
            regression = k not in allowed and old[k] == expected[k] and actual[k] != old[k]
            regression_pairs += regression
            if witness is None and (regression or actual[k] != expected[k]):
                witness = {"kind": "regression" if regression else "intent_mismatch",
                           "input": values, "output": k, "got": actual[k], "expected": expected[k]}
    return {"ok": correct_pairs == 192 and regression_pairs == 0,
            "correct_pairs": correct_pairs, "total_pairs": 192,
            "regression_pairs": regression_pairs, "witness": witness}


def validate_oracles():
    for row in ALIASES:
        _, _, current, steps, family = scenario(row)
        for stage in range(4):
            if stage: current = current.patched(steps[stage-1][1])
            for values in cases(current.inputs):
                assert tuple(current.run(values).values()) == oracle(family, stage, tuple(values.values()))


def generate_batch(model, tok, prompts):
    import torch
    chats = [tok.apply_chat_template([{"role": "user", "content": p}],
              tokenize=False, add_generation_prompt=True) for p in prompts]
    x = tok(chats, return_tensors="pt", padding=True, add_special_tokens=False)
    started = time.perf_counter()
    with torch.inference_mode():
        y = model.generate(**x, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
                           pad_token_id=tok.pad_token_id)
    elapsed = time.perf_counter() - started
    width = x.input_ids.shape[1]
    return [(tok.decode(out[width:], skip_special_tokens=True), int(n),
             len(out[width:].tolist()) - out[width:].tolist().count(tok.pad_token_id), elapsed / len(prompts))
            for out, n in zip(y, x.attention_mask.sum(dim=1).tolist())]


def main():
    validate_oracles()
    model_id = os.environ.get("LATTICE_MODEL", MODELS[0])
    manifest = {"aliases": ALIASES, "arms": ARMS, "stages": 3, "max_new_tokens": MAX_NEW_TOKENS,
                "attempts": 2, "model": model_id, "decoding": "greedy", "batch_size": 4,
                "task_definition_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    print("FROZEN_MANIFEST " + digest, flush=True)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(min(4, os.cpu_count() or 2))
    tok = AutoTokenizer.from_pretrained(model_id)
    tok.padding_side = "left"
    if tok.pad_token_id is None: tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_id); model.eval()
    rows = []
    trajectories = []
    for arm in ARMS:
        for row in ALIASES:
            split, domain, current, steps, family = scenario(row)
            if arm == "python_full": current = PythonPolicy(current.lower_python(), current.inputs)
            brief = (
                f"Initial rules: {dict(scenario(row)[2].rules)}. "
                "Rules describe output values, with dependency references evaluated using current values."
            )
            trajectories.append({"arm": arm, "split": split, "domain": domain, "current": current,
                "steps": steps, "family": family, "brief": brief, "successes": 0})
    for stage in range(1, 4):
        prepared = []
        for t in trajectories:
            request, _, allowed = t["steps"][stage-1]
            t["request"] = request
            t["allowed"] = allowed
            prepared.append((t, prompt(t["arm"], t["current"], t["brief"], request)))
        for start in range(0, len(prepared), 4):
            batch = prepared[start:start+4]
            pending = []
            outputs = generate_batch(model, tok, [p for _, p in batch])
            for (t, p), (raw, nt, ot, seconds) in zip(batch, outputs):
                result = assess(t, raw, stage)
                entry = {"arm": t["arm"], "split": t["split"], "domain": t["domain"],
                         "family": t["family"], "stage": stage, "attempt": 1,
                         "prompt": p, "raw": raw, "input_tokens": nt, "output_tokens": ot,
                         "generation_seconds": seconds, **result[1]}
                rows.append(entry)
                if result[1]["ok"]:
                    t["current"] = result[0]; t["successes"] += 1
                else:
                    feedback = json.dumps(result[1].get("witness") or result[1].get("error"), sort_keys=True)
                    repair = p + f"\nREJECTED OUTPUT:\n{raw}\nCHECKER FEEDBACK:\n{feedback}\nReturn a corrected output in the same required format.\n"
                    pending.append((t, repair))
            if pending:
                repaired = generate_batch(model, tok, [p for _, p in pending])
                for (t, p), (raw, nt, ot, seconds) in zip(pending, repaired):
                    result = assess(t, raw, stage)
                    rows.append({"arm": t["arm"], "split": t["split"], "domain": t["domain"],
                        "family": t["family"], "stage": stage, "attempt": 2,
                        "prompt": p, "raw": raw, "input_tokens": nt, "output_tokens": ot,
                        "generation_seconds": seconds, **result[1]})
                    if result[1]["ok"]:
                        t["current"] = result[0]; t["successes"] += 1
            print(f"stage={stage} batch={start//4+1} completed", flush=True)
        # Append every requested change, including rejected changes. Later steps are
        # still evaluated against the cumulative intended policy, not a relaxed oracle.
        for t in trajectories: t["brief"] += "\nPrior request: " + t["request"]
    summary = {}
    for split in ("dev", "holdout"):
        summary[split] = {}
        for arm in ARMS:
            selected = [r for r in rows if r["split"] == split and r["arm"] == arm]
            first = [r for r in selected if r["attempt"] == 1]
            ts = [t for t in trajectories if t["split"] == split and t["arm"] == arm]
            summary[split][arm] = {
                "trajectories": len(ts), "checkpoints": len(first),
                "first_attempt_successes": sum(r["ok"] for r in first),
                "successes_with_one_repair": sum(t["successes"] for t in ts),
                "all_three_checkpoints_succeeded": sum(t["successes"] == 3 for t in ts),
                "model_calls": len(selected), "input_tokens": sum(r["input_tokens"] for r in selected),
                "output_tokens": sum(r["output_tokens"] for r in selected),
                "first_attempt_regression_pairs": sum(r.get("regression_pairs", 0) for r in first),
                "first_attempt_invalid_programs": sum("error" in r for r in first),
            }
    out = {"manifest": manifest, "manifest_sha256": digest, "summary": summary, "rows": rows,
           "claim_boundary": "Synthetic finite Boolean permission-policy evolution; three short edits; one model family; no claim of repository-level or general language superiority."}
    path = Path("artifacts/exp002") / (model_id.split("/")[-1] + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("RESULT_SUMMARY " + json.dumps({"manifest_sha256": digest, "summary": summary}), flush=True)


def assess(t, raw, stage):
    try:
        candidate = propose(t["arm"], t["current"], raw)
        return candidate, check(t["current"], candidate, t["family"], stage, t["allowed"])
    except (InvalidProgram, ValueError, SyntaxError, RecursionError) as exc:
        return None, {"ok": False, "error": str(exc), "correct_pairs": 0, "total_pairs": 192}


if __name__ == "__main__":
    if "--validate" in sys.argv:
        validate_oracles()
        print("independent oracle agrees at all 8 x 4 x 64 policy checkpoints")
    else:
        main()
