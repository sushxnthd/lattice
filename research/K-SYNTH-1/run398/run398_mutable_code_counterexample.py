#!/usr/bin/env python3
"""Executable Run398 counterexample: function identity does not freeze behavior."""
import json
def original(x): return 'ORIGINAL:'+str(x)
def replacement(x): return 'REPLACEMENT:'+str(x)
def call_captured(x, cb=original): return cb(x)
alias=original
before={'default':call_captured(7),'alias':alias(7),'same_identity':alias is call_captured.__defaults__[0]}
original.__code__=replacement.__code__
after={'default':call_captured(7),'alias':alias(7),'same_identity':alias is call_captured.__defaults__[0]}
assert before=={'default':'ORIGINAL:7','alias':'ORIGINAL:7','same_identity':True}
assert after=={'default':'REPLACEMENT:7','alias':'REPLACEMENT:7','same_identity':True}
print(json.dumps({'before':before,'after':after},indent=2))
