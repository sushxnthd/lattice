"""Independent Run222 PyBaMM functional counterexample; Python stdlib only.
Usage: python run223_pybamm_witness.py run222_issue6.zip
This checks necessary behavioral conditions, NOT complete issue resolution.
"""
import ast
import json
import sys
import types
import zipfile


def get_json(z, suffix):
    names = [n for n in z.namelist() if "/raw/" in n and n.endswith(suffix)]
    assert len(names) == 1, (suffix, names)
    return json.loads(z.read(names[0]))


def witness(method, solved):
    ast.parse('class Candidate:\n' + method)
    events = []

    class QuickPlot:
        def __init__(self, value):
            events.append(['construct', value is None])

        def create_gif(self, **kwargs):
            events.append(['gif', kwargs])

    namespace = {'pybamm': types.SimpleNamespace(QuickPlot=QuickPlot)}
    exec(compile('class Candidate:\n' + method, '<raw-completion>', 'exec'), namespace)
    obj = namespace['Candidate']()
    obj.quick_plot = None
    obj.sims = ['solved'] if solved else None
    obj._solution = object() if solved else None
    error = None
    try:
        obj.create_gif(number_of_images=3)
    except Exception as exc:
        error = type(exc).__name__
    gifs = sum(e[0] == 'gif' for e in events)
    passed = (error is None and gifs == 1) if solved else (error is not None and gifs == 0)
    return {'solved': solved, 'events': events, 'error': error, 'passed': passed}


def main(archive):
    with zipfile.ZipFile(archive) as z:
        semantic_req = get_json(z, '-semantic_ir_json-request.json')
        prompt = semantic_req['messages'][0]['content'].split('SOURCE_FACTS:\n', 1)[1]
        facts, _ = json.JSONDecoder().raw_decode(prompt)
        results = {}
        for arm in ('semantic_ir_json', 'python_annotated'):
            response = get_json(z, '-' + arm + '-response.json')
            actions = json.loads(response['choices'][0]['message']['content'])['actions']
            cases = []
            for path in ('pybamm/batch_study.py', 'pybamm/simulation.py'):
                target, = [t for t in facts[path]['targets'] if t['kind'] == 'FunctionDef' and t['name'] == 'create_gif']
                replacements = [a['replacement'] for a in actions if a['op'] == 'replace' and a['path'] == path and a['selector'] == target['target_id']]
                assert len(replacements) <= 1
                method = replacements[0] if replacements else target['old_text']
                for solved in (False, True):
                    cases.append({'path': path, **witness(method, solved)})
            results[arm] = cases
    print(json.dumps(results, indent=2))
    assert not all(x['passed'] for x in results['semantic_ir_json'])
    assert not all(x['passed'] for x in results['python_annotated'])


if __name__ == '__main__':
    main(sys.argv[1])
