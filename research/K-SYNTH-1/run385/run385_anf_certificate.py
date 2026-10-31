#!/usr/bin/env python3
"""K-SYNTH-1 Run385: complete finite-domain producer-intervention certificate.

Admits only the Run383 parser's bounded pure Boolean grammar. For each of four
consumer inputs, the target under every one of the 16 producer truth tables is
encoded as a unique algebraic normal form (ANF) over GF(2). No untrusted source
is executed: all observations use the AST interpreter.

UNKNOWN means that at least one intervention cannot be proven terminating,
source is unsupported, or resource bounds are exceeded. No claim about general
Python or observational causality is implied.
"""
from dataclasses import dataclass
from run383_exact_counterfactual import parse, evaluate

INPUTS=((False,False),(False,True),(True,False),(True,True))

@dataclass(frozen=True)
class CompleteCertificate:
    verdict: str
    anf: tuple=()  # four 16-element GF(2) coefficient rows, indexed by monomial mask
    support: tuple=()  # four 4-element Boolean influence rows
    interaction: tuple=()  # four 6-element pairwise interaction rows
    truth: tuple=()  # four 16-element truth vectors, producer table indexed
    reason: str=''


def anf_transform(truth):
    """In-place GF(2) subset-lattice Moebius transform (self-inverse)."""
    if len(truth)!=16 or any(type(v) is not bool for v in truth):
        raise ValueError('invalid_truth')
    coefficients=[int(v) for v in truth]
    for bit in range(4):
        for mask in range(16):
            if mask & (1<<bit):
                coefficients[mask]^=coefficients[mask^(1<<bit)]
    return tuple(coefficients)


def decode_anf(coefficients):
    if len(coefficients)!=16 or any(v not in (0,1) for v in coefficients):
        raise ValueError('invalid_coefficients')
    return tuple(bool(sum(coefficients[subset] for subset in range(16)
                          if subset & mask == subset)%2) for mask in range(16))


def support_from_anf(coefficients):
    """A bit matters iff at least one monomial containing it has coefficient 1.

    This equivalence follows from uniqueness of the ANF of the Boolean
    derivative. It is NOT inferred from syntactic producer calls.
    """
    return tuple(any(coefficients[mask] for mask in range(16)
                     if mask & (1<<bit)) for bit in range(4))


def interaction_from_anf(coefficients):
    """Pairwise derivative nonzero iff a monomial contains both variables."""
    return tuple(any(coefficients[mask] for mask in range(16)
                     if mask & (1<<a) and mask & (1<<b))
                 for a in range(4) for b in range(a+1,4))


def certify(producer,consumer):
    try:
        aliases,functions=parse(producer,consumer)
        per_table=tuple(tuple(bool(evaluate(aliases,functions,t,*xy))
                              for xy in INPUTS) for t in range(16))
        truth=tuple(tuple(per_table[t][i] for t in range(16)) for i in range(4))
        anf=tuple(anf_transform(row) for row in truth)
        support=tuple(support_from_anf(row) for row in anf)
        interaction=tuple(interaction_from_anf(row) for row in anf)
        return CompleteCertificate('DEPENDENCE_CERTIFIED' if any(map(any,support))
                                   else 'NO_DEPENDENCE',anf,support,interaction,truth)
    except (SyntaxError,ValueError,RuntimeError,RecursionError,MemoryError) as exc:
        return CompleteCertificate('UNKNOWN',reason=str(exc))

if __name__=='__main__':
    import json
    p='def produce(x,y):\n    return x and y\n'
    c='from producer import produce as p\ndef target(x,y):\n    return p(x,y) and p(y,x)\n'
    print(json.dumps(certify(p,c).__dict__))
