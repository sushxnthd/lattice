#!/usr/bin/env python3
"""Read-only independent symbol-survival witness for a Run234 artifact directory.

Usage: python run235_remote_witness.py /path/to/unzipped/artifact
Never changes frozen Run234 verifier scores.
"""
import ast
import hashlib
import json
import pathlib
import sys


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(p.read_text())


def audit(root):
    manifest = load(root/'SHA256_MANIFEST.json')
    observed = {str(p.relative_to(root)): sha(p.read_bytes()) for p in root.rglob('*')
                if p.is_file() and p.name != 'SHA256_MANIFEST.json'}
    assert manifest == observed, 'Artifact SHA-256 manifest mismatch'
    facts = load(root/'facts.json')
    records = load(root/'records.json')
    freeze = load(root/'freeze.json')
    assert len(records) == 2
    result = []
    for r in records:
        stem = root/'raw'/(freeze['issue']+'-'+r['arm'])
        req = load(pathlib.Path(str(stem)+'-request.json'))
        raw = load(pathlib.Path(str(stem)+'-response.json'))
        after = load(pathlib.Path(str(stem)+'-after.json'))
        assert sha(req['messages'][0]['content'].encode()) == r['prompt_sha256']
        assert req['model'] == r['model'] == freeze['model']
        assert req['seed'] == r['seed'] == freeze['seed']
        assert raw['usage'] == r['usage']
        assert load(pathlib.Path(str(stem)+'-verifier.json')) == r
        actions = json.loads(raw['choices'][0]['message']['content'])['actions']
        contracts = []
        for action in actions:
            if action['op'] != 'replace' or action['path'] not in after:
                continue
            matches = [t for t in facts[action['path']]['targets']
                       if t['target_id'] == action['selector']]
            assert len(matches) == 1, 'Ambiguous selector'
            target = matches[0]
            if target['kind'] not in ('FunctionDef','AsyncFunctionDef','ClassDef'):
                continue
            tree = ast.parse(after[action['path']])
            original_first = next(x for x in target['old_text'].splitlines() if x.strip())
            top_level = original_first == original_first.lstrip()
            nodes = tree.body if top_level else ast.walk(tree)
            survived = any(isinstance(n, (ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))
                           and n.__class__.__name__ == target['kind']
                           and n.name == target['name'] for n in nodes)
            aliases = [{'line':n.lineno,'target':ast.unparse(t)}
                       for n in tree.body if isinstance(n,ast.Assign)
                       and isinstance(n.value,ast.Name) and n.value.id == target['name']
                       for t in n.targets]
            contracts.append({'name':target['name'],'top_level':top_level,
                              'survived':survived,'dangling_aliases':aliases if not survived else []})
        result.append({'arm':r['arm'],'compiler_accepted':r['accepted'],
                       'syntax_valid':all(x['valid'] for x in r['syntax']),
                       'contracts':contracts,'functional_resolution':r['functional_resolution']})
    return {'issue':freeze['issue'],'verified_files':len(observed),'arms':result}


if __name__ == '__main__':
    print(json.dumps(audit(pathlib.Path(sys.argv[1])),indent=2,sort_keys=True))
