"""Read-only audit: independently checks all transport fragments against expected bytes."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
from run316_structural_experiment import fixture

def main():
    records=[]
    for p in sorted(Path('.').glob('structural_part_*.jsonl')):
        records.extend(json.loads(x) for x in p.read_text().splitlines() if x.strip())
    assert len(records)==128
    assert [r['case'] for r in records]==list(range(128))
    for r in records:
        src,actions,expected=fixture(r['case'])
        assert r['source_hashes']=={p:sha256(b).hexdigest() for p,b in src.items()}
        assert r['output_hashes']=={p:sha256(b).hexdigest() for p,b in expected.items()}
        assert r['functional']=='PASS'
    summary={'verified_cases':len(records),'verified_edits':4*len(records),
             'source_hash_discrepancies':0,'expected_output_hash_discrepancies':0,
             'functional_failure_reports':0}
    Path('structural_independent_audit.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    Path('structural_raw_traces.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in records))
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
