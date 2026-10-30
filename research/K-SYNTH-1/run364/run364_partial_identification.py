#!/usr/bin/env python3
"""Run364: sharp factorial interaction bounds with pre-oracle failures as UNKNOWN.

Reads the ORIGINAL Run363 evidence, not reconstructed summary scores. Pure stdlib.
Do not execute untrusted model code; only JSON evidence is parsed.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import zipfile
from pathlib import Path

ORIGINAL_SHA256 = 'deff0b0a86093b6822dbd46b93239a8e3e4a66979948a7d05110f64a75ae111a'
# Bit positions: 0 app, 1 ctx, 2 helpers.
THREE_WAY = {7: 1, 6: -1, 5: -1, 3: -1, 4: 1, 2: 1, 1: 1, 0: -1}
APP_HELPERS_CTX0 = {5: 1, 4: -1, 1: -1, 0: 1}
APP_HELPERS_CTX1 = {7: 1, 6: -1, 3: -1, 2: 1}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_original(path: Path) -> tuple[dict, dict]:
    raw = path.read_bytes()
    assert digest(raw) == ORIGINAL_SHA256, 'Original artifact SHA mismatch'
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        manifest = json.loads(z.read('sha256_manifest.json'))
        assert len(manifest) == 20, len(manifest)
        for name, sha in manifest.items():
            assert name in names and digest(z.read(name)) == sha, name
        matrix = json.loads(z.read('run363_matrix.json'))
        provenance = json.loads(z.read('source_provenance.json'))
    assert matrix['schema'] == 'run363.flask.matrix.v1'
    assert set(matrix['variants']) == {str(i) for i in range(8)}
    return matrix, provenance


def observed_cases(matrix: dict) -> dict[str, dict[int, bool | None]]:
    names = [r['case'] for r in matrix['variants']['0']['results']]
    assert len(names) == len(set(names)) == 12
    assert sum(n.startswith('T') for n in names) == 6
    assert sum(n.startswith('C') for n in names) == 6
    data = {n: {} for n in names}
    for i in range(8):
        rows = matrix['variants'][str(i)]['results']
        assert [r['case'] for r in rows] == names
        for r in rows:
            if r.get('error') == 'SUBPROCESS_FAILURE':
                assert i in (1, 2, 3)
                assert r.get('returncode') != 0
                data[r['case']][i] = None
            else:
                assert 'pass' in r
                data[r['case']][i] = bool(r['pass'])
    assert sum(v is not None for case in data.values() for v in case.values()) == 60
    assert sum(v is None for case in data.values() for v in case.values()) == 36
    return data


def interval(values: dict[int, bool | None], coefficients: dict[int, int]) -> dict:
    """Exact sharp bounds over all unrestricted binary potential outcomes in missing cells."""
    known = sum(coef * int(values[i]) for i, coef in coefficients.items() if values[i] is not None)
    missing = {i: coef for i, coef in coefficients.items() if values[i] is None}
    low = known + sum(min(0, c) for c in missing.values())
    high = known + sum(max(0, c) for c in missing.values())
    lo_witness = {i: (0 if c > 0 else 1) for i, c in missing.items()}
    hi_witness = {i: (1 if c > 0 else 0) for i, c in missing.items()}
    for witness, target in ((lo_witness, low), (hi_witness, high)):
        assert sum(c * (int(values[i]) if values[i] is not None else witness[i])
                   for i, c in coefficients.items()) == target
    return {'lower': low, 'upper': high, 'missing_masks': sorted(missing),
            'lower_witness': lo_witness, 'upper_witness': hi_witness,
            'sign_identified': low > 0 or high < 0 or (low == high == 0)}


def exhaustive_check() -> int:
    """Independent brute force checks for all 3-variable ternary evidence vectors.

    3^8 = 6561 combinations, each enumerating <=256 binary completions.
    """
    count = 0
    for states in itertools.product((None, False, True), repeat=8):
        values = dict(enumerate(states))
        for coefficients in (THREE_WAY, APP_HELPERS_CTX0, APP_HELPERS_CTX1):
            result = interval(values, coefficients)
            missing = [i for i in coefficients if values[i] is None]
            all_values = []
            for assignment in itertools.product((0, 1), repeat=len(missing)):
                fill = dict(zip(missing, assignment))
                all_values.append(sum(c * (int(values[i]) if values[i] is not None else fill[i])
                                      for i, c in coefficients.items()))
            assert result['lower'] == min(all_values)
            assert result['upper'] == max(all_values)
            count += 1
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('original_zip', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--exhaustive', action='store_true')
    args = ap.parse_args()
    matrix, provenance = read_original(args.original_zip)
    cases = observed_cases(matrix)
    out = {'schema': 'lattice.run364.partial_identification.v1',
           'original_zip_sha256': ORIGINAL_SHA256,
           'original_manifest_entries_verified': 20,
           'case_observations': 60, 'preoracle_unknowns': 36,
           'source_provenance': provenance,
           'cases': {}, 'aggregate': {}}
    for case, vals in cases.items():
        out['cases'][case] = {'observed': {str(k): v for k, v in vals.items()},
                              'three_way': interval(vals, THREE_WAY),
                              'app_helpers_ctx0': interval(vals, APP_HELPERS_CTX0),
                              'app_helpers_ctx1': interval(vals, APP_HELPERS_CTX1)}
    for category, names in (('targets', [n for n in cases if n.startswith('T')]),
                            ('controls', [n for n in cases if n.startswith('C')]),
                            ('all', list(cases))):
        out['aggregate'][category] = {}
        for key in ('three_way', 'app_helpers_ctx0', 'app_helpers_ctx1'):
            bounds = [out['cases'][n][key] for n in names]
            out['aggregate'][category][key] = {
                'lower_mean': sum(x['lower'] for x in bounds) / len(bounds),
                'upper_mean': sum(x['upper'] for x in bounds) / len(bounds),
                'all_case_sign_identified': all(x['sign_identified'] for x in bounds)}
    # Non-monotone deployability: baseline imports; changing app alone breaks import.
    out['deployability_counterexample'] = {'baseline_mask': 0, 'baseline_imports': True,
                                            'app_only_mask': 1, 'app_only_imports': False}
    if args.exhaustive:
        out['bruteforce_interval_checks'] = exhaustive_check()
    payload = json.dumps(out, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload)

if __name__ == '__main__':
    main()
