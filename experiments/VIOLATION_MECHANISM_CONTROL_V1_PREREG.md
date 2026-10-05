# Violation Mechanism Control v1 — Preregistration

Status: FROZEN BEFORE MODEL EXECUTION.

Classification: DISCRIMINATION.

## Question
Does the replicated violation-normal advantage arise from the negative/violation decomposition itself, rather than merely explicit structured/formal organization?

## Fixed model and evaluator
Qwen/Qwen2.5-Coder-1.5B-Instruct; greedy decoding; max_new_tokens=220; same apply_change signature, hidden-test semantics, extraction and subprocess evaluator as CODEGEN_EQUAL_BUDGET_V1.

## Conditions
1. violation_normal: the already-tested violation predicate organization.
2. positive_normal: semantically equivalent structured rules organized around acceptance predicates and accepted transitions, with rejection as the complement. It must state the same action/state/actor/value facts and preserve-on-reject semantics.

No prose condition is needed for the primary causal contrast because the prior equal-budget experiment already established violation_normal > strong_prose on a fresh holdout.

## Fresh domains
Development: Session(new,ready,controller,guest); Ticket(open,resolved,agent,viewer); Dataset(raw,validated,steward,reader); Job(queued,running,scheduler,guest); Document(draft,published,publisher,viewer); Vault(locked,unlocked,custodian,visitor).

Fresh holdout, sealed until execution: Channel(closed,open,moderator,viewer); Snapshot(pending,committed,operator,guest); Case(unreviewed,reviewed,auditor,reader); Queue(paused,active,dispatcher,observer); Asset(staged,deployed,manager,visitor); Request(created,approved,approver,guest).

## Token/information gate
Before model loading/generation, tokenize complete chat-formatted prompts for both conditions on every domain. Abort before generation if relative token gap exceeds 5%. Only semantically equivalent pre-generation wording correction is permitted to satisfy this gate; after any model output exists, wording is frozen.

## Hidden tests
Exactly the same 12 semantic tests per domain as the frozen equal-budget evaluator: valid/invalid advance, rewind, privileged/outsider/third-actor writes, positive/zero/negative metric, drop_protection, unknown action.

## Metrics
Hidden tests passed/total, perfect-program count, mean prompt tokens, paired per-domain difference. Preserve raw outputs and per-test errors.

## Decision
Primary causal prediction: violation_normal must beat positive_normal on development and retain >=10 percentage-point advantage on fresh holdout to support a violation-specific mechanism. <=0 holdout advantage falsifies violation-specific superiority. >0 but <10 pp is inconclusive.

Even a PASS is not a Lattice breakthrough; it warrants independent evaluator reimplementation and cross-model replication.
