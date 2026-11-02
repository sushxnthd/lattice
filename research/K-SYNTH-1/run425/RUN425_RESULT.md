# K-SYNTH-1 Run425 — exact historical replay and factorial identifiability

**2026-11-02 UTC. Post-reference diagnostic only; no new qualified repair or model inference.**

## Original exact-source replay

Run424's historical GitHub workflow had failed because its evidence directory was created *after* a checksum redirection. The ordering was corrected without changing the oracle. Previous failures [41364066116](https://github.com/sushxnthd/lattice/actions/runs/41364066116) and [41364159129](https://github.com/sushxnthd/lattice/actions/runs/41364159129) remain recorded. Corrected [run 41368162492](https://github.com/sushxnthd/lattice/actions/runs/41368162492) completed **successfully**, artifact ID **13107893189**, ZIP SHA-256 `0a4b713c93b7aea332137ca1f351d31008f72bd78291e938e22519588bf056eb`. All five original artifact SHA entries independently verified.

Upstream urllib3 PR5071 merge `f5cf122346141b187cca0db6e6445297d336b610`; first parent `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305`. The workflow checked three exact historical base Git blobs, full three-file byte-identical reference reproduction, a neutral generated-version import shim and imported-module path isolation. Eight factorial source variants generated **560 real Python API observations**.

**Original frozen qualification gate FAILED:** full reference passed 10/10 positive port-zero targets but preserved only 58/60 original nonregression controls. The changed controls were `samehost_http_80` and `samehost_https_443`. No post-hoc relabeling. The independent Run424 installed urllib3 2.7.0 matrix matched all **560/560** exact historical API outcomes.

## New finite-oracle structure result

An independent read-only audit found that of 70 observations, 60 were constant, 2 depended only on `connectionpool.py`, 6 only on `poolmanager.py`, and 2 only on `util/url.py`. **Zero observations exhibited multi-file factorial interaction.** Exhaustive enumeration of all one- and two-observation subsets proves that **three rows are necessary** to distinguish all eight variants; the three post-outcome witnesses `samehost_http_80`, `proxy_http_0`, `netloc_http_0` suffice. This separates joint necessity for a conjunction of independent behaviors from a mechanistic interaction; the witness suite is not a prospective qualification oracle.

## Frozen out-of-matrix challenge

Before executing a new extension, froze manifest SHA-256 `a45d8ecbc37aa5fb5037218d923c35deb9b680034354077c507f8e65b17a7f98` and prediction: every observation remains constant or unary in source-file flags. Using archived installed urllib3 2.7.0 (not historical base), tested **4 hosts × 2 schemes × 16 ports × 5 API observations × 8 variants = 5,120 isolated CPython observations**. Independent read-only audit: 600 constant, 8 connectionpool-only, 24 poolmanager-only, 8 util/url-only, **0 interactions**. This is post-reference exploratory prediction, not unseen issue validation.

Local reproducibility: complete original GitHub artifact, exact and installed raw matrices, source snapshot/license, independent 70-row auditor, 12/12 adversarial tests, frozen 128-case manifest, 5,120-observation raw matrix, independent extension auditor and SHA-256 manifest. Complete archive retained locally.

**Status:** two independently qualified real multi-source repairs; zero new coding-model completions, no powered superiority evidence and no breakthrough. All 89 reserved issues untouched. Previous historical GitHub ZIP mirroring remains incomplete.

Next: a genuinely new issue-first, prospectively frozen two-source public-repo repair with positive/negative controls and joint target-plus-control necessity; full equal-authority editor expressibility; then matched functional open-model inference and independent evaluation.