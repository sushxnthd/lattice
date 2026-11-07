# K-SYNTH-1 Run551 — eligibility evidence is not eligibility

Implemented and locally executed a conservative structural preflight for prospectively frozen two-production-source repair qualification. Eight directed fixtures and 256 exhaustive sign-flip symmetry checks passed (266 assertions total).

The preflight deliberately returns `STRUCTURALLY_ELIGIBLE_UNVERIFIED`, **never QUALIFIED**. Boolean outcome matrices cannot independently establish freeze timing, SHA provenance, oracle isolation, or source independence. It rejects single-source cases, missing controls, malformed SHA syntax, reference regressions and nonnecessary component ablations. A control-only ablation may satisfy *joint target-plus-control* necessity; this is not target-only necessity.

A **synthetic**, non-model example with 28 IR-only and four Python-only issue outcomes has an issue-level McNemar p-value below 0.001, while seven positive and one negative perfectly clustered repository contrasts have exact sign-flip p=0.0703125. The primary estimand and exchangeability assumptions must be frozen before real trials.

Local verified reproducibility archive: run551.zip SHA256 `539dc20c78e069d1ac560cf870cdf78dd2299b9f63c169704bd5fdca91806b4c`. Executable, raw JSON, report and SHA manifest are in that archive; complete GitHub raw/source mirroring is still pending.

Next: independently pin a NEW real public PR's base/reference SHA, freeze public/heldout/nonregression oracles before ablations, require two production sources and joint target/control necessity, then run matched strong-model paired pilots. Do not retroactively qualify Werkzeug PR2535.

No new production repair qualified, no new model inference, no semantic-IR superiority. All 89 reserved issues remain sealed.