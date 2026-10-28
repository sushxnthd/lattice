"""Read-only independent Run321 AST/functional auditor. Does not import guard."""
from __future__ import annotations
import ast, copy, hashlib, json, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()

def expected(source, a):
    tree=ast.parse(source)
    hits=[n for n in ast.walk(tree) if isinstance(n,ast.expr)
          and type(n).__name__==a['node_type']
          and (getattr(n,'lineno',None),getattr(n,'col_offset',None),getattr(n,'end_lineno',None),getattr(n,'end_col_offset',None))==
          (a['lineno'],a['col_offset'],a['end_lineno'],a['end_col_offset'])
          and sha(ast.dump(n,include_attributes=False).encode())==a['node_sha256']]
    assert len(hits)==1
    target=hits[0]
    replacement=ast.parse(a['replacement'],mode='eval').body
    class Sub(ast.NodeTransformer):
        def generic_visit(self,n):
            if n is target:return ast.copy_location(copy.deepcopy(replacement),n)
            return super().generic_visit(n)
    return ast.fix_missing_locations(Sub().visit(tree))

def main():
    rows=[json.loads(line) for line in (P/'run321_primary_traces.jsonl').read_text().splitlines()]
    errors=[]; replay=[]
    for r in rows:
        a=r['action']; original=r['source'].encode('utf-8')
        if sha(original)!=r['source_sha256'] or sha(original)!=a['source_sha256']:
            errors.append((r['case'],'source hash'))
        t=expected(r['source'],a)
        if ast.dump(t,include_attributes=False)!=r['expected_ast_dump']:
            errors.append((r['case'],'expected AST'))
        if r['original_status']=='accepted':
            p=r['original_patch'].encode('utf-8')
            if sha(p)!=r['original_patch_sha256']:errors.append((r['case'],'original patch hash'))
            congruent=ast.dump(ast.parse(r['original_patch']),include_attributes=False)==ast.dump(t,include_attributes=False)
            if congruent!=r['original_congruent']:errors.append((r['case'],'original congruence'))
        if r['guard_status']=='accepted':
            p=r['guard_patch'].encode('utf-8')
            if sha(p)!=r['guard_patch_sha256']:errors.append((r['case'],'guard patch hash'))
            if ast.dump(ast.parse(r['guard_patch']),include_attributes=False)!=ast.dump(t,include_attributes=False):
                errors.append((r['case'],'guard AST mismatch'))
            replay.append({'case':r['case'],'patched':r['guard_patch'],'expected':ast.unparse(t)})
        elif r['original_congruent'] is False and r['guard_status']!='rejected':
            errors.append((r['case'],'unsafe accepted'))
    runner='''import json,sys
rows=json.load(sys.stdin)
out=[]
for r in rows:
  p={};e={}
  exec(compile(r["patched"],"<trusted-patch>","exec"),{"__builtins__":{"max":max}},p)
  exec(compile(r["expected"],"<trusted-expected>","exec"),{"__builtins__":{"max":max}},e)
  pv=p["probe"]();ev=e["probe"]()
  out.append({"case":r["case"],"patched_value":pv,"expected_value":ev,"match":type(pv)==type(ev) and pv==ev})
json.dump(out,sys.stdout)
'''
    child=subprocess.run([sys.executable,'-I','-S','-c',runner],input=json.dumps(replay),text=True,capture_output=True,timeout=30)
    if child.returncode!=0:
        errors.append(('subprocess',child.stderr[:500]))
        functional=[]
    else:
        functional=json.loads(child.stdout)
        errors.extend((x['case'],'functional mismatch') for x in functional if not x['match'])
    (P/'run321_functional_traces.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in functional))
    summary={'cases_audited':len(rows),'accepted_functional_replays':len(functional),'functional_mismatches':sum(not x['match'] for x in functional),
             'audit_discrepancies':len(errors),'errors':errors[:20],
             'primary_traces_sha256':sha((P/'run321_primary_traces.jsonl').read_bytes()),
             'functional_traces_sha256':sha((P/'run321_functional_traces.jsonl').read_bytes())}
    (P/'run321_independent_audit.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))
    assert not errors
if __name__=='__main__':main()
