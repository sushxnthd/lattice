# Run483: exact 37.5% false-positive counterexample for issue-level McNemar
Date: 2026-11-04 UTC. Kernel K-SYNTH-1. Branch research/exp003-context-order. All 89 reserved issues remain sealed.

## Claim and construction
Five independent repositories each contribute three perfectly correlated discordant repair comparisons. Under the sharp null, each repository independently chooses whether all three comparisons favor IR or all three favor Python, with probability 1/2. There are 2^5=32 equiprobable assignments. Issue-level McNemar wrongly treats the 15 comparisons as independent; a repository sign-flip test uses five independent signs. Both tests are exact two-sided binomial tail tests at alpha=.05.

## Exhaustive result
Issue-level McNemar rejects for 12/32 assignments, **37.5% type-I error** under this constructed null. It rejects for zero or one repository against the majority (or the symmetric case): 15:0 gives p=0.00006103515625 and 12:3 gives p=0.03515625. Repository sign-flip rejects 0/32 assignments: even 5:0 has p=0.0625. The null is explicitly synthetic; this is not a measured repository correlation, an empirical estimate of Lattice performance, or a general claim about cluster tests.

## Reproduce
Run `node run483_exact_cluster_null.js`. It enumerates all 32 assignments, outputs every raw row as JSON and asserts 12 issue-level false rejections and zero cluster-level rejections. No untrusted model code, external dependency, GitHub Actions or reserved benchmark issue is used.

## Interpretation
Run482 showed 12.5% with four repositories and two comparisons each. This independent five-by-three construction shows 37.5%, a stronger finite-sample failure. Prospectively preregister repository-level inference and obtain enough independent repositories; do not apply naive issue-level McNemar to clustered outcomes. This does not qualify a new real production repair or establish semantic-IR superiority. Two real repairs remain qualified.
