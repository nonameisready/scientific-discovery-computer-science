# Bandwidth-aware multi-tier KV migration

## Research question

When a paused agent session may resume with an exact KV prefix, does an
online policy that chooses among GPU prefetch, CPU retention, remote retention,
and recomputation reduce continuation TTFT under changing bandwidth and GPU
capacity, compared with GPU-only prefetch and TTL retention?

## Frozen hypothesis

`tier_aware` should reduce wasted transfers and recomputation misses at low
bandwidth while keeping mean and p95 continuation TTFT no worse than the
GPU-only `proposed` policy by more than 10%. It is not expected to dominate TTL
in every regime. The falsification gate is: if `tier_aware` fails to reduce
wasted transfers or recomputation misses in at least two low-bandwidth seeds,
or increases p95 TTFT by more than 10% in every bandwidth regime, reject the
mechanism and retain the result as a negative finding.

## Competing explanations

1. TTL may win because retaining the full prefix on GPU is cheaper than any
   migration in short or early-return workloads.
2. CPU/remote retention may avoid wasted transfers but still lose on TTFT
   because on-demand movement arrives too late.
3. The apparent benefit may be an artifact of the simulator's fixed transfer
   and recomputation costs; no production claim follows without an engine run.

## Frozen protocol

- Data: deterministic synthetic `StressSession` traces only; actual return
  duration and exact reusable length are hidden from admission decisions.
- Policies: `lru`, `ttl`, `static`, `proposed`, `tier_aware`, and `cost_aware`.
- Independent units: trace seed and bandwidth regime; no pooled per-request
  confidence claim.
- Metrics: mean/p95 continuation TTFT, wasted/cancelled/completed transfers,
  transfer tokens, CPU/remote hits, recomputation misses, evictions, and
  interference ticks.
- Exclusions: no GPU throughput, no real network measurements, no semantic
  prefix matching, and no claim of universal dominance.

The admission path uses only the explicit `prefix_survival_probability` and
return-window forecast. Realized `exact_tokens` is used only when scoring the
return outcome, not when choosing a placement.

## Boundary follow-up

The follow-up varies GPU capacity in `{800, 1600, 3200}` tokens, bandwidth in
`{50, 200, 800}` tokens/tick, and the observable return window in `{2, 8, 16}`
ticks over three independent seeds. Transfer accounting separates completed
prefetch tokens, canceled-transfer remainder, on-demand lower-tier transfer
tokens, stale-cache misses, and recomputation misses. The boundary result is
interpreted descriptively; it is not pooled as a statistical estimate of a
production workload.
