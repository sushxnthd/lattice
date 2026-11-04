# Run480: exact conditional McNemar power sensitivity

## Method
A deterministic exact-binomial computation enumerated the two-sided McNemar rejection boundary at alpha 0.05, conditional on a **fixed** number of discordant paired outcomes D. Under the null, IR-only wins X|D ~ Binomial(D,0.5); under the directional alternative X|D ~ Binomial(D,p). Rejection is at X <= k or X >= D-k, where k is the largest integer satisfying 2 P_null(X<=k)<=0.05. Computed power sums both alternative tails. Source code is included in this directory. These are exact conditional calculations, not simulation or coding-model outcomes.

| Planned pairs | Fixed D | P(IR win given discordance) | Lower/upper rejection boundaries | Conditional power |
|---:|---:|---:|---|---:|
|306|92|0.65|36 / 56|0.8267077284|
|681|204|0.60|87 / 117|0.8008053564|
|306|92|0.60|36 / 56|0.4774420762|
|681|204|0.65|87 / 117|0.9902337504|

## Finding
The optimistic n306 and moderate n681 proposals deliver approximately 82.7% and 80.1% **conditional** power respectively when the observed discordant count is fixed to 92 and 204. They are not unconditional prospective power guarantees: actual D is random, and within-repository dependence and heterogeneity can invalidate issue-independent McNemar assumptions. At fixed D=92, moving the conditional win probability from 0.65 to 0.60 reduces power to 47.7%. The 681-pair design at D=204 and p=0.65 yields 99.0% conditional power, illustrating effect-size sensitivity, not evidence for an actual effect.

## Interpretation and boundaries
- No task was newly qualified, no model inference occurred, and no semantic IR superiority is claimed.
- Design must be recalculated under random discordance and repository-cluster uncertainty; do not infer adequate power merely from these conditional numbers.
- The 89 reserved boundary issues remain sealed.
- Run479 source-text hygiene limitations remain open; this statistical check does not resolve them.
