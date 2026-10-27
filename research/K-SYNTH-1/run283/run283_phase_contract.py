#!/usr/bin/env python3
"""Run283 POSTHOC temporal phase contract for HTTPcore PR1000.

This model was constructed AFTER a prospectively frozen 8/32 holdout failure.
It is an explanatory bounded state machine, NOT a blind prediction or a
sound model of arbitrary Python/HTTPcore execution.
"""
from __future__ import annotations
import json


def transition(limit: int, active_requests: int, reference: bool) -> dict:
    """One initial idle; cleanup before each distinct-origin active creation."""
    assert type(limit) is int and limit >= 1
    assert type(active_requests) is int and active_requests >= 0
    assert type(reference) is bool
    idle, active, events = 1, 0, []
    for request in range(1, active_requests + 1):
        before = idle + active
        close = bool(idle) and (idle > limit if reference else before > limit)
        if close:
            idle = 0
        events.append({'request': request, 'precreation_total': before, 'close': close})
        active += 1
    return {'idle': idle, 'active': active, 'events': events}


def closed_form(limit: int, active_requests: int, reference: bool) -> int:
    """Under the same assumptions, retained idle iff reference OR q <= limit."""
    assert type(limit) is int and limit >= 1
    assert type(active_requests) is int and active_requests >= 0
    assert type(reference) is bool
    return int(reference or active_requests <= limit)


def verify() -> dict:
    checks = 0
    for limit in range(1, 51):
        for q in range(101):
            for reference in (False, True):
                actual = transition(limit, q, reference)['idle']
                assert actual == closed_form(limit, q, reference)
                checks += 1
    return {'posthoc_boundary_checks': checks, 'mismatches': 0,
            'negative_original_holdout_disagreements': 8,
            'scope': 'one initial idle, distinct origins, cleanup before creation, no expiry/reuse, positive limit',
            'epistemic_status': 'POSTHOC_EXPLANATION_NOT_PROSPECTIVE_SUCCESS'}


if __name__ == '__main__':
    print(json.dumps(verify(), sort_keys=True))
