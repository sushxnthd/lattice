# K-SYNTH-1 Run437 prospective issue-first freeze (before reference inspection)

Freeze UTC date: 2026-11-02. This document is written from the public report https://github.com/pallets/flask/issues/4037 only. No fixing PR, patch, or post-fix oracle has been inspected at freeze time.

Repository: pallets/flask. Issue #4037 (2021-05-13), Flask 2.0.0 reporter environment. Historical source reference: immutable release label `2.0.0` (must resolve to a full commit before executing). Source blob IDs observed before reference: `src/flask/blueprints.py` 5fb84d86a6379ec3c22d7ceea1f2ea6237b5f69d, `src/flask/app.py` f8856a52f07876542a1cecc79515e9bc0ab8feba, `src/flask/scaffold.py` 56d37ddd10f0aec02b858673acd89a7b3ce42b7d. These are Git blob IDs, NOT SHA256. A resolved immutable commit and full-file SHA256 must be recorded before historical execution.

Reported defect: constructor-provided `url_prefix` values are lost for nested blueprints; passing a prefix through `register_blueprint` works. Expected nested prefix is concatenation of outer then inner constructor prefixes; e.g. `/outer/inner/`. The report's own path names are reversed (`parent` prefix `/child`, `child` prefix `/parent`), so do not treat its string `/parent/child/` as evidence for concatenation order.

Prospectively frozen target cases (each route returns `ok`, use GET via `test_client`, assert both status and body; route-map assertions separate):
T1 outer constructor `/outer`, inner constructor `/inner`, child route `/`: GET `/outer/inner/` -> 200 `ok`.
T2 same with noncommutative prefixes `/first`, `/second`: GET `/first/second/` -> 200 `ok`.
T3 three-level constructor nesting `/a`, `/b`, `/c`: GET `/a/b/c/` -> 200 `ok`. This is a declared heldout generalization, not directly specified by the reporter.
T4 the T1 route's endpoint must be `outer.inner.index` (assuming standard nested blueprint naming).

Controls:
C1 a direct blueprint constructor prefix `/solo` yields `/solo/` and 200.
C2 a nested blueprint with no constructor prefixes and explicit `app.register_blueprint(outer, url_prefix='/app')` yields `/app/`.
C3 a nested child with explicit `outer.register_blueprint(inner, url_prefix='/explicit')` and outer constructor `/outer` yields `/outer/explicit/`.
C4 GET `/` for T1 must be 404 (no unintended root alias).
C5 an unrelated app-level `/health` route returns `healthy`.
C6 the T1 nested endpoint must not be duplicated under `/inner/` or `/outer/`.

Qualification is all-or-nothing: pinned baseline fails >=1 issue target while controls pass; fixing reference passes ALL T1–T4 and C1–C6; >=2 independently modified production Python source files; both component ablations fail the joint target-plus-control contract; no simple one-file alternative within an explicitly defined candidate repair grammar. Use an independent oracle, historical dependency closure, source hashes, and isolation. If the accepted maintainer contract differs, or only one production source changes, REJECT without retuning. No task may be counted from synthetic or installed-modern-version tests. No reserved boundary issues are touched.

This freeze does NOT assert qualification or functional results. All 89 reserved boundary issues remain SEALED.
