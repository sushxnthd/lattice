"""Run219 CI oracle: immutable Run218 model artifacts, no hidden tests."""
import ast
import hashlib
import json
import re
import sys
import zipfile
from types import SimpleNamespace

EXPECTED = [
    'bf563236c88a28d60cf80002b80b2c7ce10882e276134e41b7e544ad11a5724b',
    'c430cd2ae371d7d85a314f23ebc90b35779a4bcf5dc80fa60d70f81e2685f47b',
]
ARMS = ('semantic_ir_json', 'python_annotated')
MODEL_SHA = '509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c'
CASES = [
    ('same', ('feature liga {} liga;', 'feature liga {} liga;'), True),
    ('default_only', ('feature liga {} liga;', ''), True),
    ('different', ('feature liga {} liga;', 'feature kern {} kern;'), False),
    ('include_two', ('include(foo.fea);', 'include(foo.fea);'), False),
    ('include_three', ('include(foo.fea);',)*3, False),
]

def load(z, suffix):
    matches = [n for n in z.namelist() if n.endswith(suffix)]
    assert len(matches) == 1, (suffix, matches)
    return json.loads(z.read(matches[0]))

def evaluate_function(source):
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_featuresCompatible']
    assert len(nodes) == 1
    namespace = {'re': re, 'DesignSpaceDocument': object, 'SourceDescriptor': object}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<oracle>', 'exec'), namespace)
    results = []
    for name, features, expected in CASES:
        sources = [SimpleNamespace(font=SimpleNamespace(features=SimpleNamespace(text=x))) for x in features]
        actual = namespace['_featuresCompatible'](SimpleNamespace(sources=sources, default=sources[0]))
        results.append({'case': name, 'expected': expected, 'observed': actual, 'pass': actual is expected})
    return results

def run(paths):
    out = {'protocol': 'run219-independent-oracle-ci-v1', 'tasks': []}
    for index, path in enumerate(paths):
        raw = open(path, 'rb').read()
        assert hashlib.sha256(raw).hexdigest() == EXPECTED[index], path
        with zipfile.ZipFile(path) as z:
            records = load(z, '/records.json')
            coverage = load(z, '/target_coverage.json')
            assert coverage['information_equivalence'] is True
            task = {'issue': records[0]['task'], 'arms': []}
            for arm in ARMS:
                rec = next(r for r in records if r['arm'] == arm)
                tag = rec['task'] + '-' + arm
                request = load(z, '/' + tag + '-request.json')
                response = load(z, '/' + tag + '-response.json')
                verifier = load(z, '/' + tag + '-verifier.json')
                prompt = request['messages'][0]['content']
                assert hashlib.sha256(prompt.encode()).hexdigest() == rec['prompt_sha256']
                assert rec['seed'] == request['seed']
                assert rec['model_sha256'] == MODEL_SHA
                assert rec['accepted'] is True and verifier['accepted'] is True
                assert rec['usage'] == response['usage']
                actions = json.loads(response['choices'][0]['message']['content'])['actions']
                assert all(set(a) == {'op','path','file_sha256','selector','replacement','content'} for a in actions)
                assert sorted({a['path'] for a in actions}) == rec['changed_paths']
                entry = {'arm': arm, 'compiler_accepted': True, 'changed_paths': rec['changed_paths'],
                         'seed': rec['seed'], 'tokens': rec['usage'], 'trace': rec['trace']}
                if index == 0:
                    candidates = [a['replacement'] for a in actions if a['path'] == 'Lib/ufo2ft/featureCompiler.py']
                    assert len(candidates) == 1
                    entry['contract_cases'] = evaluate_function(candidates[0])
                    entry['necessary_contract_passed'] = all(c['pass'] for c in entry['contract_cases'])
                else:
                    entry['necessary_contract_passed'] = 'src/spikeinterface/curation/curationsorting.py' in rec['changed_paths']
                task['arms'].append(entry)
            out['tasks'].append(task)
    assert all(not a['necessary_contract_passed'] for t in out['tasks'] for a in t['arms'])
    return out

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'usage: ci_oracle.py run218-task0.zip run218-task1.zip'
    print(json.dumps(run(sys.argv[1:]), indent=2))
