"""Portable fail-closed gate for Run354 raw evidence (no source execution)."""
import hashlib
import json
import sys
from pathlib import Path

TRACE_SHA = '11e1971103065509b66982d7aeb8a5e5199589db3d0a1d59aeeb412d772de953'
SUMMARY_SHA = 'caadbb52e251c752274a8d8ec065f622fd139ddf37d58b89f57d528f0f550396'
STATES = {'baseline': 0, 'api_only': 1, 'client_only': 2, 'staged': 3}
FUNCTIONS = {'head': 'httpx/_api.py', 'Client.head': 'httpx/_client.py', 'AsyncClient.head': 'httpx/_client.py'}
CASES = {'omitted', 'explicit_false', 'explicit_true', 'params_headers', 'auth_timeout', 'cookies'}


def verify(root):
    raw = (root / 'RUN354_FUNCTIONAL_TRACES.jsonl').read_bytes()
    summary_raw = (root / 'RUN354_SUMMARY.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == TRACE_SHA
    assert hashlib.sha256(summary_raw).hexdigest() == SUMMARY_SHA
    rows = [json.loads(line) for line in raw.splitlines()]
    summary = json.loads(summary_raw)
    assert len(rows) == 72 and summary['functional_observations'] == 72
    assert len({(r['state'], r['function'], r['case']) for r in rows}) == 72
    observed = {state: 0 for state in STATES}
    for r in rows:
        state, function, case = r['state'], r['function'], r['case']
        assert state in STATES and function in FUNCTIONS and case in CASES
        assert r['path'] == FUNCTIONS[function]
        edited = state == 'staged' or (state == 'api_only' and function == 'head') or (state == 'client_only' and function != 'head')
        expected = False if case == 'explicit_false' else True if case == 'explicit_true' else edited
        assert type(r['observed_allow_redirects']) is bool and r['observed_allow_redirects'] is expected
        assert r['passed'] is True and r['call']['kwargs']['allow_redirects'] is expected
        assert r['call']['method'] == 'HEAD'
        if case == 'omitted': observed[state] += int(expected)
        correct_sha = summary['stage_sha256' if edited else 'baseline_sha256'][r['path']]
        assert r['source_sha256'] == correct_sha
    assert observed == STATES == summary['factorial_omitted_success']
    assert summary['casewise_interaction'] == {k: 0 for k in FUNCTIONS}
    assert summary['control_observations'] == 60 and len(summary['documentation_flags']) == 5
    return {'verified': True, 'rows': len(rows), 'omitted_success': observed, 'casewise_interaction': summary['casewise_interaction']}


if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1] if len(sys.argv) > 1 else '.')), sort_keys=True))
