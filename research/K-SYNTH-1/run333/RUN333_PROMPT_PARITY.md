# Run333 independent pre-inference prompt-parity audit

Read-only audit compared the original Run332 frozen requests against the Run333 locally frozen requests, using SHA-256 and bytewise prefix checks. The **only gate prompt intervention** was the same 388-character suffix in both IR and Python/AST arms. Original IR gate prompt 987 characters, new 1,375; original Python/AST 1,019, new 1,407. All other gate request fields remained equal.

Both REAL requests were **byte-identical** to the original Run332 freeze: IR SHA-256 `4c9d053cfebcbbc627d7869f3029e03be051a92717472c6c7728419d44b87a1c`; Python/AST SHA-256 `a909486c670582ed1a296bc44f4ecf89e344ea9ffc656e622e4de34d63aca181`. New gate request SHA-256: IR `eee0d80452ae7764a0b394c3d0f270472caaa78bc24739fc67350620c97ab66f`, Python/AST `827016bb3f4cd714e2998c1ad064458612a1dae4081dadc206147f42d8752b22`.

This is a **post-observation exploratory reformulation**, not a prospectively untouched primary comparison. Prompt-token lengths and actual model outcomes must be obtained from the cloud artifact. The original Run332 strict gate failures remain unchanged. No production success claimed.
