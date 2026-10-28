# Run305 sixth-issue candidate screen (NOT QUALIFIED)

Candidate: [python-hyper/wsproto PR #6](https://github.com/python-hyper/wsproto/pull/6), **Better handshake header parsing**, merged 2017-05-03. This is a new public repository distinct from the five qualified tasks.

- Historical base is **first parent** of merge commit: `7314c8428a2d02625828e5a705529b2e2fe1ac21`.
- Full merged reference: `99aeafa3f188d5fb4563d4e9543e8cd8892a793d`.
- Two substantive production files changed: `wsproto/connection.py` and `wsproto/events.py`.
- Main interaction: `connection.py` parses proposed subprotocols and passes them into the new `ConnectionRequested(proposed_subprotocols, h11request)` event constructor in `events.py`. Both components appear functionally relevant; this is a hypothesis, **not** an ablation result.
- Historical `setup.py` requires `h11 ~= 0.7.0`; the original environment is old and must be isolated/pinned. The PR changed no tests. Do not silently use modern wsproto or h11 as the oracle.
- Prospective oracle design to freeze **before executing**: client/server subprotocol negotiation targets (single/multiple proposed protocols, valid selection, invalid selection), independent malformed-header and extension-handshake controls, full reference, base, connection-only and events-only ablations. Demand joint target-plus-control necessity, no new control regressions, source SHA checks, heldout cases and isolated no-network execution.
- Qualification decision remains **PENDING / NOT QUALIFIED**. Do not count this as a sixth issue without the complete frozen oracle and ablations. If historical dependencies cannot be reproduced, preserve the failure and move to another independent PR.
- No reference-derived localization may enter model prompts. The reference diff is allowed only for candidate qualification and gold expressibility, not model task facts.

All 89 reserved boundary issues remain SEALED. Use existing K-SYNTH-1 branch and draft PR #9 only.
