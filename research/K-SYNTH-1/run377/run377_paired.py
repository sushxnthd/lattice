#!/usr/bin/env python3
"""Run377: reference-blind paired HTTPcore #670 model pilot.

Never loads reference PR #680. Model output is parsed as data, never executed
on the runner host. Docker oracle execution is isolated and network disabled.
"""
import argparse, ast, hashlib, json, pathlib, re, shutil, subprocess, time, urllib.request

BASE="5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e"
PATHS=("httpcore/_async/connection_pool.py","httpcore/_sync/connection_pool.py")
BLOBS=("e6c4ef66312d4d6f31fcbfc417905ae329ef5885","53536d05e8c3d127b466e44dcf20e9f028aadab0")
SEED=3772026
MODEL="Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M"
MAX_TOKENS=1400

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path,obj): path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
def check(root):
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    assert head==BASE,(head,BASE)
    for p,expected in zip(PATHS,BLOBS):
        got=subprocess.check_output(["git","hash-object",str(root/p)],text=True).strip()
        assert got==expected,(p,got,expected)

def extract(root):
    """Issue-visible localization and exact pinned-source AST, not reference patch."""
    facts=[]; excerpts=[]
    for path,kind,method in zip(PATHS,("async","sync"),("handle_async_request","handle_request")):
        source=(root/path).read_text()
        lines=source.splitlines(keepends=True)
        tree=ast.parse(source)
        nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==method]
        assert len(nodes)==1
        node=nodes[0]
        handlers=[h for h in ast.walk(node) if isinstance(h,ast.ExceptHandler) and isinstance(h.type,ast.Name) and h.type.id=="BaseException"]
        # There are TWO BaseException handlers: the queue-wait cleanup and the
        # later connection-response cleanup. Select the issue-linked handler
        # by the original source operation, not by reference patch content.
        matched=[]
        for h in handlers:
            removes=[n for n in ast.walk(h) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="remove"]
            if len(removes)==1 and ast.unparse(removes[0])=="self._requests.remove(status)":
                matched.append((h,removes[0]))
        assert len(matched)==1,("ambiguous issue-linked cleanup",kind,len(matched))
        h,remove_call=matched[0]
        removes=[remove_call]
        line=removes[0].lineno
        start=max(node.lineno,line-19)
        end=min(len(lines),line+13)
        excerpt="".join(f"{i:04d} {lines[i-1]}" for i in range(start,end+1))
        excerpts.append(f"FILE {path} (unaltered baseline; line numbers not source)\n{excerpt}")
        facts.append((kind,method,"BaseException","self._requests.remove(status)","raise exc","UNKNOWN"))
    return facts,"\n\n".join(excerpts)

def ir_render(facts):
    return "\n".join("IR_NODE|"+("|".join(row))+"\nIR_EDGE|"+row[0]+"|WAIT->EXCEPT->REMOVE->RAISE|MAY" for row in facts)

def python_render(facts):
    # A normal Python AST-action ledger with explicit call ordering and uncertainty.
    rows=",\n    ".join(repr(row) for row in facts)
    return "def ordinary_python_ast_actions():\n    return [\n    "+rows+"\n    ]"

def ir_reconstruct(s):
    out=[]
    for line in s.splitlines():
        if line.startswith("IR_NODE|"):
            row=tuple(line.split("|")[1:])
            assert len(row)==6
            out.append(row)
    return out

def py_reconstruct(s):
    tree=ast.parse(s)
    fn=tree.body[0]
    assert isinstance(fn,ast.FunctionDef) and len(fn.body)==1 and isinstance(fn.body[0],ast.Return)
    return [tuple(x) for x in ast.literal_eval(fn.body[0].value)]

def prompt(arm,facts,excerpts):
    presentation=ir_render(facts) if arm=="IR" else python_render(facts)
    title="Soundness-scoped semantic/control-flow IR (runtime interleavings UNKNOWN)" if arm=="IR" else "Ordinary Python AST-action representation (runtime interleavings UNKNOWN)"
    return ("You are repairing an upstream Python library from its historical issue report. "
      "No reference solution is provided. Both authorized production files must be repaired atomically.\n\n"
      "Issue encode/httpcore #670 (reported 2023-04-18): 'ValueError: list.remove(x): x not in list'. "
      "Under streaming responses, backpressure and a full connection pool, a cancellation during "
      "wait_for_connection raised CancelledError, then the exception handler raised ValueError "
      "while removing a request status that was no longer in the queue. "
      "The issue traceback identifies the async pool; consider its synchronous counterpart too.\n\n"
      "The following AST-derived facts do not certify concurrent interleavings. "
      "UNKNOWN means no sound runtime dependence conclusion is available.\n"
      +title+"\n"+presentation+"\n\nOriginal authorized source excerpts (exact bytes after line-number prefix removal):\n"
      +excerpts+"\n\n"
      "Allowed paths only: "+", ".join(PATHS)+". "
      "Return exactly one JSON object, no prose, with key edits containing exactly two objects, "
      "one for each path. Each object has path, old, new. old must be a nonempty exact "
      "substring of the original file occurring exactly once; new is the replacement. "
      "Both changes must be syntactically valid. All edits are compiled atomically by the same verifier. "
      "Example FORMAT ONLY for an unrelated file: "
      '{"edits":[{"path":"example.py","old":"x = 1\\n","new":"x = 2\\n"}]}'+"\n"
      "Do not write a unified diff, markdown fences, or any explanation.")

def freeze(root,out):
    check(root);facts,excerpts=extract(root)
    ir=ir_render(facts);py=python_render(facts)
    assert ir_reconstruct(ir)==py_reconstruct(py)==facts
    dump(out/"facts.json",facts)
    (out/"source_excerpts.txt").write_text(excerpts)
    rows={}
    for arm in ("IR","PYTHON_AST"):
        p=prompt(arm,facts,excerpts)
        req={"model":MODEL,"messages":[{"role":"user","content":p}],"temperature":0,"seed":SEED,"max_tokens":MAX_TOKENS,"stream":False}
        dump(out/f"request_{arm}.json",req)
        rows[arm]={"prompt_sha256":sha(p.encode()),"request_sha256":sha((out/f"request_{arm}.json").read_bytes()),"characters":len(p)}
    dump(out/"freeze.json",{"base":BASE,"blobs":dict(zip(PATHS,BLOBS)),"facts":facts,
          "facts_sha256":sha(json.dumps(facts,sort_keys=True).encode()),"arms":rows,
          "parity":True,"reference_patch_seen":False,"seed":SEED,"max_tokens":MAX_TOKENS})
    print(json.dumps(rows,sort_keys=True))

def infer(out,arm):
    req=(out/f"request_{arm}.json").read_bytes()
    url="http://127.0.0.1:8080/v1/chat/completions"
    start=time.monotonic()
    try:
        request=urllib.request.Request(url,data=req,headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(request,timeout=3600) as response:raw=response.read()
        (out/f"response_{arm}.raw.json").write_bytes(raw)
        data=json.loads(raw)
        text=data["choices"][0]["message"]["content"]
        (out/f"completion_{arm}.txt").write_text(text)
        dump(out/f"inference_{arm}.json",{"status":"completed","elapsed_sec":round(time.monotonic()-start,3),
             "usage":data.get("usage"),"finish_reason":data["choices"][0].get("finish_reason"),
             "raw_sha256":sha(raw),"completion_sha256":sha(text.encode())})
    except Exception as exc:
        dump(out/f"inference_{arm}.json",{"status":"infrastructure_failure_precompletion",
            "elapsed_sec":round(time.monotonic()-start,3),"error":repr(exc)})
    print((out/f"inference_{arm}.json").read_text())

def parse_completion(raw):
    raw=raw.strip()
    if raw.startswith("```"):
        raw=re.sub(r"^\x60{3}(?:json)?\s*","",raw)
        raw=re.sub(r"\s*\x60{3}$","",raw)
    return json.loads(raw)

def compile_arm(root,out,arm):
    info={"arm":arm,"status":"not_completed"}
    completion=out/f"completion_{arm}.txt"
    if not completion.exists():
        dump(out/f"compile_{arm}.json",info);return
    stage=out/"stages"/arm
    temp=out/"stages"/(arm+".tmp")
    try:
        data=parse_completion(completion.read_text())
        assert isinstance(data,dict) and set(data)=={"edits"}
        edits=data["edits"]
        assert isinstance(edits,list) and len(edits)==2
        assert set(e.get("path") for e in edits)==set(PATHS)
        check(root)
        if temp.exists():shutil.rmtree(temp)
        shutil.copytree(root,temp,ignore=shutil.ignore_patterns(".git"))
        for e in edits:
            assert isinstance(e,dict) and set(e)=={"path","old","new"}
            old,new=e["old"],e["new"]
            assert isinstance(old,str) and isinstance(new,str) and len(old)>0
            assert old!=new and len(old)<20000 and len(new)<20000
            path=temp/e["path"]
            source=path.read_text()
            assert source.count(old)==1,("preimage_count",e["path"],source.count(old))
            updated=source.replace(old,new,1)
            ast.parse(updated,filename=e["path"])
            path.write_text(updated)
        assert all(ast.parse((temp/p).read_text()) for p in PATHS)
        if stage.exists():shutil.rmtree(stage)
        temp.rename(stage)
        info={"arm":arm,"status":"accepted","source_shas":{p:sha((stage/p).read_bytes()) for p in PATHS}}
    except Exception as exc:
        info={"arm":arm,"status":"rejected","reason":repr(exc)}
        if temp.exists():shutil.rmtree(temp)
    dump(out/f"compile_{arm}.json",info)
    print(info)

def manifest(out):
    rows={}
    for path in sorted(out.rglob("*")):
        if path.is_file() and path.name!="manifest.json":
            rows[str(path.relative_to(out))]={"sha256":sha(path.read_bytes()),"size":path.stat().st_size}
    dump(out/"manifest.json",rows)
    print(json.dumps({"files":len(rows),"total_bytes":sum(x["size"] for x in rows.values())}))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=("freeze","infer","compile","manifest"))
    ap.add_argument("--root",default="upstream")
    ap.add_argument("--out",default="run377-results")
    ap.add_argument("--arm",choices=("IR","PYTHON_AST"))
    a=ap.parse_args()
    root=pathlib.Path(a.root).resolve();out=pathlib.Path(a.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    if a.mode=="freeze":freeze(root,out)
    if a.mode=="infer":infer(out,a.arm)
    if a.mode=="compile":compile_arm(root,out,a.arm)
    if a.mode=="manifest":manifest(out)

if __name__=="__main__":main()
