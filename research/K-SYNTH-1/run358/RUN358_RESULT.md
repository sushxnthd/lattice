# K-SYNTH-1 Run358: original Qwen failure recovered; real h11 ownership counterexample

2026-10-30 UTC. No model success, new qualified repair, powered IR advantage, or breakthrough is claimed.

## Original Run357b result, independently recovered

GitHub Actions [41007027701](https://github.com/sushxnthd/lattice/actions/runs/41007027701) completed and uploaded original artifact **12956780014**, ZIP SHA-256 `76911acfe755713fa56866cdd72ff19947dbbecea01b15326c3ff2e27b004317`. All **17/17 original evidence manifest entries** verified. Qwen2.5-Coder-7B Q4_K_M raw tokenizer counts: **14,315 IR**, **14,909 Python/AST**. With 3,500 completion tokens, both exceeded the original 16,384 context slot. **Zero model completions**, zero candidate compiler decisions, zero candidate oracle runs. The isolated historical baseline oracle reproduced **6/10**. Classification: **precompletion context overflow**, not model failure or representation result.

A **new prospectively frozen** replay changes only llama.cpp context from 16,384 to **20,480**, leaving original prompt hashes, Qwen model/seed/temperature, 3,500 completion budget, source, facts, authority, compiler and isolated 10-case oracle unchanged. Protocol: [PROTOCOL_CONTEXT_REPLAY.md](./PROTOCOL_CONTEXT_REPLAY.md). Workflow: [Run358 20k](../../../.github/workflows/lattice-k-synth-1-run358-httpcore-20k.yml). This is not a retrospective rescore. Original new-workflow commit `e30f3ddfaafef306b3545ac76b3b9b263d7723e9`, blob `d1609a724a5234f7df0ea3b46dabb21c01845762`. No new model artifact had been recovered at report time.

## Real h11 functional mechanism

Executed **1,536 deterministic h11 0.16.0 parser traces**: 512 each of valid GET 101 Upgrade, CONNECT 200, and ordinary GET 200. These represent correlated split/read-pattern variants (32 distinct body splits per protocol), **not 1,536 independent tasks**. Nonempty `trailing_data` occurred in **503/512** Upgrade, **494/512** CONNECT, and **493/512** ordinary GET 200 traces. Upgrade and CONNECT entered `SWITCHED_PROTOCOL`; ordinary GET 200 remained `SEND_BODY`, and `h11.next_event()` consumed the buffered bytes as ordinary `Data`. Thus **nonempty `trailing_data` is insufficient to establish upgraded-stream ownership**. The relevant distinction is protocol-switch state, not buffer presence alone.

All 1,024 switched traces reconstructed the expected 31-byte payload; all 512 ordinary traces matched h11 body consumption. Three bounded observational ownership certificates were rendered as both typed IR and information-equivalent ordinary Python/AST mapping, with explicit UNKNOWN outside observed states. **18/18 tests passed**, including tamper detection. The complete raw traces, independent auditor, original cloud artifact, frozen prompts, source hashes and SHA-256 manifest are in local archive `lattice_run358_original_cloud_and_h11_boundary.zip`, SHA-256 `87c6ad63e6a9eb6b1745c7e71e6e3253793b77d747a99b4737bdc5f15eaa1680` (22 payloads).

The h11 0.16.0 traces are **postfreeze exploratory evidence** and cannot modify the original Docker oracle (h11 0.14.0), its ten cases or model prompts. No new independent production PR was qualified. All 89 reserved boundary issues remain sealed; sole PR #9 stays open/draft/unmerged.

Next: independently audit the original expanded-context cloud artifact; then qualify a new independently selected real two-production-source PR with prospectively frozen target-plus-control necessity.
