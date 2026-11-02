# Run444 prospective paired-structure feasibility protocol (frozen before inference)

Date: 2026-11-02 UTC. Kernel K-SYNTH-1; canonical branch research/exp003-context-order; one draft PR #9.

Three tasks: previously qualified Flask PR6096 and urllib3 PR5071, plus one synthetic two-file format control. The two real task excerpts are previously source-pattern-localized using known bug mechanisms, so **this is not a blind real-repair benchmark**.

Arms: (A) typed semantic information graph with explicit UNKNOWN cross-file edges and an atomic replace-action contract; (B) conventional Python AST facts declaration and ReplaceSourceSpan action template. A frozen independent decoder must recover byte-identical task facts, source excerpts, edit authority and source SHA. UNKNOWN never certifies def-use or runtime behavior. Input prompt lengths and token counts are measured separately; factual equivalence does not imply token-budget or cognitive equivalence.

Both arms: same Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c, same seed 444001, temperature 0, max 768 completion tokens, same source checkout, shared strict atomic compiler, and independent heldout oracle when available. Prospectively accept either plain JSON or one JSON Markdown fence for both arms. Do not retroactively alter Run442 results.

Frozen local six prompt SHA256 values in task order:
- Flask IR b0dbb7e7a42947888517aca447f370df167ade11978818a52c69b97c41015da4
- Flask AST 5754d525e39ee88b5d9b8e036ee2f8132a4286d36cb12b90a4786cef4dec9bee
- urllib3 IR 7d22f3b33b14fb39a90f54cd684e1eac69bd49d532847be922d7d271fe75c638
- urllib3 AST 60b4776707579ef2061e764f05af6c131190ad4289996ad8d890964072d6b145
- control IR cc179c15162a5af4fa74062972475eb30a86fb11805170ce9d134e07ba839634
- control AST 7c5088495c2d5fef6a97aaa8ce80934c14bedfc86efbda86262fad1070503286

Outcomes separately classify precompletion failure, format failure, schema failure, authority/preimage failure, parse failure, functional failure, success. Raw request/response, prompt SHA, token usage, model SHA and compiler receipts retained. No user laptop, paid API, or execution of untrusted model-generated Python on host. Preserve original failed outcomes. No superiority or powered significance claim from n=2. All 89 reserved boundary issues sealed.