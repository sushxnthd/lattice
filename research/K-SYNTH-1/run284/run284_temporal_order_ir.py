#!/usr/bin/env python3
"""Scoped temporal transfer certificate for HTTPcore PR1000.
Requires trusted attestations. Source AST alone cannot prove purity/event order.
"""
from dataclasses import dataclass
import json,pathlib
REQUIRED=frozenset({'stable_finite_collection','pure_exact_bool_idle','one_initial_idle','distinct_origin_no_reuse','no_expiry','stable_integer_limit','trusted_event_order','no_other_pool_limits'})
@dataclass(frozen=True)
class Certificate:
    limit:int
    requests:int
    reference:bool
    order:str
    attested:frozenset[str]

def predict(c:Certificate)->dict:
    if (type(c.limit) is not int or c.limit<1 or type(c.requests) is not int or c.requests<0 or
        type(c.reference) is not bool or c.order not in ('cleanup_before_create','cleanup_after_create') or
        not REQUIRED.issubset(c.attested)):
        return {'status':'UNKNOWN','idle':None}
    if c.reference or c.requests==0:return {'status':'PROVED','idle':1}
    retained=(c.requests<=c.limit) if c.order=='cleanup_before_create' else (c.requests<c.limit)
    return {'status':'PROVED','idle':int(retained)}

def independent_step_interpreter(k:int,q:int,reference:bool,order:str)->dict:
    idle,active=1,0
    events=[]
    for request in range(q):
        if order=='cleanup_after_create':active+=1
        observed_count=idle if reference else idle+active
        closes=bool(idle) and observed_count>k
        if closes:idle=0
        events.append({'request':request+1,'active_at_cleanup':active,'idle_at_cleanup':idle,'counted':observed_count,'closed':closes})
        if order=='cleanup_before_create':active+=1
    return {'idle':idle,'active':active,'events':events}

def verify():
    rows=[];order_disagreements=0
    for k in range(1,65):
        for q in range(65):
            for ref in (False,True):
                pair=[]
                for order in ('cleanup_before_create','cleanup_after_create'):
                    c=Certificate(k,q,ref,order,REQUIRED)
                    cert=predict(c)
                    actual=independent_step_interpreter(k,q,ref,order)
                    assert cert=={'status':'PROVED','idle':actual['idle']}
                    rows.append({'limit':k,'q':q,'reference':ref,'order':order,'predicted_idle':cert['idle'],'observed_idle':actual['idle'],'event_count':len(actual['events'])})
                    pair.append(actual['idle'])
                if pair[0]!=pair[1]:order_disagreements+=1
    bad=[Certificate(1,1,False,'unknown',REQUIRED),Certificate(1,1,False,'cleanup_before_create',frozenset()),
         Certificate(1,1,False,'cleanup_before_create',REQUIRED-{'pure_exact_bool_idle'}),
         Certificate(True,1,False,'cleanup_before_create',REQUIRED),
         Certificate(1,-1,False,'cleanup_before_create',REQUIRED),
         Certificate(1,1,False,'cleanup_before_create',REQUIRED-{'trusted_event_order'})]
    assert all(predict(c)=={'status':'UNKNOWN','idle':None} for c in bad)
    assert order_disagreements==64
    return {'schema':'lattice-run284-temporal-order-scoped-certificate-v1','comparisons':len(rows),'order_sensitive_witnesses':order_disagreements,'mismatches':0,'unknown_controls':len(bad),'scope':'Attested finite pure Boolean one-idle distinct-origin state machine; not general Python semantics or model advantage','rows':rows}
if __name__=='__main__':
    r=verify();p=pathlib.Path(__file__).parent
    (p/'run284_temporal_order_trace.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in r.pop('rows')))
    (p/'run284_temporal_order_summary.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
