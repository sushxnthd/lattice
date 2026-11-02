#!/usr/bin/env python3
"""Finite evidence-scoped effect IR; never promotes observed calls to MUST."""
import hashlib,json,pathlib,itertools
ROOT=pathlib.Path(__file__).resolve().parent
V=('BASE','P','U','C','PU','PC','UC','PUC')
COMP=('P','U','C')
def digest(x):
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load():
 return {v:[json.loads(x) for x in (ROOT/'traces'/f'{v}.jsonl').read_text().splitlines()] for v in V}
def effect(rows,index,k):
 others=[x for x in COMP if x!=k]
 evidence=[]
 for flags in itertools.product((0,1),repeat=2):
  selected=[c for c,b in zip(others,flags) if b]
  low=''.join(x for x in COMP if x in selected) or 'BASE'
  high=''.join(x for x in COMP if x==k or x in selected)
  a,b=rows[low][index],rows[high][index]
  changed=(a['actual'],a['error'])!=(b['actual'],b['error'])
  evidence.append({'without':low,'with':high,'changed':changed,'outcome_sha256':[digest([a['actual'],a['error']]),digest([b['actual'],b['error']])]})
 return {'kind':'FINITE_COUNTERFACTUAL_EFFECT','component':k,'tested_contexts':evidence,'observed_effect':any(x['changed'] for x in evidence)}
def build_one(rows,i):
 base=rows['BASE'][i]
 edges=[{'kind':'OBSERVED_PROJECTED_STACK_ANCESTRY','from':a,'to':b,'observed_on_baseline':True} for a,b in base['edges'] if a!='EXTERNAL' and a.split(':')[0]!=b.split(':')[0]]
 return {'schema':'K-SYNTH-1/effect-ir/finite-v1','scope':'EXACT_URLLIB3_2_7_0_396_CASE_FACTORIAL',
         'case_index':i,'family':base['family'],'api':base['api'],
         'baseline_failure':not base['ok'],'baseline_outcome_sha256':digest([base['actual'],base['error']]),
         'projected_call_edges':edges,'counterfactual_components':[effect(rows,i,k) for k in COMP],
         'unknown':{'outside_frozen_cases':True,'unobserved_dynamic_dispatch':True,'general_python_must_edges':True},
         'must_edit_together_claims':[]}
def build(rows):
 assert all(len(rows[v])==396 for v in V)
 return [build_one(rows,i) for i in range(396)]
def validate(certs,rows):
 if len(certs)!=396:raise ValueError('CERTIFICATE_COUNT')
 for i,c in enumerate(certs):
  if c.get('schema')!='K-SYNTH-1/effect-ir/finite-v1':raise ValueError('UNKNOWN_SCHEMA')
  if c.get('must_edit_together_claims')!=[]:raise ValueError('UNSOUND_MUST_CLAIM')
  if c.get('unknown')!={'outside_frozen_cases':True,'unobserved_dynamic_dispatch':True,'general_python_must_edges':True}:raise ValueError('MISSING_UNKNOWN_SCOPE')
  if c!=build_one(rows,i):raise ValueError('PROVENANCE_OR_EFFECT_MISMATCH')
 return True
def main():
 rows=load();certs=build(rows);assert validate(certs,rows)
 p=ROOT/'RUN448_FINITE_EFFECT_IR.jsonl'
 p.write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in certs))
 print(json.dumps({'certificates':len(certs),'validated':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                   'observed_call_edges':sum(len(c['projected_call_edges']) for c in certs),
                   'nonzero_effects':sum(e['observed_effect'] for c in certs for e in c['counterfactual_components'])},sort_keys=True))
if __name__=='__main__':main()
