"""Independent read-only audit of original Run328 cloud evidence.

Does not import the experiment runner or HTTPX. Refuses incomplete records.
"""
import hashlib
import json
from pathlib import Path
import sys

BASE = '891d865044d27c229278f0fa20d84ba4007cb289'
REF = 'a226c60861f651b9874e31e66b3bb7f0db46c96d'
BLOBS = {
    'httpx/_api.py': ('a300f633e7ace1d0876a39735bf9af0c7ac64336', '4c608f0622dd58adc7d533fd16f64710c7a7f0a8'),
    'httpx/_client.py': ('e3b2f5b31913f210491a6c5fc2bff1c454833440', '53d52e5123c82e58bb154626619fbf45898bc6d5'),
}
IDS = ('target_api_head_one', 'target_client_head_one', 'heldout_client_head_two',
       'control_api_head_false', 'control_client_head_false',
       'control_api_get_default', 'control_client_get_default',
       'control_api_head_true', 'control_client_head_true')


def audit(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'SHA256_MANIFEST.json').read_text())
    for name, digest in manifest.items():
        assert name != 'SHA256_MANIFEST.json' and '/' not in name
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest, name
    summary = json.loads((directory / 'summary.json').read_text())
    assert summary['base'] == BASE and summary['reference'] == REF
    expected_oracle = '51cefba11ede1692bf543500f410fcf3406f95705f6b5876af886893574394f7'
    assert summary['oracle_sha256'] == expected_oracle
    counts = {}
    records = 0
    for bits in ('00', '10', '01', '11'):
        record = json.loads((directory / ('arm_' + bits + '.json')).read_text())
        assert record['bits'] == bits
        assert record['source_blobs'] == {p: hashes[int(bit)] for (p, hashes), bit in zip(BLOBS.items(), bits)}
        assert summary['arms'][bits]['source_blobs'] == record['source_blobs']
        assert summary['arms'][bits]['returncode'] == record['returncode']
        if record['returncode'] != 0 or 'oracle' not in record:
            counts[bits] = None
            continue
        oracle = json.loads(record['stdout'])
        assert oracle == record['oracle']
        assert oracle['schema'] == 'lattice-run328-oracle-v1' and oracle['total'] == 9
        assert tuple(c['id'] for c in oracle['cases']) == IDS
        assert sum(bool(c['passed']) for c in oracle['cases']) == oracle['passed']
        for case in oracle['cases']:
            if case['passed']:
                assert case['observed'] == case['expected'] and case['error'] is None
            else:
                assert case['observed'] != case['expected'] or case['error'] is not None
            records += 1
        counts[bits] = (sum(c['passed'] for c in oracle['cases'][:3]),
                        sum(c['passed'] for c in oracle['cases'][3:]))
    if any(v is None for v in counts.values()):
        expected_status = 'INDETERMINATE'
    else:
        base = counts['00'][0] <= 1 and counts['00'][1] >= 5
        full = counts['11'] == (3, 6)
        necessary = all(sum(counts[bits]) < 9 for bits in ('10', '01'))
        expected_status = 'QUALIFIED' if base and full and necessary else 'FAILED'
        assert summary['counts'] == {bits: {'target': t, 'control': c} for bits, (t, c) in counts.items()}
        assert summary['baseline_gate'] == base
        assert summary['reference_gate'] == full
        assert summary['joint_component_necessity'] == necessary
    assert summary['status'] == expected_status
    return {'independent_status': expected_status, 'counts': counts,
            'functional_records': records, 'sha_verified': len(manifest),
            'discrepancies': 0}


if __name__ == '__main__':
    print(json.dumps(audit(sys.argv[1]), sort_keys=True))
