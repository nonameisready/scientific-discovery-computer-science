# Implementation-consistency audit

Date: 2026-10-17. Scope: compare the CPU stress model with the inspected
SGLang HiCache implementation and the version-pinned integration plan. This
is an audit of assumptions, not a GPU result.

## Assumption matrix

| Simulator assumption | Reality supported by source/docs | Status for this project |
|---|---|---|
| GPU, CPU/host and optional remote tiers exist | SGLang has `UnifiedRadixCache`, host load-back, and an optional storage-backed L3 path | Supported at architecture level; exact tier semantics are version-dependent |
| Cache capacity can be represented in tokens | The engine allocates KV pools/pages and tracks component residency; token counts can be derived, but allocation is page/layer based | Usable proxy, must log page counts and bytes in a real run |
| Transfers have a queue/backlog and asynchronous completion | The HiCache pipeline and controller plan transfers and layer completion events; load-back can overlap scheduler/forward work | Supported conceptually; simulator's one global token/tick bandwidth is only a proxy |
| One bandwidth number describes all migration | Real transfers are per layer and backend/path, with staging, events, and possibly RDMA/storage-specific behavior | Not faithful; replace with measured bytes/sec per path |
| A transfer can be canceled at an arbitrary deadline | The audit found no stable public sidecar API for canceling arbitrary in-flight cache transfers | Unverified; current `budget_aware`/`fallback_aware` behavior is a controller abstraction |
| Scheduler can issue `PREFETCH`, `DEMOTE`, and `PIN` directly | The inspected roadmap/RFC discusses these hints, but the source audit did not verify a stable public API | Unverified; the adapter must remain a hint receipt, not an engine action |
| TTL directly controls GPU residency | Real HiCache residency is governed by engine eviction/write-through/load-back paths; a stable public TTL control was not verified | Baseline is conceptual until implemented through engine hooks or a trace replay |
| Exact prefix compatibility is one integer length | The engine must match token/prefix identity and component/layout validity; unified cache can have component-specific holes | Incomplete proxy; require prefix hash, model/layout, component validity and matched token count |
| CPU/remote fallback is immediately available for the whole prefix | Host/storage load-back is asynchronous and can fail, race with eviction, or leave incomplete data; recent upstream issues document these failure modes | Over-optimistic; simulator must charge measured admission, queue and failure time |
| Priority can reorder migration work | Request scheduling and load-back admission exist, but a public cache-transfer priority contract was not verified | Needs explicit engine instrumentation before claiming priority-aware migration |
| TTFT cost is a fixed tier constant | Real TTFT includes scheduler queueing, layer-wise load-back, synchronization, compute overlap and worker locality | Not faithful; use event timestamps and report decomposed latency |

## What is actually validated

The CPU model validates a bounded mechanism hypothesis under an explicit,
leakage-free information boundary. It does not validate a production cache
controller. The strongest surviving result is conditional: under some
capacity/bandwidth regimes, a current-cost-aware policy improves urgent-request
latency against the corrected TTL baseline.

The source audit supports using a sidecar event envelope, but not mutating
engine internals from the sidecar. The engine must remain authoritative for
exact prefix matching, page allocation, transfer completion, liveness and
failure handling.

## Minimum pre-GPU instrumentation gate

Before renting GPU time, the selected engine commit must emit, for every
request and transfer:

1. request/session id, priority, worker and arrival/return timestamps;
2. model revision, cache layout/component identity and exact matched token count;
3. GPU/host/storage residency before and after each event;
4. bytes, layers, source, destination, enqueue/start/complete/cancel timestamps;
5. transfer generation and failure reason for stale or aborted work;
6. TTFT decomposition into queue wait, load-back wait, compute and fallback;
7. GPU memory peak and active-request interference counters.

The correctness gate is that a cached continuation must produce the same output
as a no-cache replay for the same prompt/model, and a canceled or stale
transfer must never be treated as a valid cache hit. The performance gate is a
paired replay of the same priority trace under TTL and unified-aware policies;
no claim should be made from aggregate throughput alone.

## Decision

The current model is sufficient to prioritize a narrow GPU experiment, but not
to justify a broad production claim. The first real run should target the
previously identified boundary (GPU capacity 1000--2400 token-equivalents and
measured migration bandwidth corresponding to the 200--400 simulator regime),
with one engine commit, one model revision, explicit priority traces, and raw
event logs. If the required event fields cannot be collected, stop at a
feasibility result rather than renting several hours of GPU time.

Primary source anchors: [SGLang UnifiedRadixCache source](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/mem_cache/unified_radix_cache.py),
[SGLang HiCache load-back race](https://github.com/sgl-project/sglang/pull/31427),
[SGLang load-back transfer threading issue](https://github.com/sgl-project/sglang/issues/38470),
and [SGLang L3 stub/load-back issue](https://github.com/sgl-project/sglang/issues/38452).

The repository now includes `src/event_logger.py`, an engine-neutral validator
for this minimum event stream. It does not claim to collect events from
SGLang/vLLM; it makes the acceptance checks executable once an engine adapter
exists.

The CPU-only smoke protocol is in
`scripts/run_event_log_smoke.py`. It exercises valid completion/cancellation
lifecycles and intentionally invalid stale-generation/unfinished-transfer
cases; it is a logging check, not a serving benchmark.
