#!/usr/bin/env python3
"""Run312B independent held-out h11 PR115 oracle; disposable CI only."""
import hashlib, json, random, shutil, subprocess, sys
from pathlib import Path
BASE="522b00470b5776dda2dc7e98ff778eb1e418e6ad"
REF="a1197d68630bc37a941b516c7cc74833460fc97c"
HERE=Path(__file__).resolve().parent
FILES=("_receivebuffer.py","_connection.py","_readers.py")
def sha(b):return hashlib.sha256(b).hexdigest()
def cases():
    rng=random.Random(312115);out=[]
    for i in range(64):
        target=i<32; chunked=(not target and i<40)
        body=bytes((65+(i+j)%26 for j in range([0,1,3,7][i%4])))
        if chunked and not body:body=b"z"
        hdr=[(b"Transfer-Encoding",b"chunked")] if chunked else [(b"Content-Length",str(len(body)).encode())]
        hdr.extend((("X-Frozen-%d-%d"%(i,k)).encode(),("v%d-%d"%(i,k)).encode()) for k in range(i%3))
        lines=[b"HTTP/1.1 200 OK"]+[k+b": "+v for k,v in hdr]
        if target:
            mode=i%4
            ends=[(b"\n" if mode in (0,2) else b"\r\n")]
            for j in range(len(hdr)):
                ends.append(b"\n" if mode in (0,1) or (mode==3 and j==0) else b"\r\n")
            blank=b"\n" if mode in (0,1,3) else b"\r\n"
        else:ends=[b"\r\n"]*len(lines);blank=b"\r\n"
        wire=b"".join(line+ending for line,ending in zip(lines,ends))+blank
        if chunked:wire+=("%x\r\n"%len(body)).encode()+body+b"\r\n0\r\n\r\n"
        else:wire+=body
        cuts=sorted(rng.sample(range(1,len(wire)),min(i%3,len(wire)-1)))
        fragments=[wire[a:b] for a,b in zip([0]+cuts,cuts+[len(wire)])]
        out.append({"id":("T" if target else "C")+str(i%32+1),"fragments":[f.hex() for f in fragments],"headers":[(k.lower().hex(),v.hex()) for k,v in hdr],"body_hex":body.hex(),"status":200,"chunked":chunked})
    return out
def evaluate(folder):
    sys.path.insert(0,str(folder));import h11
    for case in cases():
        observed=[];error=None
        try:
            c=h11.Connection(h11.CLIENT)
            c.send(h11.Request(method=b"GET",target=b"/",headers=[(b"Host",b"example.test")]))
            c.send(h11.EndOfMessage())
            for fragment in case["fragments"]:
                c.receive_data(bytes.fromhex(fragment))
                for _ in range(40):
                    event=c.next_event()
                    if event is h11.NEED_DATA:break
                    if event is h11.PAUSED:observed.append({"kind":"PAUSED"});break
                    item={"kind":type(event).__name__}
                    if isinstance(event,h11.Response):
                        item["status"]=event.status_code
                        item["headers"]=[(bytes(k).lower().hex(),bytes(v).hex()) for k,v in event.headers]
                    if isinstance(event,h11.Data):item["data_hex"]=bytes(event.data).hex()
                    observed.append(item)
                    if isinstance(event,h11.EndOfMessage):break
            response=[e for e in observed if e["kind"]=="Response"]
            got_body=b"".join(bytes.fromhex(e["data_hex"]) for e in observed if e["kind"]=="Data")
            got_headers=response[0]["headers"] if len(response)==1 else []
            ok=len(response)==1 and response[0]["status"]==case["status"] and got_body.hex()==case["body_hex"] and sum(e["kind"]=="EndOfMessage" for e in observed)==1 and all(h in got_headers for h in case["headers"])
        except Exception as exc:
            ok=False;error={"type":type(exc).__name__,"message":str(exc)[:300]}
        print(json.dumps({"case":case["id"],"success":ok,"observed":observed,"error":error,"expected":case},sort_keys=True),flush=True)
def git(*a,cwd=None):
    return subprocess.run(["git",*a],cwd=cwd,capture_output=True,text=True,check=True).stdout.strip()
def main():
    out=HERE/"heldout_evidence";out.mkdir(exist_ok=True)
    repo=HERE/"heldout_upstream"
    if not repo.exists():git("clone","--quiet","https://github.com/python-hyper/h11.git",str(repo))
    git("fetch","--quiet","origin","pull/115/head",cwd=repo)
    for rev in (BASE,REF):assert git("rev-parse","--verify",rev+"^{commit}",cwd=repo)==rev
    git("checkout","--quiet","--detach",BASE,cwd=repo)
    base=HERE/"heldout_base";ref=HERE/"heldout_ref"
    for p in (base,ref):
        if p.exists():shutil.rmtree(p)
    shutil.copytree(repo/"h11",base/"h11")
    git("checkout","--quiet","--detach",REF,cwd=repo)
    shutil.copytree(repo/"h11",ref/"h11")
    arms={"BASE":(),"BUFFER_ONLY":("_receivebuffer.py",),"CONNECTION_ONLY":("_connection.py",),"READERS_ONLY":("_readers.py",),"BUFFER_CONNECTION":("_receivebuffer.py","_connection.py"),"BUFFER_READERS":("_receivebuffer.py","_readers.py"),"FULL":FILES}
    allrows=[];hashes={}
    for name,changes in arms.items():
        dest=HERE/("heldout_arm_"+name)
        if dest.exists():shutil.rmtree(dest)
        shutil.copytree(base/"h11",dest/"h11")
        for f in changes:shutil.copy2(ref/"h11"/f,dest/"h11"/f)
        hashes[name]={f:sha((dest/"h11"/f).read_bytes()) for f in FILES}
        proc=subprocess.run([sys.executable,"-I",str(Path(__file__).resolve()),"--eval",str(dest)],capture_output=True,text=True,timeout=120)
        (out/(name+".stdout.jsonl")).write_text(proc.stdout)
        (out/(name+".stderr.txt")).write_text(proc.stderr)
        if proc.returncode:raise RuntimeError(name+" failed: "+proc.stderr[:1000])
        rows=[json.loads(s) for s in proc.stdout.splitlines()]
        assert len(rows)==64
        allrows.extend({"arm":name,**r} for r in rows)
    (out/"traces.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in allrows))
    counts={a:{"target":sum(r["success"] for r in allrows if r["arm"]==a and r["case"].startswith("T")),"control":sum(r["success"] for r in allrows if r["arm"]==a and r["case"].startswith("C"))} for a in arms}
    f={r["case"]:r["success"] for r in allrows if r["arm"]=="FULL"}
    base_control={r["case"] for r in allrows if r["arm"]=="BASE" and r["case"].startswith("C") and r["success"]}
    full_controls={r["case"] for r in allrows if r["arm"]=="FULL" and r["case"].startswith("C") and r["success"]}
    gate=counts["BASE"]["control"]>=24 and counts["BASE"]["target"]<=8 and counts["FULL"]["target"]>=30 and counts["FULL"]["control"]>=30 and base_control.issubset(full_controls) and all(any(r["arm"]==a and not r["success"] and f[r["case"]] for r in allrows) for a in ("BUFFER_CONNECTION","READERS_ONLY","BUFFER_READERS","BUFFER_ONLY"))
    summary={"heldout_gate":"PASS" if gate else "FAIL_NOT_QUALIFIED","counts":counts,"base":BASE,"reference":REF,"case_sha256":sha(json.dumps(cases(),sort_keys=True).encode()),"source_sha256":hashes,"python":sys.version,"n_rows":len(allrows)}
    (out/"summary.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n")
    manifest={p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}
    (out/"SHA256_MANIFEST.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True));print("Evidence SHA256:",json.dumps(manifest,sort_keys=True))
if __name__=="__main__":
    if len(sys.argv)==3 and sys.argv[1]=="--eval":evaluate(Path(sys.argv[2]).resolve())
    elif len(sys.argv)==1:main()
    else:raise SystemExit("usage: script [--eval FOLDER]")
