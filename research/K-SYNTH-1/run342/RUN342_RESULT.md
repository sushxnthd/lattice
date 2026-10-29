# K-SYNTH-1 Run342: original h11 response holdout FAILED; ABI-only counterfactual removes apparent interaction

**2026-10-29 UTC.** Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole OPEN/DRAFT/UNMERGED PR #9. All 89 reserved issues SEALED.

## Freeze and historical collision

Independent client-side response parser oracle for [python-hyper/h11 PR115](https://github.com/python-hyper/h11/pull/115) was frozen **before reference inspection** in [FROZEN_PROTOCOL.md](FROZEN_PROTOCOL.md), commit `51bd01d3faf40a6f995683d9dbda8db5fab28cbc`. Exact oracle [run342_h11_oracle.py](run342_h11_oracle.py), commit `96076e5e60c71eb655c46624e03da4b04120839f`, SHA256 `a483111fe5e84ed1dca4b92b1055164774314b10b6341e9d5539ff359dbfdd3b`. Base `522b00470b5776dda2dc7e98ff778eb1e418e6ad`, ref `a1197d68630bc37a941b516c7cc74833460fc97c`, 4 LF response targets + 6 CRLF/error controls. Source group A: `_receivebuffer.py`; B: `_readers.py` + `_connection.py`.

After freezing, history reconciliation found **the same PR had already qualified in Run297** using a different server-side *request* oracle. [CANDIDATE_COLLISION.md](CANDIDATE_COLLISION.md) was committed before historical execution. **Run342 is NOT a new independent repository/task qualification**, regardless of outcome. Run297's historical qualification and Run340/341's four-repository summary require ledger reconciliation; do not double-count or silently erase h11.

## Original frozen cloud results

Original [Actions 40884219720](https://github.com/sushxnthd/lattice/actions/runs/40884219720) failed before functional testing because one expected Git blob SHA had a missing final hex character. Preserved artifact `12901352294`, ZIP SHA256 `30a628c2e353967af5ed486688bdbafd5c54bb13d39b04ca0c8f5c8006236c6e`; [failure ledger](ORIGINAL_INFRA_FAILURE.md). A deterministic one-character correction to runner only, SHA256 `438f559a59529210a682ae273457e04b1b0b7bb9bb7dec999a08652ed60cc85a`, left the frozen oracle and all scientific criteria unchanged.

Corrected [Actions 40884439253](https://github.com/sushxnthd/lattice/actions/runs/40884439253) **SUCCESS**; original artifact `12900704804`, ZIP SHA256 `014aaacfebc94d4325aadbeed46a51de856460d4c2a0faf19baf379ced72b890`. Five isolated Python 3.10 arms produced **50 original public-API functional records**. Independent read-only auditor verified **23/23 original evidence-manifest entries**, all frozen inputs, exact outputs, arm provenance, outcomes and decision.

| Original frozen configuration | LF targets | Controls |
|---|---:|---:|
| Base | 0/4 | 6/6 |
| A-only reference buffer | 0/4 | 2/6 |
| B-only reference readers+connection | 0/4 | 5/6 |
| Full reference | 4/4 | 6/6 |
| Identity ABI negative control | 0/4 | 6/6 |

**FROZEN QUALIFICATION: FAILED** because both single-component arms regress controls and interfaces drift. Original per-case factorial interactions nonzero in **8/10 cases**, total absolute interaction **9**; these are not semantic mechanism proofs.

## New executed ABI-only falsifier

Original A-only arm failed on `ReceiveBuffer.compress` (removed by the ref buffer); B-only failed the chunked CRLF control on `ReceiveBuffer.maybe_extract_next_line` (absent from base buffer). Before running counterfactuals, froze the diagnostic adapter plan in [ABI_COUNTERFACTUAL_PROTOCOL.md](ABI_COUNTERFACTUAL_PROTOCOL.md), commit `2186978f8976af5ae6cfeba0c014ef8fa6fb70b6`. A shim restores `compress` as no-op (new buffer already consumes bytes) and aliases the old CRLF-only extraction call to the new method; B shim aliases the new method to the old CRLF extractor. **No LF parser semantics were added by either shim.**

Local historical Python 3.13 execution exactly reproduced **40/40** original Python 3.10 cloud arm/case event sequences and outcome bits. A seeded differential check found **0 discrepancies in 4,096 append/extract traces and 32,070 operations** for CRLF extraction. Separately labelled post-outcome results:

| ABI-corrected arm | LF targets | Controls |
|---|---:|---:|
| A-only + compatibility | **4/4** | **6/6** |
| B-only + compatibility | **0/4** | **6/6** |

Using corrected arms, **all 10 casewise factorial contrasts become zero** (original 8 nonzero; sum absolute 9 → 0). Thus the apparent multi-file interaction is an **ABI compatibility artifact on this finite oracle**, not evidence that three files independently implement the LF semantic fix. This is a **post-outcome mechanistic counterexample, NOT a rescue of original qualification**, and not a global equivalence proof.

Executable [casewise causal gate](run342_abi_causal_gate.py) committed and Git blob SHA1 `a607b430828d80adbff81583e10e9d393fbcc369`. Full local reproducibility ZIP contains original cloud artifact, original failure artifact, original SHA-pinned runner, raw counterfactual traces, independent auditor, tests and manifests; **28/28 SHA-256 payloads verified**, archive SHA256 `5443d6f16e9722f77a99e12b97acc43c219142df5f8381fe93cefd941e71c188`. Three local audit tests and 13 adversarial evidence mutations passed; an initial ABI-flag blind spot was fixed before final audit.

**No new coding-model inference, no powered IR-vs-Python advantage, no new independent repository, no breakthrough.** Next: audit unique historical PR IDs, sample a genuinely new repository, preregister ABI-normalized factorial plus public/heldout/control oracle, then run matched model arms. All 89 reserved issues remain sealed.
