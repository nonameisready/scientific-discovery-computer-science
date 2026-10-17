# Selected algorithm: RASP (Reserve-Aware Speculation Pricing)

RASP keeps two exponentially smoothed shadow prices: pressure from headroom violations/near misses, and eviction cost from evictions plus recomputed tokens. For each request and candidate draft length `s`, it computes useful accepted work plus SLO/prefix value, subtracts pressure on the full transient-plus-persistent peak and eviction cost on persistent bytes, then greedily admits highest-score candidates subject to hard capacity and batch limits.

The distinctive decision is that a low-acceptance request can still be admitted with `s=0/1`, while a high-acceptance request can be denied a larger draft if its transient workspace displaces a reusable prefix or SLO-critical request. No future request is assumed; prefix value is an observable score supplied by the cache adapter.

Complexity is `O(n*K log n)` per decision for n requests and K candidate draft lengths; state overhead is O(1) plus the returned decisions. Failure behavior is conservative: if no candidate hard-fits, do not admit it; the engine remains the authority for allocation and correctness.
