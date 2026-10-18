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

## Corrected observed result

The first version of this experiment used `exact_tokens` for TTL admission.
That was a future-information leak: exact reusable length is only available at
return time. The simulator and the baseline test were corrected so TTL now
uses `forecast_tokens`, like every other policy, and the experiment was rerun
under protocol `MULTI-TIER-STOCHASTIC-BANDWIDTH-v2-no-leakage-ttl`.

After correction, TTL's mean TTFT was 6.67, while `queue_aware` was 4.25 and
`unified_aware` was 4.36. TTL had 4.05 mean recompute misses, compared with
1.95 for `queue_aware` and 2.00 for `unified_aware`. Mean P95 TTFT was still
10.0 for all policies, so the corrected result supports a mean-latency benefit
but not a tail-latency benefit.

This correction invalidates the earlier TTL-dominance interpretation. It does
not prove production benefit: the experiment remains a synthetic simulator
study, and migration traffic is still materially higher for the adaptive
policies. The next gate is to test whether the mean-latency advantage survives
an implementation-faithful cache model and whether tail latency can be reduced
without simply spending more transfer bandwidth.
