#!/usr/bin/env python3
"""Minimal CPython witness: equal final values, unequal intermediate traces."""
import sys

def before(x):
    left = x + 3
    right = x * 5
    return left - right

def after(x):
    right = x * 5
    left = x + 3
    return left - right

def observe(fn, x):
    events = []
    def trace(frame, event, arg):
        if frame.f_code is fn.__code__:
            if event == 'line':
                events.append(dict(frame.f_locals))
            return trace
        return None
    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        value = fn(x)
    finally:
        sys.settrace(previous)
    return value, events

if __name__ == '__main__':
    for x in (-7, 0, 1, 29):
        a, ta = observe(before, x)
        b, tb = observe(after, x)
        assert a == b
        assert ta[-1] == tb[-1]
        assert ta != tb
        print({'x': x, 'value': a, 'before': ta, 'after': tb})
