#!/usr/bin/env python3
"""Lossless trusted affine two-file edit transaction for K-SYNTH-1.

Not a general Python editor or an on-disk crash-atomic transaction. Input files
are immutable bytes; the function either returns both verified outputs or raises.
"""
from __future__ import annotations
import ast
from run436_dual_view_compiler import Unknown, inspect, canonicalize, sha


def _rhs_node(source: bytes, function: str, is_provider: bool) -> ast.AST:
    try:
        module = ast.parse(source.decode('utf-8'))
    except (UnicodeError, SyntaxError) as exc:
        raise Unknown('UNKNOWN_PARSE') from exc
    funcs = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == function]
    if len(funcs) != 1 or len(funcs[0].body) != 1 or not isinstance(funcs[0].body[0], ast.Return):
        raise Unknown('UNKNOWN_FUNCTION_BINDING')
    expression = funcs[0].body[0].value
    if not isinstance(expression, ast.BinOp) or not isinstance(expression.op, ast.Add):
        raise Unknown('UNKNOWN_EXPRESSION')
    return expression.right


def _byte_span(source: bytes, node: ast.AST) -> tuple[int, int]:
    # CPython AST column offsets are UTF-8 byte offsets, NOT character offsets.
    lines = source.splitlines(keepends=True)
    if not all(hasattr(node, name) for name in ('lineno', 'col_offset', 'end_lineno', 'end_col_offset')):
        raise Unknown('UNKNOWN_AST_LOCATION')
    a = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
    b = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
    if not (0 <= a < b <= len(source)):
        raise Unknown('UNKNOWN_INVALID_BYTE_SPAN')
    return a, b


def transact_lossless(sources: dict[str, bytes], action: dict, mode: str):
    before = inspect(sources)
    canonical = canonicalize(action, mode, before)
    locations = {'provider.py': ('core', 'provider.core.affine_b', 'affine_b'),
                 'consumer.py': ('compute', 'consumer.compute.offset', 'offset')}
    outputs = {}
    spans = {}
    for filename, (func, key, field) in locations.items():
        source = sources[filename]
        node = _rhs_node(source, func, filename == 'provider.py')
        a, b = _byte_span(source, node)
        old = before['known_effects']['provider.core' if filename == 'provider.py' else 'consumer.compute'][field]
        value = canonical[key]
        replacement = source[a:b] if value == old else str(value).encode('ascii')
        output = source[:a] + replacement + source[b:]
        # Byte-level preservation is stronger than AST equality: every
        # byte outside the explicitly authorized integer span survives.
        assert output[:a] == source[:a]
        assert output[a + len(replacement):] == source[b:]
        outputs[filename] = output
        spans[filename] = {'original_start': a, 'original_end': b,
                           'replacement_sha256': sha(replacement),
                           'no_op': value == old,
                           'original_literal_sha256': sha(source[a:b])}
    after = inspect(outputs)
    if after['known_effects']['provider.core']['affine_b'] != canonical['provider.core.affine_b'] or after['known_effects']['consumer.compute']['offset'] != canonical['consumer.compute.offset']:
        raise Unknown('UNKNOWN_POSTCONDITION_FAILURE')
    for name, control in [('provider.keep', 'provider.keep'), ('consumer.keep', 'consumer.keep')]:
        assert name in after['controls'] and control in before['controls']
    assert after['cross_file_edges'] == before['cross_file_edges']
    return outputs, {'schema':'K-SYNTH-1/LOSSLESS-ATOMIC-IN-MEMORY-v1',
                     'mode':mode, 'input_sha256':before['source_sha256'],
                     'output_sha256':after['source_sha256'],
                     'spans':spans,'canonical_effects':canonical,
                     'limitations':'trusted exact-int affine grammar; no filesystem crash atomicity; no general Python semantics'}
