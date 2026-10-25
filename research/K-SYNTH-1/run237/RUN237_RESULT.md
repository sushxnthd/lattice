# Run237 — Complete twelve-repository paired Qwen audit

Date: 2026-10-25. Original frozen experiment: GitHub Actions run 40148667367. Branch: research/exp003-context-order. The original functional endpoint remains NOT_EVALUATED for all 24 completions. This is an independent, secondary necessary-condition audit, not a preregistered functional-success comparison.

## Provenance
All twelve GitHub Actions jobs completed successfully. Recovered the two outstanding artifacts: mlcommons/medperf (index 10, artifact 12583384016) and vacanza/holidays (index 11, artifact 12583748692). The original artifacts from all twelve distinct repositories passed SHA-256 manifest, prompt-hash, source-fact-hash, model/seed, token-usage, and verifier-record checks. Model: Qwen2.5-Coder-7B-Instruct Q4_K_M, SHA-256 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c.

| Metric | Semantic IR | Annotated Python |
| --- | ---: | ---: |
| Genuine completions | 12 | 12 |
| Frozen compiler accepted | 7 | 5 |
| Frozen compiler rejected | 5 | 7 |
| Invalid model JSON | 1 | 2 |
| Prompt tokens | 100,726 | 105,695 |
| Completion tokens | 5,745 | 6,888 |
| Original full functional evaluations | 0 | 0 |

Paired compiler acceptance: 4 both accepted, 4 both rejected, 3 IR-only, 1 Python-only. Paired difference +16.7 percentage points; exact enumerated paired bootstrap percentile interval [-16.7, +50.0] percentage points; exact conditional two-sided McNemar p = 0.625. This is not a functional-correctness advantage and the pilot is underpowered.

## Independently executed Vacanza counterexample
The original full source of holidays/calendars/custom.py was reconstructed and SHA-verified against f28d1b9370c76c4c5e2cc7a1d42e5dde34695e90dcba6c26a940713cfc398e9b. An isolated executable witness defines a subclass of _CustomCalendar, gives it a public class attribute, instantiates it with no arguments, and checks the metaclass-renamed attribute. Original source passes with public_CUSTOM_CALENDAR == 7. The semantic-IR model edit deletes the _CustomCalendar declaration entirely. The annotated-Python edit preserves the declaration but introduces a four-argument __new__, so subclass instantiation fails with TypeError (three required arguments missing). Both edits were accepted by the frozen compiler and Git patch check. These are demonstrated compatibility failures, not full tests of the reported substituted-holiday bug.

The remaining new task, mlcommons/medperf, was rejected in both arms because the generated JSON was truncated.

## Bound and limitations
The earlier Run236 auditor identified 11 necessary-condition failures among 12 accepted edits (seven deleted declarations, one property descriptor regression, one invalid Git patch, one Sphinx extension-disabling workaround, and one unchanged pipx launcher argument). The Vacanza witness rules out the remaining accepted edit. The other twelve outputs were compiler rejected. Therefore all 24 outputs are either compiler rejected or fail a checked necessary condition. No issue-specific complete functional evaluation has been performed; do not report 0/24 as a measured full-repair success rate. No representation superiority or general negative result is established.

## Scientific next step
Prospectively freeze actionable multi-file tasks and independent issue-level functional oracles before generating more completions. Apply the same declaration/descriptor/constructor preservation gate and byte-faithful Git patch check to both arms. Use a genuine ordinary-Python baseline rather than the existing JSON-annotated AST_TARGET view, while holding information and authority constant. Increase the matched output budget to avoid truncation. Scale only after calibrated functional controls; the previous cluster-aware planning calculation suggests approximately 1,089 paired issues from 440 repositories under its stated modest-effect assumptions. Keep the 89 boundary issues sealed until a mechanism and unseen-condition prediction are frozen.

Full local reproducibility bundle: lattice_run237_complete_twelve_repository_audit.zip (original cloud artifacts, auditor, source-verified witness, exact uncertainty calculation, nine regression tests, SHA-256 manifest). This report does not modify the original Run234 frozen endpoint.