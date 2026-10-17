#!/usr/bin/env bash
set -euo pipefail

TARGET_MODEL="${TARGET_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
PORT="${PORT:-8000}"
LOG="${VLLM_LOG:-/tmp/rasp-vllm-baseline.log}"

exec vllm serve "$TARGET_MODEL" \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.75 \
  --max-model-len 4096 \
  --max-num-seqs 8 \
  --enable-prefix-caching \
  --port "$PORT" \
  2>&1 | tee "$LOG"
