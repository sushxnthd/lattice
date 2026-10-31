# K-SYNTH-1 Run399: Original Run398 Qwen outputs independently audited

Date: 2026-11-01 IST. Original Actions run: https://github.com/sushxnthd/lattice/actions/runs/41243696441. Original artifact ID: 13059280780. Original ZIP SHA-256: `19b106d2716a506599fe6156fe68417aedccf1de96474e7d331e1b286e93bef3`.

Recovered the **original** GitHub artifact and verified all 11 original SHA-256 manifest payloads, both exact prompt hashes, source hashes, seed 398, temperature zero, model SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, raw completions, usage and frozen compiler outcomes.

| Arm | Original strict compiler | Post-hoc Markdown fence removal | Functional edit |
| --- | --- | --- | --- |
| JSON binding facts, labeled IR | JSONDecodeError | Valid JSON | NO_CHANGE |
| Python-literal binding facts, labeled PYTHON_AST | JSONDecodeError | Valid JSON | NO_CHANGE |

Both original Qwen2.5-Coder-7B-Instruct Q4_K_M completions were **byte-identical**, SHA-256 `20b1b10439779f768cac11ad28616c865761944290bf866af272a0c320633fbb`. Independent source-span and AST checks proved that the proposed `rich/_wrap.py::divide_line` replacement was byte-identical to the baseline function. Neither original strict compiler accepted the fenced response. No model-generated Python was executed. Twelve independent regression/adversarial tests passed locally.

**Construct-validity correction:** The prompts differ only in JSON vs Python-literal serialization of the same four natural-language binding facts and two UNKNOWN caveats. They use identical source and the same Python function-replacement action language. This is **not** a genuinely distinct semantic/dataflow IR versus Python/AST-action comparison, and the historical Rich #3176 task is not a prospectively blind primary issue.

A separate local isolated real-library behavior probe identified a potentially security-relevant cross-context configuration interaction. Detailed reproduction and raw functional evidence are retained in the SHA-verified local archive, not committed publicly pending responsible-disclosure review. It is not a qualified historical multi-source repair or IR superiority evidence.

No new qualified production repair, functional model repair, powered superiority result or breakthrough. The two previously qualified primary tasks remain unchanged; all 89 reserved boundary issues remain sealed. Sole PR #9 remains draft/open/unmerged.

The complete local Run399 archive includes the original GitHub ZIP, independent read-only auditor, twelve adversarial tests, raw functional traces, executable isolated probe, exact manifest and forward protocol.
