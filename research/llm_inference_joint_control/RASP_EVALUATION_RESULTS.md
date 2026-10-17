# RASP evaluation results

Command:

```bash
python3 -m research.llm_inference_joint_control.run_reference_evaluation
```

Evidence label: `TRACE_SIMULATED`, seed `20261017`, capacity `24`, batch `8`, max ticks `200`.

The strongest negative observations are:

- severe pressure: RASP goodput 3, p95 9, versus acceptance-adaptive goodput 3, p95 4;
- low acceptance: RASP goodput 0, versus fixed-depth goodput 4;
- burst: RASP goodput 1, versus simple baselines goodput 6;
- starvation: RASP completed all 9 requests but recorded 6 starvation events, versus 0 for acceptance-adaptive.

Reusable-prefix and wrong-prefix fixtures had equal completion counts across policies; RASP did not demonstrate a goodput advantage. Full machine-readable output is recorded in `results/rasp_reference_eval_20261017.json`.

These are not measured GPU throughput, latency, or production observations.
