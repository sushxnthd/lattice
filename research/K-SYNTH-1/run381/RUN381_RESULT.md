# K-SYNTH-1 Run381 — prospective HTTPcore #724 two-source API control

2026-10-31 UTC. Sole draft PR #9, branch `research/exp003-context-order`, all 89 reserved issues SEALED.

## Preregistration and original historical source

The exact prospective freeze was committed **before reference inspection** at `c23f19a22983ccb3bc4481fe62adabf54214e6d1`. Original frozen executable oracle SHA-256 `b5524eaed8dfaa3ff4b178b682909af5cfc09a52cfb99307c12377d78b625f2a`, Git blob `fdf2d2e928a0c7f1e4a383df0edc777d419d6745`. Historical base `eb5957d60b240a0deec503a4acca0e69da2833db`; sync Git blob `5cf43b298e6e8489bcb02d6f46ca897ddfae9afc`, async `23701808b55371dda50678641660bcee47e2b95e`. Public issue [#724](https://github.com/encode/httpcore/issues/724) was opened 2023-06-14.

The [original baseline workflow](https://github.com/sushxnthd/lattice/actions/runs/41168911514) succeeded on historical HTTPcore 0.17.2, Python 3.11.17, h2 4.4.1: **0/4 target checks passed, 8/8 nonregression controls passed**. Artifact ID `13030407179`, ZIP SHA-256 `de82ded63fe23deb77cc9c9a29a36644fe468213bb931054b60df4ddb96e3ce3`. The oracle uses actual in-memory hyper-h2 wire frames, with no monkeypatch of HTTPcore request handlers or external network.

After the freeze, the exact reference was identified as [upstream PR #729](https://github.com/encode/httpcore/pull/729), commit `aacdbb940d825987689f1798e5fa999a844da517` (2023-06-16). It changes only two production files, adding the network stream response extension in each. Reference blobs: sync `2e5fe4a3a2186bbeed88f2c5a5224aacdc3bbc55`, async `af7c5b8ca64913f28d193f8409df3824168d0c6d`.

## Original 2x2 factorial

[Successful workflow](https://github.com/sushxnthd/lattice/actions/runs/41169010417), original artifact ID `13030181811`, ZIP SHA-256 `7b7fcb811519e761a198592c6ba16b148664fa3f7d42b1a738977fef86852025`.

| Arm | Targets / 4 | Controls / 8 | All / 12 |
| --- | ---: | ---: | ---: |
| Base | 0 | 8 | 8 |
| Sync-only reference | 2 | 8 | 10 |
| Async-only reference | 2 | 8 | 10 |
| Full reference | 4 | 8 | **12** |

All **48 original factorial records plus 12 separate baseline records** passed an independent read-only auditor. All 12 casewise factorial interactions were **zero**, although the aggregate all-tests-pass interaction was **+1**. This is a second independent real-source demonstration that two-file aggregate necessity is not proof of semantic cross-file coupling. Twelve local integrity/adversarial tests passed. Modern installed HTTPcore 1.0.9 passed 12/12 as a separate smoke test.

## Scope and decision

All prospective *two-source functional qualification gates* passed. However, #724 is an **enhancement**, and the issue itself prelocalizes both files. Therefore this is a historical two-file **API parity control**, **not** a newly counted independent bug-repair/model-localization task. The primary qualified bug-repair cohort remains **10 PRs**. No new model inference or IR superiority is claimed.

Initial malformed workflow interpolations were preserved as failures and corrected; original frozen oracle was not changed. Full local SHA-verified archive contains original cloud ZIPs, raw observations, independent auditor and tests. Next run: recruit a truly unseen multi-source bug repair and perform strong-model IR versus information-equivalent AST trials with prospective coupling strata.
