"""Run284 independently frozen public API phase holdout, trusted upstream only."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent
frozen=json.loads((R/'FROZEN_RUN284_HOLDOUT.json').read_text())
sp=importlib.util.spec_from_file_location('r279',R.parent/'run279'/'run279_httpcore_1000_qualify.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(m.ORACLE.encode())==frozen['original_run279_oracle_sha256']
lines=['CASES=[']
for c in frozen['cases']:
    k,q=c['limit'],c['active_requests']
    fn=f'sync_target({k},{q})' if c['mode']=='sync' else f'asyncio.run(async_target({k},{q}))'
    lines.append(f"    ({c['id']!r},lambda:{fn}),")
lines+= [']','rows=[]','for name,fn in CASES:','    try:',"        observation=fn();error=None;passed=observation['pass']",'    except Exception as exc:',"        observation=None;error=type(exc).__name__+': '+str(exc);passed=False","    rows.append({'case':name,'observed':observation,'error':error,'pass':passed})","print(json.dumps({'rows':rows},sort_keys=True,separators=(',',':')))" ]
oracle=m.ORACLE.split('CASES=[',1)[0]+'\n'.join(lines)+'\n'
assert sha(oracle.encode())==frozen['oracle_sha256']
base=pathlib.Path(sys.argv[1]);ref=pathlib.Path(sys.argv[2]);out=pathlib.Path(sys.argv[3]).resolve();out.mkdir(parents=True,exist_ok=True)
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
assert git(base,'rev-parse','HEAD')==frozen['base_commit']
assert git(ref,'rev-parse','HEAD')==frozen['reference_alias']
assert git(ref,'rev-parse','HEAD^')==frozen['base_commit']
for f in m.FILES:
    assert sha((base/f).read_bytes())==frozen['source_sha256'][f]['base']
    assert sha((ref/f).read_bytes())==frozen['source_sha256'][f]['ref']
(out/'frozen_oracle.py').write_text(oracle)
(out/'FROZEN_RUN284_HOLDOUT.json').write_text(json.dumps(frozen,sort_keys=True,indent=2)+'\n')
records=[];disagreements=[];censored=[]
with tempfile.TemporaryDirectory() as d:
    for arm,flags in {'baseline':(0,0),'sync_only':(1,0),'async_only':(0,1),'full_reference':(1,1)}.items():
        root=pathlib.Path(d)/arm;shutil.copytree(base,root,ignore=shutil.ignore_patterns('.git'))
        for f,flag in zip(m.FILES,flags):
            if flag:shutil.copy2(ref/f,root/f)
            assert sha((root/f).read_bytes())==frozen['source_sha256'][f]['ref' if flag else 'base']
        proc=subprocess.run([sys.executable,'-I',str(out/'frozen_oracle.py'),str(root)],cwd=root,text=True,capture_output=True,timeout=240)
        try:rows=json.loads(proc.stdout)['rows'] if proc.returncode==0 else []
        except Exception:rows=[]
        records.append({'arm':arm,'returncode':proc.returncode,'stderr':proc.stderr,'rows':rows})
        if len(rows)!=18:censored.append({'arm':arm,'reason':'incomplete rows'});continue
        for c,row in zip(frozen['cases'],rows):
            if row['case']!=c['id'] or row['error'] is not None or row['observed'] is None:
                censored.append({'arm':arm,'case':c['id'],'reason':row['error']});continue
            actual={k:row['observed'][k] for k in ('before','during','pass')}
            exp=frozen['expected'][arm][c['id']]
            if actual!=exp:disagreements.append({'arm':arm,'case':c['id'],'expected':exp,'actual':actual})
result={'schema':'lattice-run284-phase-holdout-v1','records':records,'disagreements':disagreements,'censored':censored,'completed':72-len(censored),'scientific_pass':not disagreements and not censored,'frozen_oracle_sha256':sha(oracle.encode()),'prior_run283_holdout':'FAILED_8_OF_32_UNCHANGED'}
(out/'raw_results.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('completed','scientific_pass','disagreements','censored')},sort_keys=True))
