"""Independent static format audit for Run31 pilot responses (NOT hidden scoring).

Never executes model-generated Python. Checks response envelope and compilability.
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
from pathlib import Path

def strict_json(s: str):
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError('duplicate JSON key')
            out[k] = v
        return out
    return json.loads(s, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def extract(arm: str, content: str):
    if arm == 'A':
        if not content.startswith('--- a/encoding.py\n+++ b/encoding.py\n'):
            raise ValueError('invalid unified diff header')
        if len(content) > 20000 or re.search(r'(?m)^\+\+\+ |^--- ', content[5:]):
            raise ValueError('additional or oversized patch')
        return {'kind': 'diff', 'text': content}
    obj = strict_json(content)
    if type(obj) is not dict:
        raise ValueError('edit must be object')
    if arm in ('B', 'D'):
        if set(obj) != {'interface', 'symbol', 'replacement'} or obj['interface'] != 'python' or obj['symbol'] != 'int_to_bytes':
            raise ValueError('invalid Python edit envelope')
        source = obj['replacement']
    elif arm == 'C':
        if (set(obj) != {'interface', 'scope', 'change'} or obj['interface'] != 'lattice' or
            obj['scope'] != {'symbol': 'int_to_bytes'} or type(obj['change']) is not dict or
            set(obj['change']) != {'source'}):
            raise ValueError('invalid Lattice edit envelope')
        source = obj['change']['source']
    else:
        raise ValueError('unknown arm')
    if type(source) is not str or len(source) > 20000:
        raise ValueError('invalid source')
    tree = ast.parse(source)
    compile(tree, '<candidate>', 'exec', dont_inherit=True)
    if len(tree.body) != 1 or type(tree.body[0]) is not ast.FunctionDef or tree.body[0].name != 'int_to_bytes':
        raise ValueError('replacement must be exactly one function')
    node = tree.body[0]
    if (len(node.args.args) != 1 or node.args.args[0].arg != 'num' or
        node.args.vararg or node.args.kwarg or node.args.kwonlyargs or node.args.defaults or
        node.decorator_list):
        raise ValueError('function authority exceeded')
    return {'kind': 'function', 'text': source}

def audit(folder: Path):
    folder = Path(folder)
    freeze = strict_json((folder / 'freeze.json').read_text())
    prompts = strict_json((folder / 'prompts.json').read_text())
    if set(prompts) != set('ABCD'):
        raise ValueError('incomplete prompts')
    for arm in 'ABCD':
        h = hashlib.sha256(prompts[arm].encode()).hexdigest()
        if h != freeze['prompts_sha256'][arm]:
            raise ValueError('frozen prompt mismatch: ' + arm)
    rows = []
    for arm in 'ABCD':
        path = folder / (arm + '_response.json')
        if not path.is_file():
            rows.append({'arm': arm, 'status': 'NO_MODEL_RESPONSE', 'format_valid': None})
            continue
        raw = path.read_bytes()
        response = strict_json(raw.decode())
        try:
            content = response['choices'][0]['message']['content']
            if type(content) is not str:
                raise ValueError('invalid content')
            parsed = extract(arm, content)
            verdict = {'status': 'FORMAT_VALID_STATIC_ONLY', 'format_valid': True,
                       'kind': parsed['kind']}
        except (ValueError, KeyError, TypeError, IndexError, SyntaxError) as exc:
            verdict = {'status': 'FORMAT_INVALID', 'format_valid': False,
                       'reason': str(exc)[:300]}
        rows.append({'arm': arm, 'response_sha256': hashlib.sha256(raw).hexdigest(), **verdict})
    return {'status': 'STATIC_FORMAT_AUDIT_NOT_HIDDEN_TEST_SCORING', 'rows': rows,
            'executed_generated_code': False, 'representation_advantage_established': False}
