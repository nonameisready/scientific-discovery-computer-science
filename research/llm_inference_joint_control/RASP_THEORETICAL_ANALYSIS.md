# RASP theoretical analysis

**PROVED:** the reference controller's returned decisions satisfy its declared hard peak-byte and batch-budget checks. The proof is a direct induction over the greedy output list.

**TESTED_ONLY:** deterministic no-future-arrival execution, deterministic tie-breaking, and the memory bound in the trace harness.

**CONJECTURED:** shadow prices could improve decisions under stationary acceptance/pressure feedback. The trace results do not support this conjecture in the tested matrix.

**DISPROVED for the present reference policy:** the informal claim that the coupling reliably improves reference-level goodput/tail behavior. It loses to simpler baselines in low-acceptance and burst fixtures.

No regret, competitive-ratio, starvation, or end-to-end performance theorem is claimed. Existing KV-constrained scheduling theory also warns against universal adversarial guarantees; RASP does not evade that limitation.
