import ast,itertools,json
cases=[]
for op in ('and','or'):
 for a,b in itertools.product((False,True),repeat=2):
  source=f'def f():\n    {a} {op} (x := {b})\n    return "x" in locals()\n'
  ns={};exec(compile(source,'<bounded-case>','exec'),ns)
  actual=ns['f']()
  expected=a if op=='and' else not a
  assert actual==expected
  cases.append({'op':op,'left':a,'right':b,'assigned':actual})
assert len(cases)==8 and sum(c['assigned'] for c in cases)==4
def classify(node):
 if not isinstance(node,ast.BoolOp) or len(node.values)!=2:return 'UNKNOWN'
 left,right=node.values
 if not isinstance(left,ast.Constant) or not isinstance(left.value,bool):return 'UNKNOWN'
 if not isinstance(right,ast.NamedExpr) or not isinstance(right.target,ast.Name):return 'UNKNOWN'
 executed=left.value if isinstance(node.op,ast.And) else not left.value if isinstance(node.op,ast.Or) else None
 return 'DEFINITE' if executed else 'NOT_ASSIGNED' if executed is False else 'UNKNOWN'
for c in cases:
 node=ast.parse(f"{c['left']} {c['op']} (x := {c['right']})",mode='eval').body
 assert (classify(node)=='DEFINITE')==c['assigned']
for op in ('and','or'):
 assert classify(ast.parse(f'flag {op} (x := True)',mode='eval').body)=='UNKNOWN'
print(json.dumps({'cases':cases,'unknown_cases':2,'assertions_passed':True},indent=2))
