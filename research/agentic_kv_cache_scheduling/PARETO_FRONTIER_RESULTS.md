# Fair Pareto comparison

The same trace is evaluated by every policy in
`results/bandwidth_fluctuation_sweep.json`. This analysis treats lower mean
TTFT, lower transfer tokens, and fewer recomputation misses as better, and
computes a Pareto frontier separately for each fixed seed, bandwidth schedule,
and urgent-arrival count.

The frontier is deliberately descriptive: it does not assign weights to
latency, network traffic, or recomputation, and it does not pool the 36 units
into a production-workload estimate. A policy appearing on the frontier means
only that no other tested policy is no worse on all three metrics for that
fixed unit.

Observed frontier counts over 36 fixed units were: `budget_aware` 36,
`unified_aware` 33, `fallback_aware` 30, and `queue_aware` 24. The absence of
a single policy dominating all units is the main result; migration traffic,
fallback latency, and recomputation are genuine competing objectives in this
model.
