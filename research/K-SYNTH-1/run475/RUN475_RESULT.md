# Run475 — signed literal compiler expressibility repair

Bounded synthetic compiler instrumentation, not a real repair or model comparison.

Run474 rejected negative integer returns because Python represents them as UnaryOp(USub, Constant), not Constant. Run475 admits unary plus/minus over integer constants and rejects calls, arithmetic, nested unary operators, floats, and boolean negation. Edit locality preserves all bytes outside the authorized return span.

2048 seeded paired IR/Python-action transactions: 1686 accepted, 158 mismatched preimages, 204 unauthorized expressions, zero compiler parity mismatches. 400 accepted negative-to-negative replacements. All 12 adversarial assertions passed. No candidate code executed.

Parity is expected because both formats normalize to the same compiler input, not evidence of IR superiority. No real repair qualification or model inference. Two independently qualified repairs remain; 89 sealed issues untouched.

Local reproducibility ZIP SHA256: 56bd2c38b57273458772c5dc7ebc7a942fcfcddde92f7b3a88d0cb2f28281ac9. Executable/raw ZIP mirroring outstanding.