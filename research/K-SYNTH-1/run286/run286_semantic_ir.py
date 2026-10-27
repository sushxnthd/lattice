#!/usr/bin/env python3
"""K-SYNTH-1 Run286: gold-blind, bounded semantic/dataflow extraction.

Scans *one supplied Python source* without reference/patch access.  This is an
abstract fact extractor, not a general proof of Python soundness.  It treats
calls, attribute resolution, comprehensions, and mutation as UNKNOWN unless
an external trusted scope certificate explicitly attests them.  Both views
are losslessly derived from the same canonical AST observations.
"""
from __future__ import annotations
import ast, dataclasses, hashlib, json

SCHEMA='lattice-ksynth1-run286-count-ir-v1'
REQUIRED=('finite_stable_iterable','pure_exact_bool_predicate','no_concurrent_mutation',
          'trusted_runtime_binding','integer_threshold')


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()


def _call_name(node):
    return ast.unparse(node.func) if isinstance(node,ast.Call) else None


def _shape(node):
    """A deliberately small, explicit family, no dynamic assumptions."""
    if not isinstance(node,ast.Call) or len(node.args)!=1 or node.keywords:
        return None
    op=_call_name(node)
    if op not in ('len','sum'):return None
    arg=node.args[0]
    if isinstance(arg,(ast.ListComp,ast.GeneratorExp)) and len(arg.generators)==1:
        g=arg.generators[0]
        if g.is_async or not isinstance(g.target,ast.Name):return None
        if op=='len' and not isinstance(arg,ast.ListComp):return None
        if op=='sum' and not isinstance(arg,(ast.ListComp,ast.GeneratorExp)):return None
        if g.ifs:
            if op!='len' or len(g.ifs)!=1 or not isinstance(arg.elt,ast.Name) or arg.elt.id!=g.target.id:return None
            pred=g.ifs[0];kind='COUNT_TRUE_FILTER'
        else:
            if not isinstance(arg.elt,ast.Call) or not isinstance(arg.elt.func,ast.Attribute):return None
            pred=arg.elt
            kind='COUNT_ALL_EVAL_PRED' if op=='len' else 'SUM_PRED_VALUES'
        if not isinstance(pred,ast.Call) or not isinstance(pred.func,ast.Attribute):return None
        if pred.args or pred.keywords or not isinstance(pred.func.value,ast.Name) or pred.func.value.id!=g.target.id:return None
        return {'kind':kind,'iterable_ast':ast.dump(g.iter,include_attributes=False),
                'iterable_source':ast.unparse(g.iter),'binder':g.target.id,
                'predicate_attribute':pred.func.attr,'expression_source':ast.unparse(node),
                'source_span':[node.lineno,node.col_offset,node.end_lineno,node.end_col_offset]}
    return None


def extract(source):
    tree=ast.parse(source)
    rows=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call):
            shape=_shape(n)
            if shape:rows.append(shape)
    rows.sort(key=lambda x:tuple(x['source_span']))
    return {'schema':SCHEMA,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'facts':rows,'facts_sha256':digest(rows),'gold_blind':True,
            'runtime_semantics':'UNKNOWN_UNLESS_SCOPE_ATTESTED'}


def render_ir(facts):
    return {'representation':'SEMANTIC_COUNT_IR','facts_sha256':facts['facts_sha256'],
            'facts':[{**f,'op':f['kind'],'runtime':'UNKNOWN'} for f in facts['facts']]}


def render_python(facts):
    # Exact ordinary Python expression and AST, with identical data fields.
    # 'kind' is included in both so no information advantage is smuggled in.
    return {'representation':'ORDINARY_PYTHON_AST','facts_sha256':facts['facts_sha256'],
            'facts':[{**f,'python_ast':ast.dump(ast.parse(f['expression_source'],mode='eval'),include_attributes=False),
                       'runtime':'UNKNOWN'} for f in facts['facts']]}


def recover_facts(view):
    """Strict common projection: proves information-equivalence of captured facts."""
    return [{k:f[k] for k in ('kind','iterable_ast','iterable_source','binder',
             'predicate_attribute','expression_source','source_span')} for f in view['facts']]


def certificate(a,b,attested=()):
    if not set(REQUIRED).issubset(attested):return {'status':'UNKNOWN','reason':'scope_not_attested'}
    if a['iterable_ast']!=b['iterable_ast'] or a['predicate_attribute']!=b['predicate_attribute']:
        return {'status':'UNKNOWN','reason':'nonidentical_binding_or_predicate'}
    if a['kind']=='COUNT_ALL_EVAL_PRED' and b['kind'] in ('SUM_PRED_VALUES','COUNT_TRUE_FILTER'):
        return {'status':'PROVED_CONDITIONAL','relation':'all_count_ge_true_count',
                'disagreement_condition':'true_count <= threshold < total_count'}
    return {'status':'UNKNOWN','reason':'unsupported_relation'}


if __name__=='__main__':
    import argparse,pathlib
    p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path)
    a=p.parse_args();facts=extract(a.source.read_text())
    result={'facts':facts,'ir':render_ir(facts),'python':render_python(facts)}
    assert recover_facts(result['ir'])==recover_facts(result['python'])==facts['facts']
    output=canonical(result)+'\n'
    if a.output:a.output.write_text(output)
    else:print(output)
