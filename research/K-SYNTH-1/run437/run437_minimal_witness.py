#!/usr/bin/env python3
"""Minimal source-loss counterexample and byte-preserving replacement."""
import pathlib,sys
here=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(here))
sys.path.insert(0,str(here.parent/'run436'))
from run436_dual_view_compiler import make_sources,make_actions,transact
from run437_lossless_transaction import transact_lossless
s=make_sources(2,3,4)
s['provider.py']=b'#!/usr/bin/env python3\n# Copyright (c) 2026 Example\n'+s['provider.py']
s['consumer.py']=b'# SPDX-License-Identifier: MIT\n'+s['consumer.py']
a,b=make_actions(s,3,4)  # no-op in both files
old,_=transact(s,a,'ir')
new_ir,_=transact_lossless(s,a,'ir')
new_ast,_=transact_lossless(s,b,'ast')
assert old!=s and b'Copyright' not in old['provider.py']
assert new_ir==new_ast==s
print('COUNTEREXAMPLE: old no-op loses legal headers; lossless IR and AST retain exact bytes')
