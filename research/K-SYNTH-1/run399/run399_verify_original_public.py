"""Read-only audit of original Run398 GitHub Actions artifact ZIP.

Usage: python run399_verify_original_public.py original_run398_artifact.zip
No model-generated Python is executed. Post-hoc Markdown recovery is diagnostic.
"""
import ast
import hashlib
import json
import sys
import zipfile


def digest(b):
    return hashlib.sha256(b).hexdigest()


def verify(path):
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
    manifest = json.loads(files['manifest.json'])
    assert len(manifest) == 11
    for name, meta in manifest.items():
        assert len(files[name]) == meta['bytes']
        assert digest(files[name]) == meta['sha256']
    freeze = json.loads(files['freeze.json'])
    outputs = []
    for arm in ('IR', 'PYTHON_AST'):
        request = json.loads(files['request_' + arm + '.json'])
        assert request == freeze['requests'][arm]
        assert request['seed'] == 398 and request['temperature'] == 0
        prompt = request['messages'][0]['content']
        assert digest(prompt.encode()) == freeze['prompt_sha256'][arm]
        original = prompt.split('ORIGINAL SOURCE:\n### rich/_wrap.py\n', 1)[1]
        wrap, cells = original.split('\n\n### rich/cells.py\n', 1)
        assert digest(wrap.encode()) == freeze['facts']['source_sha256']['rich/_wrap.py']
        assert digest(cells.encode()) == freeze['facts']['source_sha256']['rich/cells.py']
        raw = json.loads(files['response_' + arm + '.raw.json'])
        completion = raw['choices'][0]['message']['content']
        assert completion.encode() == files['completion_' + arm + '.txt']
        original_score = json.loads(files['inference_' + arm + '.json'])
        assert original_score['compiler'] == 'rejected'
        assert 'JSONDecodeError' in original_score['compiler_reason']
        assert completion.startswith('```json\n') and completion.endswith('\n```')
        try:
            json.loads(completion)
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError('Original strict JSON unexpectedly accepted')
        recovered = json.loads(completion[len('```json\n'):-len('\n```')])
        assert len(recovered['edits']) == 1
        edit = recovered['edits'][0]
        assert edit['path'] == 'rich/_wrap.py' and edit['function'] == 'divide_line'
        original_fn = next(n for n in ast.parse(wrap).body if isinstance(n, ast.FunctionDef) and n.name == 'divide_line')
        assert ast.get_source_segment(wrap, original_fn) == edit['replacement']
        assert ast.dump(ast.parse(edit['replacement']).body[0], include_attributes=False) == ast.dump(original_fn, include_attributes=False)
        outputs.append({'arm': arm, 'original': 'JSONDecodeError', 'posthoc': 'NO_CHANGE', 'sha256': digest(completion.encode())})
    assert files['completion_IR.txt'] == files['completion_PYTHON_AST.txt']
    return {'manifest_entries': 11, 'results': outputs, 'model_code_executed': False}


if __name__ == '__main__':
    print(json.dumps(verify(sys.argv[1]), indent=2))
