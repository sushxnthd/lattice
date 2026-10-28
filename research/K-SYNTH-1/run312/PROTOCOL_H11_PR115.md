# K-SYNTH-1 Run312 prospective qualification: python-hyper/h11 PR #115

Frozen **before executing the new qualification oracle**. This candidate is NOT qualified at registration.

Upstream: https://github.com/python-hyper/h11/pull/115
Historical base `522b00470b5776dda2dc7e98ff778eb1e418e6ad`; PR head `a1197d68630bc37a941b516c7cc74833460fc97c`; recorded merge `c88da54f3fe10a4a5d3f1e15b761024b0d8cf730`. Clone source from upstream in isolated GitHub Actions; assert exact commit object IDs and SHA256 each of the three production files for each arm. Python 3.9, no model-generated code.

Arms: BASE all historical base files; A = reference `h11/_receivebuffer.py` and `h11/_connection.py` only; B = reference `h11/_readers.py` only; FULL = all three reference production files. Source changes are not invented or retuned. Run each arm in a separate Python process with isolated import path. Raw events, exceptions, source hashes, runtime versions and case results are preserved.

Frozen public targets: T1 LF-only headers Content-Length 0; T2 LF-only headers Content-Length 3; T3 mixed response-line CRLF and header LF; T4 mixed response-line LF and header CRLF; T5 LF-only headers split across three receive_data chunks; T6 mixed LF/CRLF headers with Content-Length 3. Expected parsed Response, complete body and EndOfMessage. Frozen controls: C1 CRLF Content-Length 0; C2 CRLF Content-Length 3; C3 CRLF chunked body; C4 CRLF chunked body fragmented at delimiter; C5 CRLF with extra header; C6 CRLF 204 No Content. All controls must retain successful baseline behavior.

Qualification gate: BASE must fail >=4/6 targets and pass all 6 controls. FULL must pass all 6 targets and all 6 controls. A-only and B-only must each fail at least one case from the **joint 12-case target-plus-control set** that FULL passes, and each changed production component must have a demonstrated causal role. For the A grouping, the `_connection.py` removal of `compress()` must also be necessary for full reference operation. A failure or environmental incompatibility means NOT QUALIFIED; no post-outcome criteria changes. Record full 2x2 matrix and explain any interaction. This is a qualification of an historical repair, not a model repair success or IR advantage.

Isolation: upstream public code is executed only in disposable GitHub Actions runner. No untrusted model code on host. All 89 reserved issues remain sealed. Continue science even if CI/GitHub integration fails; do not mark unverified outcomes successful.
