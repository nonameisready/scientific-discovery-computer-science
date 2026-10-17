# Reproducibility plan

Pin engine commits, model/draft revisions, container image, CUDA/driver, hardware, configuration, trace hashes, seeds, and raw JSONL logs. Record exact allocator counters and verification correctness. Run each condition in randomized order after warmup, with at least three independent traces; predeclare exclusions and failure handling. Publish code/configuration and checksums, but never include credentials or restricted model weights.

The current machine cannot execute this plan: Python 3.9.6 is present, but PyTorch, vLLM, SGLang, CUDA tooling, and a GPU were not detected.
