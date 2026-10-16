# Future Computer Science Breakthrough Radar (2026-10-16)

## Scope and epistemic status

This is a bounded, source-grounded editorial radar for 2027–2028 and 2029–2031, not a calibrated forecast. The order reflects technical importance, a sharply observable bottleneck, and evidence of active progress, discounted by counterevidence and replication risk. It is not a Paper 3 model output, a Paper 4 validated action ranking, or a probability estimate. “Attention”, “resolution”, and “impact” below are separate qualitative judgments. Research-paper results are attributed to their authors unless independently reproduced in this repository.

The survey combines the project’s primary-source audits through October 2026 with focused primary-source checks for newer work. A shortlist of twelve is supportable; the universe is not exhaustive. Preprints are marked as such, and no absence-of-search-hit is treated as evidence that a question is open.

## Ranking criteria

The editorial order favors: (i) consequential measurable capability; (ii) a bottleneck that can be expressed as a falsifiable systems or mathematical question; (iii) multiple independent technical ingredients; (iv) a public evaluation path; and (v) a plausible next information-gathering step. Counterevidence lowers maturity. No synthetic weighted score is computed.

## Ranked radar

### Near horizon: 2027–2028

| Rank | Opportunity | Maturity | Horizon | Qualitative attention / resolution / impact |
|---:|---|---|---|---|
| 1 | Joint KV-cache scheduling and speculative decoding under heterogeneous, changing load | Investigate | Near | Attention: likely sustained (editorial). Direct resolution: uncertain; no calibrated forecast. Impact if solved: high—latency, throughput and memory at fixed output quality. |
| 2 | Repository-scale verified code generation and repair | Investigate | Near | Attention: likely high. Direct resolution: medium-to-low confidence; repository dependencies and long tasks remain hard. Impact: high for correctness-critical software if verified end-to-end. |
| 3 | Reliable process verification for multi-agent execution | Investigate | Near | Attention: likely high. Direct resolution: uncertain; current evidence is inconsistent. Impact: high if verifier scores predict actual task success rather than persuasive traces. |
| 4 | Adaptive privacy filters for fully adaptive compositions | Experiment-ready (protocol only; no run authorized) | Near | Attention: steady specialist interest. Direct resolution: plausible for specific parameter regimes, uncertain generally. Impact: high for tighter privacy budgets with valid guarantees. |
| 5 | Evidence-grounded scientific agents that execute and verify proposed tests | Investigate | Near/medium | Attention: likely high. Direct resolution: low confidence for general autonomous discovery; ideation is not executed evidence. Impact: potentially very high but contingent on reproducible experiments and independent verification. |
| 6 | Conflict-aware persistent memory for multi-agent systems | Watch | Near | Attention: likely high. Direct resolution: uncertain beyond narrow tasks. Impact: medium-to-high if memory state improves downstream correctness under changing evidence. |
| 7 | KV-cache eviction/retention under fixed memory and quality constraints | Investigate | Near | Attention: likely high. Direct resolution: uncertain across models/workloads. Impact: high if robust quality is retained at materially lower memory. |

### Medium horizon: 2029–2031

| Rank | Opportunity | Maturity | Horizon | Qualitative attention / resolution / impact |
|---:|---|---|---|---|
| 8 | Heterogeneous-memory placement and runtime policy for inference KV state | Investigate | Medium | Attention: likely sustained. Direct resolution: uncertain; upper-bound headroom is not an implementable policy. Impact: high if utilization gains survive transfer, contention and tail-latency costs. |
| 9 | Formal verification of real repository changes, not isolated benchmark theorems | Investigate | Medium | Attention: rising. Direct resolution: uncertain; context dependencies and specification coverage dominate. Impact: very high in safety-critical software if practical proof coverage improves. |
| 10 | Long-horizon software engineering agents on held-out repositories | Investigate | Medium | Attention: likely sustained. Direct resolution: uncertain; benchmark scores may not transfer to maintenance and deployment. Impact: high if verified issue resolution and regression safety improve. |
| 11 | AI/software supply-chain risk measured against confirmed security outcomes | Watch | Medium | Attention: likely sustained. Direct resolution: uncertain because current studies often measure discussion or taxonomy, not attributable incidents. Impact: high if provenance controls reduce confirmed compromise without blocking benign work. |
| 12 | Instance-adaptive dynamic incremental view maintenance under workload skew | Watch / current formulation NO-GO | Medium | Attention: specialist. Direct resolution: low confidence for the proposed adaptive-threshold gap; existing heavy/light rebalancing closes the broad version. Impact: potentially high for query workloads, but no current contribution is established. |

Detailed question, baseline, bottleneck, evidence, counterevidence, action, milestones, downgrade gates and citations are machine-readable in [`FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json`](FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json).

## Evidence-backed opportunity dossiers

### 1. Joint serving policy for KV cache and speculative decoding

**Question.** Under a fixed GPU-memory budget and a time-varying request mix, can a scheduler jointly choose cache retention/placement and speculative execution so that it improves end-to-end goodput or tail latency at a fixed output-quality and SLO target over separately tuned policies?

**Baseline and evidence.** Jaillet et al. model KV-constrained inference scheduling: exact average-latency optimality in a semi-online model, constant regret with stochastic arrivals, and an impossibility of constant competitive ratio in a fully adversarial online model ([primary paper](https://arxiv.org/abs/2502.07115)). SPECTRE proposes hybrid speculative decoding with heterogeneous models and reports up to 2.28× speedup in its evaluated configuration ([primary preprint](https://arxiv.org/abs/2605.08151)); this is an author-reported configuration result, not a third-party replication or a universal guarantee. Cache eviction work also reports quality/footprint trade-offs ([2605.09649](https://arxiv.org/abs/2605.09649), [2605.07234](https://arxiv.org/abs/2605.07234)).

**Unresolved bottleneck and counterevidence.** A joint policy must account for acceptance rate, cache residency, heterogeneous accelerator contention, preemption, request arrivals and tail SLOs simultaneously. Isolated gains may not compose; the adversarial online impossibility rules out an overly broad competitive claim. Quality must be measured on held-out prompts and models, not inferred from throughput.

**Paper 3 outlook (qualitative only).** Attention: likely sustained given deployment relevance. Direct resolution: not forecastable here; multiple competing system designs remain. Premise revision: plausible if fixed-model/cache assumptions fail in production. **Impact** could be high even without resolving a general online problem. **Next Paper 4-style action:** map one public serving stack’s cache, speculative decoding and scheduler controls; predeclare one fixed-memory, fixed-quality, equal-arrival replay comparison and list failure modes. This is a recommendation, not a validated optimal action. **Upgrade:** an independently replicated held-out workload gain with quality and p95/p99 constraints. **Downgrade:** benefit disappears under equal memory, realistic arrivals or independent implementation.

### 2. Repository-scale verified code generation and repair

**Question.** Can code agents produce patches that satisfy explicit formal specifications and repository tests, while proof obligations remain valid across real multi-file dependencies and unseen projects?

**Baseline and evidence.** VeriSoftBench introduces 500 Lean 4 proof obligations from repository-based formal-methods projects; its authors report that Mathlib-style provers transfer poorly, dependency-closure context helps, and multi-hop repository dependencies predict lower success ([primary preprint](https://arxiv.org/abs/2602.18307)). The vericoding benchmark contains 12,504 Lean/Verus/Dafny specifications, with authors reporting different success by language and problem family ([primary preprint](https://arxiv.org/abs/2509.22908)). SWE-Bench Pro has 1,865 problems across 41 repositories and held-out settings; the source’s reported best result is still far from broad task completion ([primary paper](https://arxiv.org/abs/2509.16941)).

**Bottleneck and counterevidence.** Passing a proof checker only verifies the formalized specification; specification completeness and correspondence to intended behavior remain central. Benchmarks can leak repository conventions or reward narrow tests. A credible milestone is an increase in independently reviewed, issue-resolving patches with proof/test coverage and no regression on hidden tests, across unseen repositories. **Next action:** audit task-level artifacts and build a benchmark map separating theorem proof, program verification, and repository repair; do not combine their denominators. **Upgrade:** held-out repository replication plus audited spec-to-code correspondence. **Downgrade:** gains vanish under hidden tests, altered specs, or independent evaluators.

### 3. Process verification for multi-agent execution

**Question.** Which verifier signals, if any, improve the probability that a multi-agent run produces a correct, complete, externally validated artifact, rather than merely a persuasive intermediate trace?

**Evidence.** MAS-ProVe evaluates three verification paradigms, two granularity levels, five verifiers, four context strategies and six multi-agent frameworks. Its authors report inconsistent performance gains and high variance, with LLM-as-judge often stronger than reward models and a context-length trade-off ([ICML 2026 primary paper](https://arxiv.org/abs/2602.03053)). This is unusually direct counterevidence to “more process checking automatically helps.”

**Bottleneck.** Define correctness at the artifact level, use independently checked task outcomes, and prevent evaluator leakage. **Next action:** prospective paired evaluation with verifier decisions frozen before artifact validation, stratified by task and run, and including verifier false-positive costs. **Upgrade:** stable gains over no-verifier and simple deterministic checks across independent task families. **Downgrade:** no net improvement after compute/context cost or evaluator disagreement is included.

### 4. Fully adaptive differential-privacy filters

**Question.** Can one construct tight, composable and numerically certifiable privacy filters for adaptive mechanism selection over the parameter regimes not covered by existing approximate filters?

**Known result.** Tran et al. prove that the natural f-DP filter can fail under fully adaptive choices, characterize validity conditions, and give an approximate GDP filter for subsampled Gaussian mechanisms for sampling rates `q<0.2` and `q>0.8` ([primary preprint](https://arxiv.org/abs/2602.06756)). This is a real theorem, not merely a trend claim.

**Gap and risk.** The intermediate regime and implementation-grade certified error bounds remain the concrete boundary in the repository’s DP audit; do not infer that the published construction is unsafe outside its stated assumptions. **Next action:** source-level theorem-to-code mapping, followed only with authorization by a formal or interval-arithmetic certificate over a narrowly fixed mechanism family. **Upgrade:** a sound, tighter, independently checked filter with explicit runtime/error bounds. **Downgrade:** no gain over existing RDP/PLD accounting or assumptions fail in the target deployment. No experiment was run here.

### 5. Scientific agents: proposals to executed evidence

**Question.** Can a research agent produce a frozen, falsifiable question and then execute a discriminating study whose raw evidence survives independent reproduction?

**Evidence and caution.** Evolving Idea Graphs reports strong benchmark-native proposal scores, but it evaluates ideation quality, not the truth or impact of executed science ([primary preprint](https://arxiv.org/abs/2605.04922)). MAS-ProVe shows that process verification itself remains unreliable. A separate historical-backtesting paper proposes a falsifiable protocol and reports an astronomy pilot, including low human outcome-label agreement and a prospective set frozen for later evaluation ([primary preprint](https://arxiv.org/abs/2608.16795)). These results make evaluation design, adjudication reliability and execution-to-evidence linkage the bottleneck—not idea fluency.

**Milestone.** A prospective blinded question set, frozen cutoffs and endpoints, independent outcome adjudication, and executed artifact-level results, reported separately from publication/attention. **Next action:** compare the existing benchmark protocols and specify an adjudication reliability gate before any prospective system evaluation. **Upgrade:** independently adjudicated executed outcomes outperform simple source-only baselines on an untouched future cohort. **Downgrade:** label disagreement or missingness prevents reproducible endpoints.

### 6–12. Remaining opportunities and explicit limits

The remaining six dossiers are kept in JSON to make this radar auditable without implying stronger evidence than exists. They cover conflict-aware memory ([LatticeMind](https://arxiv.org/abs/2608.08236)), cache eviction, heterogeneous memory placement ([2508.13231](https://arxiv.org/abs/2508.13231)), repository-scale formal verification, long-horizon coding, AI software-supply-chain evidence ([2512.23385](https://arxiv.org/abs/2512.23385)), and dynamic IVM ([2605.08397](https://arxiv.org/abs/2605.08397)). In each case, the milestone requires an objective output metric and a matched comparator. The IVM entry is deliberately Watch/NO-GO for the current formulation: its 2026 source already handles heavy/light membership changes with amortized rebalancing, so “dynamic skew” alone is not an open gap.

## Cross-paper breakthrough clusters

1. **Inference systems:** KV retention + heterogeneous placement + speculative execution. The joint bottleneck is memory/compute contention under tail-latency and quality constraints. Demonstration: equal-budget replay with held-out arrivals and quality evaluation. Disconfirmation: component improvements fail to compose or merely shift latency to transfer/preemption.
2. **Trustworthy software agents:** long-horizon repository repair + formal proof + process verification. The missing link is verified correspondence among issue, specification, patch and tests. Demonstration: unseen repositories with independent spec audit and hidden regressions. Disconfirmation: gains depend on benchmark leakage or incomplete specs.
3. **Autonomous science:** evidence-graph ideation + prospective question backtesting + independently checked experiments. The bottleneck is reliable outcome labels and execution provenance. Demonstration: frozen future cohort, adjudication agreement and reproducible raw results. Disconfirmation: human label reliability or execution yield is too low to separate methods.
4. **Private adaptive computation:** adaptive composition + certified accounting. The unresolved ingredient is tightness with rigorous numerical guarantees over realistic adaptivity. Demonstration: proof-backed certificates and matched privacy/utility accounting. Disconfirmation: existing accountants dominate or implementation assumptions do not hold.

## Exciting areas not ready for breakthrough claims

- **“Autonomous scientist” proposal scores:** benchmark ratings do not show that proposed work is correct, novel after full prior-art review, or experimentally executed.
- **Large speculative-decoding speedups:** configuration-specific throughput does not establish fixed-quality end-to-end advantage under equal memory, changing load and tail SLOs.
- **Agent memory accuracy:** a small benchmark win is not evidence of durable downstream reliability or safe conflict resolution in long tasks.
- **AI supply-chain prevalence:** discussion posts and taxonomies are not confirmed attack/incident rates or causal attribution.
- **Dynamic IVM skew adaptation:** broad “adapt to skew” framing is already covered by the source-level rebalancing result; any new claim needs an explicit objective beyond reconfiguration.

## Top five and immediate evidence actions

1. **Joint inference memory/scheduling/speculation** — strongest combination of measurable cost and converging systems mechanisms. Action: source-pinned, fixed-memory/quality/SLO comparison design before any authorized run.
2. **Repository-scale verified software change** — exact correctness endpoint is possible. Action: unify benchmark/task taxonomy and audit spec completeness, not aggregate incompatible success rates.
3. **Process verification for multi-agent runs** — clearly unresolved and directly tested with counterevidence. Action: prospective artifact-level verifier false-positive/false-negative protocol.
4. **Adaptive DP filters** — strongest near-term formal result opportunity, but narrow and assumption-sensitive. Action: identify exact uncovered parameter region and required certificate before an authorized implementation study.
5. **Executed-evidence scientific agents** — potentially transformative, but currently the weakest predictive claim. Action: frozen prospective cohort and adjudication reliability study; do not score a breakthrough probability.

## Paper 3/Paper 4 integration boundary

Paper 3 provides a useful discipline for separating attention from direct resolution and premise revision, but this radar did not run it. The existing CS cohorts have no authenticated direct outcomes sufficient for evaluation, and the distinct evidence-trajectory observations cannot be substituted for resolution labels. Paper 4 provides a structured way to record competing hypotheses, typed evidence, gaps, candidate actions, assumed information gain and costs. It has not demonstrated that its action ranking outperforms cost-only, highest-uncertainty or other simple baselines. These limits and the future validation design are detailed in [`PAPER3_PAPER4_FORECAST_INTEGRATION_AUDIT_20261016.md`](PAPER3_PAPER4_FORECAST_INTEGRATION_AUDIT_20261016.md).

**Disposition:** qualitative radar complete; no validated predictive scores; no experiments, inference, training, cohort/label changes, workers, budget renewal, or successor task. The highest-value next system evidence is not a new model score: it is authenticated, independently adjudicated outcome/action records under frozen endpoints.
