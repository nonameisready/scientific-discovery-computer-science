# Runtime hook plan for the pinned SGLang checkout

Source commit: `3b34d9f8b6edc23216f29c1edf02d1ff0306f9de`.
The locations below were inspected statically; no source files were modified
and no CUDA code was imported.

| Event-log event | Candidate source location | Fields available | Remaining gap |
|---|---|---|---|
| `transfer_enqueue` for storage prefetch | `buffer_mode/pipeline.py:_queue_prefetch` around line 1300 | request handle, operation, host indices, accepted tokens, pool transfers | stable external transfer id and serialized prefix/model identity |
| `transfer_complete` for storage prefetch | `buffer_mode/pipeline.py:stage_completed_prefetch` around line 1581 | request handle, operation id, staged token count, storage start metadata | exact completion wall-clock timestamp must be sampled at hook |
| `transfer_enqueue` for host→GPU load-back | `buffer_mode/pipeline.py:_allocate_and_queue_load_back` around line 1883 | request, load-back id, pool transfers, device allocation | generation and stable cross-layer transfer id |
| `transfer_start` for host→GPU load-back | `managers/cache_controller.py:start_loading` around line 975 | controller start event and load ack | mapping each ack to request/prefix must be retained |
| `transfer_complete` for host→GPU load-back | `unified_radix_cache.py:loading_check` around line 3467 | ack tokens/bytes, start/finish CUDA events, duration | wall-clock event timestamp and prefix identity |
| `transfer_cancel` for pending prefetch | `unified_radix_cache.py:revoke_pending_prefetch` and pipeline capacity rejection | request id and cancellation path | does not cover arbitrary in-flight transfer cancellation |
| `request_return` / TTFT breakdown | scheduler request lifecycle plus `Req` object | request id, worker, request timestamps | priority and queue/load-back/compute timestamps need one shared logger |

## Required implementation shape

The hook should call an injected callback such as
`emit_kv_event(event_dict)` at the points above. The callback must be
best-effort and non-blocking: if logging fails, cache correctness and engine
behavior must be unchanged. It should emit the existing
`agentic-kv/events/v1` envelope and use a per-request generation maintained by
the adapter, not guessed from a transfer completion.

The callback must not invoke policy decisions, evict nodes, alter transfer
ordering, or free host/device memory. Policy comparison remains an external
experiment concern until the event-only path is validated.

## Blocking gaps before GPU execution

1. `Req`/request handles expose a request id, but a stable model revision,
   cache layout and exact prefix hash must be attached by the adapter.
2. SGLang's CUDA events provide accurate device transfer duration, but the
   logger still needs host timestamps around enqueue and request return to
   decompose end-to-end TTFT.
3. `ack.num_bytes` and `ack.num_tokens_by_pool` are available at completion;
   bytes at enqueue must be computed from the transfer objects without forcing
   synchronization.
4. `CacheOperation.id` is already monotonic in the pinned source, but it must
   be threaded through `HiCacheAck.operation_id` to correlate load-back start
   and completion safely.
5. Pending prefetch revocation is observable; arbitrary cancellation after a
   backend transfer has started is not established and must be recorded as
   `cancel_unverified`, not assumed.

The next safe implementation is therefore a source-local, opt-in logger with
no policy changes and a synthetic callback test. A GPU run is still gated on
showing a complete event lifecycle for one real load-back and one real
prefetch.

The draft probe is stored at
`patches/sglang_event_logging_v1.patch`. It is deliberately marked as a draft:
the source patch must first add `operation_id` to `HiCacheAck` and pass
`CacheOperation.id` through the ack bookkeeping. Once that small change is
validated, the start/complete correlation no longer depends on object identity.
