# Joint KV-aware LLM serving research

Status: **NOVELTY_NOT_ESTABLISHED / reference-level negative audit; not GPU validated**.

The user-supplied repository URL was checked on 2026-10-17 and returned GitHub 404. No code, commit, README, or results from that URL are treated as evidence. Public sources were used instead. The package is isolated from the existing forecasting and Paper 3/4 records.

The controller was audited as a falsifiable extension of existing memory-aware and speculative schedulers. It prices the *peak transient draft workspace* separately from *expected persistent accepted-token KV*, and includes observable prefix-reuse value and SLO debt in the same admission decision. Prior-art review did not establish novelty, and the bounded trace matrix found losses to simpler baselines. The reference implementation and harness remain useful as a negative research artifact.

Run the local checks from this directory:

```bash
python3 -m unittest -v research.llm_inference_joint_control.test_reference_controller
python3 -m py_compile reference_controller.py test_reference_controller.py
```

No GPU, model, serving engine, cloud resource, or production code was run.
