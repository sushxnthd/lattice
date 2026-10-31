"""Fail-closed finite-oracle qualification gate; no claim of global semantic necessity.

Each arm is a mapping case_id -> PASS | FAIL | ABORT. A and B are distinct
production modules. A shim is *only* considered after separately documented
neutrality on the predeclared observed API. This gate cannot establish that
neutrality; it verifies that the evidence assertion is present and scoped.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Any

VALID = {'PASS', 'FAIL', 'ABORT'}


def qualify(d: dict[str, Any]) -> dict[str, Any]:
    target = tuple(d.get('targets', ()))
    heldout = tuple(d.get('heldout', ()))
    controls = tuple(d.get('controls', ()))
    ids = target + heldout + controls
    if not target or not controls or len(set(ids)) != len(ids):
        return {'decision': 'INVALID', 'reason': 'nonempty disjoint target and control sets required'}
    arms = d.get('arms', {})
    for key in ('baseline', 'full'):
        if key not in arms:
            return {'decision': 'INVALID', 'reason': 'missing original arm ' + key}
    for key, arm in arms.items():
        if set(arm) != set(ids) or any(v not in VALID for v in arm.values()):
            return {'decision': 'INVALID', 'reason': 'invalid case universe/status in ' + key}
    base, full = arms['baseline'], arms['full']
    if any(base[c] != 'PASS' for c in controls):
        return {'decision': 'REJECT', 'reason': 'baseline-contaminated controls',
                'failing_controls': [c for c in controls if base[c] != 'PASS']}
    if not any(base[c] == 'FAIL' for c in target):
        return {'decision': 'REJECT', 'reason': 'no baseline-negative target'}
    if any(full[c] != 'PASS' for c in ids):
        return {'decision': 'REJECT', 'reason': 'reference fails frozen cases'}
    for key in ('shim_A_base_B_ref', 'shim_B_base_A_ref'):
        if key not in arms:
            return {'decision': 'UNKNOWN', 'reason': 'missing shimmed ablation ' + key}
        claim = d.get('shim_evidence', {}).get(key, {})
        if (claim.get('neutrality_scope') != 'frozen_observed_api'
            or claim.get('verified') is not True
            or not isinstance(claim.get('sha256'), str)
            or len(claim['sha256']) != 64
            or any(ch not in '0123456789abcdef' for ch in claim['sha256'])):
            return {'decision': 'UNKNOWN', 'reason': 'shim neutrality unverified for ' + key}
        arm = arms[key]
        if any(arm[c] == 'ABORT' for c in ids):
            return {'decision': 'UNKNOWN', 'reason': 'nonfunctional shimmed ablation ' + key}
        if any(arm[c] != 'PASS' for c in controls):
            return {'decision': 'UNKNOWN', 'reason': 'shimmed control regression ' + key}
        if not any(arm[c] == 'FAIL' for c in target):
            return {'decision': 'REJECT', 'reason': 'module not behaviorally necessary on frozen targets',
                    'redundant_arm': key}
    return {'decision': 'ELIGIBLE_BOUNDED',
            'reason': 'two observed target necessities after documented scoped shims; not global proof',
            'target_count': len(target), 'control_count': len(controls),
            'heldout_count': len(heldout)}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_historical_run394(zip_path: str) -> dict[str, Any]:
    """Read original evidence only, preserve frozen labels and posthoc distinction."""
    import zipfile
    with zipfile.ZipFile(zip_path) as outer:
        original = outer.read('github-actions-corrected.zip')
        posthoc = outer.read('github-actions-posthoc-shim.zip')
    with zipfile.ZipFile(__import__('io').BytesIO(original)) as inner:
        masks = {n: json.loads(inner.read(f'mask_{n:02d}.json')) for n in range(16)}
        man = json.loads(inner.read('MANIFEST_SHA256.json'))
        entries = man.get('files', man)
        if isinstance(entries, dict):
            for name, sha in entries.items():
                if name == 'MANIFEST_SHA256.json':
                    continue
                if isinstance(sha, str) and len(sha) == 64:
                    assert digest(inner.read(name)) == sha, name
    with zipfile.ZipFile(__import__('io').BytesIO(posthoc)) as inner:
        post_manifest = json.loads(inner.read('MANIFEST_SHA256.json'))
        for name, sha in post_manifest.items():
            if isinstance(sha, str) and len(sha) == 64:
                assert digest(inner.read(name)) == sha, name
        shim = json.loads(inner.read('cases.json'))
    ids = [x['case'] for x in masks[0]['cases']]
    def outcome(n):
        return {x['case']: ('PASS' if x['pass'] else ('ABORT' if x['status'] != 'EXECUTED' or x.get('observed_test_count', 0) == 0 else 'FAIL'))
                for x in masks[n]['cases']}
    d = {
        'targets': [x for x in ids if x.startswith('T')],
        'heldout': [x for x in ids if x.startswith('H')],
        'controls': [x for x in ids if x.startswith('C')],
        'arms': {'baseline': outcome(0), 'full': outcome(15),
                 'A_only': outcome(1), 'B_only': outcome(2),
                 'shim_B_base_A_ref': outcome(1)},
        'original_zip_sha256': digest(original),
        'posthoc_zip_sha256': digest(posthoc),
        'posthoc_shim_passes': sum(x['pass'] for x in shim['cases']),
        'posthoc_shim_total': len(shim['cases']),
        'posthoc_not_frozen': True,
    }
    return {'evidence': d, 'gate': qualify(d)}


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        print(json.dumps(read_historical_run394(sys.argv[1]), indent=2, sort_keys=True))
    else:
        print(json.dumps(qualify(json.load(sys.stdin)), indent=2, sort_keys=True))
