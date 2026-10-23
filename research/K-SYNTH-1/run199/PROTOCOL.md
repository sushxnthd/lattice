# K-SYNTH-1 Run199: prospective real multi-file repair sampling

**Date:** 2026-10-23. **Status:** selection workflow launched; no real-repository model inference or repair success has been observed.

## Why the old benchmark cannot support the claim

The original 258 synthetic pairs have four instruction families and two graph topologies. Their task-level independence and unseen-condition assumptions are invalid. SWE-bench Lite is also unsuitable for the requested multi-file experiment: its curation **explicitly removes issues whose gold patch edits more than one file** (official dataset documentation: https://www.swebench.com/lite). A suitable source is SWE-rebench V2 (ICML 2026, https://proceedings.mlr.press/v306/badertdin26a.html), which reports 32,079 executable tasks from 3,617 repositories, with a median three edited files. The dataset is a **sampling frame**, not evidence for Lattice.

## Prospectively fixed selection

Source: PrimeIntellect/SWE-rebench-V2 (https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2), with the dataset revision resolved to its immutable Git SHA and recorded in the generated manifest. The deterministic selector is `select_real_tasks.py` at seed `lattice-199-frozen-2026-10-23`. No inference is permitted before the manifest is frozen.

Filter: Python; MIT/Apache/BSD/ISC repository license; issue >=40 words; issue date >=2024; 40-hex-character base commit; available evaluator image and FAIL_TO_PASS tests; gold patch <=20,000 characters; 2–6 modified files with at least two Python source files. These patch-derived eligibility filters are applied **only during sampling**; neither gold patches, test IDs, nor gold-derived file localization are supplied to the model.

Select at most **120 independent repositories, four unique issues per repository**, using fixed SHA-256 ranks, not outcomes. Assign 20% of repositories to an untouched boundary set. Public tasks, evaluator-only gold records and the manifest are separately hashed and stored as separate workflow artifacts. If fewer than 120 eligible repositories exist, the manifest says `inference_ready=false`; no adequately powered claim is allowed. The selection algorithm, not the sample's observed performance, is preregistered.

## Statistical planning, not a claimed experiment

The predeclared primary outcome is the **paired** issue-level difference in executable test success, analyzed with a two-sided repository-level signed-difference t test (alpha .05), reporting a repository-cluster bootstrap confidence interval and an exact/simulation sensitivity analysis. A 20,000-replication hypothetical model for 120 repositories × 4 paired issues, 30% discordance and beta-distributed within-repository directional ICC 0.5 yielded estimated null rejection 0.04895, power **0.8561** for P(IR wins | discordance)=0.65, and **0.51935** for a smaller 0.60 effect. Monte Carlo SE for the large-effect power was 0.00248. These are **assumptions**, not actual model results. The earlier 258-task target is not justified for clustered real-repository repairs.

## Matched inference and evaluation gates — still to implement

1. Pin a strong no-cost open coding model, revision/weights SHA, prompts, seeds, token counts, raw responses and failures. Freeze the task set and prompts before inference. Run positive controls and report floor failures.
2. Use an ordinary-Python source presentation versus a **lossless, invertible** semantic representation. Test round-trip source equality, same task facts, same accessible repository files, same edit authority and output patch schema. Do not mistake AST-only views that drop comments for information-equivalent conditions.
3. Both arms must pass through **the same patch compiler**, verifier and per-instance test environment. Report invalid intermediate states, semantic churn, verifier-repair loops, and per-repository outcomes. Include a conventional AST-action baseline.
4. Do not expose the evaluator-only gold patch, gold-derived file locations, FAIL_TO_PASS, PASS_TO_PASS or test patch in model prompts. Run executable tests only after freezing each attempt.
5. Freeze a specific cross-module dependency-depth boundary prediction on the discovery set **before** inspecting the boundary outcomes. Do not tune a primary result on the same issues used to test it.
6. If Python matches or beats IR in two matched reformulations, pivot the paper to authenticated epoch history and protected-output correctness, including an honest negative representation result.

**Critical blocker:** The current production compiler is a bounded Boolean-DAG editor, not a general Python multi-file semantic compiler. The new real-issue sampler is real science infrastructure, but the matched multi-file compiler and capable-model inference are **not yet complete**. No real-world representation superiority, mechanism, or boundary generalization is claimed.

## Reproduce

```sh
PYTHONPATH=research/K-SYNTH-1/run199 python -m pytest -q research/K-SYNTH-1/run199/test_selection.py
python -m pip install 'datasets==4.3.0' 'huggingface_hub==0.36.0'
python research/K-SYNTH-1/run199/select_real_tasks.py --repos 120 --per-repo 4 --out artifacts/run199
```

The GitHub Actions workflow `lattice-k-synth-1-real-multifile-freeze.yml` executes this on a cloud runner and uploads the separated provenance artifacts. Any network or dependency failure is recorded and retried in later runs; the research branch and existing draft PR remain the sole workstream.
