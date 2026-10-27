# K-SYNTH-1 Run295 preregistration (before local test execution)

Canonical branch: research/exp003-context-order. Single draft PR #9. All 89 boundary issues sealed.

Research question: Does Run294's shared exact-byte-span compiler mistakenly accept staged Python files that `ast.parse(decoded_utf8_text)` accepts but the CPython 3.13 source-file compiler rejects, or whose source-file decoding differs from decoded-UTF8 AST semantics?

Original code: research/K-SYNTH-1/run294/run294_transaction_compiler.py, SHA-256 8801e6da5c9bf37c353d8378bb334b0aeb53e104239d71bdd53a60bf7df50df3.

Prospective cases (each one UTF-8 Python file, one exact-SHA span replacement to the listed entire file, both SEMANTIC_IR and PYTHON_AST_ACTIONS encodings):
- C01 top-level `return 1\n`: reject INVALID_PYTHON_BYTECODE.
- C02 top-level `break\n`: reject INVALID_PYTHON_BYTECODE.
- C03 top-level `continue\n`: reject INVALID_PYTHON_BYTECODE.
- C04 top-level `nonlocal x\n`: reject INVALID_PYTHON_BYTECODE.
- C05 top-level `yield 1\n`: reject INVALID_PYTHON_BYTECODE.
- C06 top-level `await f()\n`: reject INVALID_PYTHON_BYTECODE.
- C07 `x = 1\nfrom __future__ import annotations\n`: reject INVALID_PYTHON_BYTECODE.
- C08 `# coding: latin-1\nvalue = "é"\n` encoded UTF-8: reject UNSUPPORTED_ENCODING.
- C09 `# coding: cp1252\nvalue = "é"\n` encoded UTF-8: reject UNSUPPORTED_ENCODING.
- C10 `# coding: utf-8\nvalue = "é"\n`: accept.
- C11 `def f():\n    return 1\n`: accept.
- C12 `pass\n`: accept.

The trusted original file is `module.py` containing `pass\n`. Each candidate transaction replaces its complete bytes; both representations must agree exactly on acceptance/rejection and staged file SHA. Original source snapshot must remain unchanged. Record raw candidate bytes, compiler outcome, exact SHA, CPython byte compilation and imported-runtime observations when valid. Keep original v1 outcomes unchanged; a v2 fix is a new prospective compiler contract, not retroactive v1 scoring.

C08/C09 are an explicit regression check of the already documented Run264 PEP-263 bug; they are NOT claimed as new discovery. C01-C07 test the separate AST-only-vs-bytecode-validity gap. All candidates are manually authored trusted fixtures, not model completions. No IR superiority, real-repo qualification, or model-repair claim.

After first execution, preserve any failed expectations, implement fail-closed v2 with `tokenize.detect_encoding` and `compile(bytes,...,dont_inherit=True)`, then test with a separate independent read-only auditor and at least 100 seeded valid paired transactions. Preserve full SHA manifest and report GitHub failures.
