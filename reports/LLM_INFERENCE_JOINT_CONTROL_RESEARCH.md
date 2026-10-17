# LLM inference joint-control research report

Date: 2026-10-17

## Result

The most important bottleneck is not whether speculation or KV caching exists; it is the missing decision-time accounting of transient draft workspace versus persistent accepted-token KV when a request competes with reusable prefixes and SLO-critical work. Spexis already addresses speculative parallelism and lookahead memory pressure, so a generic “joint scheduler” claim would be unsound.

The package initially proposed RASP (Reserve-Aware Speculation Pricing): a hard-feasible greedy controller with separate transient/persistent memory accounting, observable prefix-reuse value, SLO debt, and online pressure/eviction shadow prices. The follow-up audit found that its mechanisms are already present in prior art or are standard couplings, and its reference policy loses to simpler baselines in key trace families. The current classification is **NOVELTY_NOT_ESTABLISHED**, with **REFERENCE_LEVEL_EVIDENCE** for a negative result.

The user-supplied repository URL returned GitHub 404; no repository implementation or result was used. Local checks covered deterministic memory-safety, accounting, feedback, tie-breaking, event traces, baselines, and Python compilation. The bounded trace matrix found RASP worse than simpler policies under low acceptance, burst, and severe-pressure conditions. No GPU/model serving benchmark ran because the environment has no PyTorch, vLLM, SGLang, CUDA tooling, or detected GPU, and the mission explicitly disallows unapproved large inference campaigns.

See `research/llm_inference_joint_control/` for the novelty audit, harness, counterexamples, baseline comparison, results, and tests. Further investment should first replace the harness with engine-calibrated preemption/offload traces; the present RASP formulation does not justify a GPU campaign as a likely positive result.
