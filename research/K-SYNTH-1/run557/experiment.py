"""Run557: atomic versus sequential repair application; CPython oracle."""
import ast, json, hashlib
BASE='def f():\n    return 1\n'
A='def f():\n    if True:\n'
B='        return 2\n'
variants={'base':BASE,'A_only':A,'B_only':B,'atomic_AB':A+B}
records=[]
for label,source in variants.items():
    try:
        tree=ast.parse(source); compile(tree,'<isolated>','exec')
        ns={};exec(compile(tree,'<isolated>','exec'),ns)
        outcome={'compile':'PASS','f':ns['f']() if 'f' in ns else None}
    except (SyntaxError,IndentationError) as e:
        outcome={'compile':'FAIL','error_type':type(e).__name__,'line':e.lineno}
    records.append({'arm':label,'sha256':hashlib.sha256(source.encode()).hexdigest(),**outcome})
assert [r['compile'] for r in records]==['PASS','FAIL','FAIL','PASS']
assert records[-1]['f']==2
result={'claim':'Per-edit compile gating is incomplete for valid atomic two-edit transactions','records':records,'assertions':2,'scope':'CPython grammar witness, not real repository repair or model inference'}
print(json.dumps(result,indent=2))
