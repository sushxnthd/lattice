# Run617: Real upstream PR causal-scope triage

Original GitHub PR file metadata independently inspected for pallets/werkzeug PRs #3335, #3339, #3341, #3329. This is structural triage, not qualification.

A preliminary heuristic counts production Python files with >=5 changed lines. PR3335: 2 substantive files (response.py 397 changed lines, wsgi.py 5). PR3339: 4 substantive files of 5 (http.py only 4 changed lines). PR3341: 2 substantive files (test.py 10 and wrappers/response.py 30). PR3329: only 1 substantive file (serving.py 61 changed lines); _internal.py adds a single TypeVar line. PR3329 therefore is a false positive under naive two-production-file counting.

The >=5 threshold is an arbitrary screening heuristic, NOT a scientific qualification rule. Neither substantive file count nor reference diff proves causal necessity. PR3341 may only relocate a property. Prefer PR3339 for causal decomposition; retain PR3341 as simpler candidate. Before any candidate enters the evaluation set, prospectively freeze exact base/ref SHAs, targets, heldouts, controls and independent isolated oracle, then execute target-specific and control-specific component ablations. Do not infer joint necessity from regressions on controls alone.

No newly qualified repair, no model inference, no superiority claim. 89 reserved issues untouched.
