# Version-specific architecture map

## vLLM

The vLLM V1 scheduler documentation (accessed 2026-10-17) describes a unified token view: each request tracks `num_computed_tokens` and `num_tokens_with_spec`; the scheduler allocates scheduled tokens, KV blocks, preemptions, and speculative-decode tokens. Its KV manager is created with prefix-caching and EAGLE-related configuration. Automatic prefix caching maps logical blocks to hashed physical blocks and evicts unreferenced blocks with an LRU-like rule.

Observable insertion point: immediately before `schedule()` commits new/resumed/running requests and `req_to_new_blocks`. The proposed policy would need a serving-engine adapter that reports transient draft bytes, accepted-token bytes, prefix references, SLO slack, and post-step eviction/recompute feedback. It must not bypass the engine's hard allocator.

## SGLang

Official docs expose continuous serving with static memory fraction, KV pool/page settings, and several speculation modes. Speculative Decoding V2 uses an overlap scheduler and currently restricts EAGLE top-k to 1. SGLang also has radix/tree cache behavior and disaggregated execution paths. The adapter boundary is the batch-selection/speculation worker interface, but exact source behavior is version-dependent and was not checked out locally.

## What remains unverified

Neither engine was installed (Python 3.9.6; no CUDA, PyTorch, vLLM, or SGLang available). The target repository was 404. Therefore this is an architecture hypothesis from official docs, not a source-complete integration audit.
