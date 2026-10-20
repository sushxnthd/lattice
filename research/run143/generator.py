"""Run143 synthetic-only generator: exact frozen Run136 primary task distribution."""
import ast
import random
from research.run134 import experiment as base

SEED=13620261020
PRIMARY_CLUSTERS=168

def make_pair(cluster):
    rng=random.Random(SEED+10709*cluster)
    domain=base.DOMAINS[cluster%len(base.DOMAINS)]
    names={k:f'{rng.choice(v)}_{cluster:03d}' for k,v in base.ROLES.items()}
    inputs=list(names.values());rng.shuffle(inputs)
    depth=2 if cluster%2==0 else 5
    chains=[[f'{domain}_{rng.getrandbits(48):012x}_{cluster:03d}' for _ in range(depth)] for _ in range(2)]
    decoys=[f'{domain}_aux_{rng.getrandbits(48):012x}_{cluster:03d}' for _ in range(5)]
    audit,route=f'{domain}_audit_{cluster:03d}',f'{domain}_route_{cluster:03d}'
    retention,alert=f'{domain}_retention_{cluster:03d}',f'{domain}_alert_{cluster:03d}'
    roots=decoys+[v for chain in chains for v in chain]+[audit,route,retention,alert]
    rng.shuffle(roots)
    owners={name:f'{domain}/{["auth","policy","risk","audit","route","ops"][i%6]}/module_{i:02d}.py' for i,name in enumerate(roots)}
    pos0,pos1=(names['cred_a'],names['cred_b']) if rng.randrange(2) else (names['cred_b'],names['cred_a'])
    positives=(pos0,pos1)
    initial=[(decoys[j],f'{names["region"]} or {names["quota"]}') for j in range(3)]
    for j in range(depth):
        order=[0,1];rng.shuffle(order)
        for c in order:
            if j==0:expr=f'{positives[c]} and not {positives[1-c]}'
            else:expr=f'{chains[c][j-1]} and {names["region"] if j%2 else names["quota"]}'
            initial.append((chains[c][j],expr))
    initial += [(audit,f'{chains[0][-1]} or {names["override"]}'),
                (route,f'{names["operator"]} and {names["region"]}'),
                (retention,f'{audit} and {names["archive"]}'),
                (alert,f'{chains[0][1]} or {chains[1][1]}'),
                (decoys[3],f'{names["archive"]} and {names["override"]}'),
                (decoys[4],f'{names["quota"]} or {names["override"]}')]
    common_after=[{chains[0][0]:f'{pos0} or {pos1}'},
                  {chains[1][0]:f'{pos0} or {pos1}'},
                  {decoys[1]:f'{names["operator"]} or {names["archive"]}'}]
    common=dict(cluster=f'C{cluster:03d}',domain=domain,inputs=inputs,roots=roots,owners=owners,
                authority=[route],protected=[n for n in roots if n!=route],
                audit=audit,route=route,operator=names['operator'],depth=depth,
                request=(f'Repair {route} so it requires BOTH operator signal {names["operator"]} '
                         f'and the credential signal appearing POSITIVELY in the historical '
                         f'first-stage check reached by following immutable captures from the '
                         f'CURRENT {audit}. Multiple opaque, interleaved historical chains exist. '
                         f'Preserve all protected outputs.'))
    twins=[]
    for twin in (0,1):
        history=[{audit:f'{chains[twin][-1]} or {names["override"]}'}]+common_after
        twins.append({**common,'id':f'C{cluster:03d}T{twin}','twin':twin,
                      'initial':initial,'history':history,
                      'target_expression':f'{positives[twin]} and {names["operator"]}',
                      'holdout':cluster>=PRIMARY_CLUSTERS})
    return twins

def graph_view(t):
    nodes,roots=base.state(t)
    keys=('cluster','domain','inputs','roots','owners','authority','protected','audit','route','operator','depth','request')
    facts={k:t[k] for k in keys}
    return ('You are editing a versioned multi-file Boolean policy program. '
            'Historical references capture immutable versions. Return ONLY a JSON '
            'object mapping authorized root names to Boolean expressions. '
            'Preserve protected outputs. The same compiler/verifier is used in both arms.\n'
            'FACTS: '+base.canon(facts)+'\nVIEW:\n'+
            base.canon({'kind':'versioned_dependency_state_graph','nodes':nodes,'roots':roots}))

def ordinary_python_view(t):
    nodes,roots=base.state(t)
    owner_to_root={v:k for k,v in t['owners'].items()}
    assert len(owner_to_root)==len(t['owners'])
    class Bind(ast.NodeTransformer):
        def __init__(self,bindings):self.bindings=bindings
        def visit_Name(self,n):
            if n.id in self.bindings:
                return ast.copy_location(ast.Name(id=f'_v{self.bindings[n.id]}',ctx=ast.Load()),n)
            return n
    lines=['# Ordinary Python: immutable version assignments; no explicit dependency edge table.',
           'def policy('+', '.join(t['inputs'])+'):']
    for n in nodes:
        bound=ast.unparse(Bind(n['bindings']).visit(ast.parse(n['expr'],mode='eval').body))
        lines.append(f'    _v{n["id"]} = {bound}  # root={owner_to_root[n["owner"]]}; file={n["owner"]}')
    lines.append('    return {'+', '.join(repr(k)+f': _v{v}' for k,v in roots.items())+'}')
    return graph_view(t).split('\nVIEW:\n',1)[0]+'\nVIEW:\n'+'\n'.join(lines)

def recover_from_ordinary_python(t,prompt):
    view=prompt.split('\nVIEW:\n',1)[1]
    lines=view.splitlines()
    tree=ast.parse(view)
    fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef))
    meta={}
    for line in lines:
        if ' # root=' not in line:continue
        code,comment=line.split('  # root=',1)
        i=int(code.strip().split('=',1)[0].strip()[2:])
        root,owner=comment.split('; file=',1)
        meta[i]=(root.strip(),owner.strip())
    nodes=[];roots={}
    class Unbind(ast.NodeTransformer):
        def visit_Name(self,n):
            if n.id.startswith('_v') and n.id[2:].isdigit():
                i=int(n.id[2:]);return ast.copy_location(ast.Name(id=meta[i][0],ctx=ast.Load()),n)
            return n
    for stmt in fun.body:
        if isinstance(stmt,ast.Assign):
            target=stmt.targets[0]
            if not isinstance(target,ast.Name) or not target.id.startswith('_v'):raise ValueError('bad assignment')
            i=int(target.id[2:]);refs={}
            for n in ast.walk(stmt.value):
                if isinstance(n,ast.Name) and n.id.startswith('_v'):
                    j=int(n.id[2:]);refs[meta[j][0]]=j
            expr=ast.unparse(Unbind().visit(ast.fix_missing_locations(stmt.value)))
            nodes.append({'id':i,'expr':expr,'bindings':refs,'owner':meta[i][1]})
        elif isinstance(stmt,ast.Return):
            roots={k.value:int(v.id[2:]) for k,v in zip(stmt.value.keys,stmt.value.values)}
    return nodes,roots
