# Reproducibility

Environment: macOS local workspace, Python 3.9 standard library, no GPU benchmark, no external package dependency. The first attempted `pytest` command failed because pytest is unavailable; validation was rerun successfully with `unittest`.

Commands:

```bash
python3 research/agentic_kv_cache_scheduling/tests/test_simulator.py
PYTHONPYCACHEPREFIX=/private/tmp/agentic-kv-pycache python3 -m py_compile research/agentic_kv_cache_scheduling/src/simulator.py
```

The trace seed is `20261017`, 80 sessions, capacity 4. Actual reusable length is retained only for outcome scoring; `decide` sees the separate forecast field. No real trace, production data, credentials, or restricted PDF was added to the repository.

