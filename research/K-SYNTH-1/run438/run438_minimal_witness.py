#!/usr/bin/env python3
"""Executable mixed-version witness: direct writes vs snapshot HEAD publication."""
import tempfile,pathlib,json
from run436_dual_view_compiler import make_sources,make_actions
from run437_lossless_transaction import transact_lossless
from run438_generation_store import init_store,commit,read_snapshot,InjectedFailure
old=make_sources(2,3,5)
ir,_=make_actions(old,11,17)
new,_=transact_lossless(old,ir,'ir')
x=7
expected_old=2*x+3+5
expected_new=2*x+11+17
hybrid=2*x+11+5
assert (expected_old,hybrid,expected_new)==(22,30,42)
with tempfile.TemporaryDirectory() as t:
 root=pathlib.Path(t)/'store';init_store(root,old)
 try:commit(root,ir,'ir',fail_at='after_generation_publish')
 except InjectedFailure:pass
 before=read_snapshot(root)[1]
 assert before==old
 commit(root,ir,'ir')
 after=read_snapshot(root)[1]
 assert after==new
print(json.dumps({'naive_in_place_provider_first':{'old':expected_old,'mixed':hybrid,'new':expected_new},
 'snapshot_publication':{'before_head_replace':expected_old,'after_head_replace':expected_new},
 'conclusion':'no mixed-version snapshot through one verified HEAD read; direct path readers remain outside scope'},sort_keys=True))
