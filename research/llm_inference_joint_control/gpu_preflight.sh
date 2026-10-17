#!/usr/bin/env bash
set -euo pipefail

echo '== RASP GPU preflight =='
command -v nvidia-smi >/dev/null || { echo 'FAIL: nvidia-smi missing'; exit 2; }
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
python3 --version
python3 - <<'PY'
import importlib.util
for name in ('torch', 'vllm', 'transformers'):
    spec = importlib.util.find_spec(name)
    print(f'{name}: {"installed" if spec else "MISSING"}')
if importlib.util.find_spec('torch'):
    import torch
    print('torch.version.cuda:', torch.version.cuda)
    print('torch.cuda.is_available:', torch.cuda.is_available())
    if not torch.cuda.is_available():
        raise SystemExit('FAIL: CUDA is not available')
PY
df -h .
echo 'PASS: preflight checks completed; do not start the matrix until all dependencies are installed and model paths are fixed.'
