# RASP: an adversarial reference-level audit of joint KV-aware speculative serving

## Abstract

This manuscript audits RASP, a trace-level policy hypothesis for serving systems that jointly choose admission and speculative depth under GPU KV pressure. RASP distinguishes transient draft workspace from persistent accepted-token KV, and prices both with observable pressure, eviction/recompute feedback, prefix-reuse value, and SLO debt. Prior-art review did not establish novelty, and the deterministic reference matrix found losses to simpler baselines. There is no GPU or end-to-end serving evaluation.

## Introduction

Paged KV allocation, continuous batching, prefix caching, and speculative decoding are individually mature. The unresolved systems question studied here is how their memory consequences should be valued at the same scheduling boundary. This question matters most under tight memory, bursty arrivals, low acceptance, and multi-turn prefix reuse.

## Related work

vLLM provides paged KV management, prefix caching, token-budget scheduling, and speculative execution. SGLang provides radix/tree-style reuse, static KV pools, and several speculative modes. Spexis adds speculative-parallel execution and lookahead/eviction-aware scheduling. KV-constrained online scheduling, tail-aware cache-preemption, and SLO-aware schedulers further cover the individual components. These systems rule out a novelty claim based merely on combining scheduling and speculation.

## Formal problem

At each step, request i exposes queue demand, resident KV, acceptance estimate, prefix reuse value, SLO debt, and age. A draft length s has peak transient cost proportional to s and persistent cost proportional to expected accepted tokens. Decisions must fit capacity minus reserve and a batch-token budget.

## Method

RASP maintains exponentially smoothed pressure and eviction shadow prices. For every request and feasible draft length it scores expected accepted work plus prefix/SLO value minus peak pressure and persistent eviction costs. It then greedily admits candidates in score order while delegating actual allocation and verification correctness to the engine. This is a transparent reference coupling, not an established new algorithmic principle.

## Algorithm

The complete pseudocode and reference code are in `research/llm_inference_joint_control/ALGORITHM_PSEUDOCODE.md` and `reference_controller.py`. Complexity is O(nK log n) per scheduling step.

## Theoretical properties

The reference policy has a simple hard-feasibility invariant: returned decisions fit the configured peak-memory reserve and batch budget, and rejected tokens are not counted as persistent KV. No throughput or regret theorem is claimed. The informal value hypothesis is contradicted by the reference matrix in several workload families.

## Experimental protocol

Compare vLLM/SGLang defaults, fixed and acceptance-adaptive speculation, memory-only and scheduling-only controls, Spexis where reproducible, and RASP. Use independent trace seeds, exact peak-memory telemetry, correctness checks, goodput-under-SLO as the primary metric, and factorial ablations separating scheduling, KV admission, speculation, and interaction.

## Actual validation and limitations

Deterministic unit tests, a bounded event-trace harness, eight workload families, and simplified baseline comparisons were run. RASP lost on low acceptance, burst, and severe-pressure traces and recorded starvation events in the starvation fixture. The target URL was a GitHub 404; no target source was available. The machine lacks GPU/CUDA/PyTorch/vLLM/SGLang. Prefix values, byte layouts, transfer costs, and engine preemption are not empirically calibrated.

## Conclusion

RASP is not currently a defensible novel contribution. The useful surviving artifact is a reproducible negative reference-level audit and a clear requirement for engine-calibrated traces before any GPU experiment. Further work should focus on a genuinely distinct mechanism rather than tuning the present scalar score.

## References

1. Kwon et al., “Efficient Memory Management for Large Language Model Serving with PagedAttention,” SOSP 2023.
2. Leviathan et al., “Fast Inference from Transformers via Speculative Decoding,” ICML 2023.
3. Li et al., “EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees,” EMNLP 2024.
4. Jung et al., “Spexis: Speculative Lookahead Scheduling for LLM Inference,” arXiv:2609.34370, 2026.
5. vLLM scheduler and automatic prefix-caching documentation, accessed 2026-10-17.
6. SGLang speculative-decoding documentation, accessed 2026-10-17.
