"""Executable finite AND-aggregation counterexample for mirrored source repairs.

Pure state model. For actual HTTPcore method executions see the Run366 archive.
No network, external package, or model-generated code is executed.
"""
from itertools import product

CASES = (
    ('B', 'I'), ('I', 'B'), ('B', 'B', 'I'), ('I', 'B', 'I'),
    ('I', 'I', 'B'), ('I', 'I', 'B', 'I'), ('I', 'B', 'I', 'B'),
    ('B', 'I', 'B', 'I'),
)
CAPS = (1, 1, 1, 2, 1, 2, 2, 1)

def pool_cleanup(states, cap, repaired):
    current = list(enumerate(states))
    for i, state in enumerate(states):
        if (i, state) not in current:
            continue
        if state in ('C', 'E'):
            current.remove((i, state))
        elif state == 'I':
            n = sum(s == 'I' for _, s in current) if repaired else len(current)
            if n > cap:
                current.remove((i, state))
    return tuple(i for i, _ in current)

def expected(states, cap):
    current = [(i, s) for i, s in enumerate(states) if s not in ('C', 'E')]
    idle = [i for i, s in current if s == 'I']
    removed = set(idle[:max(0, len(idle) - cap)])
    return tuple(i for i, _ in current if i not in removed)

def interaction(f):
    return int(f(1, 1)) - int(f(1, 0)) - int(f(0, 1)) + int(f(0, 0))

def main():
    per_case = []
    for backend in ('sync', 'async'):
        for states, cap in zip(CASES, CAPS):
            def success(sync_new, async_new):
                new = sync_new if backend == 'sync' else async_new
                return pool_cleanup(states, cap, new) == expected(states, cap)
            per_case.append(interaction(success))
            assert success(0, 0) is False
            assert success(1, 1) is True
    assert len(per_case) == 16 and set(per_case) == {0}
    def all_targets(sync_new, async_new):
        return all(pool_cleanup(states, cap, flag) == expected(states, cap)
                   for flag in (sync_new, async_new)
                   for states, cap in zip(CASES, CAPS))
    assert [all_targets(*v) for v in product((0, 1), repeat=2)] == [False, False, False, True]
    assert interaction(all_targets) == 1
    assert pool_cleanup(('B', 'I', 'C'), 1, False) != expected(('B', 'I', 'C'), 1)
    assert pool_cleanup(('B', 'I', 'C'), 1, True) == expected(('B', 'I', 'C'), 1)
    print('PASS: 16 zero per-target interactions; global AND interaction +1; baseline control failure')

if __name__ == '__main__':
    main()
