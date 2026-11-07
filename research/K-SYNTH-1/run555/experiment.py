import itertools,json
arms=('base','A','B','full')
def gate(x): return x==(0,0,0,1)
def simulate(order,reset):
    cache=0; out={}
    for arm in order:
        if reset: cache=0
        cache+=1
        out[arm]=int(cache==4)
    return tuple(out[k] for k in arms)
records=[{'order':p,'reset':r,'outcomes':simulate(p,r),'qualified':gate(simulate(p,r))} for p in itertools.permutations(arms) for r in (False,True)]
assert len(records)==48
assert sum(x['qualified'] for x in records if not x['reset'])==6
assert sum(x['qualified'] for x in records if x['reset'])==0
print(json.dumps(records,indent=2))
