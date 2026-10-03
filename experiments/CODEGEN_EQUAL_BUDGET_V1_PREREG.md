# CODEGEN-EQUAL-BUDGET-v1 preregistration

Status: FROZEN BEFORE MODEL EXECUTION.

Parent evidence: Qwen2.5-Coder-1.5B prospective code-generation gate at commit 8cd157023f707dde9e9ed317ccbaa94b89077f34. That result selected violation-normal on development and scored 85% on its fresh holdout versus 55% prose. The prior holdout is spent and MUST NOT be reused as fresh evidence.

## Hypothesis
With model, semantic information, decoding, and prompt budget held fixed, violation-normal organization improves hidden functional-test performance over a strong prose specification on unseen domains.

## Fixed model and decoding
- Model: Qwen/Qwen2.5-Coder-1.5B-Instruct
- Greedy decoding; do_sample=false
- max_new_tokens=220
- Same function signature and evaluator for both conditions.

## Conditions
Only two conditions are tested:
1. strong_prose: explicit iff/exactly-when prose stating every permission, rejection condition, state mutation, and rejection-preserves-state rule.
2. violation_normal: the same facts organized as violation predicates followed by accepted-state updates.

No weaker explicit-NL or decision-table condition is included.

## Equal-information / token-budget gate
Before any generation, tokenize both complete chat-formatted prompts for every domain. The run MUST abort before generation if relative prompt-token gap exceeds 5% for any domain. The prose condition may be edited only before the first model execution to satisfy this gate; after any model output exists, wording is frozen. No outcome-dependent padding or editing is allowed.

## Frozen development domains
Account: pending -> active; administrator privileged; visitor outsider.
Build: created -> verified; engineer privileged; guest outsider.
Report: draft -> approved; reviewer privileged; reader outsider.
Device: offline -> online; operator privileged; observer outsider.
Experiment: planned -> running; scientist privileged; viewer outsider.
Package: staged -> released; maintainer privileged; guest outsider.

## Frozen fresh holdout domains
Review: requested -> completed; moderator privileged; viewer outsider.
Deployment: prepared -> live; deployer privileged; guest outsider.
Profile: new -> verified; owner privileged; visitor outsider.
Archive: open -> sealed; curator privileged; reader outsider.
Workflow: idle -> executing; operator privileged; observer outsider.
Record: draft -> final; editor privileged; guest outsider.

These holdout domains are sealed for this experiment. Once any result from them is observed, they are spent forever.

## Hidden tests per domain
Exactly 12 deterministic cases:
1. valid advance from source state.
2. advance from destination state rejected.
3. advance from an unrelated state rejected.
4. rewind rejected.
5. privileged write accepted.
6. named outsider write rejected.
7. a third, unnamed actor write rejected.
8. positive metric accepted and applied.
9. zero metric accepted and applied.
10. negative metric rejected with no mutation.
11. drop_protection rejected with no mutation.
12. unknown action rejected with no mutation.

## Primary metrics
- hidden tests passed / total
- perfect-program count
- mean prompt tokens
- paired per-domain score difference

Selection is performed on development only. Holdout is opened once for the development-selected condition and the prespecified prose baseline.

## Interpretation
PASS candidate effect: development selects violation-normal AND fresh holdout advantage over strong prose is >=10 percentage points, with token-gap gate satisfied.
FAIL: development does not select violation-normal OR fresh holdout advantage is <=0.
INCONCLUSIVE: holdout advantage is >0 but <10 points, or execution/evidence integrity fails.

Even PASS is not a Lattice breakthrough. It only warrants independent evaluator reimplementation and a fresh repository-evolution gate.

## Hygiene
Preserve raw outputs, exact commit, environment, token counts, model revision if available, artifact digest, and workflow run. No tuning from holdout. No rerun may be labeled fresh.
