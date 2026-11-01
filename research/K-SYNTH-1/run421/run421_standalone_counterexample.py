#!/usr/bin/env python3
"""Standalone bounded Python effect counterexamples. No model-generated code."""
class Add:
    def __init__(self): self.n=0
    def __add__(self,k): self.n+=k; return self.n
class Property:
    def __init__(self): self.n=0
    @property
    def value(self): self.n+=7; return self.n
class Truth:
    def __init__(self): self.n=0
    def __bool__(self): self.n+=7; return True
class Iterate:
    def __init__(self): self.n=0
    def __iter__(self): self.n+=7; return iter((1,))

def operator(change):
    x=Add(); dead=x+(107 if change else 7); live=x+2; return live

def prop(change):
    x=Property(); dead=0 if change else x.value; return x.value

def truth(change):
    x=Truth()
    if True if change else x: dead=1
    return x.n

def iteration(change):
    x=Iterate()
    for y in ((1,) if change else x): dead=y
    return x.n

def global_effect(change):
    counter=[0]
    def bump(): counter[0]+=7; return 0
    dead=0 if change else bump()
    return counter[0]

def pure(change):
    dead=107 if change else 7
    return 7

for name,fn in [('operator',operator),('property',prop),('truthiness',truth),
                ('iteration',iteration),('global',global_effect),('pure',pure)]:
    before,after=fn(False),fn(True)
    assert (before!=after)==(name!='pure')
    print(f'{name}: {before} -> {after}')
