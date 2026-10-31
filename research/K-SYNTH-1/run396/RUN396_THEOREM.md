# Run396 counterexamples: necessity and interaction depend on the observation boundary

Let A and B be independent modules with primitive observation `O_ij=(f_i(x),g_j(x))`, where i,j are baseline/reference source choices. The mixed difference `O_11-O_10-O_01+O_00` is identically (0,0).

1. Split-target false positive: T1 checks only f, T2 only g. Each single-source ablation fails some target, but neither target needs both changes. The original existential gate accepts.
2. Conjunctive-oracle false positive: define `P_ij=[f_i=f_1] AND [g_j=g_1]`. For nontrivial independent fixes, `P_00=P_10=P_01=0` and `P_11=1`; thus its mixed difference is 1 although primitive interaction is zero.
3. Observer re-encoding false positive: for `h(u,v)=uv`, the mixed difference of `h(O_ij)` is `(f_1-f_0)(g_1-g_0)`, potentially nonzero for independent modules.
4. Generated dataflow positive witness: let `f_0=x`, `f_1=x+a`, `g_0=f_i`, `g_1=b*f_i` on positive x. The B output mixed difference is `a(b-1)`, nonzero for the experiment's a>=1,b>=2.

These are exact algebraic identities corroborated by original CPython executions. They do not prove universal Python equivalence, causal identifiability, or completeness of interaction screening. Zero interaction must not automatically disqualify a genuine repair. Use explicit UNKNOWN for unverified mechanisms.
