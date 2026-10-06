# Structured Topology Control v1 — Preregistration

Status: FROZEN BEFORE MODEL EXECUTION.
Classification: DISCRIMINATION.

## Evidence motivating this test
Equal-budget violation-normal beat strong prose on a fresh holdout, but a subsequent fresh polarity control reversed violation-normal vs positive-normal. Therefore violation polarity is falsified as the privileged mechanism. The surviving hypothesis is that explicit action-partitioned semantic topology, independent of positive/negative polarity, improves fixed-model code generation relative to ordinary prose.

## Fixed model / decoding
Qwen/Qwen2.5-Coder-1.5B-Instruct. Greedy decoding, do_sample=false, max_new_tokens=220. Fixed apply_change signature. No retraining.

## Conditions
1. strong_prose — complete ordinary prose specifying every valid action, invalid action class, transition, permission, metric constraint, and preservation behavior.
2. neutral_partition — polarity-neutral action table: each action is a record with applicability domain, state/actor/value guard, state effect, metric effect, and accepted boolean; unknown actions map to a default record. Do not phrase rules as violations or as "accept iff".

Both conditions must encode the same facts. Complete chat-formatted prompt token counts must differ by <=5% on every domain. Abort before model loading/generation otherwise.

## Fresh development domains
Node: dormant -> serving; operator; guest
Message: queued -> delivered; courier; viewer
Contract: proposed -> signed; signer; reader
Batch: assembled -> processed; technician; visitor
Workspace: private -> shared; owner; guest
Alert: raised -> acknowledged; responder; observer

## Fresh sealed holdout
Token: issued -> activated; issuer; visitor
Entry: pending -> posted; clerk; reader
Module: disabled -> enabled; maintainer; guest
Shipment: packed -> dispatched; dispatcher; viewer
Certificate: requested -> granted; authority; observer
Task: waiting -> started; executor; guest

Holdout is spent forever after first model generation.

## Hidden tests
Exactly 12 per domain: valid advance; advance from destination; advance from unrelated state; rewind; privileged write; named outsider write; unnamed third actor write; positive metric; zero metric; negative metric; drop_protection; unknown action. Rejections must preserve state and metric.

## Metrics
Hidden tests passed/total; perfect programs; mean input tokens; paired per-domain score differences; per-test error categories. Preserve raw output.

## Decision rule
Development selects between strong_prose and neutral_partition by accuracy, then perfect programs, then fewer tokens. Primary hypothesis requires neutral_partition to be selected on development AND to beat strong_prose by >=10 percentage points on fresh holdout. <=0 holdout delta is FAIL; >0 and <10 pp is INCONCLUSIVE. A PASS supports a structured-topology foothold only, not a breakthrough.

## Claim boundary
This experiment does not establish novelty, cross-model transfer, repository-level SWE performance, or a new programming language. No outcome-dependent wording changes are permitted after any model output exists.
