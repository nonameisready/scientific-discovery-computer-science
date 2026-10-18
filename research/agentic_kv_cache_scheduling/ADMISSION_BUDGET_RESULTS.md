# Transfer admission-budget result

`budget_aware` cancels an in-flight transfer once it passes its forecast
deadline while still incomplete. The unit test demonstrates the gate on a
deliberately overdue transfer, but the 81-unit boundary sweep did not trigger
the gate on average (`0.00` budget cancellations per unit).

| Policy | Mean TTFT | Recompute misses | Completed transfers | Budget cancellations |
| --- | ---: | ---: | ---: | ---: |
| queue-aware | 8.681 | 11.22 | 0.56 | 0.00 |
| budget-aware | 8.741 | 11.33 | 0.67 | 0.00 |

The budget gate therefore did not improve the current fixed-bandwidth traces.
This is not evidence that deadline cancellation is useless; it means the
current workload does not create enough mid-flight bandwidth change or queue
arrival pressure for the gate to activate. The next falsifier should inject a
bandwidth drop and urgent arrivals after transfers have started. If budget
cancellation still does not reduce stale transfer tokens or TTFT there, reject
it as unnecessary complexity.
