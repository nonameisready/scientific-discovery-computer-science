# Pseudocode

```text
on_step(requests, used, feedback):
    pressure_shadow <- 0.8*pressure_shadow + 0.2*feedback.pressure
    eviction_shadow <- 0.8*eviction_shadow + 0.2*(feedback.evictions
                         + feedback.recompute_tokens / block_bytes)
    candidates <- []
    for request i:
        best <- none
        for s in 0..min(K, i.max_spec_tokens):
            accepted <- min(i.waiting_tokens, round(max(a_min,i.acceptance)*s))
            persistent <- block_bytes * max(1, accepted)  # only for s>0
            transient <- block_bytes * s
            if used + transient + persistent <= capacity-reserve:
                score <- accepted + .25*prefix_value + .5*slo_debt
                         - pressure_price*(transient+persistent)
                         - eviction_price*max(0,persistent-prefix_value)
                keep highest score (then highest s)
        append best if it exists
    sort candidates by descending score, request id
    greedily accept while batch and hard peak constraints hold
    return decisions
```

The reference implementation is `reference_controller.py`. A production adapter must report actual allocator byte counts rather than infer them from token count.
