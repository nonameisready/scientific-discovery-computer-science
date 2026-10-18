# Selected algorithm: robust option-aware admission

For each tool start, estimate `p_hat` from completed tool durations observed so far and `q_hat` from the available prefix-length forecast. Set `epsilon=0.20` as a conservative calibration reserve in the reference study. Compute saved delay, transfer, displacement, and interference charges. Admit only if the robust score exceeds the option value of waiting.

```text
on_tool_start(session i, observable state x_t):
    p <- empirical_survival(history, elapsed=0)
    q <- clamp(prefix_length_forecast(i) / prefix_length(i), .05, .99)
    robust_p <- max(0, p*q - epsilon)
    score <- robust_p*saved_delay(i) - transfer_cost(i)
             - displacement_cost(cache, i) - interference_cost(active)
    wait_value <- option_coefficient * (1-robust_p) * saved_delay(i)
    if score > wait_value and score > 0:
        reserve bounded transfer capacity
        PREFETCH_GPU; record generation and exact prefix key
    else:
        DEFER

on_tool_return(i, observed exact prefix key):
    accept only a generation-compatible exact key/layout
    cancel stale reservations; admit or recompute under capacity invariant
    update duration history and prefix-survival statistics
```

The implementation is in `src/simulator.py`. It uses a conservative exact-token-length equality check for a hit. No future return or exact reusable length is read by `decide`; the trace supplies a separate forecast field as an observable predictor and retains actual length only for outcome scoring.

