# Theoretical analysis

Established property: every returned decision satisfies the configured hard peak-memory and batch constraints, by construction. This is an implementation invariant, not a serving-engine theorem.

Proof sketch: a candidate is retained only when its `used + transient + persistent` peak is at most `C-R`; the final greedy loop repeats the same check after adding each accepted candidate. Therefore every prefix of the output is feasible, and the final sum is feasible. Since rejected draft tokens never enter `persistent`, the accounting does not silently convert rejected speculation into durable KV.

No throughput, regret, competitive-ratio, starvation, or p99 theorem is claimed. A useful future theorem would require explicit bounded arrivals, stationary acceptance, and a fully specified allocator; those assumptions are not established here.
