#!/usr/bin/env python3
"""Frozen Run312 h11 PR115 qualification, four isolated historical source arms."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
BASE="522b00470b5776dda2dc7e98ff778eb1e418e6ad"
REF="a1197d68630bc37a941b516c7cc74833460fc97c"
FILES=("_receivebuffer.py","_connection.py","_readers.py")
HERE=Path(__file__).resolve().parent
CASES=[
("T1",[b"HTTP/1.1 200 OK\nContent-Length: 0\n\n"],200,b""),
("T2",[b"HTTP/1.1 200 OK\nContent-Length: 3\n\nabc"],200,b"abc"),
("T3",[b"HTTP/1.1 200 OK\r\nContent-Length: 0\n\n"],200,b""),
("T4",[b"HTTP/1.1 200 OK\nContent-Length: 0\r\n\r\n"],200,b""),
("T5",[b"HTTP/1.1 200 OK\nCont",b"ent-Length: 3\n",b"\nabc"],200,b"abc"),
("T6",[b"HTTP/1.1 200 OK\r\nX-Test: a\nContent-Length: 3\r\n\nabc"],200,b"abc"),
("C1",[b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"],200,b""),
("C2",[b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nabc"],200,b"abc"),
("C3",[b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nabc\r\n0\r\n\r\n"],200,b"abc"),
("C4",[b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r",b"\nabc\r\n0\r",b"\n\r\n"],200,b"abc"),
("C5",[b"HTTP/1.1 200 OK\r\nX-Test: a\r\nContent-Length: 3\r\n\r\nabc"],200,b"abc"),
("C6",[b"HTTP/1.1 204 No Content\r\nX-Test: a\r\n\r\n"],204,b""),
]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evaluate(folder):
    sys.path.insert(0,str(folder))
    import h11
    for cid,chunks,status,body in CASES:
        events=[]; error=None
        try:
            c=h11.Connection(h11.CLIENT)
            c.send(h11.Request(method=b"GET",target=b"/",headers=[(b"Host",b"example.test")]))
            c.send(h11.EndOfMessage())
            for chunk in chunks:
                c.receive_data(chunk)
                for _ in range(20):
                    ev=c.next_event()
                    if ev is h11.NEED_DATA: break
                    if ev is h11.PAUSED:
                        events.append({"kind":"PAUSED"}); break
                    item={"kind":type(ev).__name__}
                    if isinstance(ev,(h11.Response,h11.InformationalResponse)): item["status"]=ev.status_code
                    if isinstance(ev,h11.Data): item["data_hex"]=bytes(ev.data).hex()
                    events.append(item)
                    if isinstance(ev,h11.EndOfMessage): break
            statuses=[e.get("status") for e in events if e["kind"]=="Response"]
            actual=b"".join(bytes.fromhex(e["data_hex"]) for e in events if e["kind"]=="Data")
            ok=statuses==[status] and actual==body and sum(e["kind"]=="EndOfMessage" for e in events)==1
        except Exception as exc:
            ok=False; error={"type":type(exc).__name__,"message":str(exc)[:500]}
        print(json.dumps({"case":cid,"success":ok,"observed":events,"error":error,"chunks_hex":[x.hex() for x in chunks],"expected_status":status,"expected_body_hex":body.hex()},sort_keys=True),flush=True)
def git(*args,cwd=None):
    return subprocess.run(["git",*args],cwd=cwd,check=True,capture_output=True,text=True).stdout.strip()
def main():
    out=HERE/"evidence";out.mkdir(exist_ok=True)
    upstream=HERE/"upstream_h11"
    if not upstream.exists():git("clone","--quiet","https://github.com/python-hyper/h11.git",str(upstream))
    # PR head lives in a fork; fetch the immutable upstream pull ref explicitly.
    git("fetch","--quiet","origin","pull/115/head",cwd=upstream)
    for commit in (BASE,REF):
        assert git("rev-parse","--verify",commit+"^{commit}",cwd=upstream)==commit
    git("checkout","--quiet","--detach",BASE,cwd=upstream)
    base=HERE/"source_base";ref=HERE/"source_ref"
    for folder in (base,ref):
        if folder.exists():shutil.rmtree(folder)
    shutil.copytree(upstream/"h11",base/"h11")
    git("checkout","--quiet","--detach",REF,cwd=upstream)
    shutil.copytree(upstream/"h11",ref/"h11")
    traces=[];hashes={}
    for name,changed in {"BASE":(),"A":("_receivebuffer.py","_connection.py"),"B":("_readers.py",),"FULL":FILES}.items():
        folder=HERE/("arm_"+name)
        if folder.exists():shutil.rmtree(folder)
        shutil.copytree(base/"h11",folder/"h11")
        for f in changed:shutil.copy2(ref/"h11"/f,folder/"h11"/f)
        hashes[name]={f:sha(folder/"h11"/f) for f in FILES}
        run=subprocess.run([sys.executable,"-I",str(Path(__file__).resolve()),"--eval",str(folder)],capture_output=True,text=True,timeout=90)
        (out/(name+".stdout.jsonl")).write_text(run.stdout)
        (out/(name+".stderr.txt")).write_text(run.stderr)
        if run.returncode:raise RuntimeError(name+" evaluator exited "+str(run.returncode)+": "+run.stderr[:1000])
        rows=[json.loads(s) for s in run.stdout.splitlines()]
        assert len(rows)==len(CASES) and [r["case"] for r in rows]==[x[0] for x in CASES]
        traces.extend({"arm":name,**r} for r in rows)
    (out/"traces.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in traces))
    counts={a:{"target_pass":sum(r["success"] for r in traces if r["arm"]==a and r["case"].startswith("T")),"control_pass":sum(r["success"] for r in traces if r["arm"]==a and r["case"].startswith("C"))} for a in ("BASE","A","B","FULL")}
    full={r["case"]:r["success"] for r in traces if r["arm"]=="FULL"}
    gate=counts["BASE"]["target_pass"]<=2 and counts["BASE"]["control_pass"]==6 and counts["FULL"]=={"target_pass":6,"control_pass":6} and all(any(r["arm"]==a and not r["success"] and full[r["case"]] for r in traces) for a in ("A","B"))
    summary={"qualification_gate":"PASS" if gate else "FAIL_NOT_QUALIFIED","counts":counts,"source_sha256":hashes,"base":BASE,"reference":REF,"python":sys.version,"n_cases":len(CASES),"n_trace_rows":len(traces),"case_sha256":hashlib.sha256(json.dumps([(x,[c.hex() for c in y],z,b.hex()) for x,y,z,b in CASES],sort_keys=True).encode()).hexdigest()}
    (out/"summary.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n")
    manifest={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}
    (out/"SHA256_MANIFEST.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True));print("Evidence SHA256:",json.dumps(manifest,sort_keys=True))
if __name__=="__main__":
    if len(sys.argv)==3 and sys.argv[1]=="--eval":evaluate(Path(sys.argv[2]).resolve())
    elif len(sys.argv)==1:main()
    else:raise SystemExit("usage: run312_h11_qualification.py [--eval ARM_DIR]")
