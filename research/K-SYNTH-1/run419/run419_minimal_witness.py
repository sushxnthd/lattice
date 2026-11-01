"""Run419 minimal independent multi-file byte-frame/AST parity witness.

Not the production editor; see local SHA-verified archive for full compiler.
"""
import ast
import hashlib


def digest(b):
    return hashlib.sha256(b).hexdigest()


def candidates(raw):
    tree = ast.parse(raw.decode('utf-8'))
    lines = raw.splitlines(keepends=True)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            target = node.test
            kind = 'IfTest'
        elif isinstance(node, ast.ImportFrom):
            target = node
            kind = 'ImportFrom'
        else:
            continue
        a = sum(map(len, lines[:target.lineno - 1])) + target.col_offset
        b = sum(map(len, lines[:target.end_lineno - 1])) + target.end_col_offset
        out.append((kind, a, b, digest(ast.dump(target, include_attributes=False).encode())))
    return sorted(out, key=lambda x: x[1])


def compile_two(files, sha, actions, mode):
    assert set(files) == set(sha)
    assert all(digest(v) == sha[k] for k, v in files.items())
    result = {}
    for path, raw in files.items():
        edits = []
        for act in actions:
            if act['path'] != path:
                continue
            table = candidates(raw)
            if mode == 'fingerprint':
                found = [x for x in table if x[0] == act['kind'] and x[3] == act['fingerprint']]
                assert len(found) == 1
                target = found[0]
            else:
                target = table[act['index']]
            replacement = act['replacement'].encode('utf-8')
            if b'\r\n' in raw:
                replacement = replacement.replace(b'\n', b'\r\n')
            if target[0] == 'ImportFrom':
                assert all(isinstance(n, (ast.ImportFrom, ast.Import)) for n in ast.parse(act['replacement']).body)
            else:
                ast.parse(act['replacement'], mode='eval')
            edits.append((target[1], target[2], replacement))
        for left, right in zip(sorted(edits), sorted(edits)[1:]):
            assert left[1] <= right[0]
        changed = raw
        for a, b, replacement in sorted(edits, reverse=True):
            changed = changed[:a] + replacement + changed[b:]
        ast.parse(changed.decode('utf-8'))
        result[path] = changed
    return result


def main():
    files = {
        'app.py': b'# copyright 2026\r\nfrom urllib.parse import quote\r\ndef f(x):\r\n    if x:\r\n        return 1\r\n    return 0\r\n',
        'other.py': b'# license stays\ndef g(x):\n    if x is None:\n        return 2\n    return 3\n',
    }
    sha = {p: digest(b) for p, b in files.items()}
    wanted = [('app.py', 'ImportFrom', 'from urllib.parse import quote\nfrom urllib.parse import urlsplit'),
              ('app.py', 'IfTest', 'x is not None'),
              ('other.py', 'IfTest', 'x == 0')]
    ir, ordinary = [], []
    for path, kind, replacement in wanted:
        table = candidates(files[path])
        i = next(i for i, row in enumerate(table) if row[0] == kind)
        ir.append({'path': path, 'kind': kind, 'fingerprint': table[i][3], 'replacement': replacement})
        ordinary.append({'path': path, 'index': i, 'replacement': replacement})
    a = compile_two(files, sha, ir, 'fingerprint')
    b = compile_two(files, sha, ordinary, 'ordinary')
    assert a == b
    assert a['app.py'].startswith(b'# copyright 2026\r\n')
    assert a['other.py'].startswith(b'# license stays\n')
    assert b'from urllib.parse import urlsplit\r\n' in a['app.py']
    print({'parity': True, 'source_files': 2, 'edit_sites': 3,
           'outputs_sha256': {p: digest(v) for p, v in a.items()}})


if __name__ == '__main__':
    main()
