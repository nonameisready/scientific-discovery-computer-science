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

## Corrected observed result

The first run inherited the TTL future-information leak from the simulator.
After correcting TTL admission to use forecast tokens only, three cells passed
the two-metric gate for `unified_aware`: `(GPU=1000, bandwidth=200)`,
`(1000, 400)`, and `(2400, 400)`. For example, at `(1000, 400)`, unified
mean TTFT was 5.46 versus TTL's 7.96, and unified mean-P95 TTFT was 9.7
versus TTL's 10.0.

The effect is not universal. At low bandwidth, unified can be worse than TTL;
at `(600, 200)` and `(600, 400)` it improves mean TTFT but not mean-P95 TTFT.
The corrected evidence therefore supports a conditional claim: migration can
help when forecasts are usable and bandwidth is sufficient, but the current
controller still has a tail-latency limitation. These are simulator results,
not production or GPU evidence.
