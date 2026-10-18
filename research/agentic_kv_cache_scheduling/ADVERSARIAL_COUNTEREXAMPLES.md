# Adversarial cases

The reference trace generator and capacity tests cover early returns, late returns, cancellations, context-changing outputs, simultaneous starts, full capacity, and small capacities. The strongest counterexample is a burst of long tool calls followed by simultaneous returns: static/predicted prefetch fills the four-entry GPU cache, causing 76 evictions and only a 5% useful-prefetch rate in the late-return run; the proposed controller still makes 8 prefetches, but keeps transfer to 5,700 reference bytes and has 62.5% useful-prefetch rate.

Other required cases are recorded as test gaps rather than invented results: transfer-bandwidth saturation, independent workers with remote KV, sub-agent shared-prefix reference counting, repeated forecast revisions/oscillation, and an active-prefix eviction cost measured against a real scheduler. A simple baseline wins in the early regime: TTL has 6.61 mean continuation TTFT versus 8.13 for the proposed controller. This falsifies any claim of universal dominance.

