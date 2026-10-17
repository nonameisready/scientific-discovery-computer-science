# RASP reproducibility

The reference harness has no third-party dependencies and is runnable with Python 3.9+. Commands:

```bash
python3 -m unittest -v research.llm_inference_joint_control.test_reference_controller research.llm_inference_joint_control.test_trace_harness
python3 -m research.llm_inference_joint_control.run_reference_evaluation
PYTHONPYCACHEPREFIX=/private/tmp/scientific-discovery-pycache python3 -m py_compile research/llm_inference_joint_control/*.py
```

All traces, capacities, batch limits, policies, and seed are in `run_reference_evaluation.py`. Output is explicitly labeled `TRACE_SIMULATED`. No model weights, credentials, GPU logs, or production-serving claims are included.
