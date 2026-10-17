# GPU integration plan

No integration patch was applied. The preferred first target would be a version-pinned vLLM V1 fork because its public scheduler exposes a unified token budget, speculative token accounting, KV manager, and prefix-cache structures. The exact hook is immediately before scheduler commit of token allocations and KV blocks; an adapter would need actual transient workspace bytes, accepted-token bytes, prefix references, SLO slack, and post-step eviction/recompute counters.

Required first experiment: one NVIDIA A100/H100, pinned vLLM commit, target/draft model revisions, fixed KV dtype/block size, identical traces, fixed capacity, and three or more independent arrival seeds. Compare vLLM default, acceptance-adaptive, Spexis where compatible, and RASP. Primary metric is SLO goodput; correctness mismatches are a hard failure. This experiment requires explicit GPU authorization and was not run.
