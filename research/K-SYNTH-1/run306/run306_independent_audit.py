#!/usr/bin/env python3
"""Independent, read-only SHA and isolated CPython replay; no experiment imports."""
import hashlib,json,pathlib,subprocess,sys,collections
P=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
raw_bytes=(P/'RUN306_RAW_FUNCTIONAL.json').read_bytes()
frozen_bytes=(P/'RUN306_FROZEN_SOURCES.json').read_bytes()
raw=json.loads(raw_bytes);frozen=json.loads(frozen_bytes)
assert raw['frozen_sha256']==sha(frozen_bytes)
assert len(raw['records'])==len(frozen['cases'])==384
by_id={r['id']:r for r in raw['records']}
assert len(by_id)==384
checks=[]
program='import json,sys,builtins\ncases=json.loads(sys.stdin.read())\nfor c in cases:\n    ns={"__builtins__":builtins.__dict__,"__name__":"__independent_replay__"}\n    exec(compile(c["source"],"<independent-trusted-fixture>","exec"),ns,ns)\n    print(json.dumps({"id":c["id"],"runtime":{"observed":ns["observed"],"runtime_is_builtin":ns["runtime_is_builtin"]}},sort_keys=True))\n'
replayed={}
for start in range(0,len(frozen['cases']),32):
    chunk=frozen['cases'][start:start+32]
    p=subprocess.run([sys.executable,'-I','-c',program],input=json.dumps(chunk),text=True,
        capture_output=True,timeout=15,check=True)
    for line in p.stdout.splitlines():
        row=json.loads(line);replayed[row['id']]=row['runtime']
for c in frozen['cases']:
    assert sha(c['source'].encode())==c['source_sha256']
    r=by_id[c['id']]
    assert r['source_sha256']==c['source_sha256']
    rt=replayed[c['id']]
    assert rt==r['runtime'],(c['id'],rt,r['runtime'])
    expected=(c['effect']=='restore' and (c['site']!='annotation' or c['mode']=='eager'))
    assert rt['runtime_is_builtin']==expected
    assert rt['observed']==(1+c['variant']%13 if expected else -777)
    assert not(expected and r['new']=='NOT_KNOWN_TARGET')
    checks.append(dict(id=c['id'],source_sha256=c['source_sha256'],runtime=rt))
summary=dict(n=len(checks),source_hashes_verified=len(checks),subprocess_replays_matched=len(checks),
    old_false_negative_count=sum(x['old_false_negative'] for x in raw['records']),
    new_false_negative_count=sum(x['new_false_negative'] for x in raw['records']),
    raw_sha256=sha(raw_bytes),frozen_sha256=sha(frozen_bytes),
    python_version=sys.version.split()[0],independence='12 families x 32 correlated variants')
(P/'RUN306_INDEPENDENT_AUDIT.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
print(json.dumps(summary,sort_keys=True))
