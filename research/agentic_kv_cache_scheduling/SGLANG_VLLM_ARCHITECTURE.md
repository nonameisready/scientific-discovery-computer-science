# SGLang/vLLM architecture audit

SGLang’s public HiCache documentation exposes hierarchical cache concepts and session-aware radix-cache documentation. The agentic roadmap describes an orchestrator above the engine for session/sub-agent/tool-call identification and `PREFETCH`, `DEMOTE`, and `PIN` hints. The PD roadmap discusses host destinations, L2-only decode radix cache, KV liveness, and router/engine coordination. These are the relevant integration surfaces, but roadmap language is not treated as shipped behavior.

vLLM is the implementation target reported by CacheScout and already has prefix caching and request scheduling. A real integration would need an explicit session/tool lifecycle channel; neither engine should be assumed to expose exact future prefix length or calibrated tool-return hazards by default.

Sources: [SGLang HiCache](https://docs.sglang.io/docs/advanced_features/hicache), [SGLang agentic roadmap](https://github.com/sgl-project/sglang/issues/43098), [SGLang PD roadmap](https://github.com/sgl-project/sglang/issues/43699), [vLLM repository](https://github.com/vllm-project/vllm), [CacheScout](https://arxiv.org/abs/2608.14624).

