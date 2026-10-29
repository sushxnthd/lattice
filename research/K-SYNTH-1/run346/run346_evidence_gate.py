"""Portable Run346 SHA and semantic-construct gate; read-only, no model code execution."""
import ast
import hashlib
import io
import json
import sys
import zipfile

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checked(data, manifest):
    z = zipfile.ZipFile(io.BytesIO(data))
    for name, digest in json.loads(z.read(manifest)).items():
        assert sha(z.read(name)) == digest, name
    return z

def facts(request, tag):
    text = request['messages'][0]['content']
    return [line.replace('SLOT=ast.arguments.kw_defaults', 'SLOT=KW_ONLY')
            .replace('SLOT=ast.arguments.defaults', 'SLOT=POSITIONAL')
            for line in (s[len(tag):] for s in text.splitlines() if s.startswith(tag))]

def audit(parent):
    outer = checked(parent, 'RUN336_SHA256_MANIFEST.json')
    inner = checked(outer.read('run335_original_artifact.zip'), 'SHA256_MANIFEST.json')
    candidates = json.loads(inner.read('candidates.json'))
    assert len(candidates) == 31
    assert all(c['call_target'] == 'UNKNOWN' and c['runtime_effect'] == 'UNKNOWN'
               for c in candidates)
    trees = {path: ast.parse(inner.read('stages/IR/' + path).decode())
             for path in ('httpx/_api.py', 'httpx/_client.py')}
    edge_count = 0
    for c in candidates:
        for edge in c['flows']:
            matches = [call for call in ast.walk(trees[c['path']])
                       if isinstance(call, ast.Call) and call.lineno == edge['line']
                       and ast.unparse(call.func) == edge['callee']
                       and any(k.arg == edge['keyword'] and isinstance(k.value, ast.Name)
                               and k.value.id == c['param'] for k in call.keywords)]
            assert len(matches) == 1, (c['id'], edge)
            edge_count += 1
    assert edge_count == 28
    counts = {}
    for arm in ('BASE', 'IR', 'PYTHON_AST'):
        rows = json.loads(inner.read('oracle_' + arm + '.json'))['cases']
        assert len(rows) == 9 and all(r['passed'] == (r['error'] is None
            and r['observed'] == r['expected']) for r in rows)
        counts[arm] = [sum(r['passed'] for r in rows if r['id'].startswith(('target_', 'heldout_'))),
                       sum(r['passed'] for r in rows if r['id'].startswith('control_'))]
    assert counts == {'BASE': [0, 6], 'IR': [1, 6], 'PYTHON_AST': [1, 6]}
    prompt_tokens = {}
    for stage in ('GATE', 'REAL'):
        ir = json.loads(inner.read('request_' + stage + '_IR.json'))
        py = json.loads(inner.read('request_' + stage + '_PYTHON_AST.json'))
        assert facts(ir, 'IR_DEFAULT ') == facts(py, 'PY_AST_DEFAULT ')
        assert {k: v for k, v in ir.items() if k != 'messages'} == {
            k: v for k, v in py.items() if k != 'messages'}
        assert inner.read('completion_' + stage + '_IR.txt') == inner.read(
            'completion_' + stage + '_PYTHON_AST.txt')
        comp_ir = json.loads(inner.read('compile_' + stage + '_IR.json'))
        comp_py = json.loads(inner.read('compile_' + stage + '_PYTHON_AST.json'))
        assert comp_ir['accepted'] and comp_py['accepted']
        assert comp_ir['edits'] == comp_py['edits']
        assert comp_ir['patched_sha256'] == comp_py['patched_sha256']
        prompt_tokens[stage] = [json.loads(inner.read('raw_' + stage + '_' + arm + '.json'))
                                ['usage']['prompt_tokens'] for arm in ('IR', 'PYTHON_AST')]
    assert prompt_tokens == {'GATE': [459, 463], 'REAL': [4088, 4208]}
    return {'original_manifest_entries_verified': [9, 44],
            'candidate_count': 31, 'verified_lexical_MAY_edges': edge_count,
            'verified_runtime_MUST_edges': 0, 'oracle_counts_targets_controls': counts,
            'model_prompt_tokens_IR_PYTHON_AST': prompt_tokens,
            'new_model_inference': False}

if __name__ == '__main__':
    print(json.dumps(audit(open(sys.argv[1], 'rb').read()), indent=2, sort_keys=True))
