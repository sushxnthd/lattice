#!/usr/bin/env python3
"""Frozen HTTPcore #1000 two-backend pool cleanup oracle.

Run with PYTHONPATH=/path/to/pinned/historical/checkout python this_file.py --label X.
No network, requests, sockets, model-generated code, or external I/O.
The oracle checks observable retained/closing identities, not implementation syntax.
"""
import argparse
import hashlib
import json
import os
import sys

# Prospectively frozen before running the historical 2x2 matrix.
# tuple: case ID, ordered connection states, keepalive cap, target/control
CASES = (
    ('busy1_idle1_cap1', ('B', 'I'), 1, 'target'),
    ('idle1_busy1_cap1', ('I', 'B'), 1, 'target'),
    ('busy2_idle1_cap1', ('B', 'B', 'I'), 1, 'target'),
    ('idle2_busy1_cap2', ('I', 'B', 'I'), 2, 'target'),
    ('idle2_busy1_cap1', ('I', 'I', 'B'), 1, 'target'),
    ('idle3_busy1_cap2', ('I', 'I', 'B', 'I'), 2, 'target'),
    ('idle2_busy2_cap2', ('I', 'B', 'I', 'B'), 2, 'target'),
    ('busy2_idle2_cap1', ('B', 'I', 'B', 'I'), 1, 'target'),
    ('idle1_cap1', ('I',), 1, 'control'),
    ('idle2_cap2', ('I', 'I'), 2, 'control'),
    ('idle3_cap1', ('I', 'I', 'I'), 1, 'control'),
    ('busy2_cap1', ('B', 'B'), 1, 'control'),
    ('idle1_cap0', ('I',), 0, 'control'),
    ('closed_idle_cap1', ('C', 'I'), 1, 'control'),
    ('expired_idle_cap1', ('E', 'I'), 1, 'control'),
    ('closed_expired_busy', ('C', 'E', 'B'), 1, 'control'),
    ('empty', (), 1, 'control'),
    ('busy_idle_closed', ('B', 'I', 'C'), 1, 'control'),
)

class FakeConnection:
    def __init__(self, label, state):
        self.label, self.state = label, state
    def is_closed(self):
        return self.state == 'C'
    def has_expired(self):
        return self.state == 'E'
    def is_idle(self):
        return self.state == 'I'

def independent_oracle(states, cap):
    # Independent state specification, not a translation of the loop predicate.
    retained = [(str(i), s) for i, s in enumerate(states) if s not in ('C', 'E')]
    closing = [str(i) for i, s in enumerate(states) if s == 'E']
    idle = [label for label, state in retained if state == 'I']
    surplus = max(0, len(idle) - cap)
    evicted = set(idle[:surplus])
    closing += idle[:surplus]
    return [label for label, _ in retained if label not in evicted], closing

def run():
    p = argparse.ArgumentParser()
    p.add_argument('--label', required=True)
    p.add_argument('--out', default='-')
    args = p.parse_args()
    from httpcore._sync.connection_pool import ConnectionPool
    from httpcore._async.connection_pool import AsyncConnectionPool
    import httpcore
    rows = []
    for backend, cls in (('sync', ConnectionPool), ('async', AsyncConnectionPool)):
        for name, states, cap, group in CASES:
            connections = [FakeConnection(str(i), state) for i, state in enumerate(states)]
            pool = object.__new__(cls)
            pool._connections = list(connections)
            pool._requests = []
            pool._max_keepalive_connections = cap
            pool._max_connections = 100
            expected_retained, expected_closing = independent_oracle(states, cap)
            error = None
            try:
                closing = pool._assign_requests_to_connections()
                actual_retained = [c.label for c in pool._connections]
                actual_closing = [c.label for c in closing]
                passed = (actual_retained == expected_retained and actual_closing == expected_closing)
            except Exception as exc:
                error = f'{type(exc).__name__}: {exc}'
                actual_retained = actual_closing = []
                passed = False
            rows.append(dict(backend=backend, case=name, group=group,
                             states=''.join(states), cap=cap, pass_=passed,
                             expected_retained=expected_retained,
                             expected_closing=expected_closing,
                             actual_retained=actual_retained,
                             actual_closing=actual_closing, error=error))
    result = dict(label=args.label, python=sys.version, httpcore_version=httpcore.__version__,
                  httpcore_location=httpcore.__file__,
                  oracle_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
                  rows=rows,
                  summary={b:{g:{'pass':sum(r['pass_'] for r in rows if r['backend']==b and r['group']==g),
                                    'total':sum(1 for r in rows if r['backend']==b and r['group']==g)}
                               for g in ('target','control')} for b in ('sync','async')})
    data = json.dumps(result, indent=2, sort_keys=True)
    if args.out == '-': print(data)
    else:
        with open(args.out, 'w') as f: f.write(data+'\n')
    return 0

if __name__ == '__main__':
    sys.exit(run())
