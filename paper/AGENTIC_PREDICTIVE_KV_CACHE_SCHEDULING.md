# Uncertainty-Aware Predictive KV-Cache Scheduling for Multi-Turn AI Agent Serving

## Abstract

Agentic LLM serving pauses inference on tools, then resumes with a context that may or may not preserve an exact KV prefix. Existing work already learns execution transitions, uses TTL retention, and accounts for queueing-aware placement. This manuscript studies a narrower controller: admit proactive prefetch only when a lower-confidence estimate of return probability times exact-prefix survival exceeds transfer, displacement, and active-request interference costs, after pricing the option to wait. A deterministic CPU reference implementation proves memory-cap and exact-prefix invariants and evaluates conceptual baselines on synthetic traces. The proposed policy reduces speculative work and evictions but loses to TTL in an early-return regime. The result is a source-grounded implementation-ready hypothesis, not a GPU validation or established novelty claim.

## 1. Introduction and motivation

Agents repeatedly call an LLM, invoke tools, and resume after uncertain delays. User-visible continuation TTFT differs from total workflow latency: retaining or prefetching a prefix can help one continuation while harming unrelated active requests. Exact token compatibility is required; semantic similarity is insufficient.

## 2. Prior art and novelty boundary

CacheScout learns online agent execution transitions and uses them for eviction/prefetch ([paper](https://arxiv.org/abs/2608.14624)). Continuum uses TTL-based retention for variable tool pauses and queueing/reload costs ([report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2026/EECS-2026-234.html)). Vesta jointly reasons about authoritative cache holders, executor placement, transfers, and queueing ([paper](https://arxiv.org/abs/2610.14686)). SGLang documents HiCache and has roadmap/RFC work for agentic cache orchestration and hints ([HiCache](https://docs.sglang.io/docs/advanced_features/hicache), [roadmap](https://github.com/sgl-project/sglang/issues/43098)). Therefore transition learning, TTL retention, queue-aware locality, and generic hierarchical caching are excluded from the novelty claim.

## 3. Formal model

At each tool-start event, observable state includes session metadata, prior durations, prefix forecast, cache layout/tier, capacity, active queue, transfer bandwidth, and SLO state. Future return time and exact reusable length are hidden. The controller chooses prefetch, retain, defer, or evict under a hard capacity.

## 4. Controller

Let `p_hat` be online return survival, `q_hat` exact-prefix survival, `B` avoided recomputation delay, and `X,D,I,O` transfer, displacement, interference, and waiting-option costs. Admit when:

`max(0, p_hat*q_hat-epsilon)B - X-D-I > O` and the left side is positive.

The implementation uses an empirical duration survival estimate, a forecast token length, an uncertainty reserve `epsilon=.20`, and a conservative exact token-length compatibility check. Pseudocode is in the isolated package’s [selected algorithm](../research/agentic_kv_cache_scheduling/SELECTED_ALGORITHM.md).

## 5. Restricted analysis

The reference implementation proves capacity safety by induction, exact-prefix safety by equality and generation checks, and no-future-information by call-path inspection plus a deterministic test. Under a single-candidate deterministic-cost model with no contention, immediate prefetch is sufficient when `p_L B-X >= Delta B`, where `p_L` is a lower confidence bound and `Delta` bounds the information gain from waiting. General regret and fairness guarantees are not claimed.

## 6. Experimental method

The simulator models tool starts/returns/cancellation, exact reusable length, transfer delay, four-entry GPU capacity, evictions, and five conceptual policies: LRU, TTL, static prefetch, predicted-return prefetch, and the proposed rule. The trace is synthetic, seed `20261017`, 80 sessions, and three fixed timing regimes. It is not a production trace.

## 7. Results and ablations

Mixed regime mean continuation TTFT was 10.00 LRU, 7.39 TTL, 7.39 static, 7.63 predicted, and 8.93 proposed. Proposed prefetches were 13 with 9,300 transfer bytes, compared with 80 and 36,620 for static. In the early regime proposed was 8.13 versus TTL 6.61; in late regime proposed was 9.42 versus TTL 9.53. Thus the proposed controller reduces speculative work and remains competitive in late uncertainty, but does not dominate.

## 8. Counterexamples and threats

Long tools, simultaneous returns, bandwidth saturation, sub-agent sharing, remote workers, and forecast revisions can invalidate the simple model. The early-return TTL win is a recorded negative result. Synthetic forecasts may not match calibrated production estimators. No GPU, real engine, energy, P99 queueing, or statistically powered held-out workload result is claimed.

## 9. Conclusion

Uncertain continuation behavior may be exploitable beyond existing agent-aware systems through a joint exact-prefix/return-time admission rule with an option to wait, but this study establishes only a reference-level hypothesis. The next decisive experiment is a version-pinned engine integration with real lifecycle signals and matched queueing interference.

## Reproducibility appendix

See [README](../research/agentic_kv_cache_scheduling/README.md), [formal model](../research/agentic_kv_cache_scheduling/FORMAL_ONLINE_MODEL.md), [results](../research/agentic_kv_cache_scheduling/EVALUATION_RESULTS.md), and [tests](../research/agentic_kv_cache_scheduling/tests/test_simulator.py).

