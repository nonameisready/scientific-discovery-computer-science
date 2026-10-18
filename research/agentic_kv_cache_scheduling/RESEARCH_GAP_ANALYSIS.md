# Gap analysis

| Gap | Prior-art coverage | Assessment |
|---|---|---|
| A. Return-time uncertainty | Continuum explicitly models variable tool duration with TTL; CacheScout learns execution transitions | Not open in broad form. A narrower decision-theoretic formulation remains testable. |
| B. Exact prefix preservation | Named systems use reusable prefixes, but the bounded sources do not establish a calibrated exact-length predictor | Strongest distinct gap candidate; exact compatibility must be separated from semantic similarity. |
| C. Wrong-prefetch opportunity cost | Continuum prices queueing/retention; Vesta prices queueing and transfer; SGLang roadmap calls for bandwidth modeling | Partly covered; explicit false-prefetch accounting across exact-prefix uncertainty is still a useful separable test. |
| D. Branch uncertainty | CacheScout is multi-agent; SGLang roadmap names sub-agents; branch-budget guarantees were not established in the bounded audit | Feasible extension, but not selected first. |
| E. Cancellation/demotion | SGLang roadmap/RFC discusses lifecycle and hints; Continuum TTL gives expiry | Integration problem more than established novelty. |
| F. Robust guarantees | Existing systems report evaluation and engineering mechanisms; no bounded theorem was located in this audit for the combined model | Selected only for restricted, transparent guarantees. |

Selected mechanism: **robust option-aware admission**. The controller acts only when a lower confidence bound on expected saved prefill exceeds transfer, displacement, and interference costs; otherwise it waits. This is a source-grounded hypothesis, not an established novel theorem over the literature.

