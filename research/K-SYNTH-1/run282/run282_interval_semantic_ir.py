#!/usr/bin/env python3
"""K-SYNTH-1 Run282: soundness-scoped interval cardinality semantics.

This is a mechanistic, deterministic diagnostic, not an LLM performance study.
No arbitrary source or model code is evaluated. Only two fixed, audited Python
expressions are compiled for the independent CPython oracle.
"""
from __future__ import annotations
import ast
import dataclasses
import hashlib
import json
from pathlib import Path

OLD = 'len([connection.is_idle() for connection in self._connections]) > self._max_keepalive_connections'
NEW = 'sum(connection.is_idle() for connection in self._connections) > self._max_keepalive_connections'
REQUIRED = ('finite', 'stable', 'pure', 'boolean_return', 'integer_threshold')
VERDICTS = ('MUST_AGREE', 'MUST_DIVERGE', 'MAY_DIVERGE', 'UNKNOWN')


def exact_pattern_match(old: str = OLD, new: str = NEW) -> bool:
    """Recognize one narrow, explicitly audited syntactic repair template."""
    try:
        a, b = (ast.parse(s, mode='eval').body for s in (old, new))
    except SyntaxError:
        return False
    if not all(isinstance(x, ast.Compare) and len(x.ops) == 1 and isinstance(x.ops[0], ast.Gt)
               and len(x.comparators) == 1 for x in (a, b)):
        return False
    if ast.dump(a.comparators[0]) != ast.dump(b.comparators[0]):
        return False
    if not (isinstance(a.left, ast.Call) and isinstance(a.left.func, ast.Name)
            and a.left.func.id == 'len' and len(a.left.args) == 1
            and isinstance(a.left.args[0], ast.ListComp)):
        return False
    if not (isinstance(b.left, ast.Call) and isinstance(b.left.func, ast.Name)
            and b.left.func.id == 'sum' and len(b.left.args) == 1
            and isinstance(b.left.args[0], ast.GeneratorExp)):
        return False
    x, y = a.left.args[0], b.left.args[0]
    if len(x.generators) != 1 or len(y.generators) != 1:
        return False
    if ast.dump(x.elt) != ast.dump(y.elt) or ast.dump(x.generators[0]) != ast.dump(y.generators[0]):
        return False
    # Do not accept arbitrary code that merely has similar outer AST shape.
    return ast.dump(a) == ast.dump(ast.parse(OLD, mode='eval').body) and \
           ast.dump(b) == ast.dump(ast.parse(NEW, mode='eval').body)


@dataclasses.dataclass(frozen=True)
class CardinalityFacts:
    total: int | None
    idle_lower: int | None
    idle_upper: int | None
    threshold: int | None
    assumptions: dict[str, bool]

    def to_python_baseline(self) -> dict:
        """Ordinary Python/AST baseline receives the identical facts and authority."""
        return dataclasses.asdict(self)

    def to_ir(self) -> dict:
        """Structured semantic IR; not an information advantage over Python."""
        return {'kind': 'cardinality_interval_v1', 'facts': self.to_python_baseline(),
                'template': 'boolean_count_vs_collection_length'}


def classify(f: CardinalityFacts) -> str:
    if not exact_pattern_match() or any(f.assumptions.get(x) is not True for x in REQUIRED):
        return 'UNKNOWN'
    values = (f.total, f.idle_lower, f.idle_upper, f.threshold)
    if any(type(v) is not int for v in values):
        return 'UNKNOWN'
    n, lo, hi, k = values
    if not 0 <= lo <= hi <= n:
        return 'UNKNOWN'
    if n <= k:
        return 'MUST_AGREE'
    if hi <= k:
        return 'MUST_DIVERGE'
    if lo > k:
        return 'MUST_AGREE'
    return 'MAY_DIVERGE'


class Connection:
    def __init__(self, idle: bool):
        self._idle = idle
    def is_idle(self) -> bool:
        return self._idle


class Pool:
    def __init__(self, n: int, i: int, k: int):
        self._connections = [Connection(j < i) for j in range(n)]
        self._max_keepalive_connections = k


_OLD_CODE = compile(ast.parse(OLD, mode='eval'), '<fixed-old>', 'eval')
_NEW_CODE = compile(ast.parse(NEW, mode='eval'), '<fixed-new>', 'eval')


def independent_cpython(n: int, i: int, k: int) -> tuple[bool, bool]:
    obj = Pool(n, i, k)
    # eval runs only the two fixed, internally authored expressions above.
    return bool(eval(_OLD_CODE, {'self': obj})), bool(eval(_NEW_CODE, {'self': obj}))


def verify(max_n: int = 12, trace_path: str | None = None) -> dict:
    assert exact_pattern_match()
    assumptions = {x: True for x in REQUIRED}
    stats = {v: 0 for v in VERDICTS}
    checks = cases = 0
    stream = open(trace_path, 'w', encoding='utf-8') if trace_path else None
    try:
        for n in range(max_n + 1):
            for lo in range(n + 1):
                for hi in range(lo, n + 1):
                    for k in range(-2, n + 3):
                        facts = CardinalityFacts(n, lo, hi, k, assumptions)
                        verdict = classify(facts)
                        assert verdict != 'UNKNOWN'
                        # Ordinary Python view contains precisely the same facts.
                        assert facts.to_ir()['facts'] == facts.to_python_baseline()
                        assert CardinalityFacts(**facts.to_ir()['facts']) == facts
                        observed = []
                        for i in range(lo, hi + 1):
                            old, new = independent_cpython(n, i, k)
                            observed.append(old != new)
                            assert not (new and not old), (n, lo, hi, k, i)
                            checks += 1
                        expected = ('MUST_DIVERGE' if all(observed) else
                                    'MUST_AGREE' if not any(observed) else 'MAY_DIVERGE')
                        assert verdict == expected, (facts, verdict, expected)
                        stats[verdict] += 1
                        cases += 1
                        if stream:
                            stream.write(json.dumps({'n': n, 'lo': lo, 'hi': hi, 'k': k,
                                                     'verdict': verdict, 'observed': observed},
                                                    sort_keys=True, separators=(',', ':')) + '\n')
    finally:
        if stream:
            stream.close()
    # Unknown is mandatory when soundness assumptions are not established.
    unknowns = 0
    for missing in REQUIRED:
        bad = assumptions.copy()
        bad[missing] = False
        assert classify(CardinalityFacts(3, 1, 2, 1, bad)) == 'UNKNOWN'
        unknowns += 1
    for bad in [CardinalityFacts(3, 0, 4, 1, assumptions),
                CardinalityFacts(3, -1, 2, 1, assumptions),
                CardinalityFacts(3, 1, 2, True, assumptions),
                CardinalityFacts(None, 1, 2, 1, assumptions)]:
        assert classify(bad) == 'UNKNOWN'
        unknowns += 1
    # An explicit non-Boolean return violates the monotonicity theorem.
    nonboolean = {'values': [2, 2], 'threshold': 3,
                  'old': len([2, 2]) > 3, 'new': sum([2, 2]) > 3}
    assert nonboolean['old'] is False and nonboolean['new'] is True
    return {'scope': 'fixed AST template, finite stable pure Boolean-returning calls, integer threshold',
            'interval_cases': cases, 'independent_cpython_evaluations': checks,
            'verdict_counts': stats, 'unknown_controls': unknowns,
            'oracle_mismatches': 0, 'nonboolean_counterexample': nonboolean,
            'trace_sha256': hashlib.sha256(Path(trace_path).read_bytes()).hexdigest() if trace_path else None,
            'interpretation': 'bounded mechanistic certificate; not a model comparison or production-wide Python soundness'}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    result = verify(12, str(root/'run282_interval_raw.jsonl'))
    (root/'run282_interval_summary.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))
