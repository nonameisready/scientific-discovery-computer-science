# Final CS breakthrough opportunity portfolio, 2027–2031

**Evidence cutoff:** 2026-10-17 03:50:01 UTC.
**Forecast status:** `QUALITATIVE_UNCALIBRATED_FORECAST`. This is one evidence-grounded research judgment, not a measured probability, model output, or consensus of independent human forecasters.
**Scope:** 10 ranked problem families across two horizons; 12 earlier radar candidates were re-screened, the 10 frozen commitments were audited without alteration, and seven newly located primary-source leads were assessed. Closely related records are merged at the family level. No numerical probability is assigned.

## Answer in brief

The strongest near-term expectation is continued, technically measurable progress in repository-scale code-and-proof synthesis and LLM inference scheduling. The sharpest theory-facing opportunity is fully adaptive privacy accounting in the intermediate subsampling regime. Dynamic matching remains a high-significance medium-horizon opportunity, but the actual approximation target must not be confused with the already-solved sublinear maximal-matching problem. Exact resolution of any one frozen open problem is less likely than substantial partial progress. The evidence does **not** support a calibrated ranking or a claim that Paper 3 predicts CS outcomes.

“Substantive progress” here means a new theorem/bound, an algorithmic improvement against a matched baseline, an independently replicated empirical improvement, an independently checked counterexample, a justified premise revision, or a substantive narrowing of a frozen question. Publication volume, citations, popularity, topic similarity, and search hits are not success. Empirical results require artifact and comparator scrutiny; theorem claims require source-level scope matching and independent proof review. Target A (direct resolution/refutation), Target B (progress without full resolution), attention, and real-world impact remain distinct.

## Ranked near-term opportunities: 2027–2028

### 1. Repository-scale implementation *and* proof synthesis

**Question / expected progress.** Can automated systems build coherent implementations and machine-checked proofs across multi-module repositories, including cross-module invariants, rather than solve isolated obligations? The near-term expectation is better solve coverage and cost-quality trade-offs on fixed repository benchmarks, not reliable autonomous software engineering in general.

**Evidence.** Vero provides 43 multi-module instances from real repositories; its authors report that the strongest evaluated configuration completely solves 27/43 code-and-proof instances, while 10 resist all evaluated configurations. VeriSoftBench supplies 500 repository-context Lean obligations and reports that multi-hop dependency closure predicts lower solve rates. CoCo-Prover (2026-10-07 preprint) reports higher solve rates across five Lean benchmarks and up to 26/43 on Vero; this is a closely related author-reported evaluation, not an independent replication. Sources: [Vero](https://arxiv.org/abs/2608.13522), [VeriSoftBench](https://arxiv.org/abs/2602.18307), [CoCo-Prover](https://arxiv.org/abs/2610.09681).

**Obstacle / countercase.** A checked proof proves the formal specification, not that the specification matches intended behavior. Vero's finite set, benchmark curation, model/tool versions, and changing inference budgets limit comparisons. Per-specification success does not imply a complete buildable repository.

**Impact and verification.** High potential in safety-critical code, conditional on specification adequacy. Verify on frozen repository versions, hidden held-out tasks, proof-kernel checking, clean builds, independent specification audits, and equal compute/cost budgets. **Paper 4 action:** compare the benchmark protocol, task-level artifacts, and cost accounting across Vero/CoCo before proposing any new run. A new model evaluation would require separate authorization.

**Frozen event:** none. This is a new qualitative family-level forecast, not a newly frozen threshold event; the existing prospective registry is not edited.

### 2. LLM inference scheduling under KV pressure and speculative execution

**Question / expected progress.** Can a serving policy jointly schedule requests, speculative work, and KV-cache residency under changing arrivals while improving end-to-end goodput or tail latency at fixed output quality, memory, and service-level constraints? Expect configuration-specific and increasingly integrated systems improvements; do not infer a universal online guarantee.

**Evidence.** Jaillet et al. give different guarantees by arrival model and prove no constant competitive ratio in a fully adversarial model. Spexis (2026-09-28 preprint) reports up to 34% higher request rate than its best pipeline/tensor-parallel baseline across several GPUs and releases source code. This indicates a concrete new scheduling axis, not independent replication or a general 34% gain. Sources: [online KV-constrained scheduling](https://arxiv.org/abs/2502.07115), [Spexis](https://arxiv.org/abs/2609.34370), [heterogeneous KV placement](https://arxiv.org/abs/2508.13231).

**Obstacle / countercase.** Component gains can disappear under equal memory, realistic load, preemption, quality constraints, or p95/p99 SLOs. The adversarial impossibility rules out an unqualified guarantee. Evaluation protocols and hardware/model generations change quickly.

**Impact and verification.** Potentially high for cost and latency. Independently replay fixed arrival traces; match hardware, memory, model, quality and throughput objectives; report tails, energy, eviction/recompute, and code version. **Paper 4 action:** inspect whether Spexis's workload and baselines isolate scheduler gain from request-rate, quality, and memory changes; that evidence most affects this ranking.

**Frozen event:** none. Radar family `JOINT_KV_SPECULATIVE_SERVING`; not a probability.

### 3. Fully adaptive privacy filters beyond asymptotic low/high sampling regimes

**Question / expected progress.** Can valid, quantitatively tight privacy filters for adaptively selected subsampled Gaussian mechanisms extend into intermediate sampling rates, with explicit error bounds and a meaningful improvement over a fixed accountant? The expectation is progress on restricted mechanism families or better characterization, not a uniform optimal filter.

**Evidence.** Tran et al. show the naive fully adaptive f-DP filter can be invalid, characterize validity conditions, and construct an approximate GDP filter in low-rate (`q<0.2`) and high-rate (`q>0.8`) regimes. This creates a precise open middle region, but the current frozen event's baseline/comparator is not fully operationalized. Source: [f-DP filters](https://arxiv.org/abs/2602.06756).

**Obstacle / countercase.** Full adaptivity is materially harder than a fixed sequence; asymptotic approximation and numerical soundness are not interchangeable. It may be that a general middle-regime extension is impossible or not tighter than RDP/PLD accounting.

**Impact and verification.** High for privacy accounting if guarantees are sound and usable. Check theorem assumptions and approximation error symbolically, then independently validate numerical bounds using certified arithmetic on the explicitly stated family. **Paper 4 action:** first resolve the exact missing theorem and comparator from the primary source; do not run numerical experiments as a substitute for a proof.

**Frozen event:** `ADAPTIVE-FDP-GDP-FILTER-MID-Q-001`, deadline 2030-12-31. Preserve its original underspecification flag; this portfolio does not repair it.

### 4. Fixed-exponent sublinear update time for approximate fully dynamic maximum matching

**Question / expected progress.** Can general-graph fully dynamic `(1−ε)`-approximate maximum matching achieve `O(n^{1−δ})` amortized update time for a fixed `δ>0`, with the frozen explicit-output and adversary guarantees? Expect further structural or parameterized bounds; exact resolution by a fixed deadline is uncertain.

**Evidence.** The 2024 matching/ORS work exposes a connection between update time and an ordered Ruzsa–Szemerédi extremal parameter. Bernstein et al. (2025) obtain sublinear deterministic and randomized update time for **maximal matching**. This is real progress in an adjacent problem but does **not** solve the frozen approximate-maximum-matching target. Sources: [dynamic matching via ORS](https://arxiv.org/abs/2406.13573), [sublinear dynamic maximal matching](https://arxiv.org/abs/2504.20780), and the separately frozen [dynamic matching event](https://github.com/nonameisready/scientific-discovery-computer-science/blob/main/data/forecast_engine/prospective_cohort_v2.json).

**Obstacle / countercase.** The maximal/maximum and maximal/approximate distinctions matter. ORS growth may remain the bottleneck; proof progress on maximal matching is not a proxy label for this event. The ORS companion event has a frozen 2030/2031 deadline conflict and must not be counted as an independent resolved outcome.

**Impact and verification.** High theoretical and algorithmic relevance. Match graph model, approximation, amortization, update adversary, output representation, preprocessing and probability quantifiers theorem-by-theorem. **Paper 4 action:** trace only the extremal lemma's later theorem-level descendants, checking whether they improve the exact update exponent.

**Frozen event:** `DYNAMIC-MATCHING-POLY-EXPONENT-001`, deadline 2031-12-31; the forecast here is progress by the near horizon, not event resolution.

### 5. Artifact-level verification of multi-agent work

**Question / expected progress.** Which, if any, verifier can reliably predict independently checked artifact correctness and improve end-to-end task success after including cost, false positives, and context? Expect better task-specific verifier designs and clearer negative boundaries, not a universal process verifier.

**Evidence.** MAS-ProVe studies multiple verifier classes, granularities, contexts, and agent frameworks and reports that process verification does not consistently improve performance and often has high variance. The strongest next result is a pre-registered artifact-level evaluation with independent correctness labels, not another judge score. Source: [MAS-ProVe](https://arxiv.org/abs/2602.03053).

**Obstacle / countercase.** Task outcomes and verifier signals may be correlated through shared models or benchmark contamination; partial traces may not contain enough information to certify a final artifact. Independent ground truth is costly.

**Impact and verification.** High if it reduces undetected failures in agentic software and research workflows. Use paired runs, frozen verifier decisions, independently tested artifacts, and full false-positive/negative and compute accounting. **Paper 4 action:** compare MAS-ProVe's task definitions and failure cases with repository-proof results; this may show that the right unit is a final artifact, not a trajectory.

**Frozen event:** none; radar family `MULTIAGENT_PROCESS_VERIFICATION`.

## Ranked medium-horizon opportunities: 2029–2031

### 1. The dynamic matching–ORS extremal bottleneck

This is the continuation of near-term opportunity 4, not an independent sample. The specific technical question is whether the ordered RS parameter at fixed linear matching density admits a polynomial lower bound strong enough to imply a fixed-exponent sublinear update bound for approximate dynamic maximum matching. The 2024/2025 sources provide a genuine, technically linked chain of progress; counterevidence is that the extremal gap is longstanding and its improvement may not transfer to the algorithm with the desired quantifiers. Verify by tracing the reduction and proving each parameter implication. **Frozen links:** dynamic matching event as above; ORS event `ORS-POLYNOMIAL-GROWTH-001` remains ambiguous and unadjudicable as written.

### 2. Exact planar (1,1,2)-terminal Three-Sets Cut-Uncut

The question is whether unweighted planar Three-Sets Cut-Uncut with two singleton terminal sets and one two-vertex set that must remain connected has an exact polynomial-time algorithm. Bentert et al. solve a neighboring planar Two-Sets version and explicitly pose this case as open; ordinary planar Multiway Cut does not preserve the uncut pair. The problem is highly specific and directly checkable, but the additional connectivity constraint may be structurally decisive. Two reviewers must compare the exact theorem and all terminal/connectivity assumptions. **Frozen link:** `PLANAR-THREE-SETS-CUT-UNCUT-112`, deadline 2030-12-31. Source: [ICALP 2024 primary paper](https://doi.org/10.4230/LIPIcs.ICALP.2024.22).

### 3. Discrete planar Fréchet distance under translation near the conditional exponent boundary

The frozen event asks for exact `O(n^4 log^C n)` computation in a comparable model. The baseline has an approximately `n^(14/3)` algorithm and a SETH-based `n^(4−o(1))` lower bound for the specified translation problem. This leaves only polylogarithmic/fine-grained room; it is plausible that algorithmic or model clarification progress occurs, but the conditional lower bound makes a polynomial-exponent improvement unlikely under the assumption. Exact value-versus-decision conversion and arithmetic/bit model are adjudication gates. **Frozen link:** `DISCRETE-FRECHET-TRANSLATION-PLANAR-N4`, deadline 2031-10-16. Source: [Bringmann, Künnemann & Nusser](https://arxiv.org/abs/1810.10982).

### 4. Two-stage integer programming with unbounded global coefficients

Can exact optimization remain fixed-parameter tractable in local dimension/coefficient parameters while global coupling matrices are unrestricted? Cslovjecsek et al. prove neighboring feasibility and uniform n-fold optimization results, not this exact optimization endpoint. The opportunity is theorem-specific and verifiable; counterevidence is that the unrestricted coefficients may encode the hard part, and the frozen parameterization must be checked exactly. **Frozen link:** `TWO-STAGE-IP-OPT-UNBOUNDED-GLOBAL-COEFF-001`, deadline 2030-12-31. Source: [TheoretiCS primary article](https://doi.org/10.46298/theoretics.25.15).

### 5. Research agents that produce independently reproducible evidence

The narrow question is not whether agents generate ideas, but whether they can produce a frozen falsifiable question, run a discriminating study, preserve raw artifacts, and obtain independent confirmation at rates above simple baselines. EIG and ResearchBench evaluate proposal/inspiration quality; PaperBench evaluates replication tasks; the astronomy backtesting work exposes serious outcome-label reliability problems. This portfolio forecast is low-confidence because evidence execution, novelty and reproducibility are not yet one standardized outcome. Sources: [EIG](https://arxiv.org/abs/2605.04922), [ResearchBench](https://aclanthology.org/2026.findings-acl.644/), [PaperBench](https://arxiv.org/abs/2504.01848), [historical backtesting](https://arxiv.org/abs/2608.16795).

**Paper 4 next action:** compare benchmark endpoints and human adjudication reliability, then specify one future outcome taxonomy. Do not infer scientific productivity from idea ratings or replication rubrics alone. No new forecast event is frozen because no defensible cross-field success threshold or common unit is established.

## Watch list and candidates not promoted

- **Broad heterogeneous KV-memory policy:** plausible system progress, but overlaps the near-horizon serving family and lacks an independent common metric; retain within that family, not as a separate ranked item.
- **Semiring incremental view maintenance:** Chmielewski et al. (2026) already provide an insert-only dichotomy for the stated no-self-join query class and semiring assumptions. A follow-on extension needs a sharper question before it becomes a forecast.
- **Dynamic maximal matching:** the sublinear update question is already answered by Bernstein et al. (2025); do not repackage it as an open forecast or confuse it with approximate maximum matching.
- **Quantum public-key encryption from one-way functions:** source-level leads are conditional and model-sensitive; no event with a stable, near-term, independently adjudicable milestone passed the inclusion gate in this cycle.
- **Conflict-aware agent memory / software supply-chain incidents / adaptive IVM:** remain watch directions; current endpoints are either too broad, retrieval/incident-limited, or already covered by known rebalancing results. The earlier radar's source-specific objections remain in force.
- **Frozen MAX BISECTION, Subset Sum, shallow-circuit identity, k-hop domination, and two-stage IP events:** retained as commitments but not automatically elevated into the top five. A prior forecast is not a quality or probability score.

## Method, sensitivity, and audit boundary

The ranking procedure was set before ordering: first require an identifiable primary-source baseline and concrete progress endpoint; then compare (i) evidence of a technically plausible path, (ii) tractability within the horizon, (iii) importance of the improvement, (iv) independent-verification feasibility, and (v) strongest counterevidence. No arithmetic weights, probabilities, attention counts, or citation counts were used. Rank is a decision priority, not an estimated chance.

Sensitivity was assessed by reordering the same eligible set under three qualitative priorities: (a) proof tractability, (b) computational/real-world impact, and (c) source maturity plus verifiability. Repository verification and inference serving remain in the leading near-term set, but exchange positions; DP moves up under tractability; dynamic matching moves up under theoretical significance; process verification and scientific agents fall under evidence maturity because their outcome labels are least settled. The medium-horizon set is less stable: dynamic matching remains high under importance weighting, while planar cut-uncut and two-stage IP rise under theorem-verifiability weighting. These are ordinal robustness checks, not sensitivity estimates with statistical meaning. Full ordering variants are in [`CS_BREAKTHROUGH_RANKING_SENSITIVITY.md`](CS_BREAKTHROUGH_RANKING_SENSITIVITY.md).

The existing ten forecasts remain unchanged. The ORS deadline mismatch is preserved as an append-only defect; no outcome labels were added. No new forecast event was frozen: the new leads either duplicate an existing family or lack a non-arbitrary common threshold. The final portfolio is explicitly qualitative and is not appended as if it were a calibrated forecast. Paper 3 model fitting/scoring, Paper 4 efficacy evaluation, experiments, workers, monitoring, and human adjudication were not run.

## What would most change this portfolio?

1. Independent replication of CoCo/Vero repository results under frozen versions and equal budgets; failure would lower rank 1.
2. An equal-memory/equal-quality independent serving comparison for Spexis; disappearance of the gain would lower rank 2.
3. A theorem or impossibility result for intermediate-rate fully adaptive privacy filters; either result would resolve the key uncertainty in rank 3.
4. A new ORS lower bound with a verified reduction to the exact maximum-matching update target; without that link, rank 4 remains a conjectural chain.
5. Independent human agreement on the scientific-progress rubric, followed by prospectively matured outcomes; low agreement would lower the entire scientific-agent opportunity and preclude forecast evaluation.

## Final scientific decision

The strongest defensible answer is that **repository-scale verified code synthesis and LLM inference scheduling are the leading near-term progress opportunities**, while **dynamic matching/ORS, specific planar cut-uncut, and fine-grained geometric algorithms** are the strongest theorem-facing medium-horizon candidates. This is a qualitative, evidence-based ordering with substantial uncertainty. It does not show that these events are more likely than not, that the system can forecast them accurately, or that any breakthrough has occurred. The primary evidence is recent, source-authenticated progress plus a bounded, explicit remaining bottleneck; the principal counterweight is that author-reported benchmark gains and a small number of recent papers provide no calibrated base rate.
