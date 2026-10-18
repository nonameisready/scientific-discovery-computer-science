# Migration boundary sweep

The boundary protocol varied three GPU capacities, three bandwidth levels,
three forecast return windows, and three independent seeds. It produced 81
trace/configuration units per policy. The complete output is
`results/migration_boundary_sweep.json`.

Across all units:

| Policy | Mean TTFT | Recompute misses | On-demand lower-tier tokens |
| --- | ---: | ---: | ---: |
| LRU | 10.000 | 15.00 | 0 |
| TTL | 6.185 | 8.44 | 0 |
| GPU-only proposed | 9.731 | 14.52 | 0 |
| tier-aware | 8.726 | 11.30 | 2,281.48 |

The new policy is directionally better than GPU-only proposed: it reduces
recomputation and mean TTFT. But it does not beat TTL, and its improvement is
partly purchased with on-demand CPU/remote movement. The return-window and
capacity sweep does not establish a universal winning regime. This is a
bounded CPU-simulator result, not a GPU/network measurement.

Decision: retain the multi-tier direction, but stop adding prediction features
until the accounting and objective are clarified. The next experiment should
compare migration against recomputation with an explicit transfer-time budget
and report useful transfer tokens separately from movement overhead.
