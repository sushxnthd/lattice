#!/usr/bin/env python3
"""Deterministic byte-frame and isolated functional experiment, no model code."""
from __future__ import annotations
import ast,hashlib,json,random,subprocess,sys
from pathlib import Path
import run402_dual_edit as base
import run416_lossless_compiler as compiler

ROOT=Path(__file__).resolve().parent
SEED=41620261101

def fixture(i):
    r=random.Random(SEED+i)
    a,b,c=[r.randint(1,999) for _ in range(3)]
    crlf=i%4==0
    tab=i%4==1
    unicode_comment=['# résumé μ 🧪', '# 漢字 Δ', '# café', '# license: keep me'][i%4]
    indent='\t' if tab else '    '
    eol='\r\n' if crlf else '\n'
    def source(name,delta):
        lines=['#!/usr/bin/env python3','# coding: utf-8', '# Copyright 2026. Preserve this header.', unicode_comment,
               '# fmt: off',f'def {name}(x):',f'{indent}dead = (x + {a})  # noqa: F841',
               f'{indent}live = x + {b}',f'{indent}return live','# fmt: on','']
        return eol.join(lines)
    files={'alpha.py':source('f',a),'beta.py':source('g',b)}
    auth={'alpha.py':['f'],'beta.py':['g']}
    sem=[{'path':'alpha.py','function':'f','definition':'dead','expression':f'x + {a+c}'},
         {'path':'beta.py','function':'g','definition':'live','expression':f'x + {b+c}'}]
    ast_actions=[{'path':'alpha.py','function':'f','statement_index':0,'expression':f'x + {a+c}'},
                 {'path':'beta.py','function':'g','statement_index':1,'expression':f'x + {b+c}'}]
    return files,auth,sem,ast_actions,{'a':a,'b':b,'c':c,'crlf':crlf,'tab':tab}

def run():
    raw=ROOT/'run416_raw.jsonl'
    cases=512
    counts={'paired_compilations':0,'ast_equivalent':0,'byte_frame_verified':0,'functional_subprocesses':0,
            'legacy_full_module_reformat':0,'preserved_license_headers':0,'crlf_preserved':0,'tabs_preserved':0}
    with raw.open('w',encoding='utf-8') as fh:
        for i in range(cases):
            files,auth,sem,ordinary,params=fixture(i)
            hashes={p:base.sha(s) for p,s in files.items()}
            ir,receipt=compiler.compile_lossless(files,hashes,auth,sem,compiler.SEMANTIC)
            py,_=compiler.compile_lossless(files,hashes,auth,ordinary,compiler.ORDINARY)
            assert ir==py
            legacy=base.compile_transaction(files,hashes,auth,ordinary,'PYTHON_AST_ACTION')
            for p in files:
                assert ast.dump(ast.parse(ir[p]),include_attributes=False)==ast.dump(ast.parse(legacy[p]),include_attributes=False)
                assert ir[p].startswith(files[p].split('def ')[0])
                assert '# Copyright 2026. Preserve this header.' in ir[p]
                assert '# noqa: F841' in ir[p]
                assert '# fmt: off' in ir[p]
                assert ('\r\n' in ir[p])==params['crlf']
                assert ('\tdead' in ir[p])==params['tab']
                counts['ast_equivalent']+=1
                counts['preserved_license_headers']+=1
                counts['legacy_full_module_reformat']+=int(ir[p]!=legacy[p])
            counts['crlf_preserved']+=int(params['crlf'])
            counts['tabs_preserved']+=int(params['tab'])
            counts['paired_compilations']+=1
            # Independent byte-frame check using original AST spans, not compiler receipts.
            for p,fn,idx in [('alpha.py','f',0),('beta.py','g',1)]:
                old=files[p].encode(); new=ir[p].encode()
                node=base._function(ast.parse(files[p]),fn).body[idx].value
                lines=old.splitlines(keepends=True)
                s=sum(len(x) for x in lines[:node.lineno-1])+node.col_offset
                e=sum(len(x) for x in lines[:node.end_lineno-1])+node.end_col_offset
                assert old[:s]==new[:s]
                assert old[e:]==new[s+len(ast.unparse(ast.parse((sem[0] if p=='alpha.py' else sem[1])['expression'],mode='eval').body).encode()):]
                counts['byte_frame_verified']+=1
            # Actual CPython oracle with a side-effecting operator: dead edit matters.
            program='state=[0]\nclass X:\n def __add__(self,v):\n  state[0]+=v\n  return state[0]\n'+ir['alpha.py']+'\nprint(f(X()))\n'
            cp=subprocess.run([sys.executable,'-I','-S','-c',program],capture_output=True,text=True,timeout=4)
            assert cp.returncode==0,cp.stderr
            assert int(cp.stdout.strip())==params['a']+params['c']+params['b']
            counts['functional_subprocesses']+=1
            fh.write(json.dumps({'case':i,'source_sha256':hashes,'output_sha256':{p:base.sha(s) for p,s in ir.items()},
                                 'receipts':receipt,'params':params,'oracle_stdout':cp.stdout,
                                 'oracle_stderr':cp.stderr,'oracle_exit':cp.returncode,
                                 'oracle_program_sha256':hashlib.sha256(program.encode()).hexdigest()},sort_keys=True)+'\n')
    counts['raw_sha256']=hashlib.sha256(raw.read_bytes()).hexdigest()
    counts['seed']=SEED
    (ROOT/'run416_summary.json').write_text(json.dumps(counts,indent=2,sort_keys=True)+'\n')
    print(json.dumps(counts,indent=2))

if __name__=='__main__':run()
