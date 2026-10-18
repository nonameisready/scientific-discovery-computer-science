# Migration boundary sweep

The boundary protocol varied three GPU capacities, three bandwidth levels,
three forecast return windows, and three independent seeds. It produced 81
trace/configuration units per policy. The admission path uses only the
explicit prefix-survival forecast; realized exact prefix length is outcome
only. The complete output is
`results/migration_boundary_sweep.json`.

Across all units:

| Policy | Mean TTFT | Recompute misses | On-demand lower-tier tokens |
| --- | ---: | ---: | ---: |
| LRU | 10.000 | 15.00 | 0 |
| TTL | 6.185 | 8.44 | 0 |
| GPU-only proposed | 9.709 | 14.48 | 0 |
| tier-aware | 8.726 | 11.30 | 2,281.48 |
| cost-aware | 8.807 | 11.41 | 2,281.48 |
| queue-aware | 8.681 | 11.22 | 2,281.48 |
| budget-aware | 8.741 | 11.33 | 2,281.48 |

The new policy is directionally better than GPU-only proposed: it reduces
recomputation and mean TTFT. But it does not beat TTL, and its improvement is
partly purchased with on-demand CPU/remote movement. The return-window and
capacity sweep does not establish a universal winning regime. This is a
bounded CPU-simulator result, not a GPU/network measurement.

Adding an explicit expected-cost choice (`cost_aware`) did not materially
improve on `tier_aware`. This weakens the claim that a simple scalar migration
price is sufficient. Decision: retain the multi-tier direction, but stop
adding prediction features until the objective and transfer scheduling model
are improved. The next experiment should compare migration against
recomputation with an explicit transfer-time budget and report useful transfer
tokens separately from movement overhead.

The queue follow-up gives a small additional improvement, but does not change
that decision; see `QUEUE_SCHEDULING_RESULTS.md`.
