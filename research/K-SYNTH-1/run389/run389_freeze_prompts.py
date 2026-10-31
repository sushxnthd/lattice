#!/usr/bin/env python3
"""Reference-excluded, information-equivalent Rich issue pilot prompt freezer."""
import ast,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
SRC={'rich/_wrap.py':(ROOT/'rich/source/base_wrap.py').read_text(),
     'rich/cells.py':(ROOT/'rich/source/base_cells.py').read_text()}
ISSUE='''Rich #3176: Chunks of text go missing when writing Asian text (wrapping issue).
When printing Chinese or Japanese text without spaces, characters at line ends
can disappear instead of being wrapped. For example:
from rich.console import Console
console = Console(width=20)
console.print("アプリケーションは1670万色を使用でき")
Reported incorrect output: "アプリケーションは16\\n0万色を使用でき" (the 7 disappears).
Another example: Console(width=20).print("TextualはPythonの高速アプリケーション開発フレームワークです")
reported missing final characters "ムワークです".
The task is to repair this without losing or duplicating characters or breaking
existing behavior. You may change zero, one, or two authorized source files.
'''

def inventory():
    rows=[]
    for path,source in SRC.items():
        tree=ast.parse(source)
        for fn in (n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))):
            calls=sorted({n.func.id for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)})
            sig=ast.unparse(fn.args)
            rows.append({'path':path,'name':fn.name,'signature':sig,'calls':calls,
                         'scope':'MAY_CALL_SYNTAX_ONLY; runtime resolution UNKNOWN'})
    return rows

def representation(rows,arm):
    if arm=='IR':
        return '\n'.join('NODE|'+json.dumps({'path':r['path'],'name':r['name'],'signature':r['signature']},ensure_ascii=False,sort_keys=True)+'\n'+'\n'.join('MAY_CALL|'+json.dumps({'from':r['name'],'to':c,'path':r['path'],'resolution':'UNKNOWN'},ensure_ascii=False,sort_keys=True) for c in r['calls']) for r in rows)
    return '\n'.join('Function(path='+repr(r['path'])+', name='+repr(r['name'])+', signature='+repr(r['signature'])+', may_call_names='+repr(r['calls'])+', runtime_resolution=UNKNOWN)' for r in rows)

HEADER='''You are repairing a real historical Python bug. Return exactly one JSON object
with the schema {"edits":[{"path":"rich/_wrap.py or rich/cells.py","function":"existing top-level function name","replacement":"complete Python function definition"}]}. No Markdown fences or explanations.
You may submit 0, 1, or 2 edits; at most one top-level function per file.
Both source files are provided in full. All function names are selectable; do not assume
which function(s) need modification. Preserve unrelated behavior. No shell commands.
The auxiliary call-name inventory is syntactic only: it does not prove dynamic
call resolution, actual data dependence, or safety. Treat these as UNKNOWN.
'''

def main():
    rows=inventory()
    prompts={}
    for arm in ('IR','PYTHON_AST'):
        for order in ('source_first','facts_first'):
            facts='AUXILIARY FUNCTION AND CALL-NAME INVENTORY ('+arm+'):\n'+representation(rows,arm)
            source='\n'.join('=== '+p+' SHA256 '+hashlib.sha256(s.encode()).hexdigest()+' ===\n'+s for p,s in SRC.items())
            blocks=[source,facts] if order=='source_first' else [facts,source]
            prompt=HEADER+'\nISSUE:\n'+ISSUE+'\n\n'+blocks[0]+'\n\n'+blocks[1]
            key=arm+'_'+order
            prompts[key]={'messages':[{'role':'user','content':prompt}], 'temperature':0,'seed':3892026,
                          'max_tokens':2048,'model':'Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M'}
    manifest={'experiment':'run389 exploratory reference-known Rich #3176',
              'reference_patch_excluded':True,'investigator_blind':False,
              'primary_representation_comparison':False,
              'source_sha256':{p:hashlib.sha256(s.encode()).hexdigest() for p,s in SRC.items()},
              'model_sha256':'509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c',
              'rows':rows,'request_sha256':{},'prompt_sha256':{},'requests':prompts}
    for key,r in prompts.items():
        manifest['prompt_sha256'][key]=hashlib.sha256(r['messages'][0]['content'].encode()).hexdigest()
        manifest['request_sha256'][key]=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    p=ROOT/'run389_frozen_requests.json'
    p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print('FROZEN',len(rows),'functions',len(prompts),'requests',len(p.read_bytes()),'bytes')
    print('SOURCE',manifest['source_sha256'])
    print('PROMPTS',manifest['prompt_sha256'])

if __name__=='__main__':main()
