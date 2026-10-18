# Random bandwidth stress result

This is a paired, local stress experiment. Each of 20 deterministic seeds
generates the same request trace and piecewise-constant bandwidth process for
all five policies. The simulator uses forecast tokens for admission and only
uses realized exact tokens at return time. This is still a synthetic simulator,
not a GPU or production result.

The predeclared question is whether `unified_aware` is a stable compromise,
rather than a winner on a few hand-written traces. The falsification gate is
that it must remain within 10% of the best policy on both mean and P95 TTFT,
and within 10% of the lowest transfer traffic. Failure means the controller is
not yet stable enough to justify renting GPU time for a claim of algorithmic
benefit.

Run with:

```text
python3 research/agentic_kv_cache_scheduling/scripts/run_stochastic_bandwidth_sweep.py
```

The raw paired rows and aggregate values are in
`results/stochastic_bandwidth_sweep.json`. Interpret the outcome together with
the Pareto result: a policy can be useful without dominating every metric, but
that is a trade-off result, not evidence of universal superiority.

## Observed result

The 20 paired traces did not pass the stability gate. The aggregate mean TTFT
was 1.92 for `ttl`, compared with 4.25 for `queue_aware`, 4.47 for
`budget_aware`, and 4.36 for both `fallback_aware` and `unified_aware`.
`ttl` used zero migration-transfer tokens in this model and had 0.70 mean
recompute misses; the other policies used roughly 4,260--4,305 transfer
tokens and had 1.95--2.10 mean recompute misses. Mean P95 TTFT was 6.4 for
`ttl` and 10.0 for every other policy.

This is a negative result for the present controller, not a claim that TTL is
better in real serving systems. The result is conditional on this simulator's
cost model: fixed GPU retention is cheap, while transfer traffic and lower-tier
fetches are charged explicitly. It does mean that another hand-tuned policy or
a GPU run is not justified yet. The next useful work is to audit this model
against an actual cache implementation and identify the workload condition
under which retention capacity is insufficient; only then can GPU validation
test a live, falsifiable claim.
