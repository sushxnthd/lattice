"""Prospectively frozen synthetic functional test of Run316 structural editor."""
from __future__ import annotations
import ast
from dataclasses import replace
from hashlib import sha256
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from run315_multifile_compiler import PatchRejected,node_digest
from run316_structural_compiler import Action,compile_structural


def action(path,src,node,op,replacement=''):
    return Action(path,sha256(src).hexdigest(),node_digest(node),type(node).__name__,
                  node.lineno,node.col_offset,node.end_lineno,node.end_col_offset,op,replacement)


def choose(tree,pred):
    hits=[n for n in ast.walk(tree) if pred(n)]
    assert len(hits)==1
    return hits[0]


def fixture(i):
    src={
      'a.py':b'# caf\xc3\xa9\nimport math\n\ndef twice(x):\n    return x + 1\n',
      'b.py':b'from a import twice\n\ndef adjust(x):\n    return twice(x)\n',
      'c.py':f'def remaining():\n    obsolete = 7\n    return {123+i}\n'.encode(),
    }
    a=ast.parse(src['a.py']);b=ast.parse(src['b.py']);c=ast.parse(src['c.py'])
    actions=[
      action('a.py',src['a.py'],choose(a,lambda n:isinstance(n,ast.Import)),'insert_before','import statistics'),
      action('a.py',src['a.py'],choose(a,lambda n:isinstance(n,ast.BinOp)),'replace_expr','x * 2'),
      action('b.py',src['b.py'],choose(b,lambda n:isinstance(n,ast.Return)),'replace_stmt','return twice(x) + 5'),
      action('c.py',src['c.py'],choose(c,lambda n:isinstance(n,ast.Assign)),'delete_stmt'),
    ]
    expected={
      'a.py':src['a.py'].replace(b'import math',b'import statistics\nimport math').replace(b'x + 1',b'x * 2'),
      'b.py':src['b.py'].replace(b'return twice(x)',b'return twice(x) + 5'),
      'c.py':src['c.py'].replace(b'    obsolete = 7\n',b''),
    }
    return src,actions,expected


def oracle(out,i):
    with tempfile.TemporaryDirectory(prefix='lattice316_oracle_') as d:
        p=Path(d)
        for path,content in out.items():(p/path).write_bytes(content)
        cmd=[sys.executable,'-I','-c',
             'import sys;sys.path.insert(0,sys.argv[1]);import a,b,c;'
             'x=int(sys.argv[2]);assert a.twice(x)==2*x;'
             'assert b.adjust(x)==2*x+5;assert c.remaining()==123+x;'
             'print("PASS")',d,str(i)]
        cp=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
        assert cp.returncode==0,(cp.stdout,cp.stderr)
        assert cp.stdout.strip()=='PASS'


def main():
    counts={'byte_identical':0,'functional_replays':0,'edits_verified':0,'negative_rejections':0}
    traces=[]
    for i in range(128):
        src,actions,expected=fixture(i)
        out=compile_structural(src,actions,allowed_paths=frozenset(src))
        assert out==expected
        oracle(out,i)
        counts['byte_identical']+=1
        counts['functional_replays']+=1
        counts['edits_verified']+=len(actions)
        traces.append({'case':i,'source_hashes':{p:sha256(b).hexdigest() for p,b in src.items()},
                       'output_hashes':{p:sha256(b).hexdigest() for p,b in out.items()},
                       'functional':'PASS'})
    src,actions,_=fixture(0)
    bad=[
        ([replace(actions[0],source_sha256='0'*64)],frozenset(src)),
        ([replace(actions[0],path='../escape.py')],frozenset(src)),
        ([actions[0]],frozenset({'b.py','c.py'})),
        ([actions[0],actions[0]],frozenset(src)),
        ([replace(actions[1],replacement='(')],frozenset(src)),
        ([replace(actions[2],replacement='return (')],frozenset(src)),
        ([replace(actions[3],replacement='return 9')],frozenset(src)),
        ([replace(actions[0],node_sha256='0'*64)],frozenset(src)),
    ]
    for edits,allowed in bad:
        try:compile_structural(src,edits,allowed_paths=allowed)
        except PatchRejected:counts['negative_rejections']+=1
        else:raise AssertionError('negative control unexpectedly accepted')
    Path('structural_raw_traces.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in traces))
    Path('structural_result.json').write_text(json.dumps(counts,sort_keys=True,indent=2)+'\n')
    print(json.dumps(counts,sort_keys=True))

if __name__=='__main__':main()
