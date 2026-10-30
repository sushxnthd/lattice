"""Portable bounded pool ownership counterexample, no dependencies.
NOT a historical httpcore execution. Run: python run370_minimal_bounded_witness.py
"""
from collections import deque


def edges(s, mode):
    req, conn, pool, harmed = s
    for i in range(2):
        t = list(req)
        if req[i] == 'absent':
            t[i] = 'queued'
            yield f'enqueue:{i}', (tuple(t), conn, pool, harmed)
        if req[i] == 'queued':
            t[i] = 'assigned'
            if not pool:
                yield f'assign_new:{i}', (tuple(t), 'connecting', True, harmed)
            elif conn in ('available', 'idle'):
                yield f'assign_shared:{i}', (tuple(t), 'available', True, harmed)
        if req[i] == 'assigned':
            t[i] = 'active'
            yield f'start_request:{i}', (tuple(t), 'available', pool, harmed)
        if req[i] in ('queued', 'assigned'):
            t[i] = 'timedout'
            other = any(t[j] in ('assigned', 'active') for j in range(2) if j != i)
            if req[i] == 'assigned' and pool and mode != 'historical':
                if mode == 'naive' or not other:
                    hurt = harmed or any(t[j] == 'active' for j in range(2) if j != i)
                    yield f'timeout_and_close:{i}', (tuple(t), 'closed', False, hurt)
                else:
                    yield f'timeout_keep_shared:{i}', (tuple(t), conn, pool, harmed)
            else:
                yield f'timeout_only_dequeue:{i}', (tuple(t), conn, pool, harmed)
        if req[i] == 'active':
            t[i] = 'done'
            other = any(t[j] in ('assigned', 'active') for j in range(2) if j != i)
            yield f'finish:{i}', (tuple(t), 'available' if other else 'idle', pool, harmed)


def scan(mode):
    start = (('absent', 'absent'), 'none', False, False)
    parents = {start: None}
    steps = {}
    todo = deque([start])
    count = 0
    orphan = unsafe = None
    while todo:
        s = todo.popleft()
        req, conn, pool, harmed = s
        if orphan is None and pool and conn == 'connecting' and 'queued' in req and not any(x in ('assigned', 'active') for x in req):
            orphan = s
        if unsafe is None and harmed:
            unsafe = s
        for action, nxt in edges(s, mode):
            count += 1
            if nxt not in parents:
                parents[nxt] = s
                steps[nxt] = action
                todo.append(nxt)
    def witness(target):
        if target is None:
            return None
        result = []
        while parents[target] is not None:
            result.append(steps[target])
            target = parents[target]
        return result[::-1]
    return len(parents), count, witness(orphan), witness(unsafe)


if __name__ == '__main__':
    for mode, expected in [('historical', (42, 70, True, False)),
                           ('naive', (46, 74, False, True)),
                           ('guarded', (42, 72, False, False))]:
        states, transitions, orphan, unsafe = scan(mode)
        assert (states, transitions, orphan is not None, unsafe is not None) == expected
        print(mode, 'states', states, 'transitions', transitions,
              'orphan_witness', orphan, 'shared_close_witness', unsafe)
