#!/usr/bin/env python3
"""Exact finite counterfactual influence support for Run383's verified Boolean grammar.

Support[target_input][producer_truth_table_bit] is true iff flipping only
that producer output changes target output for some assignment of the
remaining producer bits. UNKNOWN for unsupported or non-total programs.
No generated source is executed: this uses the whitelisted Run383 AST interpreter.
"""
from dataclasses import dataclass
from run383_exact_counterfactual import parse, evaluate

INPUTS = ((False, False), (False, True), (True, False), (True, True))

@dataclass(frozen=True)
class Certificate:
    verdict: str
    support: tuple = ()
    witnesses: tuple = ()
    reason: str = ''

def certify(producer, consumer):
    try:
        aliases, functions = parse(producer, consumer)
        outputs = tuple(
            tuple(bool(evaluate(aliases, functions, table, *xy)) for xy in INPUTS)
            for table in range(16)
        )
        support = []
        witnesses = []
        for i in range(4):
            row = []
            for bit in range(4):
                witness = None
                for t0 in range(16):
                    if t0 & (1 << bit):
                        continue
                    t1 = t0 | (1 << bit)
                    if outputs[t0][i] != outputs[t1][i]:
                        witness = (i, bit, t0, t1, outputs[t0][i], outputs[t1][i])
                        break
                row.append(witness is not None)
                if witness is not None:
                    witnesses.append(witness)
            support.append(tuple(row))
        return Certificate(
            'DEPENDENCE_CERTIFIED' if witnesses else 'NO_DEPENDENCE',
            tuple(support), tuple(witnesses)
        )
    except (SyntaxError, ValueError, RuntimeError, RecursionError, MemoryError) as exc:
        return Certificate('UNKNOWN', reason=str(exc))
