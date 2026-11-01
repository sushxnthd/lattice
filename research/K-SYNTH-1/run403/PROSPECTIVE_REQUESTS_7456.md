# K-SYNTH-1 Run403 — prospective issue-first freeze (2026-11-01 IST)

**Candidate:** psf/requests issue #7456, https://github.com/psf/requests/issues/7456. The issue describes `typing.get_type_hints` raising `NameError` on public classes after 2.34.0. This candidate was chosen from issue text before inspecting any reference fix. It is **not qualified**.

**Pinned base:** `psf/requests` release v2.34.0 commit `0b401c76b6e80a4eecf3c690085b2553f6e261ca`, independently resolved through the GitHub commit API. Frozen Git blob SHAs:
- `src/requests/models.py`: `4142f2a4bbf39820b46b414a15af805a34b1a013`
- `src/requests/cookies.py`: `2e3fc215095fad13817562bbaee871cba57eec08`
- `src/requests/sessions.py`: `8f13887d187deda256e08f305950a56a9c145ea5`
- `src/requests/api.py`: `eeb3b54d7f27e2c843080dfe81dfdb0d460c2b31`
- `src/requests/utils.py`: `120336ddc6ed5d802735685349c3c3cd42e0c597`
- `src/requests/compat.py`: `deab3c091fed207315c5af60fb415d7407a08b48`

**Frozen independent functional oracle (not reference-derived):** all cases run in fresh Python processes, with source pinned to this commit, no network traffic, `PYTHONPATH=src`, and timeout. Targets T1/T2/T3 require `typing.get_type_hints` on `requests.Response`, `requests.PreparedRequest`, and `requests.Request` respectively to return a dict without exception. Heldout H1/H2/H3 require the same for fresh subclasses of each respective public class. H4 requires all three original classes to work in reverse order within a single interpreter. The heldout tests are not to be used for model prompt selection. Baseline controls C1-C7: import requests, instantiate Response, construct Request('GET', 'https://example.invalid'), instantiate PreparedRequest, instantiate Session, instantiate RequestsCookieJar, and construct a CaseInsensitiveDict with one header. All controls must pass at baseline. Tests must be kept byte-for-byte unchanged once execution begins.

**Eligibility:** at least one target fails on base, full historical repair passes all targets/heldouts/controls, both separate production-source ablations exhibit behavioral necessity on frozen target-plus-control outcomes, and neutral interface shims cannot explain the coupling. Import failure alone does not count as behavioral necessity. If the historical fix edits only one production source or any other gate fails, label NOT QUALIFIED; do not retune. Source/PR relationship must be independently verified before reference comparison.

**Claim boundaries:** this is a *candidate* only, with no observed outcomes yet. No reference code has been inspected at protocol freeze. The 89 reserved boundary issues remain sealed. Primary matched IR vs AST experiment remains pending.
