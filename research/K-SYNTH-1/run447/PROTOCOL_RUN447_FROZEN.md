# K-SYNTH-1 Run447: prospective Python × oracle-protocol falsification

**Frozen before new cloud execution, 2026-11-02 UTC.** This is a mechanism experiment on already-qualified Flask PR6096, not a new benchmark issue, not coding-model inference, and not evidence of IR superiority.

## Immutable historical evidence

- Run445 Actions [41522993332](https://github.com/sushxnthd/lattice/actions/runs/41522993332), job 125543461677: logs identify Python **3.12.15** (setup-python 3.12). Original artifact ID 13177664423, ZIP SHA-256 `5cca13b9d9e6c781f187282c75f8cf3480207ba2ad8e2ce57e2d0aa3febf8ef0`. Original legacy oracle baseline session 60/128, reference 128/128. It ran a mocked `Flask.run` before the session probe; no pip freeze or request/cookie internals were captured.
- Run446 Actions [41527974055](https://github.com/sushxnthd/lattice/actions/runs/41527974055): Python **3.11.17**, Werkzeug **3.1.3**. Original artifact ZIP SHA-256 `eddf9f012646157488504af923cefee0c55286af8c4a59fa42fb697a1a76f060`. Diagnostic oracle baseline 64/128, reference 128/128.
- The exact same 128 frozen authorities have SHA-256 `b04edef3965002c27c5194ae4b4ca7bf5464ad7bfd757d4e39d987b09d84c3b3`. Only `dns_with_port_01/09/17/25` differ between historical baseline oracles. The reference observations agree 128/128.

**Identifiability finding:** The two observed cells (Python3.12 + legacy protocol: four failures; Python3.11 + diagnostic protocol: zero) cannot distinguish a Python-only effect from a protocol-only effect. Both causal functions exactly fit the observations and predict different crossed cells. The original Run445 dependency versions were not recorded.

## Frozen crossed design

Execute a 2 Python (3.11.17 vs 3.12.15) × 2 protocol (original byte-identical Run445 oracle vs canonical Run446 diagnostic) × 2 source variant (parent vs reference) × 128 frozen cases = **1,024 real Flask session transactions**, plus the original protocol's mocked Flask.run probes. Isolated subprocesses per condition. No untrusted model code.

- Exact historical Flask parent `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`, reference `7203feabf723edae0286ae5dc64fec8ac4c91735`; SHA-check base `testing.py` `60c60294d716a6102e9993ad8f14930ad421fde322d8d3b54c7be642acbad560` and reference `629d481658aaec7076a55913eda38c270ec45d430b34b2f9d38b2eec2b0ad3da`.
- Recover original `actual_oracle.py` directly from Run445 immutable Actions artifact and SHA-check `f41112919d3627b3cbf3416398c76a1f7c6c611e26a1ad3e0c8b1ca0ba6f728e`.
- Canonical Run446 diagnostic source pinned by Git blob SHA-1 `11d444973b14f1520cd22c61df8b914f29af93c9`.
- Pin Werkzeug 3.1.3, blinker 1.9.0, click 8.5.0, itsdangerous 2.2.0, Jinja2 3.1.6, MarkupSafe 3.0.4. Capture Python exact patch, full pip freeze, raw 128-case JSONL per cell, stdout/stderr, SHA manifest and failures.

**Predictions:** Python-only: 3.12 has four failures in both protocols, 3.11 zero in both. Protocol-only: legacy has four in both versions, diagnostic zero. Interaction: four only under 3.12 + legacy. Other patterns are negative or unresolved. Analyze exact case IDs and difference-in-differences. Do not claim a pure Python effect if dependency versions diverge; even a conditional pinned effect does not identify the original unpinned environment's cause.

All 89 reserved boundary issues remain sealed. Exactly two independently qualified real multi-source repairs. One K-SYNTH-1 kernel, branch `research/exp003-context-order`, exactly one OPEN/DRAFT/UNMERGED PR #9. No superiority or breakthrough claim.