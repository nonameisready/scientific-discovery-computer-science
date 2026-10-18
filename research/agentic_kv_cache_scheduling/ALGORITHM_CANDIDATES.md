# Candidate algorithms

1. **LRU / reactive radix:** no proactive action; evict by recency.
2. **Static prefetch:** prefetch every tool-call prefix immediately.
3. **Predicted-return prefetch:** prefetch if the empirical mean return is below a fixed threshold.
4. **TTL retention:** retain a tool-call prefix without transfer, subject to capacity/expiry.
5. **Robust option-aware admission (selected):** combine return survival, forecast exact-prefix survival, transfer and displacement costs, an interference budget, and a value-of-waiting reserve.

The first four are deliberately strong conceptual categories. Candidate 5 was selected for separability and implementability, not because the bounded literature audit proves it is globally novel.

