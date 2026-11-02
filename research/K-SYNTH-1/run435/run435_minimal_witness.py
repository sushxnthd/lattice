#!/usr/bin/env python3
"""Minimal independent PEP669 counterexample (CPython >=3.13)."""
import sys

source='def f(x):\n    a = x + 3\n    b = x * 5\n    return a - b\n'
swapped='def f(x):\n    b = x * 5\n    a = x + 3\n    return a - b\n'

def observed(s):
    namespace={};exec(s,namespace)
    f=namespace['f'];events=[]
    m=sys.monitoring;m.use_tool_id(m.OPTIMIZER_ID,'minimal-pep669-witness')
    try:
        def cb(code,line):
            if code is not f.__code__:return
            events.append(line)
            if len(events)==2:sys._getframe(1).f_locals['x']=99
        m.register_callback(m.OPTIMIZER_ID,m.events.LINE,cb)
        m.set_events(m.OPTIMIZER_ID,m.events.LINE)
        assert sys.gettrace() is None
        value=f(7)
    finally:
        m.set_events(m.OPTIMIZER_ID,0)
        m.register_callback(m.OPTIMIZER_ID,m.events.LINE,None)
        m.free_tool_id(m.OPTIMIZER_ID)
    return value,events

if __name__=='__main__':
    a=observed(source);b=observed(swapped)
    assert a[0]==-485 and b[0]==67 and a[0]!=b[0]
    print('original:',a,'swapped:',b,'sys.gettrace():',sys.gettrace())
