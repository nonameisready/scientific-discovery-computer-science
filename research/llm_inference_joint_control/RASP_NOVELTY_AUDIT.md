# RASP novelty audit

| RASP mechanism | Classification | Evidence |
|---|---|---|
| Hard KV-cap admission | KNOWN_IN_PRIOR_ART | PagedAttention/vLLM and KV-constrained online scheduling. |
| Acceptance-adaptive speculation | KNOWN_IN_PRIOR_ART | vLLM/SGLang controls and speculative-decoding literature. |
| SLO/deadline priority | KNOWN_IN_PRIOR_ART | Tail-aware scheduling, Kairos, SOLA, SuperInfer. |
| Prefix-aware cache value | KNOWN_IN_PRIOR_ART | Automatic prefix caching and cache-aware scheduling. |
| Eviction/recompute-aware scheduling | KNOWN_IN_PRIOR_ART | Spexis and cache-aware preemption work. |
| One scalar score coupling all terms | KNOWN_BUT_DIFFERENTLY_COUPLED | RASP specifies one interpretable score, but the present evidence does not establish that this coupling is new or superior. |
| Online pressure shadow update | NOT_SUBSTANTIATED_AS_NOVEL | A standard feedback heuristic; no theorem or source comparison establishes novelty. |
| Transient versus persistent draft accounting | POTENTIALLY_NEW_INTERFACE DETAIL | Plausible implementation clarification, not a demonstrated algorithmic contribution. |

Narrowest defensible claim: RASP is a small reference policy that makes an explicit transient/persistent accounting choice. Novelty and value are not established. The strongest prior comparator is Spexis for speculative/memory lookahead, supplemented by KV-constrained online scheduling and tail-aware cache-preemption work.

Sources: [Online Scheduling for LLM Inference with KV Cache Constraints](https://arxiv.org/abs/2502.07115), [Spexis](https://arxiv.org/abs/2609.34370), [Beyond Prediction](https://www.microsoft.com/en-us/research/publication/beyond-prediction-tail-aware-scheduling-for-llm-inference/), [Kairos](https://ieeexplore.ieee.org/abstract/document/11666706), [vLLM V1 guide](https://github.com/vllm-project/vllm/blob/main/docs/usage/v1_guide.md).
