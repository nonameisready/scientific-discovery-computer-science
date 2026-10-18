# GPU-capacity pressure result

The previous random experiment allowed TTL to keep almost all prefixes on the
GPU. This follow-up holds the exact same 20 paired request traces fixed, but
varies GPU capacity over 600, 1000, 1600 and 2400 tokens and bandwidth over 50,
100, 200 and 400 tokens/tick. The question is deliberately narrow: can
`unified_aware` beat TTL on both mean and mean-P95 TTFT once GPU retention is
insufficient?

Run with:

```text
python3 research/agentic_kv_cache_scheduling/scripts/run_capacity_pressure_sweep.py
```

The raw paired rows and 16 cell summaries are in
`results/capacity_pressure_sweep.json`. A cell that only saves migration
traffic but increases latency is not counted as an algorithmic win. This is a
simulator result; it does not establish a production or GPU result.

## Observed result

No cell passed the predeclared two-metric gate. There were, however, two
boundary cells where `unified_aware` improved mean TTFT over TTL: at 600 GPU
tokens with bandwidth 200, mean TTFT was 6.54 versus 7.17; at bandwidth 400,
it was also 6.54 versus 7.17. The mean-P95 metric did not improve in either
cell (both remained 10), so these are partial signals, not wins.

At higher GPU capacities, TTL remained better on mean TTFT. The migration
controller also paid substantial transfer traffic in every cell while TTL's
measured migration traffic was zero. The current evidence therefore narrows
the viable claim: migration may help average latency when GPU retention is
severely undersized and bandwidth is moderate-to-high, but the present policy
does not control tail latency. A real GPU test should only target this narrow
boundary if cache-capacity and tail-latency instrumentation can be frozen in
advance.
