# Engine integration plan

1. Add an out-of-band versioned session envelope: session, sub-agent, tool start/return/cancel, exact prefix hash, model/cache layout, and forecast provenance.
2. At the router/orchestrator, compute the policy score and issue a bounded hint with a reservation generation and byte budget.
3. Let the engine remain authoritative for allocation, liveness, exact prefix compatibility, transfer completion, and failure/abort handling.
4. Implement demotion and cancellation only through existing HiCache/KV-transfer lifecycle hooks; never mutate a live radix node behind the scheduler.
5. Export per-event traces so TTFT, interference, wasted bytes, and stale-generation cancellations can be matched across policies.

This is implementation-ready at the interface level but not a patch: the inspected roadmap/RFC does not guarantee a stable upstream hint API. Real GPU validation still requires version-pinned engine source, a correctness test for exact KV reuse, and matched hardware/load experiments.

