"""Run frozen Run328 four-arm public-API oracle in independent Python processes.

Only trusted research code runs on the host. Historical source executes in CI.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = '891d865044d27c229278f0fa20d84ba4007cb289'
REF = 'a226c60861f651b9874e31e66b3bb7f0db46c96d'
FILES = {
    'httpx/_api.py': ('a300f633e7ace1d0876a39735bf9af0c7ac64336', '4c608f0622dd58adc7d533fd16f64710c7a7f0a8'),
    'httpx/_client.py': ('e3b2f5b31913f210491a6c5fc2bff1c454833440', '53d52e5123c82e58bb154626619fbf45898bc6d5'),
}


def cmd(*args, cwd=None, timeout=60, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        raise RuntimeError('%s: %s' % (args, r.stderr))
    return r


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    checkout = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    oracle = Path(__file__).with_name('run328_oracle.py').resolve()
    out.mkdir(parents=True, exist_ok=True)
    assert cmd('git', 'rev-parse', BASE + '^{commit}', cwd=checkout).stdout.strip() == BASE
    assert cmd('git', 'rev-parse', REF + '^{commit}', cwd=checkout).stdout.strip() == REF
    for path, (base_sha, ref_sha) in FILES.items():
        for commit, sha in [(BASE, base_sha), (REF, ref_sha)]:
            actual = cmd('git', 'rev-parse', commit + ':' + path, cwd=checkout).stdout.strip()
            assert actual == sha, (path, commit, actual, sha)
    environment = dict(os.environ)
    environment.update(PYTHONPATH=str(checkout), PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1',
                       HTTP_PROXY='', HTTPS_PROXY='', ALL_PROXY='', NO_PROXY='*')
    cases = []
    for bits in ('00', '10', '01', '11'):
        cmd('git', 'checkout', '--force', BASE, cwd=checkout)
        source = {}
        for bit, (path, (base_sha, ref_sha)) in zip(bits, FILES.items()):
            if bit == '1':
                data = subprocess.check_output(['git', 'show', REF + ':' + path], cwd=checkout)
                (checkout / path).write_bytes(data)
            observed = cmd('git', 'hash-object', path, cwd=checkout).stdout.strip()
            expected = ref_sha if bit == '1' else base_sha
            assert observed == expected, (bits, path, observed, expected)
            source[path] = observed
        start = time.monotonic()
        try:
            r = subprocess.run([sys.executable, str(oracle)], cwd=checkout,
                               env=environment, capture_output=True, text=True, timeout=45)
            stdout, stderr, returncode = r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, returncode = (exc.stdout or b'').decode(errors='replace'), 'TIMEOUT', 124
        elapsed = round(time.monotonic() - start, 5)
        record = {'bits': bits, 'source_blobs': source, 'returncode': returncode,
                  'elapsed_seconds': elapsed, 'stdout': stdout, 'stderr': stderr}
        if returncode == 0:
            try:
                parsed = json.loads(stdout)
                assert parsed['schema'] == 'lattice-run328-oracle-v1'
                assert parsed['total'] == 9 and len(parsed['cases']) == 9
                record['oracle'] = parsed
            except Exception as exc:
                record['parse_error'] = repr(exc)
        (out / ('arm_' + bits + '.json')).write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
        cases.append(record)
    by_bits = {x['bits']: x for x in cases}
    all_valid = all('oracle' in x for x in cases)
    if all_valid:
        counts = {bits: {'target': sum(c['passed'] for c in rec['oracle']['cases'][:3]),
                         'control': sum(c['passed'] for c in rec['oracle']['cases'][3:])}
                  for bits, rec in by_bits.items()}
        baseline = counts['00']['target'] <= 1 and counts['00']['control'] >= 5
        full = counts['11'] == {'target': 3, 'control': 6}
        full_score = sum(counts['11'].values())
        necessity = all(sum(counts[bits].values()) < full_score for bits in ('10', '01'))
        status = 'QUALIFIED' if baseline and full and necessity else 'FAILED'
    else:
        counts, baseline, full, necessity, status = {}, None, None, None, 'INDETERMINATE'
    summary = {'schema': 'lattice-run328-result-v1', 'status': status,
               'counts': counts, 'baseline_gate': baseline, 'reference_gate': full,
               'joint_component_necessity': necessity,
               'oracle_sha256': sha256(oracle.read_bytes()), 'base': BASE, 'reference': REF,
               'arms': {x['bits']: {'returncode': x['returncode'], 'source_blobs': x['source_blobs']}
                        for x in cases}}
    (out / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True))
    manifest = {p.name: sha256(p.read_bytes()) for p in sorted(out.glob('*.json'))}
    (out / 'SHA256_MANIFEST.json').write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n')
    assert all(sha256((out / name).read_bytes()) == digest for name, digest in manifest.items())


if __name__ == '__main__':
    main()
