# Final research decision: predictive KV-cache scheduling for agentic serving

## Decision

**Classification:** `SOURCE_GROUNDED_HYPOTHESIS`, `IMPLEMENTATION_READY_ALGORITHM`, `REFERENCE_LEVEL_VALIDATED`, `THEORY_SUPPORTED`. Not `GPU_EMPIRICALLY_VALIDATED`; broad novelty is `NOVELTY_NOT_ESTABLISHED`.

The unresolved bottleneck is not “learn agent transitions” or “keep a tool-call cache alive.” CacheScout and Continuum already cover those mechanisms, while Vesta covers queueing-aware cache locality and SGLang’s roadmap names the relevant orchestration hooks. The narrower unresolved question is whether exact-prefix survival uncertainty can be priced jointly with return-time uncertainty and an explicit value of waiting, without allowing speculative work to harm active traffic.

The selected controller is a robust lower-confidence expected-benefit rule with an option value for deferral. It is mathematically `max(0, p_hat q_hat-epsilon)B-X-D-I > O`, with exact-prefix compatibility checked separately. A restricted threshold proposition is proved under deterministic, no-contention assumptions; memory cap, no-future-information, and exact-prefix invariants are proved for the reference implementation.

## Evidence

On a fixed synthetic CPU trace, the proposed policy reduced mean continuation TTFT from 10.00 to 8.93 in the mixed regime and from 10.00 to 9.42 in the late regime, while using 9,300 and 5,700 transfer bytes versus 36,620 and 40,280 for static prefetch. It lost to TTL in the early regime (8.13 versus 6.61), so there is no universal dominance claim. These are simulator units and synthetic traces.

The strongest counterexample is simultaneous long returns: aggressive policies prefetch almost everything, evict heavily, and waste transfers. The proposed policy limits work but can still lose to a well-tuned TTL policy. Wrong prefix forecasts and transfer contention remain incompletely modeled.

## What remains

GPU validation requires a real SGLang or vLLM version-pinned integration, exact KV correctness checks, real tool traces or a license-compatible benchmark, matched load and memory, queueing interference, P95/P99, worker migration, bandwidth saturation, and confidence intervals across held-out seeds. No cloud GPU or production service was used.

Code and detailed artifacts: [isolated package](../research/agentic_kv_cache_scheduling/README.md), [evaluation](../research/agentic_kv_cache_scheduling/EVALUATION_RESULTS.md), and [manuscript](../paper/AGENTIC_PREDICTIVE_KV_CACHE_SCHEDULING.md).

