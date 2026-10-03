# Equal-budget replication v1

Status: FROZEN, NOT YET EXECUTED.

This prospective replication tests whether the prior violation-normal advantage survives a strict information/budget control. It uses Qwen/Qwen2.5-Coder-1.5B-Instruct with deterministic decoding, a strong prose baseline, the violation-normal representation, eight development domains, and eight new holdout domains. The two prompts must contain the same semantic facts and must have identical chat-template token counts within each task before generation. Raw outputs, token counts, per-domain hidden-test scores, and perfect-program rates must be retained. No representation or evaluator change is allowed after the new holdout is opened.

Primary comparison: paired holdout hidden-test accuracy for violation-normal versus strong prose. A positive result is only a candidate semantic-representation effect; it is not evidence of a new programming language or long-horizon software engineering capability.

Parent frozen evidence: commit 8cd157023f707dde9e9ed317ccbaa94b89077f34; Actions run 37103981199; manifest 096d70e3194d208355a9a38634638aad8587acd629a4405c4b4f029731767c0c.
