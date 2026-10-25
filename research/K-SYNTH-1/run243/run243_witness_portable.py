#!/usr/bin/env python3
"""Independent, narrowly restricted token-stream witness for Run242 native output.
Usage: python run243_witness_portable.py path/to/python_native_source-raw-completion.txt
Does not import upstream repository code; this is not a complete functional oracle.
"""
import ast, json, re, sys, textwrap
from pathlib import Path

raw=Path(sys.argv[1]).read_text()
m=re.search(r'(?ms)^# LATTICE_EDIT_BEGIN 0f3bcf8c3c91b17686a3c1d6\n(.*?)^# LATTICE_EDIT_END',raw)
assert m, 'frozen parser selector missing'
tree=ast.parse(textwrap.dedent(m.group(1)))
allowed=(ast.Module,ast.FunctionDef,ast.arguments,ast.arg,ast.Assign,ast.Expr,
         ast.Call,ast.Attribute,ast.Name,ast.Constant,ast.If,ast.While,
         ast.Compare,ast.Subscript,ast.Load,ast.Store,ast.Eq,ast.Return)
assert len(tree.body)==1 and tree.body[0].name=='parse_if_statement'
assert all(isinstance(n,allowed) for n in ast.walk(tree))
for n in ast.walk(tree):
    if isinstance(n,ast.Call):
        if isinstance(n.func,ast.Name):
            assert n.func.id=='IfNode'
        else:
            assert isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name)
            assert (n.func.value.id,n.func.attr) in {
                ('self','eat'),('self','parse_expression'),('self','parse_block'),('if_body','append')}
ns={'__builtins__':{},'IfNode':lambda *x:x}
exec(compile(tree,'<audited parser>','exec'),ns)
class P:
    def __init__(self,t):
        self.t=t+['EOF'];self.i=0;self.current_token=(self.t[0],None)
    def eat(self,x):
        y=self.current_token[0]
        if x!=y:raise SyntaxError(f'Expected {x}, got {y}')
        self.i+=1;self.current_token=(self.t[self.i],None)
    def parse_expression(self):self.eat('IDENT');return 'x'
    def parse_block(self):self.eat('LBRACE');self.eat('RBRACE');return []
I=['IF','LPAREN','IDENT','RPAREN','LBRACE','RBRACE']
EI=['ELSE']+I
E=['ELSE','LBRACE','RBRACE']
cases={'if_only':I,'plain_else':I+E,'single_elif_no_else':I+EI,
       'chain_two_elif_else':I+EI+EI+E,'newline_else_if':I+EI}
result={}
for label,tokens in cases.items():
    try:ns['parse_if_statement'](P(tokens));result[label]='pass'
    except Exception as exc:result[label]=f'{type(exc).__name__}: {exc}'
assert result=={'if_only':'pass','plain_else':'pass',
 'single_elif_no_else':'SyntaxError: Expected ELSE, got EOF',
 'chain_two_elif_else':'SyntaxError: Expected LBRACE, got IF',
 'newline_else_if':'SyntaxError: Expected ELSE, got EOF'}
print(json.dumps(result,sort_keys=True,indent=2))
