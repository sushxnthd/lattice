# Run254 — real-upstream control recovery and prospective Qwen pilot

Date: 2026-10-26 IST. Branch: `research/exp003-context-order`; draft PR #9. **No semantic-IR superiority or capable-model repair result is claimed.**

## Independent Run253 failure audit

GitHub Actions run [40226877874](https://github.com/sushxnthd/lattice/actions/runs/40226877874) **failed before model inference**. Artifact ID `12612210541`, ZIP SHA256 `14f559659273727c17eca8eb815fbb3c8d8f7b129ece4b2268297f746f23613a`. Both real tasks were rejected by controls, zero completions.

- `python-humanize/humanize` PR #206: the pinned baseline **and reference** failed with `ModuleNotFoundError: humanize._version` from package initialization. The Run254 control imports the exact SHA-verified upstream `filesize.py` directly, avoiding the missing generated version module. **Independent local re-execution:** baseline public FAIL, baseline heldout FAIL, reference public PASS, reference heldout PASS (4 complete traces archived).
- `pypa/packaging` PR #1411: original baseline public FAIL, baseline heldout PASS, reference public PASS, reference heldout PASS. Run253 wrongly required baseline to fail heldout as well. A heldout non-regression check may pass before and after repair; requiring baseline-negative for *every* hidden check introduces task-selection bias. Revised prospective qualification: baseline fails a targeted public test for a non-environmental reason; reference passes public and heldout. Packaging must still be rerun against the full pinned upstream checkout.

## Run254 frozen comparison

SHA-pinned [deterministic protocol overlay](run254_overlay.py.zlib.b64) and [cloud workflow](../../../.github/workflows/lattice-k-synth-1-run254-real-paired.yml) committed. Corrected workflow commit `de98e18f3b691de370daa792207481b12c69b362`. Original Run253 runner and fixed-point CFG-v2 remain pinned; final runner SHA256 `fcdc3d101caae528cfbb820b6455d7085f7e1921691c5842af64d226095b15b4`. New workflow verifies source, overlay and final runner SHA before qualification, then verifies locally preregistered request hashes before model inference.

Both conditions display **identical unescaped Python source** and **identical canonical CFG facts**, with JSON vs Python-comment fact encoding. This tests formatting, **not** true semantic IR versus ordinary Python. Identical literal-patch compiler, editable paths, task information, and network-isolated oracles. Model Qwen2.5-Coder-7B-Instruct Q4_K_M, SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seeds 254001/254002, temperature 0, 1536 max output tokens, 24576 context. Pinned llama.cpp commit `620d2225cc436ab0b001e3200e590e3b286ef9ab`. Exact frozen request hashes and all raw prompts are in the local archive. Prompt token counts, raw model outputs and functional results **not yet observed**. Workflow push submitted; run status not confirmed.

Independent local validation: **6/6** protocol tests, **10/10** inherited strict patch-compiler tests; **4/4** exact prompt and fact-parity hashes.

## Genuine multi-source-edit candidate

Identified `pallets/flask` [PR #6096](https://github.com/pallets/flask/pull/6096), merged commit `05e9c6bd630ecf4ec0ec884b1fc7901663737bc7`. It edits **two production files** (`src/flask/app.py`, `src/flask/testing.py`) for IPv6 host parsing and session-cookie handling. Public and heldout test candidates recorded in the archive. **Not qualified yet**, and excluded from Run254 inference.

## Limits and persistence

Run254 has at most two single-editable-source tasks. It cannot support significance or a mechanism claim. Previous power planning: independent McNemar n=306 under optimistic q=.30,p=.65, n=681 at q=.30,p=.60, larger when clustered. The 89 sealed boundary issues remain untouched.

Complete local reproducibility ZIP `/mnt/data/lattice_run254/lattice_run254_control_recovery_and_paired_launch.zip`, SHA256 `92abf3828e7b505f09f605508bdc5aedb213629bd88fc74463b1b26b2966ae42`, **36 SHA-verified entries**. The ZIP and full independent auditor are local, not fully mirrored to GitHub. Preserve and retry persistence; do not pause hourly science for integration failures.
