#!/usr/bin/env python3
"""Read-only verification of original Run389 artifact; never execute model code."""
import ast, hashlib, io, json, pathlib, re, sys, zipfile
def sha(b): return hashlib.sha256(b).hexdigest()
def main(root):
    original=(root/"lattice_run389_cloud_original.zip").read_bytes()
    assert sha(original)=="a8e57250868ab0897e464c72650cd8fda429e916a7325e6ff97b29c9a4083717"
    with zipfile.ZipFile(io.BytesIO(original)) as z:
        manifest=json.loads(z.read("manifest.json"))
        assert len(manifest)==26
        for name,meta in manifest.items():
            data=z.read(name)
            assert len(data)==meta["size"] and sha(data)==meta["sha256"],name
        freeze=json.loads(z.read("freeze.json"))
        assert freeze["model_sha256"]=="509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c"
        sources={"rich/_wrap.py":(root/"base_wrap.py").read_bytes(),
                 "rich/cells.py":(root/"base_cells.py").read_bytes()}
        for path,data in sources.items(): assert sha(data)==freeze["source_sha256"][path]
        old=sources["rich/_wrap.py"].decode()
        fn=next(n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef) and n.name=="divide_line")
        old_fn="".join(old.splitlines(keepends=True)[fn.lineno-1:fn.end_lineno])
        ids=set(); completions=set()
        for arm in ("IR_facts_first","IR_source_first","PYTHON_AST_facts_first","PYTHON_AST_source_first"):
            raw=z.read("completion_"+arm+".txt")
            completions.add(sha(raw))
            inf=json.loads(z.read("inference_"+arm+".json"))
            response=json.loads(z.read("response_"+arm+".raw.json"))
            ids.add(response["id"])
            assert sha(raw)==inf["completion_sha256"]
            assert inf["compiler"]=="rejected" and inf["status"]=="completed"
            assert response["choices"][0]["message"]["content"]==raw.decode()
            try: json.loads(raw)
            except json.JSONDecodeError: pass
            else: raise AssertionError("Unexpected strict JSON success")
            m=re.fullmatch(r"```json\r?\n([\s\S]*?)\r?\n```\s*",raw.decode())
            assert m
            edits=json.loads(m.group(1))["edits"]
            assert len(edits)==1
            assert edits[0]["path"]=="rich/_wrap.py" and edits[0]["function"]=="divide_line"
            assert edits[0]["replacement"].rstrip("\r\n")+"\n"==old_fn
        assert len(ids)==4 and len(completions)==1
    print("PASS: 26 original payloads; 4 distinct responses; 1 identical no-op; 0 valid repairs")
if __name__=="__main__":
    main(pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "."))
