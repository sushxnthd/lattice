"""K-SYNTH-1: prospective, paired 7B structural-view feasibility experiment.

Synthetic four-file policy abstractions, NOT independent real-repository tasks.
Model output is parsed as a bounded Boolean expression; never exec model code.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import time
import urllib.request

from lattice.semantic_edits import Program, cases
from lattice.framed_edits import FramedProgram

SEED = 175
MAX_OUTPUT = 192
MODEL = "Qwen2.5-Coder-7B-Instruct-GGUF-Q4_K_M"
DOMAINS = [
    ("identity", "authenticated mfa staff suspended verified locked"),
    ("billing", "paid active premium overdue invoiced frozen"),
    ("content", "reviewed original adult flagged attributed removed"),
    ("shipment", "addressed stocked paid recalled packed insured"),
    ("support", "open assigned urgent duplicate verified escalated"),
    ("health", "consented adult clinician revoked reviewed private"),
    ("education", "enrolled graded passed suspended verified appealed"),
    ("payments", "funded signed trusted disputed settled blocked"),
    ("deploy", "tested reviewed signed vulnerable staged enabled"),
    ("travel", "ticketed checked valid cancelled screened delayed"),
    ("privacy", "consented scoped encrypted expired deleted exported"),
    ("storage", "available owned writable readonly synced archived"),
]
def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
def digest(value):
    return hashlib.sha256(value).hexdigest()
def taskset():
    tasks = []
    for d, (domain, names) in enumerate(DOMAINS):
        ins = tuple(names.split())
        # Each policy has four logical source files and immutable capture semantics.
        roots = tuple(domain + "_" + s for s in
            ("basis", "restriction", "eligible", "gateway", "audit", "decision", "endpoint"))
        a,b,c,e,f,g = ins
        r0,r1,r2,r3,r4,r5,r6 = roots
        rules = ((r0,f"{a} and {b}"), (r1,f"{c} or {e}"),
                 (r2,f"{r0} and not {r1}"), (r3,f"{r2} or {f}"),
                 (r4,f"{r3} and {g}"), (r5,f"{r3} or {r1}"),
                 (r6,f"{r5} and {g}"))
        files = {"identity.py":[r0,r1], "policy.py":[r2,r3],
                 "audit.py":[r4], "service.py":[r5,r6]}
        for variant in range(2):
            replacement = (f"{r2} and {f}" if variant == 0
                           else f"{r2} or ({f} and not {e})")
            request = (f"In the {domain} service, change the gateway condition: "
                       + (f"require both eligibility and {f}."
                          if variant == 0 else
                          f"allow eligibility, or {f} only when {e} is false.")
                       + " Keep the historical audit decision unchanged; "
                       "the public endpoint must reflect the updated gateway.")
            before = FramedProgram.from_program(Program(ins,rules))
            allowed = [r3,r5,r6]
            target = before.edit({r3:replacement},set(allowed))
            goal = [int(target.run(x)[r6]) for x in cases(ins)]
            protected = [int(before.run(x)[r4]) for x in cases(ins)]
            tasks.append({"id":f"{domain}-{variant}", "inputs":ins,
                "rules":rules,"files":files,"request":request,
                "allowed":allowed,"protected":[r4],"goal_root":r6,
                "goal":goal,"protected_table":protected,
                "reference_patch":{r3:replacement},
                "depth_stratum":"high" if variant else "low"})
    return tasks

def view(task, arm):
    p = Program(tuple(task["inputs"]),tuple(tuple(x) for x in task["rules"]))
    before = FramedProgram.from_program(p)
    ctx = before.context()
    public = {"request":task["request"],"inputs":task["inputs"],
              "file_roots":task["files"],"authorized_roots":task["allowed"],
              "protected_roots":task["protected"],"goal_root":task["goal_root"],
              "patch_format":{"edits":{"root_name":"Boolean Python expression"}},
              "rules":"Return only JSON. No markdown. Use only declared inputs and root names. No calls."}
    if arm == "IR":
        structure = {"immutable_nodes":ctx["nodes"],"root_versions":ctx["roots"],
                     "current_sources":dict(task["rules"])}
        label = "VERSIONED SEMANTIC GRAPH"
    else:
        # Strong Python control: same node IDs, source expressions, bound references,
        # versions, roots and authority, not just bare unannotated source.
        lines = ["# Version-indexed ordinary Python view; captures are immutable."]
        for n in ctx["nodes"]:
            refs = ", ".join(f"{k}=v{v}" for k,v in n["references"].items()) or "none"
            lines.append(f"# v{n['id']} binds {refs}; expression: {n['expression']}")
        lines.append(before.lower_python())
        lines.append("# root versions: "+repr(ctx["roots"]))
        lines.append("# current source rules: "+repr(dict(task["rules"])))
        structure = "\n".join(lines)
        label = "VERSION-INDEXED PYTHON"
    return ("You are making a scoped semantic repair. Both views use the same "
            "trusted compiler and verifier.\n" + label + "\n"
            + (json.dumps(structure,sort_keys=True) if arm == "IR" else structure)
            + "\nCOMMON CONTRACT\n" + canonical(public).decode()
            + "\nOnly emit a JSON patch in the shared grammar.")

def inference(endpoint, prompt, seed):
    body = canonical({"model":MODEL,"messages":[{"role":"user","content":prompt}],
                      "temperature":0.0,"top_p":1.0,"seed":seed,
                      "max_tokens":MAX_OUTPUT,"stream":False})
    req = urllib.request.Request(endpoint,data=body,method="POST",
                                 headers={"Content-Type":"application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req,timeout=1200) as response:
        raw = response.read(4_000_001)
    if len(raw)>4_000_000: raise RuntimeError("oversized model response")
    parsed = json.loads(raw)
    usage = parsed.get("usage",{})
    if not all(type(usage.get(k)) is int for k in ("prompt_tokens","completion_tokens")):
        raise RuntimeError("token accounting unavailable")
    return body,raw,parsed

def evaluate(task, response):
    """Same trusted patch compiler and verifier in both randomized arms."""
    try:
        message = response["choices"][0]["message"]["content"]
        tx = json.loads(message)
        if set(tx)!={"edits"} or not isinstance(tx["edits"],dict):
            return {"success":0,"failure":"malformed patch"}
        if not tx["edits"] or not set(tx["edits"])<=set(task["allowed"]):
            return {"success":0,"failure":"unauthorized or empty patch"}
        before = FramedProgram.from_program(
            Program(tuple(task["inputs"]),tuple(tuple(x) for x in task["rules"])))
        after = before.edit(tx["edits"],set(task["allowed"]))
        for i,values in enumerate(cases(tuple(task["inputs"]))):
            out=after.run(values)
            if int(out[task["goal_root"]])!=task["goal"][i]:
                return {"success":0,"failure":"goal mismatch","witness":values}
            if int(out[task["protected"][0]])!=task["protected_table"][i]:
                return {"success":0,"failure":"protected mismatch","witness":values}
        return {"success":1,"failure":None}
    except Exception as exc:
        return {"success":0,"failure":type(exc).__name__+":"+str(exc)[:120]}

def run(out,endpoint=None):
    if out.exists(): raise ValueError("never overwrite prior evidence")
    out.mkdir(parents=True)
    tasks=taskset()
    frozen=[{k:v for k,v in t.items() if k not in ("goal","protected_table","reference_patch")}
            for t in tasks]
    (out/"tasks_public.json").write_bytes(canonical(frozen))
    # Sealed before inference; opened only after ALL model calls.
    sealed=canonical([{k:t[k] for k in ("id","goal","protected_table","reference_patch")} for t in tasks])
    (out/"sealed_sha256.txt").write_text(digest(sealed)+"\n")
    manifest={"schema":"lattice-run175-v1","seed":SEED,"model":MODEL,
              "temperature":0,"max_output_tokens":MAX_OUTPUT,
              "task_count":len(tasks),"synthetic":True,
              "independent_real_tasks":0,"tasks_sha256":digest(canonical(frozen)),
              "sealed_sha256":digest(sealed),
              "hypothesis":"IR improves first-attempt verified repair vs indexed Python",
              "primary":"paired verified repair success, IR minus Python",
              "unseen_prediction":"IR advantage should increase with cross-file coupling; here not independently varied"}
    (out/"freeze.json").write_bytes(canonical(manifest))
    prompts={(t["id"],arm):view(t,arm) for t in tasks for arm in ("IR","PY")}
    (out/"prompt_hashes.json").write_bytes(canonical({k+"-"+a:digest(p.encode())
                                for (k,a),p in prompts.items()}))
    if endpoint is None:
        return {"status":"DRY_RUN","task_count":len(tasks),"freeze":manifest}
    if endpoint!="http://127.0.0.1:8080/v1/chat/completions":
        raise ValueError("only loopback model inference")
    raw_dir=out/"raw";raw_dir.mkdir()
    responses={}
    # Balanced arm order, no feedback, no verifier use during inference.
    for i,t in enumerate(tasks):
        order=("IR","PY") if i%2==0 else ("PY","IR")
        for arm in order:
            body,raw,decoded=inference(endpoint,prompts[t["id"],arm],SEED+i)
            stem=t["id"]+"-"+arm
            (raw_dir/(stem+"-request.json")).write_bytes(body)
            (raw_dir/(stem+"-response.json")).write_bytes(raw)
            responses[(t["id"],arm)]=decoded
    # Holdout is scored only after the final model response has been recorded.
    rows=[]
    for t in tasks:
        for arm in ("IR","PY"):
            decoded=responses[t["id"],arm]
            score=evaluate(t,decoded)
            usage=decoded["usage"]
            rows.append({"id":t["id"],"arm":arm,**score,
                         "prompt_tokens":usage["prompt_tokens"],
                         "completion_tokens":usage["completion_tokens"],
                         "stratum":t["depth_stratum"]})
    (out/"rows.json").write_bytes(canonical(rows))
    pairs={t["id"]:{arm:next(r["success"] for r in rows if r["id"]==t["id"] and r["arm"]==arm)
                   for arm in ("IR","PY")} for t in tasks}
    n10=sum(v["IR"]==1 and v["PY"]==0 for v in pairs.values())
    n01=sum(v["IR"]==0 and v["PY"]==1 for v in pairs.values())
    summary={"n":len(tasks),"ir_only":n10,"python_only":n01,
             "paired_difference":(n10-n01)/len(tasks),
             "status":"UNDERPOWERED_SYNTHETIC_FEASIBILITY_ONLY",
             "model":MODEL,"zero_real_repository_tasks":True}
    (out/"summary.json").write_bytes(canonical(summary))
    return summary

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--endpoint")
    args=parser.parse_args()
    print(json.dumps(run(args.output,args.endpoint),indent=2))
