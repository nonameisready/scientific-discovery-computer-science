# RASP engine adapter specification

This is the final pre-GPU implementation boundary. It is deliberately independent of vLLM internals so that a missing or changed vLLM symbol cannot silently invalidate the experiment.

The engine-specific patch must provide, at each scheduler step:

- request id and waiting token count;
- resident target KV bytes, not merely logical token count;
- observed speculative acceptance rate;
- current SLO debt and age;
- maximum speculation budget accepted by the runner;
- total used KV bytes, hard capacity, and batch token budget;
- pressure signal, eviction count, and recomputed-token count from the previous step.

The adapter returns per-request speculative token budgets. The engine must still perform allocation, target verification, lossless rejection sampling, prefix-cache reference counting, preemption, and rollback. The adapter must never allocate memory or claim that a draft token was accepted.

## vLLM mapping to verify on the pinned checkout

The integration patch must locate the V1 scheduler's request token counters, speculative token list, KV cache manager allocation result, prefix-cache references, and preemption/recompute events. Exact symbol names must be recorded after checking out the pinned vLLM revision. If any required field is unavailable, stop the GPU comparison and report the missing observable rather than substituting future information or logical-token estimates.

## Acceptance gate

Do not rent the GPU for RASP comparison until the following pass without GPU access:

```bash
python3 -m unittest -v \
  research.llm_inference_joint_control.test_engine_adapter
```

Then use a pinned engine checkout to implement and test the actual mapping. The current adapter is a contract plus fake-engine test, not a production vLLM patch.

`vllm_bridge.py` now implements the object-shape mapping for the pinned V1
surface and is tested with fake scheduler/KV objects. It is still not a
production patch: the missing per-request acceptance, SLO, and telemetry fields
are read from optional `rasp_*` attributes and default conservatively. A real
vLLM fork must populate those attributes and apply the returned decisions before
`KVCacheManager.allocate_slots()`.
