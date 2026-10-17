# CPU sweep result

Command:

```bash
python3 research/agentic_kv_cache_scheduling/scripts/run_multitier_sweep.py
```

The run used three deterministic seeds, five bandwidth settings (50, 100,
200, 400, and 800 tokens/tick), 16 sessions per seed, and GPU/CPU/remote
capacities of 1600/3200/6400 tokens. The machine-readable output is
`results/multitier_bandwidth_sweep.json`.

The new `tier_aware` policy reduced recomputation misses relative to the
GPU-only `proposed` policy at every tested bandwidth (for example, 32 versus
45 total misses at 50 tokens/tick across the three seeds). It also produced CPU
and remote hits instead of treating every incomplete GPU prefetch as a miss.
However, TTL still had the lowest mean TTFT in this synthetic sweep, and
`tier_aware` generated more lower-tier transfers/wasted-transfer events under
the current accounting. This is partial support for the migration mechanism,
not evidence of end-to-end superiority.

Decision: continue with bandwidth-aware placement and improve the cost model;
do not rent a GPU yet. The next falsifier is a matched sweep that separates
useful on-demand migration cost from canceled or stale transfer cost and tests
whether CPU retention remains beneficial when GPU capacity and return timing
are varied independently.
