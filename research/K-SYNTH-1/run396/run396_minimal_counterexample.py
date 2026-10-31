"""Executable minimal counterexamples to behavioral coupling proxies."""
from run395_gate import qualify

def old_gate(status):
    return qualify({'targets':['T1','T2'],'heldout':[],'controls':['C1'],
        'arms':{'baseline':status['00'],'full':status['11'],
                'shim_A_base_B_ref':status['01'],'shim_B_base_A_ref':status['10']},
        'shim_evidence':{k:{'verified':True,'neutrality_scope':'frozen_observed_api',
                            'sha256':'0'*64} for k in ('shim_A_base_B_ref','shim_B_base_A_ref')}})

def check():
    status={'00':{'T1':'FAIL','T2':'FAIL','C1':'PASS'},
            '10':{'T1':'PASS','T2':'FAIL','C1':'PASS'},
            '01':{'T1':'FAIL','T2':'PASS','C1':'PASS'},
            '11':{'T1':'PASS','T2':'PASS','C1':'PASS'}}
    assert old_gate(status)['decision']=='ELIGIBLE_BOUNDED'
    assert not any(status['10'][c]=='FAIL' and status['01'][c]=='FAIL' for c in ('T1','T2'))
    f={0:0,1:2};g={0:0,1:3}
    raw={(i,j):(f[i],g[j]) for i in (0,1) for j in (0,1)}
    primitive=tuple(raw[1,1][k]-raw[1,0][k]-raw[0,1][k]+raw[0,0][k] for k in (0,1))
    boolean={(i,j):int(raw[i,j]==raw[1,1]) for i in (0,1) for j in (0,1)}
    boolean_delta=boolean[1,1]-boolean[1,0]-boolean[0,1]+boolean[0,0]
    product={(i,j):raw[i,j][0]*raw[i,j][1] for i in (0,1) for j in (0,1)}
    product_delta=product[1,1]-product[1,0]-product[0,1]+product[0,0]
    assert primitive==(0,0) and boolean_delta==1 and product_delta==6
    return {'old_gate_split':'ELIGIBLE_BOUNDED','joint_target_count':0,
            'primitive_delta':primitive,'boolean_pass_delta':boolean_delta,
            'product_observer_delta':product_delta}

if __name__=='__main__':
    import json
    print(json.dumps(check(),sort_keys=True))
