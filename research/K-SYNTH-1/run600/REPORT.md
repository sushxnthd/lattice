# K-SYNTH-1 Run600: bounded AST-call inventory

Eight deterministic Python AST fixtures: direct calls, deferred function/lambda bodies, short-circuit, decorator, default expressions, generator deferral and dynamic eval. Local executable recorded 10 syntactic calls in 8 cases, zero MUST-execute claims, five illustrative UNKNOWN/deferred labels. No model inference, runtime oracle or qualified production repair. Initial fixture `@print` was a Name rather than Call; corrected to `@print(1)` before final output.

Local reproducibility ZIP SHA256 cf393c5dffac878c11ae850f0f42da886ab73dc46f4e16fa7c14343d7da50e6f; executable, raw JSON, stdout, manifest remain local and require GitHub mirroring. No reserved boundary issues touched. Two qualified real repairs remain; no superiority claim.