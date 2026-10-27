#!/usr/bin/env python3
"""Trusted CPython 3.13 annotation evaluation-time counterexample.
No user/model-generated source. The same identifier `len` resolves at
annotation definition or first force depending on the construct.
"""
import json, sys
assert sys.version_info[:2] == (3, 13), 'CPython 3.13 required'

def eager():
    events=[]
    def len(xs): events.append('old'); return 11
    def f(x: len((1,2,3))): pass
    def len(xs): events.append('new'); return 22
    first=f.__annotations__['x']
    return {'values':[first,f.__annotations__['x']], 'events':events}

def alias():
    events=[]
    def len(xs): events.append('old'); return 11
    type A = len((1,2,3))
    def len(xs): events.append('new'); return 22
    first=A.__value__
    def len(xs): events.append('last'); return 33
    return {'values':[first,A.__value__], 'events':events}

def bound():
    events=[]
    def len(xs): events.append('old'); return 11
    def f[T: len((1,2,3))](x): pass
    def len(xs): events.append('new'); return 22
    first=f.__type_params__[0].__bound__
    def len(xs): events.append('last'); return 33
    return {'values':[first,f.__type_params__[0].__bound__], 'events':events}

result={'eager':eager(),'alias':alias(),'bound':bound()}
assert result['eager']=={'values':[11,11],'events':['old']}
assert result['alias']=={'values':[22,22],'events':['new']}
assert result['bound']=={'values':[22,22],'events':['new']}
print(json.dumps(result,sort_keys=True,indent=2))
