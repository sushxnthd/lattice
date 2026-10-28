# K-SYNTH-1 Run309: prospective nested assignment-expression soundness check

## Frozen hypothesis and scope

The Run308 source-only module-binding analyzer is expected to produce a definite-negative false exclusion of `builtins.len` after a shadowing lambda when a *nested* Python assignment expression (`NamedExpr`, `:=`) rebinds `len` inside a module-level RHS. Run309 tests whether expression-tree side effects must invalidate module binding identity, rather than being ignored when the enclosing expression is not itself an `ast.Call`.

Freeze 16 scenario templates x 24 correlated variants = 384 trusted Python 3.13 source cases before functional execution. Eight positive scenarios must restore the builtin; eight negative/control scenarios must not. Independent CPython subprocess oracle executes only authored trusted fixtures, with a fixed timeout. No model-generated code is run on the host. The exact source manifest and its SHA-256 are frozen on GitHub before execution. Any parse/runtime failure remains in the denominator. The original Run308 transfer must be run unmodified; correction must never retroactively alter the original observations.

The correction is conservative: for every assignment RHS containing `ast.NamedExpr`, invalidate the named target's binding to `UNKNOWN`, whether or not control flow executes it. Preserve definite negatives for controls without assignment expressions; quantify lost precision on non-executed walrus controls. Reject a superiority claim: this tests a bounded semantic soundness defect, not real-repo repair performance.

Separately, independently audit ORIGINAL Run307 CPython 3.14.8/3.14.9 GitHub Actions artifacts and Run308 CPython 3.13.16 artifact against frozen SHA sources, local Run307 predictions and original CPython 3.13.5 observations. Record all version differences and any mismatches. Do not relabel earlier predictions as observed until verified.

## Qualification and next steps

Do not promote wsproto PR #6 or any sixth production task without independently frozen target, heldout, controls, joint component necessity and isolated oracle. Keep one K-SYNTH-1 kernel, one open/draft/unmerged PR #9, the canonical research branch, and all 89 reserved boundary issues sealed. No powered IR-versus-Python claim.
