"""Run365 closed-world import-name gate. Scope: ordinary direct relative imports only.
NO_DIRECT_NAME_MISSING does NOT certify runtime importability. Unknown stays UNKNOWN.
"""
import ast
import itertools
import json

def gate(sources, closed_world=True):
    exports, edges, unknown = {}, [], []
    for module, source in sorted(sources.items()):
        try:
            tree = ast.parse(source)
        except SyntaxError:
            unknown.append(f"{module}:parse")
            continue
        names = set()
        dynamic = False
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(node.name)
                dynamic |= node.name == "__getattr__"
            elif isinstance(node, ast.Assign):
                names.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                edges.extend((module,node.module,a.name) for a in node.names if a.name != "*")
                dynamic |= any(a.name == "*" for a in node.names)
            elif isinstance(node, (ast.If,ast.Try,ast.For,ast.While,ast.With)):
                dynamic = True
            if any(isinstance(c,ast.Call) and isinstance(c.func,ast.Name)
                   and c.func.id in {"exec","eval","setattr","__import__"}
                   for c in ast.walk(node)):
                dynamic = True
        exports[module]=(names,dynamic)
    missing=[]
    for consumer,provider,name in edges:
        if provider not in exports:
            unknown.append(f"{consumer}->{provider}.{name}:external")
        elif exports[provider][1]:
            unknown.append(f"{consumer}->{provider}.{name}:dynamic")
        elif name not in exports[provider][0]:
            if closed_world:
                missing.append((consumer,provider,name))
            else:
                unknown.append(f"{consumer}->{provider}.{name}:open")
    status="DEFINITE_MISSING_STATIC_NAME" if missing else "UNKNOWN" if unknown else "NO_DIRECT_NAME_MISSING"
    return {"status":status,"missing":missing,"unknown":unknown}

def historical_witnesses():
    flask={}
    for mask in range(8):
        flask[mask]={"app":"from .helpers import _CollectErrors" if mask&1 else "BASE=1",
                     "ctx":"from .helpers import _CollectErrors" if mask&2 else "BASE=1",
                     "helpers":"class _CollectErrors: pass" if mask&4 else "BASE=1"}
    urllib={}
    for mask in range(4):
        urllib[mask]={"connectionpool":"class HTTPConnectionPool: pass\ndef _is_same_host(): pass" if mask&1 else "class HTTPConnectionPool: pass",
                      "poolmanager":"from .connectionpool import _is_same_host" if mask&2 else "from .connectionpool import HTTPConnectionPool"}
    return flask,urllib

if __name__=="__main__":
    flask,urllib=historical_witnesses()
    a={str(i):gate(src)["status"] for i,src in flask.items()}
    b={str(i):gate(src)["status"] for i,src in urllib.items()}
    assert {i for i,v in a.items() if v=="DEFINITE_MISSING_STATIC_NAME"}=={"1","2","3"}
    assert {i for i,v in b.items() if v=="DEFINITE_MISSING_STATIC_NAME"}=={"2"}
    print(json.dumps({"flask":a,"urllib3":b},indent=2,sort_keys=True))
