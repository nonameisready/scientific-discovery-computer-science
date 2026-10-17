# Formal problem

At decision epoch t, request i has observable state `x_i=(q_i, k_i, r_i, a_i, p_i, d_i, age_i)`: queued output demand `q`, resident KV tokens `k`, estimated acceptance `a` from past verification, prefix reuse value `r`, SLO debt `d`, and age. Let `b` be bytes per token/block, `C` GPU KV capacity, and `R` a safety reserve.

Action `u_i=(admit_i, s_i, evict_i)` chooses admission and speculative draft length `s_i`; eviction is delegated to the engine and is only charged, not directly fabricated by this reference policy. Expected persistent KV is `b*min(q_i,max(1,round(a_i*s_i)))`; transient draft workspace is `b*s_i`. The hard constraint is `used + Σ persistent + Σ transient ≤ C-R` and batch token budget `Σs_i≤B`.

Principal objective: maximize accepted useful work per decision epoch subject to the hard memory constraint. Secondary terms are SLO debt and prefix reuse; pressure, eviction, and recompute are costs. Arrivals may be stochastic or bursty; no adversarial competitive guarantee is claimed.

Correctness is inherited from lossless target verification: reducing speculation must never alter the target sampling/decoding semantics. The controller only chooses whether and how much to speculate.
