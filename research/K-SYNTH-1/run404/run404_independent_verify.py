#!/usr/bin/env python3
"""Independent bounded replay of original Run403 Qwen outputs. No exec/eval."""
import ast,hashlib,json,pathlib,sys,zipfile

VALUES=(-1000000,-11,-7,-3,-1,0,1,2,5,11,1000000)
def sha(b):return hashlib.sha256(b).hexdigest()
def val(node,env):
    if isinstance(node,ast.Constant) and type(node.value) is int:return node.value
    if isinstance(node,ast.Name):return env[node.id]
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -val(node.operand,env)
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.UAdd):return val(node.operand,env)
    if isinstance(node,ast.BinOp):
        x,y=val(node.left,env),val(node.right,env)
        if isinstance(node.op,ast.Add):return x+y
        if isinstance(node.op,ast.Sub):return x-y
        if isinstance(node.op,ast.Mult):return x*y
    raise AssertionError('UNSAFE')
def replay(row,actions):
    src=row['common']['source'];result={};out=[]
    for action in actions:
        path=action['path'];fn=ast.parse(src[path]).body[0]
        idx=next((j for j,s in enumerate(fn.body[:2]) if s.targets[0].id==action['definition']),None) if row['arm']=='SEMANTIC_DATAFLOW' else action['statement_index']
        if type(idx) is not int or idx not in (0,1):return 'REJECTED',{},[]
        e=ast.parse(action['expression'],mode='eval').body
        free={n.id for n in ast.walk(e) if isinstance(n,ast.Name)}
        available={fn.args.args[0].arg}|{s.targets[0].id for s in fn.body[:idx]}
        if not free<=available:return 'REJECTED',{},[]
        fn.body[idx].value=e;ast.fix_missing_locations(fn)
        result[path]=ast.unparse(ast.Module(body=[fn],type_ignores=[]))+'\n'
    for path,code in sorted(result.items()):
        fn=ast.parse(code).body[0]
        for x in VALUES:
            env={fn.args.args[0].arg:x}
            for stmt in fn.body[:2]:env[stmt.targets[0].id]=val(stmt.value,env)
            out.append((path,x,env[fn.body[2].value.id]))
    return 'COMPILED',{p:sha(s.encode()) for p,s in sorted(result.items())},out

def run(zpath,apath):
    audit=json.loads(pathlib.Path(apath).read_text())
    assert sha(pathlib.Path(zpath).read_bytes())==audit['archive_sha256']
    verified=0;executions=0
    with zipfile.ZipFile(zpath) as z:
        frozen={(r['task'],r['arm']):r for r in json.loads(z.read('frozen_prompts.json'))}
        for rec in audit['rows']:
            row=frozen[(rec['task'],rec['arm'])]
            actions=json.loads(z.read(f"completion_{rec['task']}_{rec['arm']}.txt"))
            status,hashes,values=replay(row,actions)
            assert status==rec['transaction']['status']
            if status=='COMPILED':
                assert hashes==rec['transaction']['source_sha256']
                traces={(t['path'],t['input']):t for t in rec['oracle']['traces']}
                for p,x,y in values:
                    assert traces[(p,x)]['actual']==y
                    assert traces[(p,x)]['pass']==(y==traces[(p,x)]['expected'])
                    executions+=1
            verified+=1
    return {'verified_model_records':verified,'independently_recomputed_function_outputs':executions,'disagreements':0,'independent_model_code_execution':False}
if __name__=='__main__':
    out=run(sys.argv[1],sys.argv[2]);pathlib.Path(sys.argv[3]).write_text(json.dumps(out,indent=2)+'\n');print(out)
