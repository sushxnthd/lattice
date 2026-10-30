"""Constructive nonidentifiability proof using original Run361 case outcomes.
Original audit SHA256: d58135d7e8f48591151c2664c91dc6c1354b2dca42a4d434d50b5e112895468b
The adapter intervention is hypothetical, NOT an executed Jinja experiment.
"""
import json

# name, kind, baseline, compiler_only, runtime_only, full.
# Transcribed without alteration from the independently audited original Run361 matrix.
ROWS = [
 ('control_context_top_level','control',1,1,1,1),
 ('control_empty_loop','control',1,1,1,1),
 ('control_ordinary_block_call','control',1,0,1,1),
 ('control_ordinary_loop_call','control',1,0,1,1),
 ('control_plain_scope','control',1,1,1,1),
 ('control_scoped_block_no_loop','control',1,1,1,1),
 ('target_block_local_context','target',0,0,0,1),
 ('target_heldout_block_shadow','target',0,0,0,1),
 ('target_heldout_shadowed_assignment','target',0,0,0,1),
 ('target_loop_local_context','target',0,0,0,1),
 ('target_nested_scoped_context','target',1,0,1,1),
 ('target_scoped_loop','target',0,1,0,1),
]

def demonstrate(rows=ROWS):
    assert len(rows)==12
    observed=[]; counterfactual=[]
    for name,kind,b,c,r,f in rows:
        table={(0,0):b,(1,0):c,(0,1):r,(1,1):f}
        assert all(v in (0,1) for v in table.values())
        # Two SCMs agree under all observed H=0 interventions.
        # M_sem: adapter H is inert. M_abi: H rescues eligible compiler-only failures.
        for compiler in (0,1):
            for runtime in (0,1):
                y=table[(compiler,runtime)]
                observed.append({'case':name,'compiler':compiler,'runtime':runtime,
                                 'shim':0,'semantic_model':y,'abi_model':y})
        if c==0 and f==1:
            counterfactual.append({'case':name,'compiler':1,'runtime':0,
                                   'shim':1,'semantic_model':0,'abi_model':1,
                                   'status':'HYPOTHETICAL_NOT_MEASURED'})
    assert len(observed)==48 and len(counterfactual)==7
    return {'observational_agreements':len(observed),
            'counterfactual_disagreements':len(counterfactual),
            'observed':observed,'unmeasured_counterfactual':counterfactual,
            'theorem':'Finite 2x2 source-factorial outcomes at shim=0 do not identify the outcome under an unmeasured ABI-adapter intervention shim=1.',
            'caveat':'Constructive SCM counterexample only. Does not assert that any shim actually fixes Jinja.'}

if __name__=='__main__':
    print(json.dumps(demonstrate(),indent=2,sort_keys=True))
