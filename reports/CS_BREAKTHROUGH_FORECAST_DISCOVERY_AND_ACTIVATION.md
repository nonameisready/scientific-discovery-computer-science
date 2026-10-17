# CS Breakthrough Forecast Discovery and Activation

**Record:** `CS-BREAKTHROUGH-FORECAST-DISCOVERY-ACTIVATION-20261017`

**Issued:** 2026-10-17 02:47:37 UTC

**Evidence cutoff:** 2026-10-17 02:47:37 UTC

**Decision:** three qualitative theorem forecasts frozen; outcome adjudication pending; monitoring inactive.

## Scope and decision

The original 2026-10-16 radar remains unchanged. All 12 broad directions were reviewed and none was silently promoted from a broad editorial direction to a prediction. I then examined 10 additional candidate questions across six fields in depth: computational geometry, algorithms/data structures and offline dynamic algorithms, parameterized graph algorithms, distributed algorithms, differential privacy, and parameterized integer programming. Three candidates passed operationalization and skeptical source-level review and were frozen below. This met the bounded search budget (12 original + 10 additional; at most 6 fields in depth; at most 8 operationalized; at most 5 frozen).

These are qualitative editorial judgments, not calibrated probabilities or evidence that Paper 3 predicts CS outcomes. Each snapshot was made at the actual issue time, with a same-time evidence cutoff. No future labels, success records, or numerical prediction scores were created. Two independent human reviews are still required for later adjudication; an LLM is not counted as a reviewer. Monitoring specifications are prepared but inactive, with no scheduled job or worker.

## Frozen events

### 1. `PLANAR-THREE-SETS-CUT-UNCUT-112`

**Question/event.** For a finite simple unweighted planar graph and disjoint sets `S1={s}`, `S2={t}`, `S3={a,b}`, will a public primary theorem by **2030-12-31** give an exact polynomial-time algorithm minimizing edge deletions that put the three terminal sets in pairwise distinct connected components while keeping `a` and `b` connected? The algorithm must return an optimum and realizing deletion set, or correctly report infeasibility; randomized algorithms must succeed on every input with probability at least 2/3. Approximation, special cases, or dropping the `a`–`b` connectivity requirement do not count.

**Baseline and significance.** Bentert et al. give a one-sided-error randomized FPT algorithm for planar Two-Sets Cut-Uncut and explicitly ask whether planar Three-Sets Cut-Uncut is polynomial-time solvable when two sets are singletons and the third has size two. This is a direct author-stated open case, not an inference from missing search results. The nearby fixed-terminal planar Multiway Cut result does not preserve the required pair's connectivity, so it does not solve this event. There is no defensible event-specific historical success rate: the exact three-set endpoint is a newly frozen problem, and adjacent results are not interchangeable trials.

**Outlook.** `HIGHLY_UNCERTAIN_WITH_DIRECTIONAL_LEAN` toward an algorithm before the deadline. The exact case is small and source-explicit, with adjacent planar cut-uncut techniques; however, the added “uncut” connectivity constraint is precisely the difficulty and related unrestricted variants are hard. The horizon is a judgment, not a base-rate estimate.

**Primary sources:** [ICALP 2024 proceedings paper](https://doi.org/10.4230/LIPIcs.ICALP.2024.22); [full author preprint](https://arxiv.org/abs/2305.01314). The preprint conclusion states the (1,1,2) open question. The preprint was available 2023-05-02; the proceedings article is dated 2024-07-02. No later matching result was found in the bounded source/citation check through the cutoff; that search observation is not a proof of continued openness.

**Adjudication.** Two independent reviewers must check the exact terminal pattern, unweighted edge deletion, planarity, connectedness of `{a,b}`, exact optimum, polynomial runtime, and feasibility reporting against the theorem and proof. A theorem covering a broader class qualifies; a restricted subclass or a relaxed objective does not. No search hit alone is not a negative. Without adequate source coverage, outcome is `INSUFFICIENT_EVIDENCE`.

**Snapshot:** `SNAP-PROSP-PLANAR-THREE-SETS-CUT-UNCUT-112-6d8f427acc00`; content SHA-256 `6d8f427acc005c14b1b3194044fd1fc30e272b13f45ff87bf90d8ed6d06b3426`; event snapshot SHA-256 `6b6bfa8354d788e520563719d1a94c6fff4687cd3570dbe386f8f922e1465aaf`.

### 2. `DISCRETE-FRECHET-TRANSLATION-PLANAR-N4`

**Question/event.** For two unrestricted `n`-vertex polygonal curves in `R²`, will a primary theorem by **2031-10-16** prove exact discrete Fréchet distance under arbitrary translation in worst-case `O(n⁴ log^C n)` time for some fixed `C`? The theorem must state its computation and arithmetic model; reviewers must establish that these assumptions are not materially stronger than the cited baseline. A decision algorithm counts only with an explicit reduction giving the same exact-value bound. Approximation, continuous Fréchet, one-dimensional curves, or restricted inputs do not count.

**Baseline and significance.** Bringmann, Künnemann, and Nusser report an exact `~O(n^(14/3))` algorithm and a conditional `n^(4-o(1))` lower bound under SETH, leaving the exponent gap open. Their historical progression includes a prior `~O(n^5)` algorithm, then `~O(n^(14/3))`; these are a few milestone results, not a statistically meaningful forecast rate. Two 2025 nearby papers improve 1D translation/scaling or continuous transformation cases but do not close the frozen 2D discrete problem. The model language is deliberately not assumed equivalent across papers: comparability is an adjudication obligation.

**Outlook.** `UNLIKELY_BEFORE_DEADLINE`. The 2D exponent gap is long-standing and the 2025 results are adjacent variants, not direct solutions. Conversely, the conditional lower bound is near the target exponent and does not rule out the desired algorithm. This is a directional editorial judgment without a numeric probability.

**Primary sources:** [2019 SODA / TALG paper, author version](https://arxiv.org/abs/1810.10982); [SoCG 2025, 1D translation/scaling](https://doi.org/10.4230/LIPIcs.SoCG.2025.22); [ICALP 2025, transformation variants](https://doi.org/10.4230/LIPIcs.ICALP.2025.36). The 2019 paper gives the exact 2D upper/lower bounds and labels closing the gap open. The two 2025 sources are cross-checks only and are not counted as progress on the event.

**Adjudication.** Two independent reviewers verify dimension, discrete versus continuous distance, unrestricted translation, exact value, asymptotic bound, and model comparability. Any mismatch or unclear computational primitive yields `UNRESOLVED`, not success. A conditional lower bound alone is not resolution; a search miss is not a verified negative.

**Snapshot:** `SNAP-PROSP-DISCRETE-FRECHET-TRANSLATION-PLANAR-N4-c47e93314cc2`; content SHA-256 `c47e93314cc25e7ff928d0ab2c8774ddc6a259fb0cfcab47f5feef91a27def98`; event snapshot SHA-256 `8e1e2607540d96fe8a54efdf8f89d5fa50f4ae73d815f6bd6b6eaf2ad14ca1e0`.

### 3. `K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH`

**Question/event.** For every fixed integer `k≥1` and graph family with the source-defined bounded `k`-hop expansion `f(k)`, will a public theorem by **2031-10-16** provide a deterministic port-numbering/LOCAL small-message algorithm with at most `3k+O(1)` rounds and approximation `C·(k+f(k)^(k/(k+1)))` for a universal constant `C`, without a girth assumption? Narrower graph classes, randomized-only results, or asymptotically weaker ratios do not count.

**Baseline and significance.** Lenzen and Wenning (SSS 2024) prove a `3k`-round `O(k+f(k)^(k/(k+1)))` result for girth at least `4k+3`, and explicitly ask whether the girth restriction is an artifact or whether the result extends to all graphs with the same expansion. The paper describes prior `O(kf(k))` approximation and its improved bound, which gives a qualitative result progression but not a reliable event base rate. The source's deterministic lower bound is close in approximation order, but it does not prove that high girth is necessary for the upper bound.

**Outlook.** `UNLIKELY_BEFORE_DEADLINE`: removing the structural hypothesis while retaining the round and approximation guarantees requires handling short-cycle structure that the current proof exploits. Counterevidence is substantial: the authors state the extension question, and high girth may be a proof convenience. No numeric probability is assigned.

**Primary source:** [Lenzen and Wenning, author preprint](https://arxiv.org/abs/2408.12998), submitted 2024-08-23; see the abstract, model definition, Theorem 1.5, and final open question. This is source-explicit, but no absence claim is made about later literature beyond the bounded check at this cutoff.

**Adjudication.** Two independent reviewers check expansion definition, every `k`, model/message assumptions, round count, universal constant, approximation order, and absence of girth restrictions. Partial progress is not success; no result located is not negative without a separate comprehensive coverage audit.

**Snapshot:** `SNAP-PROSP-K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH-e9ab8051c265`; content SHA-256 `e9ab8051c2654946acecc816ccfcebaaf16897d9d70f1bf08f7fbe9b907988ed`; event snapshot SHA-256 `6a5908e8ed403d451599174dacbb7fee1da3b10272991fa31b5d16c2991be67b`.

## Search process and rejected leads

The bounded search reviewed all 12 original radar directions and 10 additional concrete questions. Six fields were examined in depth. The original radar's adaptive-DP, verified software, code generation, agent reliability/memory, and inference-systems directions were not made into forecasts because source-native, independently decidable theorem or empirical endpoints were not yet frozen; the parent radar stays unchanged. This does not assert those directions lack scientific merit.

Additional screening included these explicit dispositions:

| Candidate | Decision and reason |
|---|---|
| Adaptive approximate-GDP filter at intermediate sampling rate | Not frozen: the 2026 paper's formal guarantees focus on asymptotic low/high rates and caution that CLT filters can be optimistic at realistic rates; a particular finite-rate threshold would be investigator-invented. [Primary source](https://arxiv.org/abs/2602.06756). |
| Polylog-update offline directed-grid reachability | Not frozen: overlaps the selected Fréchet gap and the existing offline problem has a meaningful `~O(N^(1/3))`-per-update result; polylog updates were not grounded as the next canonical milestone. |
| Two-stage stochastic-IP FPT optimization | Rejected as solved before cutoff by a June 2026 primary preprint on FPT optimization. [Primary source](https://arxiv.org/abs/2606.30330). |
| 4-block integer programming FPT | Rejected as solved before cutoff; a September 2026 preprint addresses the candidate. [Primary source](https://arxiv.org/abs/2609.23711). |
| Planar Network Diversion | Rejected as already covered by planar Two-Sets Cut-Uncut results, with later practical deterministic work; not a new open forecast. |
| Two-Sets Cut-Uncut on interval graphs | Screened, not operationalized: an IPEC 2024 source calls it open, but this bounded round did not establish later status or a distinct enough directional event. |
| Network Diversion on general graphs | Screened, not operationalized: long-standing question, but too broad and without a sufficiently tight source-grounded next milestone for this batch. |

Other candidates were reviewed within the total limit; none was substituted for a frozen event without passing the same source, scope, novelty, and adjudication gates. A non-freeze decision is not a negative scientific label.

## Provenance, immutability, and limits

- The 2026-10-16 radar bytes remain unchanged; baseline snapshot `SNAP-QUAL-EDITORIAL-20261016-184eb27b5dcb`, SHA-256 `184eb27b5dcb7cd367ed1b54ebd5847a3d52dc6fa902aa0c58bdf2fb8fb0afbd`.
- Activation snapshot: `SNAP-PROSPECTIVE-CS-58653ac8f32cf0d1`, SHA-256 `5a86daba86c299f6e92cbc0ce4f923723a7065e87dc526fb2696a99e49f6312f`.
- Activation-bundle SHA-256: `cfeaf1a813771776a84d8eb271ce1b46ba23d253ff1318af44904c49138f1806`.
- Per-source hashes identify citation-metadata records only; they are not full-text hashes or claims that source PDFs were archived.
- Monitoring is `PREPARED_INACTIVE`, with zero active specifications, no scheduled jobs, and no worker. A pre-commit audit corrected a literal placeholder milestone to each frozen event's actual deadline and added event-specific technical checkpoints plus explicit evidence/partial-progress/premise-revision/contradiction/missingness adjudication categories. The correction notice is retained in the monitoring artifact. Forecast records and append-only snapshot were not changed by these monitoring-only corrections.
- Paper 3 and Paper 4 protocols, results, cohorts, and scores were not changed. No model, experiment, benchmark, worker, or service was started. No historical labels or numeric probabilities were created.

## Scientific decision

The minimum activation condition is met: three concrete, future-dated qualitative theorem events are frozen prospectively, with explicit ambiguity/missingness rules and inactive adjudication specifications. This is a forecasting commitment, not evidence of forecasting accuracy, calibration, breakthrough discovery, or Paper 3 transfer validity. At the future deadlines, only authenticated matching theorem evidence can resolve an event; incomplete search stays censored/insufficient rather than being turned into a negative.
