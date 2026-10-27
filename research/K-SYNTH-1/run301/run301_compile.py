#!/usr/bin/env python3
"""Strict shared adapter + paired compiler audit; no untrusted code execution."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import run295_compiler_v2 as compiler
import run301_shared_adapter as adapter

def main(root,out,arm,stages):
    status={'arm':arm,'accepted':False}
    try:
        completion=(out/('completion_'+arm+'.txt')).read_text()
        ir,py=adapter.to_views(completion,root)
        a=compiler.compile_to_isolated_stage(root,ir,stages/(arm+'-ir'))
        b=compiler.compile_to_isolated_stage(root,py,stages/(arm+'-python'))
        assert a['canonical_sha256']==b['canonical_sha256']
        assert a['files']==b['files']
        selected=a if arm=='IR' else b
        status={'arm':arm,'accepted':True,'canonical_sha256':selected['canonical_sha256'],
                'files':selected['files'],'edits':selected['edits'],'stage':selected['stage'],
                'paired_compiler_parity':True}
    except Exception as e:
        status.update(error_type=type(e).__name__,error=str(e)[:1000])
    (out/('compile_'+arm+'.json')).write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
    print(json.dumps(status,sort_keys=True))

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3],Path(sys.argv[4]))
