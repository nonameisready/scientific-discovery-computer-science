# Uncertainty-aware predictive KV-cache scheduling

This isolated package studies predictive KV management for multi-turn agents that pause on tools. It is a CPU reference study, not a GPU or production-engine result.

Status: `SOURCE_GROUNDED_HYPOTHESIS`, `IMPLEMENTATION_READY_ALGORITHM`, `REFERENCE_LEVEL_VALIDATED`, `THEORY_SUPPORTED`; not GPU-empirically validated.

The selected mechanism is a robust, option-aware prefetch controller. It combines an online return-time survival estimate with an exact-prefix survival estimate, subtracts transfer/residency/interference costs, and reserves a value for waiting for more information. It never treats semantic similarity as a cache hit.

Run the bounded validation:

```bash
python3 research/agentic_kv_cache_scheduling/tests/test_simulator.py
python3 - <<'PY'
import sys
sys.path.insert(0, 'research/agentic_kv_cache_scheduling/src')
from simulator import generate_trace, run
print(run(generate_trace(20261017, 80, 'mixed'), 'proposed', capacity=4))
PY
```

The simulator, tests, and machine-readable output are in `src/`, `tests/`, and `results/`.

The second stress model, `src/stress_simulator.py`, adds GPU/CPU/remote tiers, shared-prefix branches, transfer queues, bandwidth contention, cancellation, and forecast revisions. Its stress result is intentionally negative for the current controller under severe bandwidth pressure; see `results/stress_scenario.json`.

The follow-up research question is frozen in
`MULTI_TIER_MIGRATION_HYPOTHESIS.md`. The new `tier_aware` policy explicitly
chooses GPU prefetch, CPU/remote retention, or later recomputation. This is a
CPU reference experiment; it is not a production network or GPU result.
The capacity/bandwidth/return-window boundary result is summarized in
`MIGRATION_BOUNDARY_RESULTS.md`.
The transfer-ordering follow-up is summarized in
`QUEUE_SCHEDULING_RESULTS.md`.
The deadline-budget follow-up is evaluated by the same reproducible sweep.
Its result and current no-effect boundary are recorded in
`ADMISSION_BUDGET_RESULTS.md`.
The dynamic bandwidth-shock validation is recorded in
`BANDWIDTH_SHOCK_RESULTS.md`.
Repeated-shock and urgent-arrival trade-offs are recorded in
`BANDWIDTH_FLUCTUATION_RESULTS.md`.
The fallback-aware cancellation comparison is recorded in
`FALLBACK_AWARE_RESULTS.md`.
