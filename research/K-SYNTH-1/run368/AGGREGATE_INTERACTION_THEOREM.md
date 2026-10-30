# Run368 finite-interaction theorem and falsifiable predictions

For two binary source interventions A and B, let each case j have binary correctness Y_j(a,b). Define its factorial interaction delta_j = Y_j(1,1)-Y_j(1,0)-Y_j(0,1)+Y_j(0,0). Define aggregate success F(a,b)=product_j Y_j(a,b). In general, Delta_F is not sum_j delta_j, nor does Delta_F != 0 imply any delta_j != 0.

**Constructive proof:** Take two cases, Y_1(a,b)=a and Y_2(a,b)=b. Then delta_1=delta_2=0, but F(a,b)=ab, so Delta_F=1-0-0+0=1. Thus an all-tests-pass qualification can make two independent repairs appear synergistic. This is a mathematical identity, not a claim about the semantic independence of arbitrary production code.

**Predictions, frozen before historical execution:** For HTTPX #1532, _client.py and _models.py repair separate public-API cases. Hypothesis H0 predicts each case-level delta_j=0 while aggregate ALL_PASS delta=+1, if no cross-file behavior is exposed by the frozen oracle. Alternative H1 predicts nonzero casewise delta for one or more cases, indicating an observed dependency requiring further ABI and semantic intervention tests. Import failures make interactions partially identified and block qualification. Reference-aware issue selection limits generalizability. The experiment is not a blinded coding-model comparison.

**Caveat:** A zero observed casewise delta only proves absence of interaction on the 13-case finite oracle, not all inputs. Even a nonzero delta is not a unique causal mechanism certificate. The separate soundness-scoped IR must retain UNKNOWN for unresolved dynamic dependencies.

**Local preflight (modern HTTPX 0.28.1, not historical):** 13/13 API cases pass; four unit tests pass, including six adversarial auditor mutations. No historical qualification or model repair inferred from this preflight. The exact historical 4x13 test is running in an isolated GitHub Actions workflow. All 89 boundary issues remain sealed.
