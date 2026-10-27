# Run302 fixture freeze, before execution

- Preregistered protocol commit: `2aee2823dfefe16de6987a7283aae19e150af9a0`.
- Deterministic generator: `run302_experiment.py` local SHA-256 `39d5a4ec85397d9a767b595702e4efadd1040b62e4f7850d7384d4ecdf1a93f7`.
- Full frozen 512-case manifest (8 families x 16 variants x 4 fragmentations) SHA-256: `efca87263ce57d6116599772b9c769df1d11c5a3ede0b02ebaaa956e738b2f1b`.
- Trusted historical h11 source hashes: _readers.py `05c760d59ecfb456d30075c053e2a65559d7c3260f7902339949f98dd6f18777`; _connection.py `0891e53f7351b696494aac1ec6586f78d7c389e4760ed647f5990b6543ab975f`; _receivebuffer.py `8719682225b96f983f71d6c50333f0fadbfa6292a70c8b0de33d45516968a5c8`; _abnf.py `b4c2aa80e1244c71e9f2c3ddfe0994f50a307bfc975eb8a172deb7457db326c8`.
- Primary frozen predictions: CRLF_VALID and CRLF_EXTRA_VALID succeed, all other families do not. No candidate model code on host. Additional request-line strip-LF counterfactual is diagnostic only.
- This fixture freeze is not a qualification of a new repair task and does not change original Run301 outcomes.
