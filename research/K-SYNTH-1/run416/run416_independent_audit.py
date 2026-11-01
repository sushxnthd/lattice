#!/usr/bin/env python3
"""Read-only audit: independent byte-frame reconstruction and functional replay."""
from __future__ import annotations
import ast,hashlib,json,subprocess,sys
from pathlib import Path
import run402_dual_edit as base
from run416_experiment import fixture
ROOT=Path(__file__).resolve().parent

def main():
    lines=(ROOT/'run416_raw.jsonl').read_text().splitlines()
    checks=0
    for i,line in enumerate(lines):
        r=json.loads(line)
        assert r['case']==i;checks+=1
        files,auth,sem,ordinary,params=fixture(i)
        assert r['source_sha256']=={p:base.sha(s) for p,s in files.items()};checks+=1
        assert r['params']==params;checks+=1
        for rec in r['receipts']:
            p=rec['path'];fn=rec['function'];idx=rec['statement_index']
            original=files[p].encode()
            node=base._function(ast.parse(files[p]),fn).body[idx].value
            rows=original.splitlines(keepends=True)
            start=sum(len(t) for t in rows[:node.lineno-1])+node.col_offset
            end=sum(len(t) for t in rows[:node.end_lineno-1])+node.end_col_offset
            assert rec['start_byte']==start and rec['end_byte']==end;checks+=2
            assert rec['old_rhs_sha256']==hashlib.sha256(original[start:end]).hexdigest();checks+=1
            expression=next(a['expression'] for a in sem if a['path']==p and a['definition']==node_name(files[p],fn,idx))
            replacement=ast.unparse(ast.parse(expression,mode='eval').body).encode()
            assert rec['new_rhs_sha256']==hashlib.sha256(replacement).hexdigest();checks+=1
            patched=original[:start]+replacement+original[end:]
            assert r['output_sha256'][p]==hashlib.sha256(patched).hexdigest();checks+=1
            assert patched[:start]==original[:start] and patched[start+len(replacement):]==original[end:];checks+=2
            assert b'# Copyright 2026. Preserve this header.' in patched;checks+=1
        program='state=[0]\nclass X:\n def __add__(self,v):\n  state[0]+=v\n  return state[0]\n'
        alpha=files['alpha.py'].replace('x + '+str(params['a']),'x + '+str(params['a']+params['c']))
        # Reconstruct via byte span to avoid replacing comments or unrelated numbers.
        rec=next(q for q in r['receipts'] if q['path']=='alpha.py')
        orig=files['alpha.py'].encode();expr=f"x + {params['a']+params['c']}".encode()
        alpha=(orig[:rec['start_byte']]+expr+orig[rec['end_byte']:]).decode()
        program+=alpha+'\nprint(f(X()))\n'
        assert hashlib.sha256(program.encode()).hexdigest()==r['oracle_program_sha256'];checks+=1
        cp=subprocess.run([sys.executable,'-I','-S','-c',program],capture_output=True,text=True,timeout=4)
        assert (cp.stdout,cp.stderr,cp.returncode)==(r['oracle_stdout'],r['oracle_stderr'],r['oracle_exit']);checks+=3
        assert int(cp.stdout.strip())==params['a']+params['b']+params['c'];checks+=1
    assert len(lines)==512
    summary={'rows':len(lines),'independent_checks':checks,'replayed_subprocesses':len(lines),'disagreements':0,
             'raw_sha256':hashlib.sha256((ROOT/'run416_raw.jsonl').read_bytes()).hexdigest()}
    (ROOT/'run416_audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

def node_name(src,fn,idx):
    return base._function(ast.parse(src),fn).body[idx].targets[0].id

if __name__=='__main__':main()
