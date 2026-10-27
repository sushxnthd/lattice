#!/usr/bin/env python3
"""Replay frozen Run279 oracle using byte-identical reachable upstream merge.

The original PR-head ref is unavailable from a fresh encode/httpcore clone.
The merged direct-child commit is reachable and has identical production blobs.
Scientific criteria and oracle source remain unchanged.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, pathlib, subprocess

BASE = '5974b03c7df89d3ee4e23779900d5349d550753c'
ORIGINAL_REF = '7fb20526175e2300185ce2b472a97acca95b2525'
MERGE_REF = '10a658221deb38a4c5b16db55ab554b0bf731707'
ORIGINAL_BLOBS = {
    'httpcore/_sync/connection_pool.py':'4b26f9c63032be5c6c932b9d1339c43d4029368e',
    'httpcore/_async/connection_pool.py':'5ef74e6497f1fe44b7be520f8e1502e8786e91fd',
}

def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()

def verify_transport(base:pathlib.Path, ref:pathlib.Path)->dict:
    assert git(base,'rev-parse','HEAD')==BASE
    assert git(ref,'rev-parse','HEAD')==MERGE_REF
    assert git(ref,'rev-parse','HEAD^')==BASE
    actual={p:git(ref,'hash-object',p) for p in ORIGINAL_BLOBS}
    assert actual==ORIGINAL_BLOBS, (actual,ORIGINAL_BLOBS)
    return {'original_frozen_ref':ORIGINAL_REF,'reachable_merge_ref':MERGE_REF,
            'base_commit':BASE,'production_git_blobs':actual,
            'interpretation':'identical production source bytes, transport-only alias; scientific criteria unchanged'}

def replay(base:pathlib.Path, ref:pathlib.Path, out:pathlib.Path)->dict:
    provenance=verify_transport(base,ref)
    path=pathlib.Path(__file__).resolve().parent.parent/'run279'/'run279_httpcore_1000_qualify.py'
    if not path.exists():path=pathlib.Path(__file__).resolve().parent/'run279_httpcore_1000_qualify.py'
    spec=importlib.util.spec_from_file_location('frozen_run279_qualify',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    assert module.BASE==BASE and module.REF==ORIGINAL_REF
    assert tuple(module.FILES)==tuple(ORIGINAL_BLOBS)
    original_ref=module.REF
    try:
        module.REF=MERGE_REF
        result=module.qualify(base,ref,out)
    finally:
        module.REF=original_ref
    out.mkdir(parents=True,exist_ok=True)
    prov_path=out/'transport_alias_provenance.json'
    prov_path.write_text(json.dumps(provenance,sort_keys=True,indent=2)+'\n')
    return {'qualified':result['qualified'],'counts':result['counts'],
            'original_ref':ORIGINAL_REF,'transport_ref':MERGE_REF,
            'original_oracle_sha256':result['oracle_sha256'],
            'transport_provenance_sha256':hashlib.sha256(prov_path.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--base',type=pathlib.Path,required=True)
    p.add_argument('--ref',type=pathlib.Path,required=True)
    p.add_argument('--out',type=pathlib.Path,required=True)
    a=p.parse_args()
    print(json.dumps(replay(a.base,a.ref,a.out),sort_keys=True))
