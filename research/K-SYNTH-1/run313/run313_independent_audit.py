#!/usr/bin/env python3
"""Independent read-only Run313 audit. Does not import the original generator."""
import collections
import hashlib
import json
from pathlib import Path
import sys
import zipfile

def sha(b):
    return hashlib.sha256(b).hexdigest()

def outcome(r):
    return (bool(r['complete']), tuple(r['statuses']), r['body_hex'],
            None if r['error'] is None else r['error']['type'])

def audit(files):
    byarm={}
    stats={}
    for name, raw in files.items():
        rows=[json.loads(x) for x in raw.decode().splitlines()]
        assert len(rows)==1191, (name,len(rows))
        assert len({r['case'] for r in rows})==1191
        assert len({r['stream'] for r in rows})==22
        assert len({r['wire_sha256'] for r in rows})==22
        assert all(r['case'].startswith(r['stream']+'/') for r in rows)
        streams=collections.defaultdict(list)
        for r in rows:
            assert r['group'] in {'valid_control','valid_target','adversarial'}
            streams[r['stream']].append(r)
        divergent={k:len({outcome(r) for r in v}) for k,v in streams.items()
                   if len({outcome(r) for r in v})>1}
        stats[name]={'rows':len(rows),'streams':len(streams),
                     'fragmentation_divergent_streams':divergent,
                     'n_by_group':{g:sum(r['group']==g for r in rows)
                                   for g in ('valid_control','valid_target','adversarial')},
                     'complete_by_group':{g:sum(r['group']==g and r['complete'] for r in rows)
                                          for g in ('valid_control','valid_target','adversarial')}}
        byarm[name]={r['case']:r for r in rows}
    names=list(byarm)
    for name in names[1:]:
        assert byarm[name].keys()==byarm[names[0]].keys()
        for key in byarm[name]:
            assert byarm[name][key]['wire_sha256']==byarm[names[0]][key]['wire_sha256']
            assert byarm[name][key]['group']==byarm[names[0]][key]['group']
    pairwise={}
    for i,a in enumerate(names):
        for b in names[i+1:]:
            diffs=[k for k in byarm[a] if outcome(byarm[a][k])!=outcome(byarm[b][k])]
            pairwise[a+' vs '+b]={'n_different':len(diffs),
                'by_group':dict(collections.Counter(byarm[a][k]['group'] for k in diffs)),
                'example_cases':sorted(diffs)[:20]}
    return {'arms':stats,'pairwise':pairwise,'independent_audit':'PASS',
            'notes':'Correlated variants; no exploit or IR superiority claim.'}

def main():
    p=Path(sys.argv[1])
    if p.suffix=='.zip':
        with zipfile.ZipFile(p) as z:
            entries={k:z.read(k) for k in z.namelist() if k.endswith('.stdout.jsonl')}
            manifests=[k for k in z.namelist() if k.endswith('SHA256_MANIFEST.json')]
            if manifests:
                manifest=json.loads(z.read(manifests[0]))
                for name,expected in manifest.items():
                    hits=[k for k in z.namelist() if k==name or k.endswith('/'+name)]
                    assert len(hits)==1 and sha(z.read(hits[0]))==expected,(name,'SHA MISMATCH')
            files={Path(k).name.replace('.stdout.jsonl',''):v for k,v in entries.items()}
    else:
        files={'MODERN_0_16_0':p.read_bytes()}
    result=audit(files)
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    main()
