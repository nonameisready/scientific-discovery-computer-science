# Candidate hypotheses

| Hypothesis | Novelty | Feasibility | Main falsifier | Decision |
|---|---:|---:|---|---|
| A. Joint memory admission/speculation | medium | high | no gain over tuned acceptance-aware scheduler | primary |
| B. Tail-aware slack control | low-medium | high | p99 worsens or only duplicates priority aging | secondary |
| C. Workload-shift adaptation | medium | high | adaptation lag causes regressions | secondary |
| D. Agent-aware prefix residency | medium | medium | future-turn observability unavailable | fallback |
| E. Restricted-model guarantee | high | low-medium | theorem needs unrealistic arrival/memory assumptions | theory support only |

Primary: A, refined into explicit transient/persistent KV pricing plus feedback shadows. This selection is not a claim of novelty; it is the best implementation-ready falsifiable question after Spexis is treated as a serious prior.
