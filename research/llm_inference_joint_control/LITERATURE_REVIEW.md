# Literature review

The review is bounded to primary papers and official implementation documents available on 2026-10-17.

| Work | What it solves | Remaining gap relevant here |
|---|---|---|
| PagedAttention/vLLM (Kwon et al., SOSP 2023) | Paged KV allocation and high-throughput continuous batching | Allocation is not by itself a joint utility controller for draft workspace, accepted KV, prefix value, and SLO debt. |
| Leviathan et al. (ICML 2023) | Lossless draft/verify speculative decoding | Does not define serving admission under shared KV pressure. |
| EAGLE/EAGLE-2 (ICML 2024; EMNLP 2024) | Better draft quality and dynamic trees | Draft quality/branching does not equal a memory-pressure admission policy. |
| vLLM V1 scheduler (v0.13.0 docs) | Token-budget scheduling, KV manager, prefix caching, speculative lookahead tokens | The public scheduler exposes token and KV feasibility, but the policy proposed here is a separate shadow-price objective. |
| SGLang Speculative Decoding V2 docs | Overlap scheduler, EAGLE/standalone/MTP variants, static memory fraction | Current flags constrain the pool and speculation; no published evidence of the proposed prefix/SLO opportunity-cost controller. |
| Spexis (arXiv:2609.34370; code fork vLLM v0.8.4) | Speculative-parallel execution plus confidence/length-aware lookahead and eviction-aware cost model | It is the strongest counterevidence to naive novelty claims. The proposed distinction is the explicit transient-versus-persistent KV ledger with online event prices and prefix reuse value; this remains an unverified novelty hypothesis. |
| SpecStream (arXiv:2609.33184) | Overlap KV restoration and drafting for long-context/offload settings | Focuses on transfer/verification overlap, not the same admission objective. |
| SPECTRE (arXiv:2605.08151) | Hybrid ordinary/parallel speculation and priority scheduling | Threshold and overlap policy differ from the proposed memory opportunity-cost ledger. |

Primary links: [vLLM scheduler](https://docs.vllm.ai/en/v0.13.0/api/vllm/v1/core/sched/scheduler/), [vLLM prefix caching](https://docs.vllm.cc/en/latest/design/automatic_prefix_caching.html), [SGLang speculative decoding](https://github.com/sgl-project/sglang/blob/main/docs/advanced_features/speculative_decoding.md), [Spexis paper](https://arxiv.org/abs/2609.34370), [Spexis code](https://github.com/mlsys-seo/spexis).
