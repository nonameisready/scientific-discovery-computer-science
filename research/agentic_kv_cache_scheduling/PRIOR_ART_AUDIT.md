# Prior-art audit

## Named systems

**CacheScout.** The primary paper describes online learning of agent execution transitions without predefined workflow graphs or offline training, using the learned model for eviction and proactive prefetching. It is implemented over vLLM and reports multi-agent workload experiments. This directly covers transition learning, agent-aware eviction, and predictive prefetch; those are not claimed here. The remaining distinction tested here is a conservative decision rule over two uncertainties—return time and exact reusable length—with an explicit value-of-waiting and interference price. Source: [arXiv:2608.14624](https://arxiv.org/abs/2608.14624).

**Continuum.** The Berkeley report explicitly addresses tool-call pauses, variable tool durations, reload/recompute cost, queueing delay, and a GPU TTL selected from reload cost and induced queueing delay. It evaluates agent workloads and is the strongest named baseline for retention timing. The proposed study therefore does not claim uncertain tool timing or TTL retention as new; it adds a different controller formulation only as a bounded hypothesis. Sources: [EECS report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2026/EECS-2026-234.html), [OpenReview record](https://openreview.net/pdf?id=sVzK0LC9pn).

**Vesta.** Vesta assigns an authoritative cache holder while selecting an executor per request, accounting for backlog, reusable prefixes, transfers, and queueing externalities. Joint cache locality/queue-aware routing is prior art. This package models one worker-local reference controller and does not claim Vesta’s distributed placement result. Source: [arXiv:2610.14686](https://arxiv.org/abs/2610.14686).

**SGLang.** The inspected HiCache documentation describes hierarchical caching and session-aware radix-cache features. The inspected Q4 roadmap calls for an agentic orchestrator that identifies sessions, sub-agents, and tool calls and exposes `PREFETCH`, `DEMOTE`, and `PIN` hints; it also calls for transfer-bandwidth modeling. Those roadmap items are not treated as shipped proof. Sources: [HiCache documentation](https://docs.sglang.io/docs/advanced_features/hicache), [agentic cache roadmap #43098](https://github.com/sgl-project/sglang/issues/43098), [PD roadmap #43699](https://github.com/sgl-project/sglang/issues/43699), [versioned KV hint RFC #36224](https://github.com/sgl-project/sglang/issues/36224).

## Broader boundary

vLLM and SGLang already provide prefix/radix caching; distributed serving work already studies KV transfer and cache-aware placement. Standard LRU, TTL, offload, and learning-augmented caching are baseline families, not novelty claims. A complete claim that no related work exists is not justified by this bounded audit.

## Reproducibility observations

The named papers expose source-level descriptions and reported evaluations, but the local workspace did not contain their pinned code/traces. The prototype therefore implements conceptual baselines and labels them as such; it does not call any homemade policy “the CacheScout implementation,” “the Continuum implementation,” or “the Vesta implementation.”

