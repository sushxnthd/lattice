"""Prospective Run218 target-recall corrected, matched short-ID real-issue pilot.
No claim of functional resolution or representation superiority."""
import argparse, json, pathlib, re, urllib.request
import paired_repo_pilot_210 as prior
import run217_matched_real_issues as old
from repo_transaction import digest, tracked_authority

PROTOCOL="K-SYNTH-1/run218-matched-target-id-function-recall-v1"
ARMS=("semantic_ir_json","python_annotated")

def issue_names(issue):
    return set(re.findall(r"(?<![\\w])([A-Za-z_]\\w*)\\s*\\(",issue["problem_statement"]))

def facts(files,issue,max_chars=26000):
    names=issue_names(issue)
    words=set(re.findall(r"[a-z_][a-z_0-9]{3,}",issue["problem_statement"].lower()))
    out={}
    for path,item in sorted(prior.target_facts(files).items()):
        def score(t):
            named=t["kind"] in ("FunctionDef","AsyncFunctionDef","ClassDef")
            return (10000*(t["name"] in names)+100*named+
                    20*sum(w in t["name"].lower() for w in words)+
                    sum(min(2,t["old_text"].lower().count(w)) for w in words),
                    -len(t["old_text"]),-t["start_line"])
        eligible=[t for t in item["targets"] if 0<len(t["old_text"])<=5500]
        chosen=sorted(eligible,key=score,reverse=True)[:(4 if path.endswith(".py") else 2)]
        if not chosen:continue
        targets=[{k:t[k] for k in ("target_id","kind","name","start_line","end_line","old_text")} for t in chosen]
        lines=item["source"].splitlines(keepends=True)
        excerpts=[]
        for t in chosen[:2]:
            a=max(0,t["start_line"]-2)
            excerpts.append("".join(f"{j+1}: {lines[j]}" for j in range(a,min(len(lines),t["end_line"]+2,a+12))))
        out[path]={"file_sha256":item["file_sha256"],"full_source_bytes":len(files[path]),
                   "targets":targets,"source_excerpt":"\n".join(excerpts)[:1200]}
    def size():return len(json.dumps(out,sort_keys=True,ensure_ascii=False,separators=(",",":")))
    while size()>max_chars:
        removable=[(len(t["old_text"]),p,i) for p,d in out.items()
                   for i,t in enumerate(d["targets"])
                   if not(t["kind"] in ("FunctionDef","AsyncFunctionDef") and t["name"] in names)]
        if removable:
            _,p,i=max(removable);out[p]["targets"].pop(i)
        else:
            for p in sorted(out,key=lambda p:len(out[p]["source_excerpt"]),reverse=True):
                out[p]["source_excerpt"]=""
                if size()<=max_chars:break
            if size()>max_chars:raise ValueError("protected targets exceed context budget")
    return out

def prompt(issue,f,arm):
    view=(json.dumps(f,sort_keys=True,separators=(",",":"),ensure_ascii=False)
          if arm=="semantic_ir_json" else old.python_view(f))
    guide=("structured semantic-node JSON" if arm=="semantic_ir_json"
           else "annotated Python source with AST_TARGET comments")
    return ("Repair this repository issue. Both conditions have identical information, target IDs, "
      "file authority, compiler and output grammar. Use the exact 24-character target_id of a "
      "listed target as selector; NEVER use its old_text, name or a placeholder. "
      "For replace, provide op=replace, path, file_sha256, selector, the COMPLETE new target "
      "text as replacement, and content empty. For create, set op=create, path and content, "
      "other fields empty. For delete, set op=delete, path and file_sha256, other fields empty. "
      "Return only JSON with actions array, each action having exactly six string fields "
      "op,path,file_sha256,selector,replacement,content. Do not access hidden tests. "
      "Presentation: "+guide+"\nISSUE:\n"+issue["problem_statement"]+"\nSOURCE_FACTS:\n"+view)

def invoke(endpoint,raw,issue,f,files,authority,arm):
    p=prompt(issue,f,arm)
    seed=int(digest((PROTOCOL+issue["instance_id"]).encode())[:8],16)
    req={"model":prior.MODEL,"messages":[{"role":"user","content":p}],
         "temperature":0,"seed":seed,"max_tokens":2048,"stream":False,
         "response_format":prior.response_format("python_short_id")}
    tag=issue["instance_id"]+"-"+arm
    (raw/(tag+"-request.json")).write_bytes(prior.canonical(req))
    record={"task":issue["instance_id"],"arm":arm,"seed":seed,
            "model":prior.MODEL,"model_sha256":prior.MODEL_SHA,
            "prompt_sha256":digest(p.encode()),"facts_sha256":digest(prior.canonical(f)),
            "accepted":False,"functional_resolution":"NOT_EVALUATED"}
    try:
        body=urllib.request.urlopen(urllib.request.Request(endpoint,data=prior.canonical(req),
          headers={"Content-Type":"application/json"},method="POST"),timeout=2400).read(4_000_000)
        (raw/(tag+"-response.json")).write_bytes(body)
        response=json.loads(body);choice=response["choices"][0]
        record.update(usage=response.get("usage"),finish_reason=choice.get("finish_reason"),
                      model_reported=response.get("model"))
        tx=prior.compile_arm(files,json.loads(choice["message"]["content"]),authority,"python_short_id")
        record.update(accepted=True,trace=tx.trace,before=tx.before,after=tx.after,
                      changed_paths=sorted(tx.changes))
    except Exception as exc:record["error"]=repr(exc)
    (raw/(tag+"-verifier.json")).write_bytes(prior.canonical(record))
    return record

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cohort",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--task-index",type=int,choices=(0,1),required=True)
    ap.add_argument("--freeze-only",action="store_true")
    ap.add_argument("--endpoint",default="http://127.0.0.1:8080/v1/chat/completions")
    a=ap.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cohort=json.loads(pathlib.Path(a.cohort).read_text())
    assert [r["instance_id"] for r in cohort]==["googlefonts__ufo2ft-930","spikeinterface__spikeinterface-2775"]
    issue=cohort[a.task_index]
    freeze={"protocol":PROTOCOL,"issue":issue["instance_id"],"base_commit":issue["base_commit"],
      "model":prior.MODEL,"model_sha256":prior.MODEL_SHA,"arms":ARMS,
      "seed":int(digest((PROTOCOL+issue["instance_id"]).encode())[:8],16),
      "schema_sha256":digest(prior.canonical(prior.response_format("python_short_id"))),
      "shared_compiler":"repo_transaction; python_short_id normalization in both arms",
      "shared_authority":"all tracked regular files; same create/replace/delete",
      "shared_retrieval":"gold-blind model-selected files before representation assignment",
      "target_policy":"issue-name priority; <=5500 target chars; <=26000 shared facts chars",
      "primary":"compiler acceptance only; functional resolution NOT EVALUATED",
      "status":"prospective exploratory pilot; no superiority claim; unseen boundary untouched"}
    (out/"freeze.json").write_bytes(prior.canonical(freeze))
    if a.freeze_only:return
    root=pathlib.Path("/tmp")/("lattice-run218-"+str(a.task_index))
    prior.clone_issue(issue,root);authority=tracked_authority(root)
    files=prior.retrieve(issue,root,authority,out,a.endpoint)
    f=facts(files,issue)
    assert json.loads(json.dumps(f))==old.parse_python_view(old.python_view(f))
    names=issue_names(issue)
    matched=[(p,t["name"],t["target_id"]) for p,d in f.items()
             for t in d["targets"] if t["name"] in names]
    (out/"target_coverage.json").write_bytes(prior.canonical({
      "issue_identifiers":sorted(names),"matched_targets":matched,
      "facts_sha256":digest(prior.canonical(f)),"facts_chars":len(json.dumps(f)),
      "shared_paths":sorted(files),"information_equivalence":True}))
    raw=out/"raw";raw.mkdir(exist_ok=True)
    records=[]
    for arm in (ARMS if a.task_index==0 else tuple(reversed(ARMS))):
        records.append(invoke(a.endpoint,raw,issue,f,files,authority,arm))
        (out/"records.json").write_bytes(prior.canonical(records))

if __name__=="__main__":main()
