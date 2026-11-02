#!/usr/bin/env python3
"""Independent read-only receipt sanity check. Requires original Run437 Actions ZIP."""
import hashlib, json, sys, zipfile
p=sys.argv[1]
b=open(p,'rb').read()
assert hashlib.sha256(b).hexdigest()=='2708ecd7c476c963ac27b168e60d3f66cb08aa26813994bf01b8ad9e606bb6d5'
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    sha=json.loads(z.read('tmp/lattice437/sha256.json'))
    for k,v in sha.items():
        assert hashlib.sha256(z.read('tmp/lattice437/'+k)).hexdigest()==v
    meta=json.loads(z.read('tmp/lattice437/meta.json'))
    rows=[json.loads(x) for x in z.read('tmp/lattice437/raw.jsonl').splitlines()]
assert meta['base_commit']=='6f7762538bffe3ce9d03508ecab230bfff3e3dcd'
assert meta['reference_commit']=='190dd4df86874495f56bb088fbd0cb1d9f0e77a0'
assert len(rows)==84 and len({(r['variant'],r['case']) for r in rows})==84
idx={(r['variant'],r['case']):r for r in rows}
for c in ('T1_reporter','T2_reverse','T3_three'):
    assert idx['base',c]['result']['exit']==1
    assert idx['ref',c]['result']['exit']==0
assert idx['base','C4_runtime']['result']['exit']==0
assert idx['ref','C4_runtime']['result']['exit']==1
assert "cannot import name 'safe_join'" in idx['ref','C4_runtime']['result']['stderr']
print('PASS original artifact SHA, two internal hashes, 84 receipts, target/control contradiction')
