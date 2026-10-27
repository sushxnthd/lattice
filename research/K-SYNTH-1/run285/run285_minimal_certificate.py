#!/usr/bin/env python3
"""Run285 minimal soundness-scoped multi-idle temporal certificate.

This is a finite abstract pool, NOT a proof of general Python/HTTPcore behavior.
Source syntax cannot establish purity, event order, concurrency or bindings.
"""
from dataclasses import dataclass

REQUIRED = frozenset({
    "stable_finite_pool", "pure_exact_boolean_idle", "no_expiry_or_reuse",
    "no_concurrent_mutation", "trusted_event_order",
    "trusted_source_identity", "unbounded_capacity",
})

@dataclass(frozen=True)
class State:
    idle: int
    keepalive: int
    new_requests: int
    reference: bool
    after_create: bool = False
    attested: frozenset = frozenset()

def transfer(s):
    if (type(s.idle) is not int or type(s.keepalive) is not int
        or type(s.new_requests) is not int or type(s.reference) is not bool
        or type(s.after_create) is not bool or s.idle < 0
        or s.keepalive < 0 or s.new_requests < 0
        or s.idle > s.keepalive or not REQUIRED.issubset(s.attested)):
        return ("UNKNOWN", None)
    if s.new_requests == 0 or s.reference:
        return ("PROVED_CONDITIONAL", s.idle)
    active_at_cleanup = s.new_requests - (not s.after_create)
    return ("PROVED_CONDITIONAL",
            min(s.idle, max(0, s.keepalive - active_at_cleanup)))

class Conn:
    def __init__(self, idle):
        self.idle = idle
    def is_idle(self):
        return self.idle

def independent_operational(s):
    # Actual CPython list mutation, not the transfer arithmetic recurrence.
    pool = [Conn(True) for _ in range(s.idle)]
    for _ in range(s.new_requests):
        if s.after_create:
            pool.append(Conn(False))
        for conn in list(pool):
            if conn.is_idle() and (
                sum(x.is_idle() for x in pool) if s.reference
                else len([x.is_idle() for x in pool])
            ) > s.keepalive:
                pool.remove(conn)
        if not s.after_create:
            pool.append(Conn(False))
    return sum(x.is_idle() for x in pool)

if __name__ == "__main__":
    n = 0
    for k in range(13):
        for m in range(k + 1):
            for q in range(17):
                for ref in (False, True):
                    for after in (False, True):
                        s = State(m, k, q, ref, after, REQUIRED)
                        status, count = transfer(s)
                        assert status == "PROVED_CONDITIONAL"
                        assert count == independent_operational(s)
                        n += 1
    assert transfer(State(2, 2, 2, False))[0] == "UNKNOWN"
    assert transfer(State(3, 2, 2, False, attested=REQUIRED))[0] == "UNKNOWN"
    assert len([v for v in [2, 2]]) == 2 and sum([2, 2]) == 4
    print("PASS:", n, "finite operational comparisons; zero mismatches")
