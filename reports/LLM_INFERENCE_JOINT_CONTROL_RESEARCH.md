# LLM inference joint-control research report

Date: 2026-10-17

## Result

The most important bottleneck is not whether speculation or KV caching exists; it is the missing decision-time accounting of transient draft workspace versus persistent accepted-token KV when a request competes with reusable prefixes and SLO-critical work. Spexis already addresses speculative parallelism and lookahead memory pressure, so a generic “joint scheduler” claim would be unsound.

The package proposes RASP (Reserve-Aware Speculation Pricing): a hard-feasible greedy controller with separate transient/persistent memory accounting, observable prefix-reuse value, SLO debt, and online pressure/eviction shadow prices. It is a SOURCE-GROUNDED RESEARCH HYPOTHESIS and IMPLEMENTATION-READY ALGORITHM, not a THEORETICALLY VALIDATED performance result or EMPIRICALLY VALIDATED result.

The user-supplied repository URL returned GitHub 404; no repository implementation or result was used. Local checks covered deterministic memory-safety, accounting, feedback, tie-breaking, and Python compilation. No GPU/model serving benchmark ran because the environment has no PyTorch, vLLM, SGLang, CUDA tooling, or detected GPU, and the mission explicitly disallows unapproved large inference campaigns.

See `research/llm_inference_joint_control/` for the literature boundary, architecture map, formal model, algorithm, counterexamples, protocol, and tests. GPU experimentation remains necessary to establish any benefit.
