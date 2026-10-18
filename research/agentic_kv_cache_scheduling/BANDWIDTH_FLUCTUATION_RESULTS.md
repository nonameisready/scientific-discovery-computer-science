# Repeated bandwidth fluctuation result

This sweep used four bandwidth schedules, three urgent-arrival counts, and
three seeds. It compares `queue_aware` with `budget_aware`.

The main pattern is mixed:

- Under a single drop, budget-aware reduced transfer traffic by 700 tokens per
  trace without changing mean TTFT.
- Under drop-and-recover, both policies were usually identical because the
  recovery allowed the queue to finish useful work.
- Under a double drop with one urgent arrival, budget-aware reduced transfer
  traffic by 250 tokens but increased mean TTFT from 2.5 to 7.0.
- With five urgent arrivals in the same double-drop schedule, the TTFT gap
  disappeared, but this was not consistent across all schedules.

Conclusion: deadline cancellation is useful for reducing network work during a
shock, but it is not unconditionally latency-safe. A production policy needs
to price the fallback path (CPU fetch or recomputation) before canceling, not
only the remaining network work. This is a bounded CPU simulation result and
does not justify a GPU or production claim.
