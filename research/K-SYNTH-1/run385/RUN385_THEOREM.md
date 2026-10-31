# Run385 finite-domain completeness and interaction theorem

For each target input i in {00,01,10,11}, let F_i(t) be the Boolean target output when the producer's 2-input truth table is replaced by t in {0,...,15}. The admitted Run383 grammar is pure Boolean, whitelisted and total under all 64 interventions. Otherwise the certificate is UNKNOWN.

The unique algebraic normal form over GF(2) is F_i(t) = XOR_{S subseteq bits(t)} a[i,S], with coefficients a[i,S] = XOR_{T subseteq S} F_i(T). The Boolean-lattice Moebius transform is self-inverse. Hence the four 16-coefficient rows are injective and complete for all 64 finite counterfactual observations: two admitted programs have the same certificate if and only if their outputs agree under every producer-table intervention and target input.

The derivative D_j F(t)=F(t) XOR F(t XOR 2^j) is identically zero if and only if no nonzero ANF monomial contains j. Similarly D_j D_k F is identically zero if and only if no nonzero monomial contains both j and k. These characterize exact input-indexed support and pairwise interaction.

Counterexample: guard g=(x and not y) or (not x and y). Compare g and (p(x,y) and p(y,x)) against g and ((p(x,y) and not p(y,x)) or (not p(x,y) and p(y,x))). They have the same complete 4x4 support but different truth tables, ANF, and second-order interactions. A guarded product of p(x,y), p(y,x), p(x,x), p(y,y) has a degree-four monomial. Thus support-only semantic IR is insufficient to represent higher-order behavior even in this restricted grammar.

The theorem is NOT a claim about unrestricted Python, production repository semantics, observational causal identification, or model-repair superiority. Independent fresh CPython replay: 83,648 frozen observations plus 320 separate adversarial observations, zero mismatches.
