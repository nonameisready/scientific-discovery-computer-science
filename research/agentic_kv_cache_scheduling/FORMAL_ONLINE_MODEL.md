# Formal online model

At event time `t`, session `i` exposes `(sid, worker, tool_type, start_time, cancellation_state, prefix_id, prefix_tokens, cache_layout, tier, capacity, queue, bandwidth, active_requests, and forecast state)`. The actual tool return time `R_i`, exact reusable length `L_i`, and next worker are future random variables and are unavailable at admission.

The reference action set is `{PREFETCH_GPU, KEEP_GPU, DEFER, EVICT}`. CPU/remote demotion and routing are represented in the integration plan, but are not silently simulated by the small prototype.

Let `p_i(t)` be the estimated probability of return in the decision horizon, `q_i(t)` the estimated probability that the exact requested prefix remains compatible, `B_i` the avoided recomputation delay, `X_i` the transfer/residency cost, `D_i` the expected displacement cost, `I_i` the active-request interference charge, and `O_i` the value of waiting for another observation. The robust admission score is

`S_i(t) = max(0, p_hat_i q_hat_i - epsilon_i) B_i - X_i - D_i - I_i`.

Prefetch occurs only when `S_i(t) > O_i` and `S_i(t) > 0`; otherwise the controller defers. `epsilon_i` is an explicit uncertainty reserve, not a claim of calibrated probability. In the implementation `p_hat` is an empirical survival estimate with smoothing, `q_hat` is a prefix-length forecast, and the coefficients are heuristic reference-unit costs.

The primary objective is continuation TTFT under a hard GPU capacity, with end-to-end workflow latency reported separately. A policy that improves cache hit rate while increasing active-request latency is not a win.

