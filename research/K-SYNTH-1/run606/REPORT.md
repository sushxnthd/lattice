# Run606: exact unconditional McNemar power audit

Independent-issue planning only. Exact two-sided conditional binomial test at alpha 0.05, integrated over D ~ Binomial(n, discordance).

| Discordance | Conditional IR win | First n reaching 80% | Power at 306 | Power at 681 |
|---|---|---:|---:|---:|
| .30 | .65 | 306 | .800367 | .989749 |
| .30 | .60 | 681 | .443642 | .800498 |
| .20 | .65 | 460 | .613388 | .933183 |
| .20 | .60 | 1021 | .303869 | .618009 |

These verify the earlier 306/681 planning figures under the explicitly assumed .30 discordance. At .20 discordance, 681 issues is insufficient for the moderate effect. Repository clustering, model inference, candidate qualification, and external validity are not established by these calculations. No model output, repair success, or semantic-IR superiority is claimed. All 89 sealed boundary issues remain untouched.

Reproduction: for each n, sum Binomial(n,d) probabilities times exact conditional two-sided Binomial(k,p) rejection probabilities. The local artifact includes executable scipy implementation and raw JSON.
