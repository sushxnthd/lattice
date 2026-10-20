"""Run134: paired captured-dependency representation experiment.

Synthetic, not product-scale. Graph and indexed Python are information-equivalent;
model output is a root-name->Boolean-expression JSON patch. All model output is
parsed as data, never executed. Never open holdout outcomes in primary run.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path
import random
import time
import urllib.request

SEED = 13420261020
PRIMARY_CLUSTERS = 168
HOLDOUT_CLUSTERS = 24
MODEL = "Qwen2.5-Coder-7B-Instruct-GGUF-Q4_K_M"
ENDPOINT = "http://127.0.0.1:8080/v1/chat/completions"
MAX_OUTPUT = 192
CTX = 4096
DOMAINS = ("access", "billing", "dispatch", "compliance", "inventory", "incident", "workflow", "messaging")
ROLES = {
    "cred_a": ("login_ok", "signature_ok", "mfa_ok", "token_ok", "proof_ok"),
    "cred_b": ("otp_ok", "device_ok", "backup_ok", "identity_ok", "badge_ok"),
    "operator": ("operator_ok", "handler_ready", "staff_approved", "agent_ready"),
    "region": ("region_ok", "scope_ok", "tenant_ok", "market_ok"),
    "override": ("override_ok", "emergency_ok", "fallback_ok", "rescue_ok"),
    "archive": ("archive_ok", "retention_ok", "log_ok", "storage_ok"),
    "quota": ("quota_ok", "capacity_ok", "budget_ok", "rate_ok"),
}

def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(x):
    if isinstance(x, str): x = x.encode()
    return hashlib.sha256(x).hexdigest()

def refs(expr):
    tree = ast.parse(expr, mode="eval")
    allowed = (ast.Expression, ast.Name, ast.Load, ast.Constant, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not)
    if any(not isinstance(n, allowed) for n in ast.walk(tree)):
        raise ValueError("unsupported Boolean expression")
    return set(n.id for n in ast.walk(tree) if isinstance(n, ast.Name))

def make_pair(cluster, holdout=False):
    """Twin tasks have identical headers, different captured historical semantics."""
    rng = random.Random(SEED + cluster * 10007)
    domain = DOMAINS[cluster % len(DOMAINS)]
    names = {k: f"{rng.choice(v)}_{cluster:03d}" for k, v in ROLES.items()}
    inputs = list(names.values())
    rng.shuffle(inputs)
    depth = 2 if cluster % 2 == 0 else 5
    stage_names = [f"{domain}_check_{i}_{cluster:03d}" for i in range(depth)]
    audit = f"{domain}_audit_{cluster:03d}"
    route = f"{domain}_route_{cluster:03d}"
    retention = f"{domain}_retention_{cluster:03d}"
    alert = f"{domain}_alert_{cluster:03d}"
    outputs = stage_names + [audit, route, retention, alert]
    owner = {name: f"{domain}/{['auth','policy','risk','audit','route','ops'][i % 6]}/module_{i:02d}.py"
             for i, name in enumerate(outputs)}
    common = {
        "cluster": f"C{cluster:03d}", "domain": domain,
        "inputs": inputs, "roots": outputs, "owners": owner,
        "authority": [route], "protected": [n for n in outputs if n != route],
        "audit": audit, "route": route, "first_stage": stage_names[0],
        "operator": names["operator"], "depth": depth,
        "request": (
            f"Repair {route} so it requires BOTH the operator signal {names['operator']} "
            f"and the credential signal that appears POSITIVELY (not under 'not') "
            f"in the historical first-stage check captured by {audit} through its "
            f"upstream dependency chain. The current first-stage root was replaced "
            f"after the audit captured the old version. Follow the captured "
            f"dependencies, not the current source. Preserve every other output."
        ),
    }
    out = []
    for twin in (0, 1):
        positive = names["cred_a"] if twin == 0 else names["cred_b"]
        negative = names["cred_b"] if twin == 0 else names["cred_a"]
        initial = [(stage_names[0], f"{positive} and not {negative}")]
        for j in range(1, depth):
            guard = names["region"] if j % 2 else names["quota"]
            initial.append((stage_names[j], f"{stage_names[j-1]} and {guard}"))
        initial += [
            (audit, f"{stage_names[-1]} or {names['override']}"),
            (route, f"{names['operator']} and {names['region']}"),
            (retention, f"{audit} and {names['archive']}"),
            (alert, f"{stage_names[1]} and {names['quota']}"),
        ]
        history = [{stage_names[0]: f"{names['cred_a']} or {names['cred_b']}"}]
        out.append({**common, "id": f"C{cluster:03d}T{twin}", "twin": twin,
                    "initial": initial, "history": history,
                    "target_expression": f"{positive} and {names['operator']}",
                    "holdout": holdout})
    return out

def tasks():
    return [t for i in range(PRIMARY_CLUSTERS + HOLDOUT_CLUSTERS)
            for t in make_pair(i, i >= PRIMARY_CLUSTERS)]

def state(t):
    nodes, roots = [], {}
    inputs = set(t["inputs"])
    for name, expr in t["initial"]:
        binding = {r: roots[r] for r in sorted(refs(expr) - inputs)}
        roots[name] = len(nodes)
        nodes.append({"id": len(nodes), "expr": expr, "bindings": binding, "owner": t["owners"][name]})
    for patch in t["history"]:
        name, expr = next(iter(patch.items()))
        binding = {r: roots[r] for r in sorted(refs(expr) - inputs)}
        roots[name] = len(nodes)
        nodes.append({"id": len(nodes), "expr": expr, "bindings": binding, "owner": t["owners"][name]})
    return nodes, roots

def header(t):
    keys = ("cluster", "domain", "inputs", "roots", "owners", "authority", "protected",
            "audit", "route", "first_stage", "operator", "depth", "request")
    return {k: t[k] for k in keys}

def render(t, arm):
    nodes, roots = state(t)
    preamble = (
        "You are editing a versioned, multi-file Boolean policy program. "
        "A historical reference captures an immutable version; later edits do "
        "not change protected captures. Return ONLY a JSON object mapping "
        "authorized root names to Boolean expression strings. No markdown, "
        "no explanations. Do not edit protected roots. The same compiler and "
        "verifier check both representations.\nFACTS: " + canon(header(t)) + "\nVIEW:\n"
    )
    if arm == "graph":
        body = canon({"kind": "versioned_dependency_state_graph", "nodes": nodes, "roots": roots})
    elif arm == "python":
        class Rewrite(ast.NodeTransformer):
            def __init__(self, bindings): self.bindings = bindings
            def visit_Name(self, n):
                return ast.copy_location(ast.Name(id="_v" + str(self.bindings[n.id]), ctx=ast.Load()), n) if n.id in self.bindings else n
        lines = ["# Versioned Python SSA view; each assignment is an immutable capture.",
                 "def policy(" + ", ".join(t["inputs"]) + "):"]
        for n in nodes:
            bound = ast.unparse(Rewrite(n["bindings"]).visit(ast.parse(n["expr"], mode="eval").body))
            lines.append(f"    _v{n['id']} = {bound}  # source={n['expr']}; references={canon(n['bindings'])}; file={n['owner']}")
        lines.append("    return {" + ", ".join(repr(k) + ": _v" + str(v) for k, v in roots.items()) + "}")
        body = "\n".join(lines)
    else: raise ValueError(arm)
    return preamble + body

def independent_eval(expr, env):
    node = ast.parse(expr, mode="eval").body
    def rec(n):
        if isinstance(n, ast.Name): return env[n.id]
        if isinstance(n, ast.Constant) and type(n.value) is bool: return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not): return not rec(n.operand)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.And): return all(rec(x) for x in n.values)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or): return any(rec(x) for x in n.values)
        raise ValueError("not a Boolean expression")
    return rec(node)

def independent_run(nodes, roots, values):
    memo = {}
    def visit(i):
        if i not in memo:
            node = nodes[i]
            env = dict(values)
            env.update({k: visit(j) for k, j in node["bindings"].items()})
            memo[i] = independent_eval(node["expr"], env)
        return memo[i]
    return {k: visit(i) for k, i in roots.items()}

def score(t, answer):
    from lattice.semantic_edits import Program
    from lattice.framed_edits import FramedProgram
    try:
        patch = json.loads(answer.strip())
        if not isinstance(patch, dict) or not patch or any(type(k) is not str or type(v) is not str for k, v in patch.items()):
            return {"ok": False, "reason": "patch_schema"}
        if not set(patch) <= set(t["authority"]):
            return {"ok": False, "reason": "authority"}
        before = FramedProgram.from_program(Program(tuple(t["inputs"]), tuple(map(tuple, t["initial"]))))
        for historical in t["history"]:
            before = before.edit(historical, set(historical))
        after = before.edit(patch, set(t["authority"]))
        nodes, roots = state(t)
        if before.context()["roots"] != roots:
            return {"ok": False, "reason": "state_mismatch"}
        ctx = after.context()
        independent_after = [{"expr": n["expression"], "bindings": n["references"]} for n in ctx["nodes"]]
        checked = 0
        for bits in itertools.product((False, True), repeat=len(t["inputs"])):
            env = dict(zip(t["inputs"], bits))
            old = independent_run(nodes, roots, env)
            got = after.run(env)
            independently_got = independent_run(independent_after, ctx["roots"], env)
            if got != independently_got:
                return {"ok": False, "reason": "independent_oracle_disagreement", "witness": env}
            expected = {**old, t["route"]: independent_eval(t["target_expression"], env)}
            if got != expected:
                return {"ok": False, "reason": "semantic_mismatch", "witness": env}
            checked += 1
        return {"ok": True, "checked": checked}
    except Exception as exc:
        return {"ok": False, "reason": "compiler_or_parser", "error": str(exc)}

def freeze(out):
    if out.exists(): raise FileExistsError("refusing to overwrite frozen task data")
    out.mkdir(parents=True)
    all_tasks = tasks()
    ts = [t for t in all_tasks if not t["holdout"]]
    holdout_commitment = digest(canon([t for t in all_tasks if t["holdout"]]))
    prompts = [{"id": t["id"], "graph": render(t, "graph"), "python": render(t, "python")} for t in ts]
    taskbytes, promptbytes = canon(ts) + "\n", canon(prompts) + "\n"
    (out / "tasks.json").write_text(taskbytes)
    (out / "prompts.json").write_text(promptbytes)
    m = {"seed": SEED, "primary_clusters": PRIMARY_CLUSTERS, "holdout_clusters": HOLDOUT_CLUSTERS,
         "tasks_per_cluster": 2, "primary_tasks": 2 * PRIMARY_CLUSTERS,
         "status": "SYNTHETIC_CAPTURED_DEPENDENCY_ONLY_NOT_REAL_REPOS",
         "model": MODEL, "context_tokens": CTX, "max_completion_tokens": MAX_OUTPUT,
         "tasks_sha256": digest(taskbytes), "prompts_sha256": digest(promptbytes),
         "primary_endpoint": "mean_cluster_pair_first_attempt_exact_success_graph_minus_python",
         "mechanism_prediction": "graph advantage greater at depth=5 than depth=2",
         "holdout_sealed": True, "holdout_tasks_commitment_sha256": holdout_commitment,
         "run132_holdout_not_reused": True}
    (out / "freeze.json").write_text(canon(m) + "\n")
    return m

def inference(out, shard, nshards):
    if out.exists(): raise FileExistsError("refusing to overwrite raw evidence")
    out.mkdir(parents=True)
    frozen = freeze(out / "frozen")
    rows = []
    for t in tasks():
        if t["holdout"] or int(t["cluster"][1:]) % nshards != shard: continue
        arms = ("graph", "python") if (int(t["cluster"][1:]) + t["twin"]) % 2 == 0 else ("python", "graph")
        for arm in arms:
            prompt = render(t, arm)
            req = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                   "temperature": 0.0, "top_p": 1.0, "seed": SEED,
                   "max_tokens": MAX_OUTPUT, "stream": False}
            body = canon(req).encode()
            request = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={"Content-Type": "application/json"})
            start = time.monotonic()
            try:
                with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request, timeout=1800) as resp:
                    raw = resp.read(2_000_001)
                if len(raw) > 2_000_000: raise ValueError("oversize_response")
                decoded = json.loads(raw)
                answer = decoded["choices"][0]["message"]["content"]
                row = {"id": t["id"], "cluster": t["cluster"], "twin": t["twin"],
                       "arm": arm, "depth": t["depth"], "model_id": decoded.get("model"),
                       "request": req, "response": decoded, "answer": answer,
                       "usage": decoded.get("usage"), "score": score(t, answer),
                       "request_sha256": digest(body), "response_sha256": digest(raw),
                       "elapsed_seconds": round(time.monotonic()-start, 2), "status": "completed"}
            except Exception as exc:
                row = {"id": t["id"], "cluster": t["cluster"], "twin": t["twin"],
                       "arm": arm, "depth": t["depth"], "request": req,
                       "request_sha256": digest(body), "error": str(exc),
                       "elapsed_seconds": round(time.monotonic()-start, 2), "status": "inference_error"}
            rows.append(row)
            (out / "partial.json").write_text(canon({"freeze": frozen, "rows": rows}) + "\n")
    (out / "results.json").write_text(canon({"freeze": frozen, "rows": rows}) + "\n")
    return {"shard": shard, "nshards": nshards, "calls": len(rows), "freeze_sha256": digest(canon(frozen))}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--freeze", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--shard", type=int, default=0)
    p.add_argument("--nshards", type=int, default=8)
    args = p.parse_args()
    if args.freeze: print(canon(freeze(args.freeze)))
    else:
        if args.output is None: p.error("--output required")
        print(canon(inference(args.output, args.shard, args.nshards)))

if __name__ == "__main__": main()
