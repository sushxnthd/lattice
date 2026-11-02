#!/usr/bin/env python3
"""Self-contained CPython 3.13+ final-return counterexample."""
import sys
assert sys.implementation.name == 'cpython' and sys.version_info >= (3,13)
original='def f(x):\n    a = x + 3\n    b = x * 5\n    return a - b\n'
swapped='def f(x):\n    b = x * 5\n    a = x + 3\n    return a - b\n'
def call(src, *, attack):
    ns={};exec(compile(src,'<trusted-minimal>','exec'),ns)
    f=ns['f'];n=0;events=[]
    def tracer(frame,event,arg):
        nonlocal n
        if frame.f_code is f.__code__ and event=='line':
            n+=1
            if n==2:frame.f_locals['x']=99
            events.append((frame.f_lineno,dict(frame.f_locals)))
        return tracer
    if attack:sys.settrace(tracer)
    try:r=f(7)
    finally:sys.settrace(None)
    return r,events
assert call(original,attack=False)[0]==call(swapped,attack=False)[0]==-25
left,lt=call(original,attack=True)
right,rt=call(swapped,attack=True)
assert (left,right)==(-485,67)
assert left-right==6*(7-99)
print({'closed_world_return':-25,'active_trace_original':left,
       'active_trace_swapped':right,'delta':left-right,
       'original_line_trace':lt,'swapped_line_trace':rt})
