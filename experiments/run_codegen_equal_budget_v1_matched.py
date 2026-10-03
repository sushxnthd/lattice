"""Pre-generation token-budget correction permitted by frozen preregistration.

The first attempt aborted before model loading/generation at 211 vs 231 tokens.
This wrapper changes only strong-prose wording, then invokes the frozen evaluator.
"""
import codegen_equal_budget_v1 as exp

_base = exp.rules

def matched_rules(s, c):
    text = _base(s, c)
    if c == "strong_prose":
        text += " These rules are exhaustive; no additional action, actor, state, metric case, permission, or state change is allowed."
    return text

exp.rules = matched_rules
exp.main()
