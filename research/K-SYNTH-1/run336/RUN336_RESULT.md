# K-SYNTH-1 Run336: original Run335 recovery and rule-baseline falsifier

2026-10-29 UTC. Canonical branch `research/exp003-context-order`; one OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues SEALED.

## Original Run335 genuine model evidence

[Actions 40831990253](https://github.com/sushxnthd/lattice/actions/runs/40831990253) COMPLETED SUCCESS. Original artifact 12880171099 ZIP SHA-256 `7c32afb0a49bc206684c9708b1777192524c6e990e6d99f4c9341de5c859f7d0`. Independently audited **44/44** manifest entries, all **31** original AST candidate slots and source SHA preconditions, and **27** recorded isolated functional oracle cases, zero discrepancies. Both genuine Qwen2.5-Coder-7B gates passed. Both real completions finished normally (46 tokens each) and were **byte-identical**, choosing only `httpx/_api.py:head allow_redirects=False -> True`. Both original shared-compiler transactions were accepted. Baseline **0/3 targets + 6/6 controls**; both IR and Python/AST **1/3 targets + 6/6 controls**. Neither completed the repair. No model outputs were corrected or rescored. Run335's identical minimal-delta suffix eliminated Run333 IR truncation, not the one-edit selection failure.

## Retrospective deterministic baseline: a difficulty warning

A new independent, issue-conditioned Python/AST selector uses the original pre-fix issue's stated HEAD default inconsistency and the **same 31 frozen authorized source-derived candidates**. It selects the three `head` entries with `allow_redirects=False` and rewrites them to `True` across `httpx/_api.py` and `httpx/_client.py`. All 31 source hashes and actual AST default slots were independently verified; all nonselected slots remained unchanged. The two patched source SHA-256 values exactly match the previously executed trusted Run329 three-edit patch: `81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe` and `97f9ba016b14033c347a398444662e795e02e0118729d67ecbfbfa0192a0bd60`. Run329's frozen isolated oracle gave **3/3 targets + 6/6 controls** on these exact bytes.

**Crucial limitation:** This is a *retrospective post-outcome rule*, NOT a preregistered baseline, NOT new model inference, and NOT a newly executed oracle. The exact source-hash equivalence links it to previously recorded Run329 functional evidence. It demonstrates that two-file functional necessity does not imply semantic-IR representation necessity, and that this particular issue/candidate presentation is easy for a specialized deterministic selector. It does not establish general repair ability.

Five adversarial selector tests passed. Five recomputed-manifest/source mutation audits were rejected. The first auditor iteration missed a tampered nonselected candidate hash; the corrected auditor checks **every** candidate's source SHA and actual AST slot. Preserve that initial audit weakness, do not rewrite original evidence.

## Reproducibility and next direction

Local full original-evidence archive: `lattice_run336_original_model_and_rule_baseline_falsifier.zip`, SHA-256 `d26de3aa304ce41abe42ebba17482067983543b6e4bc8ca5cdb25e7cd41bb42f`. Contains original Run335 artifact, prior Run329 trusted evidence, full independent read-only replay, adversarial tests, original model responses, oracle traces and 9-entry local manifest. GitHub does not yet mirror this ZIP.

Stop optimizing HTTPX-specific prompts as a proxy for science. Next study must prospectively include an issue-only deterministic ordinary Python baseline, semantic IR, matched Python/AST actions and a source-only ablation; recruit additional independent repositories and freeze oracles before reference inspection. Include easy tasks rather than filtering post-outcome; preregister a separate hard stratum. McNemar iid planning remains n306 optimistic / n681 moderate, larger with clustering. Three qualified historical tasks remain Flask PR6096, urllib3 PR5071, HTTPX PR1183. No powered superiority, general soundness, or breakthrough claim.
