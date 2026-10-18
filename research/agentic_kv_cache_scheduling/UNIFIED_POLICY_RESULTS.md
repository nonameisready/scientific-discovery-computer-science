# Unified migration decision result

`unified_aware` evaluates an overdue transfer using only current state: the
estimated cost to finish the remaining transfer, the cost of CPU/remote
fallback, and the cost of recomputation. It continues, demotes, or cancels
according to the cheapest current option.

The repeated bandwidth-fluctuation sweep shows a mixed but useful result:

- In the double-drop / one-urgent-request case, unified-aware matched the
  fallback policy at mean TTFT 4.0 but remained slower than queue-aware at 2.5.
- In the double-drop / three-urgent-request case, unified-aware reached 3.25,
  matching queue-aware and improving over budget-aware (5.5) and fallback-aware
  (4.75).
- In recovery and oscillation cases, all policies were usually identical.

The unified rule is therefore a better compromise than fixed cancellation or
fixed demotion, but it is not universally optimal. It still uses more lower-tier
movement than queue-only in some regimes. This remains CPU simulation evidence;
no GPU or physical-network claim is made.
