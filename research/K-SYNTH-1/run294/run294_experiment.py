#!/usr/bin/env python3
"""Run prospectively frozen adversarial paired-compiler experiment (trusted fixtures only)."""
import copy, hashlib, json, pathlib, random, shutil, tempfile, traceback
from run294_transaction_compiler import Rejected, compile_to_isolated_stage, encode_views, sha, canonicalize

HERE=pathlib.Path(__file__).resolve().parent
FREEZE=json.loads((HERE/'RUN294_PROSPECTIVE_FREEZE.json').read_text())
assert sha((HERE/'run294_transaction_compiler.py').read_bytes()) == FREEZE['compiler_sha256']

def edit(path,source,start,end,replacement):
    b=source.encode('utf-8')
    return {'path':path,'start_byte':start,'end_byte':end,'expected_file_sha256':sha(b),
            'expected_span_sha256':sha(b[start:end]),'replacement_utf8':replacement}

def inputs_for_case(case,kind,root):
    a=FREEZE['fixtures']['a.py']; b=FREEZE['fixtures']['pkg/b.py']
    x=edit('a.py',a,0,5,'x = 3')
    y=edit('pkg/b.py',b,0,5,'y = 4')
    edits=[x,y] if case=='valid_two_file' else [x]
    if case=='stale_file':edits[0]['expected_file_sha256']='0'*64
    elif case=='bad_span':edits[0]['expected_span_sha256']='0'*64
    elif case=='overlap':edits=[edit('a.py',a,0,3,'x ='),edit('a.py',a,2,5,' 3')]
    elif case=='traversal':edits[0]['path']='../a.py'
    elif case=='symlink_target':
        (root/'a.py').unlink();(root/'a.py').symlink_to('pkg/b.py')
    elif case=='invalid_syntax':edits[0]['replacement_utf8']='x ='
    elif case=='split_utf8':
        offset=a.encode('utf-8').index('é'.encode('utf-8'))
        edits=[edit('a.py',a,offset,offset+1,'x')]
    elif case=='out_of_bounds':edits[0]['end_byte']=100
    elif case=='absolute_path':edits[0]['path']='/tmp/a.py'
    elif case=='unsupported_suffix':edits[0]['path']='a.txt'
    elif case=='ambiguous_insertions':edits=[edit('a.py',a,0,0,'# hi\n'),edit('a.py',a,0,0,'# there\n')]
    elif case=='boolean_offset':edits[0]['start_byte']=True
    elif case=='edit_count':edits=[copy.deepcopy(x) for _ in range(65)]
    elif case=='valid_nonoverlap':
        off=a.encode('utf-8').index('café'.encode('utf-8'))
        edits=[x,edit('a.py',a,off,off+len('café'.encode('utf-8')),'tea')]
    elif case=='valid_unicode':
        off=a.encode('utf-8').index('café'.encode('utf-8'))
        edits=[edit('a.py',a,off,off+len('café'.encode('utf-8')),'thé')]
    elif case=='missing_file':edits[0]['path']='missing.py'
    elif case=='root_symlink':pass
    ir,py=encode_views(edits)
    raw=ir if kind=='SEMANTIC_IR' else py
    if case in ('bad_representation','bad_assumptions','extra_key','empty_edits'):
        d=json.loads(raw)
        if case=='bad_representation':d['representation']='UNSUPPORTED'
        if case=='bad_assumptions':d['assumptions']['runtime_binding']='VERIFIED'
        if case=='extra_key':d['extra']=1
        if case=='empty_edits':d['edits']=[]
        raw=json.dumps(d,ensure_ascii=False)
    elif case=='duplicate_json_key':raw=raw[:-1]+',"representation":"SEMANTIC_IR"}'
    elif case=='invalid_json':raw='{"edits":'
    return raw

def make_root(parent):
    root=parent/'root';root.mkdir()
    for path,source in FREEZE['fixtures'].items():
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source,encoding='utf-8')
    return root

def run_one(case,kind):
    with tempfile.TemporaryDirectory(prefix='ksynth1-run294-') as tmp:
        parent=pathlib.Path(tmp);root=make_root(parent)
        raw=inputs_for_case(case,kind,root)
        if case=='root_symlink':
            alias=parent/'root_alias';alias.symlink_to(root,target_is_directory=True)
            target=alias
        else:target=root
        before={p:sha((root/p).read_bytes()) for p in FREEZE['fixtures'] if (root/p).is_file()}
        try:
            result=compile_to_isolated_stage(target,raw,parent/'stages')
            actual='ACCEPT'
            staged={p:sha((pathlib.Path(result['stage'])/p).read_bytes()) for p in FREEZE['fixtures']}
            if result['canonical_sha256'] != sha(json.dumps(canonicalize(raw),sort_keys=True,separators=(',',':')).encode()):
                raise AssertionError('canonical SHA differs')
            shutil.rmtree(result['stage'])
        except Rejected as e:
            actual=e.code;result=None;staged=None
        after={p:sha((root/p).read_bytes()) for p in FREEZE['fixtures'] if (root/p).is_file()}
        return {'case':case,'representation':kind,'expected':FREEZE['scenarios'][case],
                'observed':actual,'match':actual==FREEZE['scenarios'][case],
                'input_unchanged':before==after,'raw_sha256':sha(raw.encode()),
                'canonical_sha256':result['canonical_sha256'] if result else None,
                'staged_file_sha256':staged}

def fuzz_valid():
    rng=random.Random(FREEZE['random_seed']);rows=[]
    for i in range(FREEZE['random_valid_parity_trials']):
        with tempfile.TemporaryDirectory(prefix='ksynth1-run294-fuzz-') as tmp:
            parent=pathlib.Path(tmp);root=make_root(parent)
            a=FREEZE['fixtures']['a.py']
            val=rng.randint(-999999,999999)
            edits=[edit('a.py',a,0,5,f'x = {val}')]
            if rng.randrange(2):
                b=FREEZE['fixtures']['pkg/b.py'];val2=rng.randint(-999999,999999)
                edits.append(edit('pkg/b.py',b,0,5,f'y = {val2}'))
            ir,py=encode_views(edits)
            r1=compile_to_isolated_stage(root,ir,parent/'stages')
            r2=compile_to_isolated_stage(root,py,parent/'stages')
            same=r1['canonical_sha256']==r2['canonical_sha256'] and r1['files']==r2['files']
            rows.append({'trial':i,'edits':len(edits),'ir_canonical':r1['canonical_sha256'],
                         'python_canonical':r2['canonical_sha256'],'same':same,
                         'ir_files':r1['files'],'python_files':r2['files']})
    return rows

def main():
    rows=[run_one(c,k) for c in FREEZE['scenarios'] for k in FREEZE['representations']]
    fuzz=fuzz_valid()
    (HERE/'RUN294_RAW_ADVERSARIAL.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
    (HERE/'RUN294_RAW_FUZZ_PARITY.json').write_text(json.dumps(fuzz,indent=2,sort_keys=True)+'\n')
    summary={'scenario_rows':len(rows),'scenario_matches':sum(r['match'] for r in rows),
             'input_unchanged':sum(r['input_unchanged'] for r in rows),
             'valid_fuzz_trials':len(fuzz),'valid_fuzz_parity':sum(r['same'] for r in fuzz),
             'failures':[r for r in rows if not r['match'] or not r['input_unchanged']],
             'freeze_sha256':sha((HERE/'RUN294_PROSPECTIVE_FREEZE.json').read_bytes()),
             'compiler_sha256':FREEZE['compiler_sha256']}
    (HERE/'RUN294_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
