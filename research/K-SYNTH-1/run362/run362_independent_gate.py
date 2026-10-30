"""Independent read-only Run362 evidence gate. No historical source execution."""
import hashlib
import json
from pathlib import Path

EXPECTED_GIT_BLOBS = {
    ('base','anyio/_backends/_asyncio.py'): 'dd1f09c7998e45c496b4b6501f7a46225caaa964',
    ('base','anyio/streams/memory.py'): 'f74f8b8f123d69c345827565c018e268f2e83ae7',
    ('head','anyio/_backends/_asyncio.py'): 'f8ed75609c0249ddae5273f589e2df6c7194d63f',
    ('head','anyio/streams/memory.py'): '530c60679d98a43e7ae5bdb158473f2b43d0c66e',
}
TARGETS = ('T1_event_cancel_after_set','T2_event_cancel_after_set_nested',
           'T3_event_cancel_after_set_shielded','T4_memory_race_0',
           'T5_memory_race_1','T6_memory_race_2')
CONTROLS = ('C1_event_regular','C2_memory_buffered','C3_memory_rendezvous',
            'C4_blocked_receive_cancel','C5_stream_end','C6_cancel_checkpoint')
VARIANTS = ('base','backend_only','memory_only','full')

class EvidenceError(ValueError): pass

def fail_if(cond, message):
    if cond: raise EvidenceError(message)

def verify(directory):
    root=Path(directory)
    manifest=json.loads((root/'sha256_manifest.json').read_text())
    fail_if(not isinstance(manifest,dict) or not manifest, 'empty manifest')
    for filename, expected in manifest.items():
        fail_if('/' in filename or '..' in filename, 'unsafe manifest path')
        p=root/filename
        fail_if(not p.is_file(), 'missing evidence '+filename)
        fail_if(hashlib.sha256(p.read_bytes()).hexdigest()!=expected, 'bad sha256 '+filename)
    required={*(v+'.json' for v in VARIANTS),'source_verification.json',
              'qualification_summary.json','pip_freeze.txt','image_digest.txt'}
    fail_if(not required.issubset(manifest), 'missing manifest entries')
    source=json.loads((root/'source_verification.json').read_text())
    fail_if(not isinstance(source,list) or len(source)!=4, 'source count')
    observed={}
    for row in source:
        fail_if(set(row)!={'side','path','git_blob'},'source fields')
        key=(row['side'],row['path'])
        fail_if(key in observed,'duplicate source identity')
        observed[key]=row['git_blob']
    fail_if(observed!=EXPECTED_GIT_BLOBS,'source mismatch')
    data={v:json.loads((root/(v+'.json')).read_text()) for v in VARIANTS}
    expected_ids=list(TARGETS)+list(CONTROLS)
    for variant, record in data.items():
        fail_if(record.get('schema')!='lattice.run362.anyio.v1','schema '+variant)
        fail_if(not record.get('python','').startswith('3.11.'),'python '+variant)
        fail_if(not record.get('anyio_path','').startswith('/src/anyio/'),'wrong package '+variant)
        rows=record.get('outcomes')
        fail_if(not isinstance(rows,list) or len(rows)!=12,'outcome count '+variant)
        fail_if([r.get('name') for r in rows]!=expected_ids,'case order '+variant)
        for i,r in enumerate(rows):
            fail_if(set(r)!={'name','kind','passed','error'},'case fields')
            fail_if(r['kind']!=('target' if i<6 else 'control'),'kind mismatch')
            fail_if(type(r['passed']) is not bool,'non-boolean pass')
            fail_if((r['error'] is None)!=r['passed'],'error/status mismatch')
    counts={v:{kind:sum(r['passed'] for r in data[v]['outcomes'] if r['kind']==kind)
               for kind in ('target','control')} for v in VARIANTS}
    qualified=(counts['full']=={'target':6,'control':6}
               and counts['base']['target']<6 and counts['base']['control']==6
               and all(counts[v]['target']<6 or counts[v]['control']<6
                       for v in ('backend_only','memory_only'))
               and any(data['backend_only']['outcomes'][i]['passed']!=data['memory_only']['outcomes'][i]['passed'] for i in range(12)))
    interaction={expected_ids[i]:int(data['full']['outcomes'][i]['passed'])
                 -int(data['backend_only']['outcomes'][i]['passed'])
                 -int(data['memory_only']['outcomes'][i]['passed'])
                 +int(data['base']['outcomes'][i]['passed']) for i in range(12)}
    summary=json.loads((root/'qualification_summary.json').read_text())
    fail_if(summary.get('counts')!=counts or summary.get('qualified') is not qualified
            or summary.get('interactions')!=interaction or summary.get('case_count')!=12,
            'reported summary mismatch')
    return {'qualified':qualified,'counts':counts,'interactions':interaction,
            'manifest_entries':len(manifest),'source_blobs':len(source)}

if __name__=='__main__':
    import sys
    print(json.dumps(verify(sys.argv[1]),sort_keys=True,indent=2))
