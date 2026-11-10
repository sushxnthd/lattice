# Run633: missing-oracle fail-closed enumeration

Executed 3^12 = 531,441 three-valued synthetic outcome configurations across four factorial arms and target/control/heldout observations. Results: PASS 16; FAIL 4,080; UNKNOWN 527,345. Every deletion of one of the 12 observed values from a known PASS returns UNKNOWN (12/12). An unobserved heldout is not a heldout success. This establishes a finite logical property of this explicit gate, not correctness of an independent production oracle.

**No real PR qualification, model inference, causal repair result, or semantic-IR advantage.** Two historical qualified repairs remain; 89 sealed boundary issues untouched. Source `reproduce.py` recomputes raw enumeration. The `raw_summary.json` is an abbreviated mirror; complete raw enumeration is algorithmically reproducible from source and not stored as 531,441 JSON rows.
