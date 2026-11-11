"""Run651 exhaustive target/control necessity counterexample; synthetic only."""
import itertools, json
TARGET=("plain_changed","client_changed")
CONTROL=("plain_initial","client_initial")
CELLS=TARGET+CONTROL
ARMS=("base","parent","subclass")
def old(m):
    return all(m["full"].values()) and all(not all(m[a].values()) for a in ARMS)
def strict(m):
    return all(m["full"].values()) and all(any(not m[a][c] for c in TARGET) for a in ARMS)
def run():
    counts={"total":0,"old":0,"strict":0,"false_candidate":0,"control_only_failure":0}
    examples=[]
    for bits in itertools.product((False,True),repeat=12):
        m={a:dict(zip(CELLS,bits[i*4:(i+1)*4])) for i,a in enumerate(ARMS)}
        m["full"]={c:True for c in CELLS}
        o,s=old(m),strict(m)
        counts["total"]+=1;counts["old"]+=o;counts["strict"]+=s
        counts["false_candidate"]+=o and not s
        counts["control_only_failure"]+=o and all(all(m[a][c] for c in TARGET) for a in ARMS)
        if o and not s and len(examples)<2:examples.append(m)
    assert counts=={"total":4096,"old":3375,"strict":1728,"false_candidate":1647,"control_only_failure":27}
    print(json.dumps({"counts":counts,"examples":examples},indent=2))
if __name__=="__main__":run()
