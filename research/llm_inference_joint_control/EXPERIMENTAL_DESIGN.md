# Experimental design

No GPU experiment was authorized or run. The required future evaluation is a randomized, version-pinned comparison of vLLM default, SGLang default, fixed speculation, acceptance-adaptive speculation, memory-pressure-only, scheduling-only, Spexis where reproducible, and RASP.

Freeze before execution: target/draft model revisions, tokenizer, GPU, KV dtype/block size, capacity, arrival trace, prompt/output distributions, prefix-reuse fraction, acceptance regimes, SLO, warmup, repetitions, seed, and primary metric. Primary metric: goodput (completed requests/s meeting the SLO). Secondary: p50/p95/p99 TTFT/TPOT, accepted tokens/s, eviction/recompute, peak KV bytes, wasted draft FLOPs, and correctness mismatch count.

Use factorial ablations: scheduling only, KV admission only, speculation pricing only, and full interaction. Include low/high load, bursts, long prompts/decodes, low/high acceptance, strong/weak prefix reuse, multi-turn agent traces, and tight memory. Report paired confidence intervals over independent arrival traces; do not infer production gains from the deterministic reference tests.
