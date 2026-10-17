# GPU readiness checklist

## Current status

The experiment is **not yet ready to rent a GPU for the RASP comparison**. The baseline protocol and collection scripts are prepared, but RASP has not been integrated into a real vLLM/SGLang scheduler. Running now would measure the baselines only and cannot answer whether RASP helps.

## Fixed first rental

Use one A100 80GB, 4 hours, Python 3.10/3.11, at least 32GB host RAM and 100GB disk. Use the exact settings in `gpu_experiment_config.json`. Download target and draft models once, run the preflight, then run a three-request smoke test before any matrix run.

## Prepared commands on the rented machine

```bash
bash research/llm_inference_joint_control/gpu_preflight.sh
bash research/llm_inference_joint_control/start_vllm_baseline.sh
python3 research/llm_inference_joint_control/send_trace.py \
  --base-url http://127.0.0.1:8000/v1 \
  --trace research/llm_inference_joint_control/gpu_trace.jsonl \
  --output /tmp/rasp-gpu-baseline.jsonl
```

The final comparison must not start until an engine adapter can route the same scheduling observation into RASP and return a real speculation/admission decision. That adapter is the remaining implementation task; no GPU result should be claimed before it exists.
