import ast,hashlib,json,subprocess,sys,tempfile,pathlib,shutil

def sha(b): return hashlib.sha256(b).hexdigest()
def run(root):
 p=subprocess.run([sys.executable,'-B','main.py'],cwd=root,capture_output=True,text=True,timeout=5)
 return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr[-500:]}
def static_imports(source):
 tree=ast.parse(source)
 return sorted({n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)} | {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module})

def main():
 with tempfile.TemporaryDirectory() as td:
  root=pathlib.Path(td)/'live'; root.mkdir()
  (root/'main.py').write_text('import importlib\nm=importlib.import_module("helper")\nprint(m.read())\n')
  (root/'helper.py').write_text('from pathlib import Path\ndef read(): return Path("payload.txt").read_text().strip()\n')
  (root/'payload.txt').write_text('ORIGINAL\n')
  initial={p.name:sha(p.read_bytes()) for p in root.iterdir()}
  frozen=pathlib.Path(td)/'frozen';shutil.copytree(root,frozen)
  baseline=run(root)
  (root/'payload.txt').write_text('MUTATED\n')
  mutated=run(root)
  entryonly=pathlib.Path(td)/'entryonly';entryonly.mkdir();shutil.copy(root/'main.py',entryonly/'main.py')
  static=static_imports((root/'main.py').read_text())
  records={'baseline':baseline,'mutated':mutated,'entrypoint_only':run(entryonly),'full_snapshot':run(frozen),'initial_sha256':initial,'after_entry_sha256':sha((root/'main.py').read_bytes()),'static_imports':static,'dynamic_import_literal':'helper','data_dependency':'payload.txt'}
  assert baseline['stdout']=='ORIGINAL\n'
  assert mutated['stdout']=='MUTATED\n'
  assert records['after_entry_sha256']==initial['main.py']
  assert records['full_snapshot']['stdout']==baseline['stdout']
  assert records['entrypoint_only']['returncode']!=0
  assert 'helper' not in static
  print(json.dumps(records,sort_keys=True,indent=2))
if __name__=='__main__':main()
