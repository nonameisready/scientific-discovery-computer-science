# RASP validation plan

Status: completed reference-level audit; no GPU campaign authorized.

Primary metric was frozen before the trace run as SLO goodput: completed requests whose completion tick is no later than the request deadline. Secondary metrics were p95 completion latency, deadline misses, starvation events, peak modeled bytes, accepted tokens, and speculative tokens. Capacity was 24 units, batch budget 8, max 200 ticks, and seed/trace generation is fixed in `run_reference_evaluation.py`.

The matrix contains eight workload families: low pressure, severe pressure, burst, low acceptance, reusable prefixes, wrong prefix values, strict SLO, and starvation. Baselines are fixed depth, acceptance-adaptive depth, and SLO-priority. Results are `TRACE_SIMULATED`, not GPU measurements.
