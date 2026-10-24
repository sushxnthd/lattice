#!/usr/bin/env python3
"""Run232 frozen matched lifecycle-context inference; byte-verified before model call."""
from __future__ import annotations
import argparse,hashlib,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'run230'))
import run230_cloud as old

ARMS=('semantic_ir_json','python_annotated')
UPSTREAM='c3def31a04df163769851733657d9b49b3700bca'
LIFECYCLE={
 'pybamm/batch_study.py':[
  {'symbol':'BatchStudy.__init__','line':88,'fact':'self.quick_plot = None'},
  {'symbol':'BatchStudy.solve','line':116,'fact':'self.sims = []'},
  {'symbol':'BatchStudy.solve','line':142,'fact':'sim = pybamm.Simulation(...)'},
  {'symbol':'BatchStudy.solve','line':157,'fact':'sol = sim.solve(...)'},
  {'symbol':'BatchStudy.solve','line':172,'fact':'self.sims.append(sim)'}],
 'pybamm/simulation.py':[
  {'symbol':'Simulation.__init__','line':137,'fact':'self._solution = None'},
  {'symbol':'Simulation.solve','line':584,'fact':'self._solution = solver.solve(...)'},
  {'symbol':'Simulation.solution','line':1117,'fact':'return self._solution'}]}

def parse_python(view):
 out={};lines=view.splitlines(keepends=True);i=0
 while i<len(lines):
  assert lines[i].startswith('# LATTICE_META ')
  row=json.loads(lines[i][len('# LATTICE_META '):]);i+=1
  src=[]
  while i<len(lines) and lines[i]!='# LATTICE_END\n':
   src.append(lines[i]);i+=1
  assert i<len(lines);i+=1
  row['method_source']=''.join(src);out[row['path']]=row
 return out

def prepare(base,out,prereg):
 out.mkdir(parents=True,exist_ok=True)
 f=json.loads(prereg.read_bytes())
 assert f['status']=='prospectively_frozen_before_new_inference'
 assert f['lifecycle_evidence_sha256']==old.sha(old.canonical(LIFECYCLE))
 assert f['schema_sha256']==old.sha(old.canonical(old.schema()))
 reqs={a:json.loads((base/(a+'-request.json')).read_bytes()) for a in ARMS}
 raw={}
 for a in ARMS:
  issue,view=reqs[a]['messages'][0]['content'].split('\nISSUE:\n',1)[1].split('\nSOURCE_FACTS:\n',1)
  facts=json.loads(view) if a==ARMS[0] else parse_python(view)
  raw[a]=(issue,facts)
 assert raw[ARMS[0]]==raw[ARMS[1]]
 issue,facts=raw[ARMS[0]]
 assert old.sha(old.canonical(facts))==f['base_fact_sha256']
 enriched={p:{**row,'lifecycle_evidence':{'upstream_commit':UPSTREAM,'path':p,'observations':LIFECYCLE[p]}} for p,row in facts.items()}
 assert old.sha(old.canonical(enriched))==f['enriched_fact_sha256']
 views={ARMS[0]:old.canonical(enriched).decode()}
 parts=[]
 for p in ('pybamm/batch_study.py','pybamm/simulation.py'):
  row=enriched[p]
  parts.append('# LATTICE_META '+old.canonical({k:v for k,v in row.items() if k!='method_source'}).decode()+'\n')
  parts.append(row['method_source'])
  if not row['method_source'].endswith('\n'):parts.append('\n')
  parts.append('# LATTICE_END\n')
 views[ARMS[1]]=''.join(parts)
 assert parse_python(views[ARMS[1]])==enriched
 for a in ARMS:
  req=reqs[a]
  req['messages'][0]['content']=old.PREFIX+issue+'\nSOURCE_FACTS:\n'+views[a]
  data=old.canonical(req)
  assert old.sha(data)==f['request_sha256'][a],(a,old.sha(data))
  assert old.sha(req['messages'][0]['content'].encode())==f['prompt_sha256'][a]
  (out/(a+'-request.json')).write_bytes(data)
 # old.infer expects this basename; contents remain the Run232 preregistration.
 (out/'run230-preregistration.json').write_bytes(prereg.read_bytes())
 (out/'run232-preregistration.json').write_bytes(prereg.read_bytes())
 print('RUN232 FROZEN REQUEST HASHES VERIFIED',f['request_sha256'],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--prepare',action='store_true');p.add_argument('--infer',action='store_true')
 p.add_argument('--base',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path,required=True)
 p.add_argument('--prereg',type=pathlib.Path)
 p.add_argument('--endpoint',default='http://127.0.0.1:8080/v1/chat/completions')
 a=p.parse_args()
 if a.prepare:prepare(a.base,a.out,a.prereg)
 if a.infer:old.infer(a.out,a.endpoint)
