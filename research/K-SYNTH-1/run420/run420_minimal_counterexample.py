#!/usr/bin/env python3
"""Run420 minimal independently executable exact-int contract counterexample.

No model-generated code is executed. Annotation `x: int` does not enforce exact
built-in int. This falsifies unconditional dead-assignment noninterference.
"""
class StatefulInt(int):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj.accumulator = 0
        return obj

    def __add__(self, other):
        self.accumulator += int(other)
        return self.accumulator

def before(x: int):
    dead = x + 1
    live = x + 2
    return live

def after(x: int):
    dead = x + 101
    live = x + 2
    return live

if __name__ == "__main__":
    assert before(3) == after(3) == 5
    original = before(StatefulInt(3))
    modified = after(StatefulInt(3))
    assert original != modified
    assert type(StatefulInt(3)) is not int
    print({"exact_int": 5, "stateful_before": original,
           "stateful_after": modified,
           "conditional_type_contract_required": True})
