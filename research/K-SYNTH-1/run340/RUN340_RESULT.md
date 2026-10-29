# K-SYNTH-1 Run340: frozen HTTPcore #882 four-arm qualification and zero-interaction counterexample

Date: 2026-10-29 UTC. Canonical branch: `research/exp003-context-order`; sole draft PR #9. All 89 reserved boundary issues remain SEALED.

## Original experiment and evidence

The prospectively frozen protocol is `research/K-SYNTH-1/run339/PROTOCOL_RUN340.md`, committed before inspecting the reference implementation. Historical base `c46802478cdd8a82ee8cb333420080fab1aed00b`; reference head `c617b700fe0b06b33af8a604d3c8d6e1fbbe806c`. Only `httpcore/_sync/http11.py` and `httpcore/_async/http11.py` were substituted, with all other historical source fixed.

Original GitHub Actions run [40857666714](https://github.com/sushxnthd/lattice/actions/runs/40857666714), original artifact ID `12889498758`, original ZIP SHA-256 `d1ebbc8393f5cd5e6077b4d48ac94473007307a904806c8e6d2acbcde6f2664a`. The four-arm functional experiment itself succeeded, but the reporting job failed because the read-only auditor required `HISTORICAL_PINNED` while the immutable original oracle emitted `HISTORICAL_PINN`. The auditor-only typo was corrected in commit `ae156e7b7df51614f1fc0b24d136a4571bc5fca5`. **No original prompts, cases, results, model outputs, or oracle were modified or rescored.**

The original public-API functional results, recovered and independently reaudited:

| Source arm | Frozen targets passed | Frozen controls passed | Total |
|---|---:|---:|---:|
| Base sync + base async | 0/4 | 6/6 | 6/10 |
| Ref sync + base async | 2/4 | 6/6 | 8/10 |
| Base sync + ref async | 2/4 | 6/6 | 8/10 |
| Ref sync + ref async | 4/4 | 6/6 | 10/10 |

All 40 original records were independently checked against the immutable case definitions, observed statuses, byte-exact public network-stream reads, mock backend traces, nonregression cases, source revisions and Git blob IDs. Eight deliberately corrupted evidence variants were all detected by the separate read-only auditor. The source Git blobs were independently cross-checked against the original public HTTPcore repository at both pinned commits.

**Original prospective decision: QUALIFIED under the predeclared multi-production-source two-component necessity rule.** Baseline fails four targets, preserves six controls; full reference repairs all targets and preserves controls; each single-component variant leaves two unrepaired target failures and preserves controls, without ABI-related exceptions. This is the fourth independently qualified repository-level historical task (Flask, urllib3, HTTPX, HTTPcore).

## New negative result: necessity is not semantic interaction

Let `Y_i(S,A)` denote success on target case `i`, where `S` and `A` indicate reference sync and async source. The per-case factorial interaction is `D_i = Y_i(1,1) - Y_i(1,0) - Y_i(0,1) + Y_i(0,0)`.

For both sync targets, `Y_i(S,A)=S`; for both async targets, `Y_i(S,A)=A`. Therefore `D_i=0` for **all four targets**, and the aggregate interaction is `4-2-2+0=0`. Nevertheless, full target completion requires **both** source files. Thus the proposition “both components are necessary to pass all targets, therefore there is a cross-file semantic interaction” is false.

This is a real-production, public-API, SHA-pinned counterexample to a *methodological inference*, not a counterexample to the HTTPcore fix. The task can be used for general two-file repair feasibility but **cannot** establish a cross-file dataflow mechanism. Future mechanism tests must distinguish independent parallel implementation coverage from cross-file semantic dependence; prospectively preregister a nonzero ABI-factored interaction criterion where cross-file interaction is the scientific hypothesis. Do not retroactively disqualify HTTPcore #882 or reinterpret the frozen result.

## Limits and next steps

No new coding-model inference was run. The reference-informed 2x2 qualification is not prospective model success. A 10-case oracle does not establish complete production correctness, and this case's parallel sync/async structure may favor simple ordinary Python editing. The new result does not support IR superiority. Continue with a frozen four-arm paired model comparison and additional independent production tasks, preserving identical task facts, edit authority, compiler and isolated oracle; report negative outcomes and clustering-adjusted uncertainty. Do not change the 89 sealed issues or merge PR #9.

## Exact rerun after audit-only fix

The rerun [40866524756](https://github.com/sushxnthd/lattice/actions/runs/40866524756) completed **SUCCESS**, artifact ID `12893373572`, ZIP SHA-256 `6a28444a170e572f5b20143a2ccbcbbfaac5c5a8d7d92556aca9c18e791bc7b9`. Its `raw/decision.json` explicitly records `qualified: true`, no reasons or exceptions. Independently compared the rerun with the original failed-audit artifact: all four raw result JSON files, source manifest, pinned commits, frozen oracle and protocol are **byte-identical**. The only scientific difference is the corrected read-only audit output. This is a reproducibility rerun, not a second independent task or a new model inference.
