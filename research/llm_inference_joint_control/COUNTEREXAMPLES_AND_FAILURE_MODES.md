# Counterexamples and failure modes

1. A short request with low acceptance may be delayed by a high-score long request; age/SLO debt must be calibrated and starvation-tested.
2. Prefix reuse value can be wrong under a workload shift; overvaluing a never-reused prefix reduces goodput.
3. Draft bytes may be allocated in implementation-specific layouts, so token-count accounting can understate peak activation or workspace memory.
4. A high acceptance rate can still lose if draft-model compute or verification bandwidth is saturated; acceptance is not speedup.
5. Under low load, the controller can add overhead without benefit; a bypass threshold is required.
6. Offloading can turn a memory saving into transfer latency; this package does not model that path.

Strongest counterexample: with one nearly-full GPU and two requests, a reusable 100-token prefix may have high future value, but if that future turn never arrives, protecting it is strictly worse than evicting it and serving the current request. This is why prefix value must be learned from actual reuse events and tested under adversarial phase shifts.
