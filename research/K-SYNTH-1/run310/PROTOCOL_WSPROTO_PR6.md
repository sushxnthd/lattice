# Run310 wsproto PR #6 independent historical repair qualification: prospective freeze

This is a **separate** prospective qualification experiment, registered before any isolated oracle execution. It does not alter the earlier annotation-counterexample primary endpoint.

## Source and environment

- Upstream [python-hyper/wsproto PR #6](https://github.com/python-hyper/wsproto/pull/6).
- Historical merge commit: `99aeafa3f188d5fb4563d4e9543e8cd8892a793d`.
- Historical baseline: first merge parent `7314c8428a2d02625828e5a705529b2e2fe1ac21`; second parent `97b9e99d43a727ec6d2d80230a84067965f14f89`.
- Two production files only: `wsproto/connection.py` (base blob `0908d7035ba723656f89e42e38dd80d036d1a7b0`, reference `f2903f31ee867ebb7ea0762337c2ff7375848e67`); `wsproto/events.py` (base `b88912ae2e333285a275a3f21ef2519041af5194`, reference `a9646fad71061178d6078fb1ece121273f97bf9d`).
- Oracle file `run310_wsproto_qualification.py` committed **before experiment** in `0426f195319dccd13312db89fcdf8c80da2547a6`; Git blob SHA `47fb9529024bd79597d0a7415556c8400c37dc4b`.
- Isolated GitHub Actions Ubuntu runner, Python 3.8, pinned `h11==0.7.0`; no user machine, no secrets, no untrusted model-generated code.

## Frozen four-arm factorial

1. `baseline`: baseline connection + baseline events.
2. `connection_only`: reference connection + baseline events.
3. `events_only`: baseline connection + reference events.
4. `reference`: reference connection + reference events.

Each arm uses identical independent public API oracle and dependencies. Each source blob must pass exact Git object SHA verification before executing. No edit to the historical source beyond selecting these two pinned files.

## Frozen tests and qualification criteria

Public targets (3): single proposed subprotocol; repeated proposed-subprotocol headers; accepting a selected subprotocol.
Heldout targets (2): reject an unoffered subprotocol; select the second of two proposals.
Nonregression controls (6): no-subprotocol request; default accept response; invalid Connection header; invalid Upgrade header; missing version; wrong request method.

**Qualify only if** the original baseline fails at least one target but passes **all six controls**; the full reference passes **all five targets and all six controls**; and **each** one-component ablation fails at least one target **and** at least one control. Any environment/import failure, missing evidence, source-hash mismatch or ambiguous behavior is a **NOT QUALIFIED / INCONCLUSIVE** result, never an inferred success. Do not change tests, source commits, dependency version or criteria after seeing results.

The 11 test cases are correlated and are not independent real repairs. This would be a single qualified task at most. Preserve all four raw JSON traces, exact runtime versions, source hashes, failure logs and original workflow artifacts.
