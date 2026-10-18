# Evaluation results

Command: `python3` with `generate_trace(20261017, 80, regime)` and `run(policy, capacity=4)`. Three fixed regimes were run: mixed, early-return, and late-return. There are 80 tool starts; cancellations reduce scored continuations to 76 or 77. Units are simulator units, not milliseconds.

| regime / policy | mean continuation TTFT | mean workflow latency | prefetches | useful rate | wasted | evictions | transfer bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| mixed / LRU | 10.00 | 18.07 | 0 | 0.000 | 0 | 0 | 0 |
| mixed / TTL | 7.39 | 15.46 | 0 | 0.000 | 0 | 75 | 0 |
| mixed / static | 7.39 | 15.46 | 80 | 0.275 | 58 | 75 | 36620 |
| mixed / predicted | 7.63 | 15.70 | 72 | 0.278 | 52 | 67 | 32220 |
| mixed / proposed | 8.93 | 17.00 | 13 | 0.692 | 4 | 9 | 9300 |
| early / TTL | 6.61 | 9.43 | 0 | 0.000 | 0 | 73 | 0 |
| early / proposed | 8.13 | 10.95 | 17 | 0.941 | 1 | 12 | 10640 |
| late / TTL | 9.53 | 34.52 | 0 | 0.000 | 0 | 76 | 0 |
| late / proposed | 9.42 | 34.40 | 8 | 0.625 | 3 | 4 | 5700 |

Interpretation: the proposed policy trades TTFT for much less speculative work and fewer evictions. It loses to TTL in the early regime and does not establish superiority. The result supports the mechanism as a robustness hypothesis, not as a validated production improvement.

