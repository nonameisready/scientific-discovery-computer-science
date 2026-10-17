# Prior-art comparison and novelty boundary

The target URL is currently a 404, so no claim is made about its authors' implementation or novelty.

| Dimension | Existing systems | Proposed research question |
|---|---|---|
| Speculation | Fixed/configured or acceptance/quality-aware depth; Spexis selective speculation | Can depth be selected from the marginal *peak memory opportunity cost* rather than acceptance alone? |
| KV accounting | Paged allocation, prefix sharing, eviction, recomputation | Can transient draft workspace and accepted persistent KV be charged separately at each decision? |
| Prefix reuse | Hash/radix caches and LRU-like eviction | Can measured reuse value enter admission without pretending future requests are known? |
| Feedback | Runtime metrics and scheduler state | Can observed pressure, evictions, and recompute events update bounded shadow prices online? |
| Tail latency | SLO-aware/priority systems exist | Can SLO debt be a tie-breaking utility while hard memory safety remains dominant? |

The contribution is therefore not “joint scheduling and speculation.” That is prior art. It is a bounded, trace-testable hypothesis about the *accounting interface* between these decisions. It must be rejected if source inspection finds the same ledger and update rule in a prior system, or if controlled GPU tests show no interaction benefit over a tuned acceptance-aware baseline.
