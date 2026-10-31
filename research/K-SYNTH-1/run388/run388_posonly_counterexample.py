"""Executable CPython counterexample: positional-only name plus **kwargs.

This demonstrates why a keyword matching a positional-only formal is not
necessarily a binding error. It is a bounded binding example, not a proof of
runtime semantic soundness for arbitrary Python.
"""

def f(x, /, **kwargs):
    return x, kwargs

assert f(1, x=2) == (1, {"x": 2})
try:
    f(x=2)
except TypeError:
    pass
else:
    raise AssertionError("missing positional-only x was accepted")
print("PASS: positional-only name captured by **kwargs; required x still enforced")
