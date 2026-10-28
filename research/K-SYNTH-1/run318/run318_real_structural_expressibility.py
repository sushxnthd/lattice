"""Gold-only, read-only, exact production source structural-compiler expressibility.

Does NOT give reference-derived localization to a model. Does NOT execute upstream code.
Requires a separate Git clone of public urllib3 with the pinned commits present.
"""
from __future__ import annotations
import argparse, ast, hashlib, json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'run315'))
sys.path.insert(0,str(HERE.parent/'run316'))
from run315_multifile_compiler import node_digest
from run316_structural_compiler import Action,compile_structural

BASE='f4e4bc31f40f8c94c6a1f1685df28f97ff48c305'
HEAD='8b6b36f57e139755356074908abbcb0b07732d6d'
# Pinned independently observed Git blob IDs for the three production files.
SPECS={
'src/urllib3/connectionpool.py':{
 'base_blob':'7e6f54c82e3b8d4b5bfee7b48c8717fa2b650f1f',
 'head_blob':'427e5dfba2021b9f637daa442b5f6139045cf2cf',
 'edits':[('self.port and not port','self.port is not None and port is None'),('not self.port and port == port_by_scheme.get(scheme)','self.port is None and port == port_by_scheme.get(scheme)')]},
'src/urllib3/poolmanager.py':{
 'base_blob':'b7248d210dc8adea1b48dccab2c08860ad543328',
 'head_blob':'935712bf821ecb7fe200609012952e749d617d69',
 'edits':[('not port','port is None'),('not proxy.port','proxy.port is None')]},
'src/urllib3/util/url.py':{
 'base_blob':'6d0c66a30f5abea74db7bf0cd99da1c62b23a10d',
 'head_blob':'36529382f665f8e2127a815694fda3fbc2ff84bb',
 'edits':[('self.port','self.port is not None')]},
}

def git_show(repo,commit,path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],timeout=30)

def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',default='run318_raw_result.json');args=ap.parse_args()
    repo=Path(args.repo)
    sources={};references={};actions=[];details=[]
    for path,spec in SPECS.items():
        base=git_show(repo,BASE,path);head=git_show(repo,HEAD,path)
        assert blob_sha(base)==spec['base_blob'],('base blob mismatch',path)
        assert blob_sha(head)==spec['head_blob'],('head blob mismatch',path)
        text=base.decode('utf-8');tree=ast.parse(text,path)
        sources[path]=base;references[path]=head
        for old,new in spec['edits']:
            hits=[n.test for n in ast.walk(tree) if isinstance(n,ast.If) and ast.get_source_segment(text,n.test)==old]
            assert len(hits)==1,('nonunique If.test',path,old,len(hits))
            node=hits[0]
            a=Action(path,hashlib.sha256(base).hexdigest(),node_digest(node),type(node).__name__,node.lineno,node.col_offset,node.end_lineno,node.end_col_offset,'replace_expr',new)
            actions.append(a)
            details.append({'path':path,'old':old,'new':new,'node_type':type(node).__name__,'span':[node.lineno,node.col_offset,node.end_lineno,node.end_col_offset],'node_sha256':node_digest(node)})
    patched=compile_structural(sources,actions,allowed_paths=frozenset(SPECS))
    results=[]
    for path,spec in SPECS.items():
        assert patched[path]==references[path],('not byte-exact',path)
        assert blob_sha(patched[path])==spec['head_blob']
        results.append({'path':path,'base_sha256':hashlib.sha256(sources[path]).hexdigest(),'patched_sha256':hashlib.sha256(patched[path]).hexdigest(),'head_sha256':hashlib.sha256(references[path]).hexdigest(),'head_git_blob':blob_sha(patched[path]),'byte_exact':True})
    report={'repo':'urllib3/urllib3','pr':5071,'base':BASE,'head':HEAD,'production_files':len(results),'AST_replace_expr_actions':len(actions),'all_byte_exact':True,'actions':details,'files':results,'model_inference':False,'claim':'Reference-patch structural-compiler expressibility only, not model performance or semantic-IR superiority'}
    Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'production_files':len(results),'AST_replace_expr_actions':len(actions),'all_byte_exact':True,'result_sha256':hashlib.sha256(Path(args.output).read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
