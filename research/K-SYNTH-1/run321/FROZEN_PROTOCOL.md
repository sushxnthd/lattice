# K-SYNTH-1 Run321 prospective AST-congruence protocol

Frozen before execution of Run321 primary experiment. Previous Run320 comment-swallow and precedence-leak witnesses are DEVELOPMENT data, excluded from primary evidence.

## Question
Does byte-splicing a valid Python expression silently change the AST outside the requested target node? Can an independently specified whole-module AST congruence guard reject every such mutation without rejecting ordinary safe replacements?

## Primary design
Generate 512 deterministic trusted synthetic Python fixtures using seed 321028, eight context families and 64 cases per family: multiplication precedence, addition precedence, boolean precedence, conditional expressions, trailing inline comments, unicode identifiers, CRLF newline sources, and nested call expressions. Each case uses a fixed target literal AST node and a deterministic replacement drawn from four classes: integer literal, binary expression, comment-bearing expression, and conditional expression. No case is derived from a production reference patch. The experiment must preserve every raw source, action, replacement, original compiler outcome, guarded outcome, AST comparison and SHA-256 digest.

## Comparator
The existing Run320 compiler is the unchanged baseline. A new guarded compiler must invoke the same byte-splice compiler, then independently construct the expected whole-module AST by replacing exactly the selected target AST node in the original tree with ast.parse(replacement, mode='eval').body. Compare ast.dump(..., include_attributes=False) of the resulting expected AST to the actual patched module AST. Ambiguous node matches, parsing failures and any AST mismatch must fail closed. This checks structural congruence, NOT general semantic equivalence or security.

## Frozen decisions
Success requires (a) every guarded accepted patch matches expected AST exactly; (b) every original compiler AST mismatch is rejected by guard; (c) at least 128 safe original patches remain accepted; (d) 0 independent audit discrepancies; (e) all accepted source files compile without execution of untrusted code. Count correlated fixtures, not independent repairs. Preserve original failures and do not adjust seed/families after outcomes. If acceptance criterion fails, report failure honestly and continue a postfreeze correction separately.

## Independent audit
Separate read-only script must recompute source SHA, actual patched AST and expected substituted AST without calling the guard implementation. For trusted generated sources, execute accepted functions in isolated subprocesses with timeout and compare deterministic outputs against separately compiled expected AST where feasible. Raw traces and audit outputs must be SHA-256 manifested.

## Scope and exclusions
This experiment is engineering correctness only. It is not model inference, does not qualify a new repository, and cannot establish IR superiority. Do not execute untrusted model code on host. Canonical sushxnthd/lattice, branch research/exp003-context-order, one open/draft/unmerged PR #9; 89 reserved boundary issues SEALED.