# K-SYNTH-1 Run297: prospective independent h11 PR115 qualification freeze

Frozen before any base/reference/ablation functional oracle execution. 2026-10-27 UTC.

**Candidate:** python-hyper/h11 PR #115 (merged 2020-12-26); independent of previously tested Flask, urllib3, Werkzeug, HTTPcore, Click issues. Selected after examining upstream PR diff, so this is **not** a gold-blind model task.

**Exact base:** `522b00470b5776dda2dc7e98ff778eb1e418e6ad`.
**Exact head:** `a1197d68630bc37a941b516c7cc74833460fc97c`.

| Production file | base Git blob SHA1 | head Git blob SHA1 |
|---|---|---|
| h11/_connection.py | 410c4e91a04587d4c7254cc5d439b36ce37393f8 | c4baa80e64bf828eb8c7e63c5401653889d31842 |
| h11/_readers.py | cc86bffb5b36fb019a0bcb53e34d3e439f13f932 | bafc00a23afc2cb6e610446b9326936e6e44c803 |
| h11/_receivebuffer.py | c56749a3a80733d89b6279dc4af7de94cdbea24d | b32f20ea38136e47f834caf39fe5464f7b804d2e |

**Frozen independent public API oracle:** instantiate `h11.Connection(h11.SERVER)`; feed specified byte chunks with `receive_data`, collect `next_event` until `NEED_DATA` or `EndOfMessage`. Compare event type sequences, Request method/target, expected normalized headers and body bytes; record all exceptions. No upstream test cases, private APIs, or model code in oracle.

**Public targets:** T1 simple GET with LF-only delimiters; T2 GET with LF-only and two headers; T3 mixed CRLF request-line delimiter and LF header/blank delimiters. **Heldout targets:** T4 POST with LF-only delimiters and Content-Length 3 body `abc`; T5 LF-only GET split across three `receive_data` calls. Expected successful Request then optional Data then EndOfMessage, with exact body and headers.

**Nonregression controls:** C1 CRLF GET; C2 CRLF GET with two headers; C3 CRLF POST with Content-Length 3 body; C4 CRLF POST with Transfer-Encoding chunked and body `abc`; C5 CRLF GET split across three receive calls. Expected successful Request, optional Data, EndOfMessage. All control outcomes must be correct on baseline and full reference. All 10 expected successful outcomes are frozen *without executing either source version*.

**Configurations:** base, full reference, and three leave-one-production-file-out reference ablations. Qualification requires: (i) base passes every control and fails at least one target; (ii) full reference passes **all targets and controls**; (iii) every leave-one-out ablation fails at least one combined target/control; (iv) every source file matches pinned Git blob SHA1; (v) isolated interpreter, no model code executed. Any deviation is **FAILED**, without relabeling cases or retrying criteria. Runtime/compatibility errors are recorded as failures. No posthoc changes to the frozen oracle.

**Scope and limitations:** A single historical PR is not an independent blind coding-model success. A passing qualification would add one eligible repository task, not model evidence or superiority. The 89 reserved boundary issues remain SEALED. Keep one K-SYNTH-1 kernel, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9.