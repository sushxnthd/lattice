#!/usr/bin/env python3
"""Independent read-only audit of original Run381 Actions ZIP artifacts.
Never executes untrusted code; checks raw observations and factorial interactions.
"""
import argparse, hashlib, io, json, pathlib, zipfile
BASE_ZIP_SHA='de82ded63fe23deb77cc9c9a29a36644fe468213bb931054b60df4ddb96e3ce3'
BASE='eb5957d60b240a0deec503a4acca0e69da2833db'
REF='aacdbb940d825987689f1798e5fa999a844da517'
CASES=('public_network_stream_identity','heldout_network_stream_server_addr','control_http_version','control_status','control_body','control_reuse')
ARMS=('base','sync_only','async_only','full')
EXPECTED={'base':(0,8),'sync_only':(2,8),'async_only':(2,8),'full':(4,8)}

def sha(b):return hashlib.sha256(b).hexdigest()
def readzip(path,expected_sha=None):
    raw=pathlib.Path(path).read_bytes()
    if expected_sha is not None and sha(raw)!=expected_sha: raise AssertionError('original ZIP SHA mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        assert len(names)==len(set(names)), 'duplicate archive members'
        assert all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts for n in names), 'unsafe member path'
        return {n:z.read(n) for n in names},sha(raw)

def validate_records(rows):
    assert len(rows)==12,'must have 12 frozen cases'
    seen=set()
    for x in rows:
        assert x['kind'] in ('sync','async')
        assert x['case'] in CASES
        assert x['role']==('target' if x['case'].startswith(('public_','heldout_')) else 'control')
        assert type(x['pass']) is bool
        assert not x.get('error'), 'unexpected oracle error'
        key=(x['kind'],x['case']);assert key not in seen,'duplicate case';seen.add(key)
        t=x['trace']
        assert t['status']==201 and t['body']=='OK' and t['http_version']=='HTTP/2'
        assert ['x-lattice','381'] in t['headers']
        assert t['reuse'] is True and t['stream_id']==1
        assert x['pass']=={
            'public_network_stream_identity':t['network_stream_identity'],
            'heldout_network_stream_server_addr':t['network_stream_server_addr']==['127.0.0.1',443],
            'control_http_version':t['http_version']=='HTTP/2' and type(t['stream_id']) is int,
            'control_status':t['status']==201,
            'control_body':t['body']=='OK' and ['x-lattice','381'] in t['headers'],
            'control_reuse':t['reuse'],
        }[x['case']],'verdict inconsistent with trace'
    assert seen=={(k,c) for k in ('sync','async') for c in CASES}
    return sum(x['pass'] for x in rows if x['role']=='target'),sum(x['pass'] for x in rows if x['role']=='control')

def audit_baseline_members(members):
    assert members['base_commit.txt'].decode().strip()==BASE
    assert members['oracle_exit.txt'].decode().strip()=='0'
    assert members['baseline_stderr.txt']==b''
    summary=json.loads(members['baseline_summary.json'])
    data=members['baseline_raw.json']
    assert summary['raw_sha256']==sha(data)
    assert summary['base']==BASE and summary['prospective_baseline_qualifies'] is True
    rows=json.loads(data)['observations']
    assert validate_records(rows)==(0,8)
    assert (summary['target_pass'],summary['control_pass'])==(0,8)
    return rows

def audit_factorial_members(members):
    summary=json.loads(members['summary.json'])
    assert summary['base']==BASE and summary['reference']==REF
    assert summary['prospective_qualifies'] is True
    assert set(summary['arms'])==set(ARMS)
    by_arm={}
    for arm in ARMS:
        assert members[arm+'.exit'].decode().strip()=='0'
        assert members[arm+'.stderr']==b''
        raw=members[arm+'.json']; data=json.loads(raw)
        assert summary['arms'][arm]['raw_sha256']==sha(raw)
        rows=data['observations']
        assert validate_records(rows)==EXPECTED[arm]
        assert (summary['arms'][arm]['target_pass'],summary['arms'][arm]['control_pass'])==EXPECTED[arm]
        by_arm[arm]={(x['kind'],x['case']):int(x['pass']) for x in rows}
        assert len(by_arm[arm])==12
    interactions={}
    for key in by_arm['base']:
        interactions['/'.join(key)]=by_arm['full'][key]-by_arm['sync_only'][key]-by_arm['async_only'][key]+by_arm['base'][key]
    assert all(v==0 for v in interactions.values()),'unexpected casewise interaction'
    aggregate={a:int(all(v.values())) for a,v in by_arm.items()}
    assert aggregate=={'base':0,'sync_only':0,'async_only':0,'full':1}
    aggregate_interaction=aggregate['full']-aggregate['sync_only']-aggregate['async_only']+aggregate['base']
    assert aggregate_interaction==1
    return {'arms':{a:{'target_pass':EXPECTED[a][0],'control_pass':EXPECTED[a][1]} for a in ARMS},'casewise_interactions':interactions,'aggregate_interaction':aggregate_interaction}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--factorial');ap.add_argument('--output');args=ap.parse_args()
    base,base_sha=readzip(args.baseline,BASE_ZIP_SHA)
    rows=audit_baseline_members(base)
    report={'baseline_zip_sha256':base_sha,'baseline_records':len(rows),'baseline_target_pass':0,'baseline_control_pass':8}
    if args.factorial:
        f,fsha=readzip(args.factorial)
        report['factorial_zip_sha256']=fsha
        report['factorial']=audit_factorial_members(f)
    raw=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:pathlib.Path(args.output).write_text(raw)
    print(raw)

if __name__=='__main__':main()
