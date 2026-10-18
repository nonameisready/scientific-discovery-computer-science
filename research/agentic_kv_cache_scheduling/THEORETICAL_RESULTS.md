# Theoretical results

## Proved for the reference controller

**Memory safety.** With capacity `C`, `_admit` evicts before inserting a GPU entry, so the number of GPU entries is at most `C`. This is an implementation invariant, proved by induction on admissions: the base cache is empty; each admission either leaves occupancy unchanged below `C` or removes one before adding one.

**No-future-information.** `decide` reads only session forecasts, prior duration history, current cache, capacity, and current active-request count. It does not read `tool_duration`, `reusable_tokens`, or future events. This is a code-level property tested by `test_no_future_information_in_decision_path`; it is not a proof that an external predictor itself is calibrated.

**Exact-prefix safety.** A hit requires the stored token length to equal the requested reusable length in the reference model, plus GPU readiness. Therefore a shorter or stale entry cannot be reported as an exact hit. This is deliberately conservative and stronger than semantic similarity.

## Restricted threshold proposition

Assume one candidate, deterministic transfer cost `X`, deterministic saved delay `B`, no displacement/interference, and calibrated lower bound `p_L <= P(return and exact-prefix-compatible | x_t)`. Immediate prefetch has nonnegative expected gain whenever `p_L B > X`. If the next observation can increase the lower bound by at most `Delta`, waiting one tick has value at most `Delta B`; immediate prefetch is sufficient when `p_L B - X >= Delta B`.

**Proof.** The worst-case immediate expected gain is at least `p_L B-X`. The maximum additional benefit from waiting is the increase in the probability lower bound, at most `Delta`, times `B`; transfer cost is unchanged under the assumptions. Thus the immediate action weakly dominates waiting under the displayed inequality. ∎

The proposition excludes capacity displacement, queueing, nonstationary hazards, partial transfer, and cancellation; it is not a theorem for production serving. Fairness, regret, P99 SLO preservation, and optimality under adversarial arrivals are `NOT_TESTED`.

