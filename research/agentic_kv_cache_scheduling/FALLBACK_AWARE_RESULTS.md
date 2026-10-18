# Fallback-aware cancellation result

`fallback_aware` extends deadline cancellation: when an overdue GPU prefetch
is abandoned, the predicted prefix is demoted to CPU if space exists, or to
remote storage otherwise. This explicitly models the fallback cost instead of
turning cancellation into an unconditional recomputation miss.

Under the repeated bandwidth-fluctuation sweep:

- In the single-drop, one-urgent-request case, mean TTFT was 4.0 for
  fallback-aware versus 7.0 for budget-aware and 7.0 for queue-aware.
- In the double-drop, one-urgent-request case, mean TTFT was 4.0 for
  fallback-aware versus 7.0 for budget-aware and 2.5 for queue-aware.
- In recovery and oscillation cases, the policies were usually identical.
- Fallback-aware used substantially more on-demand transfer tokens because it
  preserves the prefix in a lower tier rather than recomputing it.

Conclusion: fallback-aware cancellation protects latency in some bandwidth
shock regimes, but it is not a free improvement and can lose to simply
finishing the GPU transfer. The correct decision must account for expected
future bandwidth, fallback capacity, and recomputation cost together. No GPU
or production-network claim follows.
