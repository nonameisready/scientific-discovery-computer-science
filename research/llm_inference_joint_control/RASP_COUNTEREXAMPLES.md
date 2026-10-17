# RASP counterexamples and deterministic observations

| Scenario | Observation | Evidence level |
|---|---|---|
| Low acceptance | RASP completed 0/6 in the fixed-capacity fixture; fixed depth completed 6/6. | DETERMINISTIC_TRACE |
| Severe pressure | RASP goodput 3, p95 9; acceptance-adaptive goodput 3, p95 4. | DETERMINISTIC_TRACE |
| Burst | RASP goodput 1 versus 6 for the simple baselines; starvation count 1357. | DETERMINISTIC_TRACE |
| Wrong prefix value | RASP matched completion count but had p95 5 versus 2 for simple baselines. | DETERMINISTIC_TRACE |
| Starvation | RASP completed all requests but recorded 6 starvation events; acceptance-adaptive recorded 0. | DETERMINISTIC_TRACE |
| Reusable prefix | RASP matched completion/goodput but did not improve p95. | DETERMINISTIC_TRACE |

The main counterexample is a high-pressure, low-acceptance workload: the score can spend scarce batch/memory budget on speculative work that produces little progress, while a simpler conservative controller makes more reliable progress. The harness does not yet model engine-level preemption/host offload; therefore these observations are reference-policy failures, not claims about production engines.
