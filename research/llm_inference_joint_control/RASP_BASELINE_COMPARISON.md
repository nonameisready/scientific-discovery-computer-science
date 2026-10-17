# Baseline comparison

Implemented simplified baselines:

1. `fixed-4`: fixed speculative depth.
2. `accept-adaptive-4-0.5`: depth 4 only above a 0.5 observed acceptance threshold.
3. `slo-priority`: deadline-debt ordering with the same simplified depth rule.
4. `rasp`: shadow-price controller.

These are explicitly not vLLM, SGLang, or Spexis implementations. Real-engine comparisons remain unrun because no GPU stack is installed. The trace harness keeps identical capacity, batch budget, traces, and stopping rule across policies. The matrix does not support a causal claim for any component because it is a small deterministic reference study.
