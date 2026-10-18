# Tail-latency decomposition result

The capacity-pressure sweep now records short/urgent requests separately from
long requests. A short request is defined by the frozen simulator rule
`duration <= 8`; this is a workload label, not a post-hoc outcome label. The
purpose is to avoid hiding urgent-request behavior inside one aggregate P95.

The strongest corrected cells were:

| GPU capacity | bandwidth | policy | urgent mean TTFT | urgent P95 TTFT |
|---:|---:|---|---:|---:|
| 1000 | 200 | TTL | 7.49 | 10.00 |
| 1000 | 200 | unified-aware | 4.85 | 8.95 |
| 1000 | 400 | TTL | 7.49 | 10.00 |
| 1000 | 400 | unified-aware | 4.78 | 8.95 |
| 2400 | 400 | TTL | 6.33 | 10.00 |
| 2400 | 400 | unified-aware | 3.94 | 7.45 |

The effect is conditional. At bandwidth 50, unified-aware was worse than TTL
for urgent requests in every tested capacity. At bandwidth 100, the advantage
was small or absent. The result supports a narrower hypothesis: when transfer
bandwidth is sufficient and GPU retention is constrained, current-cost-aware
migration can protect urgent requests better than a no-leakage TTL baseline.

This remains a simulator result. The next validation target is an
implementation-faithful trace with explicit request priority and a frozen
definition of urgent latency. A GPU run should target the `(1000--2400,
200--400)` boundary, not an arbitrary workload.
