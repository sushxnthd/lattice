"""Run217: frozen real-issue paired presentation experiment.

Semantic-node JSON vs annotated Python source. Both expose identical facts and
use exact-text actions, identical compiler, authority, verifier, model and seed.
Compiler acceptance is exploratory; functional resolution is NOT evaluated.
"""
import argparse, hashlib, json, pathlib, urllib.request
import paired_repo_pilot as base
from repo_transaction import digest, tracked_authority

SEED="K-SYNTH-1/run217-real-issues-freeze-v1"
PROTOCOL="K-SYNTH-1/run217-paired-presentation-v1"
ARMS=("semantic_ir_json","python_annotated")
IDS=("googlefonts__ufo2ft-930","spikeinterface__spikeinterface-2775")
DATA_SHA="f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2"

def cohort(data):
    eligible=[x for x in data if x["split"]=="discovery" and 70<=len(x["problem_statement"])<=1700]
    eligible.sort(key=lambda x:hashlib.sha256((SEED+"|"+x["instance_id"]).encode()).hexdigest())
    out=[];seen=set()
    for x in eligible:
        if x["repo"] in seen:continue
        out.append(x);seen.add(x["repo"])
        if len(out)==2:break
    assert tuple(x["instance_id"] for x in out)==IDS
    return out

def python_view(f):
    parts=[]
    for path,item in sorted(f.items()):
        parts.append("### FILE "+json.dumps(path))
        parts.append("# file_sha256: "+item["file_sha256"])
        parts.append("# full_source_bytes: "+str(item["full_source_bytes"]))
        for t in item["targets"]:
            parts.append("# AST_TARGET "+json.dumps(t,sort_keys=True,ensure_ascii=False))
        parts.append("### SOURCE_EXCERPT "+json.dumps(item["source_excerpt"],ensure_ascii=False))
        parts.append("### END_FILE")
    return "\n".join(parts)

def parse_python_view(s):
    out={};path=None;item=None
    for line in s.splitlines():
        if line.startswith("### FILE "):
            assert path is None
            path=json.loads(line[9:]);item={"targets":[]}
        elif line.startswith("# file_sha256: "):item["file_sha256"]=line[15:]
        elif line.startswith("# full_source_bytes: "):item["full_source_bytes"]=int(line[21:])
        elif line.startswith("# AST_TARGET "):item["targets"].append(json.loads(line[13:]))
        elif line.startswith("### SOURCE_EXCERPT "):item["source_excerpt"]=json.loads(line[19:])
        elif line=="### END_FILE":
            assert set(item)=={"file_sha256","full_source_bytes","targets","source_excerpt"}
            out[path]=item;path=item=None
        else:raise ValueError("invalid view")
    assert path is None
    return out

def prompt(issue,f,arm):
    if arm=="semantic_ir_json":
        view=json.dumps(f,sort_keys=True,ensure_ascii=False,separators=(",",":"))
        guide="Read the typed semantic-node JSON representation."
    else:
        view=python_view(f)
        guide="Read the annotated ordinary Python source and AST_TARGET comments."
    return ("Repair the repository issue. Both conditions receive identical source and semantic target facts, "
      "identical file access, and identical edit authority. The only intervention is presentation. "
      "Use exact original text as edit selector; no high-level semantic rename operation is available. "
      "Return a JSON object with actions array. Each action has EXACTLY six string fields: "
      "op,path,file_sha256,selector,replacement,content. "
      "For replace, use op=replace, selector=exact old_text from a listed target, "
      "replacement=complete new target text, content=empty string. "
      "For create, set op=create, path and content, other fields empty. "
      "For delete, set op=delete, path and file_sha256, other fields empty. "
      "Do not delete files merely to edit them. No Markdown. "
      +guide+"\nISSUE:\n"+issue["problem_statement"]+"\nSOURCE_FACTS:\n"+view)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--public",required=True);p.add_argument("--out",required=True)
    p.add_argument("--task-index",type=int,choices=(0,1),required=True)
    p.add_argument("--freeze-only",action="store_true")
    p.add_argument("--endpoint",default="http://127.0.0.1:8080/v1/chat/completions")
    a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    raw=pathlib.Path(a.public).read_bytes();assert digest(raw)==DATA_SHA
    selected=cohort(json.loads(raw));issue=selected[a.task_index]
    seed=int(digest((PROTOCOL+issue["instance_id"]).encode())[:8],16)
    freeze={"protocol":PROTOCOL,"cohort":[{"id":x["instance_id"],"repo":x["repo"],"base_commit":x["base_commit"]} for x in selected],
       "dataset_sha256":DATA_SHA,"arms":ARMS,"model":base.MODEL,"model_sha256":base.MODEL_SHA,
       "seed":seed,"max_tokens":2048,"temperature":0,"boundary_used":False,
       "same_authority":True,"same_compiler":True,"same_action_schema":True,
       "functional_resolution":"NOT_EVALUATED","confirmatory":False}
    (out/"freeze.json").write_bytes(base.canonical(freeze))
    if a.freeze_only:return
    root=pathlib.Path("/tmp")/("lattice-run217-"+str(a.task_index))
    base.clone_issue(issue,root)
    authority=tracked_authority(root)
    files=base.retrieve(issue,root,authority,out,a.endpoint)
    f=base.compact_facts(files,issue,max_chars=26000)
    assert json.loads(json.dumps(f,sort_keys=True))==parse_python_view(python_view(f))
    (out/"information_equivalence.json").write_bytes(base.canonical({
       "facts_sha256":digest(base.canonical(f)),"verified":True,
       "authority_sha256":digest(base.canonical(sorted(authority))),
       "paths":sorted(files),"authority_count":len(authority)}))
    results=[];folder=out/"raw";folder.mkdir(exist_ok=True)
    for arm in (ARMS if a.task_index==0 else tuple(reversed(ARMS))):
        text=prompt(issue,f,arm)
        req={"model":base.MODEL,"messages":[{"role":"user","content":text}],
           "temperature":0,"seed":seed,"max_tokens":2048,"stream":False,
           "response_format":base.response_format("python_text")}
        tag=issue["instance_id"]+"-"+arm
        (folder/(tag+"-request.json")).write_bytes(base.canonical(req))
        record={"task":issue["instance_id"],"arm":arm,"seed":seed,
            "model":base.MODEL,"model_sha256":base.MODEL_SHA,
            "prompt_sha256":digest(text.encode()),"facts_sha256":digest(base.canonical(f)),
            "accepted":False,"functional_resolution":"NOT_EVALUATED"}
        try:
            request=urllib.request.Request(a.endpoint,data=base.canonical(req),
                        headers={"Content-Type":"application/json"},method="POST")
            body=urllib.request.urlopen(request,timeout=2400).read(4_000_000)
            (folder/(tag+"-response.json")).write_bytes(body)
            response=json.loads(body);choice=response["choices"][0]
            record.update(usage=response.get("usage"),model_reported=response.get("model"),
                          finish_reason=choice.get("finish_reason"))
            tx=base.compile_arm(files,json.loads(choice["message"]["content"]),authority,"python_text")
            record.update(accepted=True,trace=tx.trace,before=tx.before,after=tx.after,
                          changed_paths=sorted(tx.changes))
        except Exception as exc:record["error"]=repr(exc)
        (folder/(tag+"-verifier.json")).write_bytes(base.canonical(record))
        results.append(record);(out/"records.json").write_bytes(base.canonical(results))

if __name__=="__main__":main()
