# Run622 — prospective candidate oracle contract (not executed)

Candidate: [Werkzeug PR #3335](https://github.com/pallets/werkzeug/pull/3335), “modify headers and body in place.” This run defines six distinct prospective behavior assertions: target 205 body/header removal, 304 body suppression, HEAD body suppression; controls GET 200 payload retention and 204 empty body; heldout 205 alternate payload. These are **proposed**, not verified outcomes, and the candidate remains **NOT_QUALIFIED**. No source SHAs have been independently pinned in this run. No component-necessity result is claimed.

The executable local freeze validator passed 6 unique IDs and 6 required gates. Canonical JSON SHA256: `3feb2b3ba2f1dc124a453b4ca3aebe6acf59bdd72e5ecb6b6d2963b7b0c04a11`. Local archive SHA256: `c962c7f9635cbef58655d8a863422261b2662b6204818a86010aa2de5ab0d9ba`. The archive contains the executable, JSON, stdout and checksum list. Full raw artifact GitHub mirroring remains outstanding.

**Next:** pin base/ref SHA, independently verify API assertions and test in isolated oracle against baseline, reference and each component ablation. Do not count this candidate as qualified before all joint target/control gates and target-specific necessity are satisfied. Two real qualified tasks remain. No model inference or IR superiority claim. All 89 sealed issues untouched.
