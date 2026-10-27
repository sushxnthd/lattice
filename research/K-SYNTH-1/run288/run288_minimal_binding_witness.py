#!/usr/bin/env python3
"""Run288 minimal reproducible source-only identifiability counterexample.
Trusted fixed source only; no model-generated code is executed.
"""
import ast, builtins, hashlib, json
SOURCE = '''def old(xs, k):
    return len([x.ok() for x in xs]) > k

def new(xs, k):
    return sum(x.ok() for x in xs) > k
'''
class Item:
    def ok(self): return True

def execute(patch=None):
    env={'__builtins__':dict(vars(builtins))}
    if patch:env.update(patch)
    exec(compile(SOURCE,'<trusted-fixed-source>','exec'),env)
    return env['old']([Item()],0),env['new']([Item()],0)

def main():
    pristine=execute()
    shadow_len=execute({'len':lambda seq:0})
    shadow_sum=execute({'sum':lambda seq:0})
    assert pristine==(True,True)
    assert shadow_len==(False,True)
    assert shadow_sum==(True,False)
    result={'source_sha256':hashlib.sha256(SOURCE.encode()).hexdigest(),
            'ast_sha256':hashlib.sha256(ast.dump(ast.parse(SOURCE),include_attributes=False).encode()).hexdigest(),
            'pristine':pristine,'shadow_len':shadow_len,'shadow_sum':shadow_sum,
            'conclusion':'IDENTICAL_SOURCE_AND_AST_DO_NOT_IDENTIFY_RUNTIME_BINDINGS'}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
