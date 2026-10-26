# K-SYNTH-1 Run267 — definition-time call coverage and causal identification audit

2026-10-26. Canonical sushxnthd/lattice, branch research/exp003-context-order, one draft PR #9. All 89 boundary issues sealed.

## Executable semantic counterexample
Run266 MAY provenance v2 omitted function/class definition headers. Default-argument calls execute when a def executes, and decorators implicitly invoke callables even if the decorator expression is a Name rather than an AST Call. V3 records these sites with explicit UNKNOWN; also conservatively scans keyword defaults, class bases, decorator factories and possibly-lazy annotations. This is bounded call-site coverage, NOT sound unrestricted Python.

256 seeded independently executed examples (seed2672026): v2 missed 256/256 default-argument calls, v3 missed 0/256, and v3 missed 0/256 implicit decorator applications. All 77 inherited/new tests passed. On pinned Flask PR6096 baseline, call records rose from 179 to 180 (one implicit decorator event); no useful precision or repair-performance claim. V3 SHA256 98fe3ed68113c44be5eba5c81834f2b46bc627fa460beec6bdb0fb1e8bb86874.

## Critical causal construct-validity audit
Independently audited exact unchanged Run265 frozen Flask requests: BOTH IR-anchor and ordinary-Python byte-span arms receive identical serialized semantic graph facts (25 nearby may-call records), identical task/source/edit authority, same model SHA, seed265001/temp0, and privileged reference-derived OLD-span localization. Only OUTPUT ACTION SYNTAX differs. Therefore even if this paired pilot succeeds, it cannot identify benefit of providing a semantic/dataflow IR instead of ordinary Python; it estimates at most an action-language/format effect.

Let success be Y(presentation, action). Run265 holds presentation=shared graph facts and varies action, so Y(graph,graph-anchor)-Y(graph,byte-span) does NOT identify Y(graph,action)-Y(python,action). Required prospective factorial: information-equivalent verified semantic-graph versus ordinary Python/AST presentation crossed with graph-anchor versus byte-span action language, identical source/task/authority/compiler/oracle, reversible fact bijection, randomized order. Original frozen prompts remain immutable.

## Evidence, limitations, next work
Local 90-entry SHA256-verified ZIP /mnt/data/lattice_run267/lattice_run267_header_calls_and_identifiability.zip, archive SHA256 9340468716a297d06ab69cfc455b34202a726c66014844ad0c209b7661696072. Witness SHA256 7f0175bb11d302bd3fc8d1caeb0c4c8319afe1c524ab4cf6dcab8923034e099c; independent audit SHA256 a8950d0c9f7fbe48a1803ec287dc275a4282fa16951e223ae2fb2c7612236ad6. Full executable core/tests/frozen prompts local; GitHub mirroring pending.

NO new Qwen inference, model token counts, model-patch functional oracle, or independently qualified real issue. Qualified independent issues remain Flask PR6096 and urllib3 PR5071; urllib3 prompts not yet frozen. Prior Flask pilot is not a semantic-IR-vs-Python test. Next: mirror full source, freeze urllib3, run pinned capable-model inference on both tasks, implement prospective 2x2 design and qualify more independent multi-source repairs. No breakthrough/significance without powered evidence.