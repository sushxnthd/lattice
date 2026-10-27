#!/usr/bin/env python3
"""Trusted CPython counterexample for the original Run293 alias-flow analyzer."""
import builtins
import run293_conservative_transfer as old
import run301_decorator_transfer as new
source='def dec(f): return len\n@dec\ndef g(x): return 0\n'
probe=source+'g([])\n'
original=[c for c in old.extract(probe)['calls'] if c['name']=='g'][0]['classification']
corrected=[c for c in new.extract(probe)['calls'] if c['name']=='g'][0]['classification']
ns={'__builtins__':builtins.__dict__}
exec(compile(source,'trusted-run301-witness','exec'),ns,ns)
assert ns['g'] is builtins.len
assert ns['g']([1,2,3])==3
assert original=='NOT_KNOWN_TARGET'
assert corrected=='UNKNOWN_DYNAMIC'
print({'runtime_identity':'builtins.len','runtime_result':3,
       'original':original,'corrected':corrected})
