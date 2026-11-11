# Run650: fail-closed functional adjudication

Executed 16/16 synthetic four-arm outcome patterns; exactly one matches the necessary candidate-only pattern. Provenance rejection returns UNKNOWN. An initial test fixture had boolean observations, was corrected, and tests reran successfully.

The Run641 four-cell oracle has no independent heldout/nonregression controls, so **CANDIDATE_ONLY is never a qualified production repair**. The upstream Werkzeug four-arm experiment was not executed. No model comparison or new qualified repair; count remains two. All 89 reserved issues untouched.

Local reproducibility archive SHA256: `8666b8997ab94c7d87ae6c1ebfc115498861dabf6538aa238f440161b27d950c`. Includes executable adjudicator, Run649 verifier, original Run641 runner, synthetic exhaustive tests, raw outcomes and per-member SHA manifest. Code commit `a3720a11c70a388e8523baec4407acf891f7a79f`.

Next: isolated execution against pinned upstream revisions, independently frozen heldout/nonregression oracle, then paired model evaluation.