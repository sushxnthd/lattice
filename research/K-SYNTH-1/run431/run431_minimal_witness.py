#!/usr/bin/env python3
"""Finite historical HTTPX #1833 distinguishing witness. Original cloud ZIP only."""
import itertools, json, pathlib, zipfile
zpath=pathlib.Path(__file__).resolve().parent/'run430_historical_original.zip'
with zipfile.ZipFile(zpath) as z:
    rows=[json.loads(s) for s in z.read('run430_historical_raw.jsonl').decode().splitlines()]
    cases=json.loads(z.read('run430_historical_manifest.json'))['cases']
variants=['base','reference_parser_only','onefile_query_strip','full_ref']
vectors={}
for v in variants:
    records=[r['record'] for r in rows if r['variant']==v and r['record']['type']=='case']
    vectors[v]=tuple((r['actual'],r['error']) for r in records)
assert vectors['base']==vectors['reference_parser_only']
assert all(len(vectors[v])==8 for v in variants)
classes=[vectors['base'],vectors['onefile_query_strip'],vectors['full_ref']]
solutions=[]
for k in range(1,9):
    for indices in itertools.combinations(range(8),k):
        if len({tuple(v[i] for i in indices) for v in classes})==3:
            solutions.append(indices)
    if solutions:break
assert k==2 and solutions==[(0,6),(1,6)],solutions
print(json.dumps({'minimum_case_count':k,'all_minimum_witnesses':solutions,'witness_cases':[cases[i] for i in (0,6)]},indent=2))
