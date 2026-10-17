# vLLM v0.13.0 source audit

Pinned source:

- repository: `https://github.com/vllm-project/vllm`
- tag requested: `v0.13.0`
- resolved commit: `72506c98349d6bcd32b4e33eec7b5513453c1502`
- checkout: `/private/tmp/vllm-ramp-v0.13.0`

## Confirmed scheduler surfaces

- `vllm/v1/core/sched/scheduler.py::Scheduler.schedule()` owns the token budget and builds `num_scheduled_tokens` and `scheduled_spec_decode_tokens`.
- The scheduler calls `KVCacheManager.allocate_slots(..., num_lookahead_tokens=self.num_lookahead_tokens)`.
- The stock path uses one scheduler-level `num_lookahead_tokens`, not a RASP-selected per-request budget.
- Preemption is performed inside `Scheduler.schedule()` through `_preempt_request` and the running queue.
- `KVCacheManager.usage` exposes a global utilization fraction.
- `KVCacheManager.allocate_slots` receives lookahead tokens and commits only finalized `request.num_tokens` to the prefix cache; rejected draft tokens are not automatically treated as persistent target KV.
- `Request.num_cached_tokens` exists as a prefix-cache hit count, but it is not a complete per-request byte valuation.
- `SpecDecodingStats` exposes aggregate accepted/draft counters and Prometheus metrics, not a scheduler-ready per-request acceptance estimate.

## Missing fields needed by RASP

The pinned source does not expose stable Request fields for:

1. per-request acceptance rate at scheduler decision time;
2. per-request resident KV bytes;
3. explicit SLO deadline or debt.

Therefore the current RASP adapter contract is not a drop-in integration. A faithful integration needs a small vLLM fork that adds instrumentation and changes the scheduler before `allocate_slots`. It must preserve allocator ownership and target verification semantics.

Run the audit without importing vLLM:

```bash
python3 -m research.llm_inference_joint_control.check_vllm_source_audit \
  --vllm-root /private/tmp/vllm-ramp-v0.13.0
```

The source audit is a blocker report, not a performance result.
