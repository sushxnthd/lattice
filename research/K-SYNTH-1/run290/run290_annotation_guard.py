#!/usr/bin/env python3
"""Soundness-scoped annotation temporal MAY analysis (no source execution).
Every call has runtime binding UNKNOWN. This is deliberately NOT a proof of
function identity, purity, temporal stability, or general Python semantics.
"""
import ast, hashlib, json

class Guard(ast.NodeVisitor):
    def __init__(self, source):
        self.source=source
        self.future=False
        self.context=['MODULE']
        self.records=[]
        self.unsupported=[]
        self.tree=ast.parse(source)
        self.future=any(isinstance(x,ast.ImportFrom) and x.module=='__future__' and
                        any(y.name=='annotations' for y in x.names)
                        for x in self.tree.body)
    def visit_in(self, node, kind):
        if node is None:return
        self.context.append(kind)
        try:self.visit(node)
        finally:self.context.pop()
    def visit_FunctionDef(self,node):
        for d in node.decorator_list:self.visit_in(d,'DEFINITION_DECORATOR')
        for d in node.args.defaults:self.visit_in(d,'DEFINITION_DEFAULT')
        for d in node.args.kw_defaults:self.visit_in(d,'DEFINITION_DEFAULT')
        for arg in node.args.posonlyargs+node.args.args+node.args.kwonlyargs+([node.args.vararg] if node.args.vararg else [])+([node.args.kwarg] if node.args.kwarg else []):
            self.visit_in(arg.annotation,'POSTPONED_ANNOTATION' if self.future else 'EAGER_ANNOTATION')
        self.visit_in(node.returns,'POSTPONED_ANNOTATION' if self.future else 'EAGER_ANNOTATION')
        for p in node.type_params:self.visit_in(p,'LAZY_TYPE_PARAMETER_SCOPE_UNKNOWN')
        for b in node.body:self.visit_in(b,'FUNCTION_BODY')
    visit_AsyncFunctionDef=visit_FunctionDef
    def visit_ClassDef(self,node):
        for d in node.decorator_list:self.visit_in(d,'DEFINITION_DECORATOR')
        for b in node.bases:self.visit_in(b,'DEFINITION_BASE')
        for k in node.keywords:self.visit_in(k.value,'DEFINITION_BASE')
        for p in node.type_params:self.visit_in(p,'LAZY_TYPE_PARAMETER_SCOPE_UNKNOWN')
        for b in node.body:self.visit_in(b,'CLASS_BODY')
    def visit_TypeAlias(self,node):
        for p in node.type_params:self.visit_in(p,'LAZY_TYPE_PARAMETER_SCOPE_UNKNOWN')
        self.visit_in(node.value,'LAZY_TYPE_ALIAS')
    def visit_TypeVar(self,node):
        self.visit_in(node.bound,'LAZY_TYPE_PARAMETER_BOUND')
        self.visit_in(node.default_value,'LAZY_TYPE_PARAMETER_DEFAULT')
    def visit_AnnAssign(self,node):
        self.visit_in(node.annotation,'POSTPONED_ANNOTATION' if self.future else 'EAGER_ANNOTATION')
        self.visit_in(node.value,'VALUE_EXPRESSION')
    def visit_Call(self,node):
        if isinstance(node.func,ast.Name) and node.func.id in ('len','sum'):
            self.records.append({'name':node.func.id,'line':node.lineno,'column':node.col_offset,
                                 'context':list(self.context),'runtime_identity':'UNKNOWN',
                                 'binding_stable':'UNKNOWN','temporal_guarantee':'UNKNOWN'})
        self.generic_visit(node)
    def result(self):
        self.visit(self.tree)
        self.records.sort(key=lambda r:(r['line'],r['column']))
        facts={'schema':'lattice-run290-annotation-may-v1',
               'source_sha256':hashlib.sha256(self.source.encode()).hexdigest(),
               'future_annotations':self.future,'records':self.records,
               'unconditional_soundness':'NOT_ESTABLISHED'}
        return facts

def extract(source):return Guard(source).result()

def views(facts):
    common={'source_sha256':facts['source_sha256'],'records':facts['records'],
            'future_annotations':facts['future_annotations']}
    return ({'representation':'SEMANTIC_TEMPORAL_IR','facts':common},
            {'representation':'ORDINARY_PYTHON_AST_ACTIONS','facts':common})

if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:raise SystemExit('usage: guard.py source.py')
    with open(sys.argv[1]) as f: s=f.read()
    print(json.dumps(extract(s),sort_keys=True,indent=2))
