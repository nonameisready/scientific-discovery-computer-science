# RASP: a research hypothesis for joint KV-aware speculative serving

## Abstract

This manuscript presents RASP, a trace-level policy hypothesis for serving systems that jointly choose admission and speculative depth under GPU KV pressure. RASP distinguishes transient draft workspace from persistent accepted-token KV, and prices both with observable pressure, eviction/recompute feedback, prefix-reuse value, and SLO debt. The package contains a deterministic reference implementation and invariant tests, but no GPU or end-to-end serving evaluation. The contribution is therefore an implementation-ready hypothesis, not an experimentally validated result.

## Introduction

Paged KV allocation, continuous batching, prefix caching, and speculative decoding are individually mature. The unresolved systems question studied here is how their memory consequences should be valued at the same scheduling boundary. This question matters most under tight memory, bursty arrivals, low acceptance, and multi-turn prefix reuse.

## Related work

vLLM provides paged KV management, prefix caching, token-budget scheduling, and speculative execution. SGLang provides radix/tree-style reuse, static KV pools, and several speculative modes. Spexis adds speculative-parallel execution and lookahead/eviction-aware scheduling. These systems rule out a novelty claim based merely on combining scheduling and speculation.

## Formal problem

At each step, request i exposes queue demand, resident KV, acceptance estimate, prefix reuse value, SLO debt, and age. A draft length s has peak transient cost proportional to s and persistent cost proportional to expected accepted tokens. Decisions must fit capacity minus reserve and a batch-token budget.

## Method

RASP maintains exponentially smoothed pressure and eviction shadow prices. For every request and feasible draft length it scores expected accepted work plus prefix/SLO value minus peak pressure and persistent eviction costs. It then greedily admits candidates in score order while delegating actual allocation and verification correctness to the engine.

## Algorithm

The complete pseudocode and reference code are in `research/llm_inference_joint_control/ALGORITHM_PSEUDOCODE.md` and `reference_controller.py`. Complexity is O(nK log n) per scheduling step.

## Theoretical properties

The reference policy has a simple hard-feasibility invariant: returned decisions fit the configured peak-memory reserve and batch budget, and rejected tokens are not counted as persistent KV. No throughput or regret theorem is claimed.

## Experimental protocol

Compare vLLM/SGLang defaults, fixed and acceptance-adaptive speculation, memory-only and scheduling-only controls, Spexis where reproducible, and RASP. Use independent trace seeds, exact peak-memory telemetry, correctness checks, goodput-under-SLO as the primary metric, and factorial ablations separating scheduling, KV admission, speculation, and interaction.

## Actual validation and limitations

Only deterministic unit tests and Python compilation were run. The target URL was a GitHub 404; no target source was available. The machine lacks GPU/CUDA/PyTorch/vLLM/SGLang. Prefix values, byte layouts, transfer costs, and acceptance dynamics are not empirically calibrated. The strongest failure mode is stale prefix valuation under workload phase shifts.

## Conclusion

RASP is a falsifiable implementation-ready research direction. Its value is unestablished until a controlled GPU experiment shows an interaction effect over tuned baselines and until source inspection confirms that the ledger is not already implemented.

## References

1. Kwon et al., “Efficient Memory Management for Large Language Model Serving with PagedAttention,” SOSP 2023.
2. Leviathan et al., “Fast Inference from Transformers via Speculative Decoding,” ICML 2023.
3. Li et al., “EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees,” EMNLP 2024.
4. Jung et al., “Spexis: Speculative Lookahead Scheduling for LLM Inference,” arXiv:2609.34370, 2026.
5. vLLM scheduler and automatic prefix-caching documentation, accessed 2026-10-17.
6. SGLang speculative-decoding documentation, accessed 2026-10-17.
