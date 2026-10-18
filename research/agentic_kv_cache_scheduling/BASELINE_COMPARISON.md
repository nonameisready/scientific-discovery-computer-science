# Baseline comparison

The local study uses conceptual, matched-trace policies: LRU/reactive, TTL retention, static prefetch, predicted-return prefetch, and the selected controller. CacheScout, Continuum, and Vesta are not reimplemented and are not presented as exact replicas; their source-grounded mechanisms and evaluation claims are in `PRIOR_ART_AUDIT.md`.

Primary metric: mean continuation TTFT in simulator time units. Secondary metrics: workflow latency, useful-prefetch rate, wasted prefetches, transfer bytes, and evictions. The simulated workload is explicitly synthetic and not representative of all production agents.

