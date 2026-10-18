# Transfer-queue follow-up

The queue follow-up adds `queue_aware`: when several GPU prefetches are in
flight, it gives the full bandwidth to the transfer with the earliest forecast
deadline, breaking ties by remaining tokens. Existing policies split bandwidth
equally. This is a deliberately simple queue policy, not an optimal scheduler.

Across the 81 boundary units per policy:

| Policy | Mean TTFT | Recompute misses | Completed transfers |
| --- | ---: | ---: | ---: |
| TTL | 6.185 | 8.44 | 0.00 |
| GPU-only proposed | 9.709 | 14.48 | 0.33 |
| tier-aware | 8.726 | 11.30 | 0.48 |
| cost-aware | 8.807 | 11.41 | 0.70 |
| queue-aware | 8.681 | 11.22 | 0.56 |

The queue policy is directionally better than equal-sharing tier-aware on mean
TTFT and recomputation, but the effect is small and it still loses to TTL.
There is no evidence yet that queue ordering alone solves the migration
problem. The next useful experiment is to add an explicit transfer admission
budget: once a transfer misses its forecast deadline, cancel it and prevent it
from consuming bandwidth needed by newer urgent transfers.
