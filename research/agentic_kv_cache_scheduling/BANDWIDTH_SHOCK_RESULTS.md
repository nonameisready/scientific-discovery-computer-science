# Dynamic bandwidth-shock result

This follow-up starts a long migration at 800 tokens/tick, drops bandwidth to
50 tokens/tick at time 2, and injects two urgent arrivals at times 4 and 5.
Three seeds compare `queue_aware` with `budget_aware`.

| Policy | Mean TTFT | Budget cancellations | Transfer tokens |
| --- | ---: | ---: | ---: |
| queue-aware | 6.0 | 0.0 | 3,450 |
| budget-aware | 6.0 | 1.0 | 2,750 |

The budget gate triggered in all three seeds and reduced transfer traffic by
700 tokens per trace without worsening mean TTFT. This supports the narrow
claim that deadline cancellation is useful under an actual mid-flight
bandwidth shock. It does not establish a general serving improvement: the
trace is synthetic, the urgent requests are fixed, and no GPU or real network
was used.
