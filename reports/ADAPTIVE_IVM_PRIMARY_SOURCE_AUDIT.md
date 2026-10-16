# Adaptive IVM under dynamic skew — primary-source audit

**Decision: NO-GO for a new adaptive-threshold algorithm in this bounded cycle.** The primary paper was available as the authors’ arXiv full text. It already handles changing heavy/light membership, database-size-driven threshold-base changes, and oscillation-safe rebalancing with amortized update bounds. Its exponent parameter is optimized per query and kept fixed during the update sequence; it does not select a new exponent from the observed instance distribution. That distinction leaves a possible instance-sensitive optimization question, but no correctness-preserving, migration-accounted policy or strict improvement over the strongest baseline was established here. No algorithm design is admitted, no experiments are authorized or run, and no successor task is created.

## 1. Primary-source identity and scope

The source is Abo-Khamis, Chmielewski, Draghici, Kara, and Olteanu, “Maintaining Queries under Updates Using Heavy-Light Partitioning of the Input Relations,” arXiv:2605.08397v1 (8 May 2026), published in *Proceedings of the ACM on Management of Data* 4(2), May 2026, DOI [10.1145/3801905](https://doi.org/10.1145/3801905). The arXiv HTML full text was read, including Sections 2–8 and Appendices B–D. The published bibliographic identity matches the preprint title and authors via the authors’ Oxford publication listing. The ACM full-text endpoint was not independently compared with the preprint; publication-version changes beyond the matching bibliographic record remain unaudited.

The scan that produced this lead had reported an ACM 403. This cycle resolves that access blocker using the author preprint; a web-access obstacle is not treated as a research gap.

## 2. Reconstructed mathematical model

### Query and data semantics

The theorem is in data complexity for a fixed full conjunctive/join query
`Q(F) = sum_B R_1(X_1) · ... · R_m(X_m)` over the integer ring. Each relation maps tuples to integer multiplicities. Support-based set operations regard tuples with positive multiplicity as present; the join computation propagates multiplicities, and the enumeration result lists distinct output tuples with their multiplicities. Relation symbols are distinct in the query; self-join atoms are handled by making separate copies of the physical relation.

An update is one tuple insertion or deletion, represented by multiplicity change `+1` or `-1`; updates are processed sequentially. Both insertions and deletions are allowed. After every update, the algorithm must support constant-delay enumeration of the exact current query output. The theorem is for full join queries. The authors state that free-variable conjunctive queries can be extended using free-connex hypertree decompositions, with free-connexity needed for constant-delay enumeration; that extension is not Theorem 11 itself.

### Heavy/light partition and delta maintenance

For each join variable `Y`, values are divided into `Light(Y)` and `Heavy(Y)`. The source's degree is global across all query atoms containing `Y`: the sum of the sizes of the corresponding `Y=y` fibers. For a fixed exponent `ε ∈ [0,1]`, the ideal scale is `N^ε` for light fibers and `N^(1−ε)` for the number of heavy values, with `N` the current database size.

For every degree configuration `d ∈ {L,H}^{vars(Q)}`, the algorithm stores the corresponding relation fragments and selects a view tree appropriate to that configuration. A view tree has relation atoms at leaves and materialized join/projection views internally. On an update, the algorithm evaluates the corresponding delta-view tree, using degree constraints and a polymatroid/AGM-style linear program to bound each delta view. The best view tree may differ by degree configuration; the algorithm is already adaptive in this sense.

The maintenance width `mw(Q)` is the query-dependent exponent obtained by optimizing `ε` against the worst degree configuration, while allowing a best view tree for each configuration and accounting for the most expensive delta view. In schematic form:

`mw(Q) = min_{ε∈[0,1]} max_{d∈D(Q)} min_{T∈T(Q)} max_{delta-view v in T,d} exponent(v, ε)`.

The paper expands the inner exponent using degree-constraint sets, projected constraints, and feasible LP vertices. It shows `mw(Q) ≤ dw(Q)` (dynamic width). For the 4-cycle it derives `mw=2/3` with `ε=1/3`; for the Loomis–Whitney 4 query it derives `mw=1/2` with `ε=1/2`. These are examples, not a claim that the same exponent is optimal for every workload or every concrete data trajectory.

### Theorem 11 and costs

**Theorem 11 (source statement, data complexity).** For any fixed join query `Q`, the paper's construction supports preprocessing in `O(N^(1+mw(Q)))`, amortized `O(N^mw(Q))` time per single-tuple update, and `O(1)` delay for enumerating the output. The bound is query-dependent; `N` is the database size at the update, up to the paper's threshold-base invariant. The update bound includes amortized major and minor rebalancing.

The theorem provides a concrete materialized state: heavy/light value sets, fragments for degree configurations, and materialized view trees. The paper does not state a separate asymptotic peak-space theorem for that entire state in Theorem 11. This audit therefore does not infer that a threshold portfolio or duplicated shadow views fit the same memory bound. Preprocessing/rebuild is charged separately as `O(N^(1+mw))` in Appendix C. Enumeration is of the current exact output (distinct tuples and multiplicities), not an eventually consistent snapshot.

## 3. Rebalancing: what changing skew already receives

The authors fix `ε` for `Q`, but the realized partition and state change with updates:

* **Minor rebalancing (membership drift).** The threshold is relaxed to avoid flip-flopping: for a threshold base `M`, light values have global degree at most about `(3/2)M^ε`; heavy values have degree greater than about `(1/2)M^ε`. Thus a value near `M^ε` may validly lie in either class, but it cannot cross both hysteresis boundaries after one update. When it crosses a boundary, tuples are moved between the affected degree-configuration fragments and the affected view trees are updated. The paper bounds the movement by `O(M^ε)` tuples; with `O(N^mw)` per tuple, rebalancing costs `O(N^mw M^ε)`. Since `Ω(M^ε)` updates are needed between consecutive transitions of a value, the amortized cost is `O(N^mw)` per update.
* **Major rebalancing (database-size drift).** The threshold base satisfies roughly `M/4 ≤ N < M`; the initial base is `2N+1`. If `N` exits this band, `M` is halved or doubled, and partitions, fragments, and view trees are recomputed at the same fixed `ε`. The rebuild costs `O(N^(1+mw))`, and `Ω(M)=Ω(N)` updates separate such rebuilds, giving amortized `O(N^mw)` work per update.
* **Per-configuration adaptation.** The algorithm selects a view tree by current degree configuration and can use multiple trees; it does not bind all data to one static join plan.

Therefore oscillation around a heavy/light boundary, a key moving between classes, or `N` changing over time are not new limitations of the 2026 approach. “Adaptive” in its title and text refers to these query-plan choices and heavy/light configurations. It does **not** mean that `ε` is reoptimized from the empirical distribution at each time.

## 4. The remaining candidate problem, formally

Fix a query `Q`, initial database `D_0`, and an online update stream `u_1,…,u_T`, where each update changes one tuple by `+1` or `−1`. Let `D_t` be the resulting multiset database and `Q(D_t)` the exact output. A policy chooses a threshold exponent `ε_t` using only the query, current database/statistics and update history available at time `t`—never future updates. Its state `M_t` includes the selected heavy/light partition, all fragments needed for its degree configurations, the selected view trees/materialized views, and any migration log/version state.

For every `t`, correctness requires that the active state enumerates exactly `Q(D_t)` with the declared delay. Total cost must separately account for (i) delta update work, (ii) tuple classification and movement, (iii) rebuilding or migrating all affected views, (iv) any dual-maintenance/log-replay work during migration, (v) peak memory including old and new states, and (vi) enumeration delay during every update and cutover. A switch cannot be modeled as a free assignment `ε_t := ε'` because the maintained partitioned relations and materialized views are functions of that threshold.

The comparison models are distinct:

| Model | Threshold policy | Information / cost interpretation |
|---|---|---|
| A. Fixed initially | One `ε` fixed before updates | Current paper's minimax query exponent is an appropriate worst-case baseline. |
| B. Size-driven | `ε` fixed; scale follows current `N` | Already covered by the paper's `M` doubling/halving major rebalancing. |
| C. Online adaptive | `ε_t` chosen from current/history only | Requires charging switch/migration work and preserving exact answers throughout. |
| D. Best fixed in hindsight | Choose one `ε` after seeing the entire stream | Offline comparator only; an online policy may not use future stream information. |
| E. Offline dynamic sequence | Choose `ε_0,…,ε_T` with explicit switching costs | Stronger oracle; competitive/regret claims need restrictions on stream or switching. |

The 3.0 proposal's “bounded threshold portfolio with hysteresis” did not fix whether its target was worst-case exponent, per-instance realized work, competitive ratio to D, or regret to E. Those are different problems; the policy is not admitted without one exact objective.

## 5. Theorem-level prior-art comparison

| Work | What is established and relevant here | Boundary relative to changing-skew `ε` selection |
|---|---|---|
| Abo-Khamis et al., PODS 2026 / arXiv:2605.08397 | Arbitrary fixed join query; single tuple inserts/deletes; degree-configuration-specific view trees; query-level optimized fixed `ε`; exact enumeration; minor and major rebalancing amortized into `O(N^mw)` update time. | Directly defeats the broad novelty pitch that dynamic skew or heavy/light membership changes are unhandled. It does not state per-instance online `ε_t` optimization or a migration-cost competitive theorem against a dynamic-`ε` oracle. |
| Kara et al., IVM-ε triangle maintenance, ICDT 2019 / TODS 2020 | For triangle queries, threshold parameter trades update time, space, and enumeration delay; the algorithm partitions heavy/light data and uses amortized rebalancing. The 2026 paper explicitly adapts this rebalancing method. | Threshold tuning and hysteresis/rebalancing are established components, not new mechanisms. The older result is query-specific; it does not by itself establish a distribution-adaptive `ε_t` theorem for arbitrary joins. |
| Kara et al., “Conjunctive Queries with Free Access Patterns under Updates,” LMCS 2025 | Dynamic degree/partition machinery and amortized rebalancing extend to a broader access-pattern setting. | Further evidence that update-driven partition changes are prior art; no claimed per-instance dynamic exponent-selection guarantee was found in the checked source. |
| Kara et al., F-IVM, VLDB Journal 2024 | Higher-order IVM with a hierarchy of factorized views; materialization choices depend on which relations are static/updatable and the update workload; exact ring semantics. | Adapts maintained views to update workload, not the heavy/light exponent to a changing degree distribution. It is a strong baseline for view-state choices, not proof that `ε_t` migration is solved. |
| Liang, Elmore, and Krishnan, DQM, arXiv:1903.01363 | An online RL policy creates/evicts opportunistic inner-join views under a storage cap, trained using asynchronous paired counterfactual runtime experiments. It evaluates evolving query workloads and several skew patterns in SparkSQL. | Direct prior art for adaptive view portfolio selection under changing workload/skew, but not for exact single-tuple IVM: the paper states Spark recomputes and re-materializes affected views when base tables change. Its guarantees are experimental cumulative-latency results under an in-memory/stateless-query assumption, not a worst-case update/delay theorem. |
| DBToaster / dynamic Yannakakis / Crown | Compile fixed queries into view trees and maintain deltas; the 2026 paper compares these as single-tree baselines and motivates multiple trees by degree configuration. | Not evidence for cost-free threshold migration. They are necessary algorithm baselines when the query class overlaps. |
| Ross et al. (1996), Mistry et al. (2001), and view adaptation after redefinition | Choose additional/transient/permanent views and maintenance plans for a set of SQL views and update workloads; later view-adaptation work studies changing the view definition and reusing old materialization. | These papers establish that selecting or adapting view state under changing needs is not itself new. Their objective and semantics differ from a theorem for fully dynamic conjunctive-query updates with heavy/light threshold changes; no direct implication to a causal `ε_t` competitive bound is claimed. |

Primary sources: [2026 author preprint](https://arxiv.org/abs/2605.08397) ([full HTML](https://arxiv.org/html/2605.08397)); [PODS 2026 DOI](https://doi.org/10.1145/3801905); [IVM-ε, arXiv:2004.03716](https://arxiv.org/abs/2004.03716); [F-IVM, VLDB Journal DOI](https://doi.org/10.1007/s00778-023-00817-w); [free-access-pattern queries, LMCS DOI](https://doi.org/10.46298/lmcs-21(2:23)2025); [DBSP](https://arxiv.org/abs/2203.16684); [DQM adaptive view materialization](https://arxiv.org/abs/1903.01363); [Ross et al. view materialization](https://doi.org/10.1145/233269.233361); [Mistry et al. multi-query view maintenance](https://arxiv.org/abs/cs/0003006); [view redefinition adaptation](https://doi.org/10.1145/223784.223817). The 2026 source's own references identify its predecessors and explicitly cite the IVM-ε rebalancing method.

This is a targeted audit, not proof that no paper anywhere studies online exponent choice. The specific evidence-backed result is narrower: the dynamic-skew/repartitioning components originally motivating C5 are already present, and the remaining instance-adaptive `ε` claim is not supported by an isolated primary-source novelty gap or theorem.

## 6. Candidate mechanism and adversarial review

The candidate was a finite portfolio of exponents with hysteretic switching and versioned exact migration. No complete pseudocode is admitted because its central costs and target guarantee are unspecified. The required invariant would be `ActiveView_t = Q(D_t)` at every committed update, including while a second threshold state is built. If the old state remains query-active while the new one is built, updates must either be maintained in both states or logged and replayed before an atomic cutover; either choice consumes time and/or memory. Maintaining many complete threshold states multiplies materialized space and per-update work. These are not optional implementation details.

**Concrete failure of the naïve rebuild-on-switch implementation (not an impossibility theorem).** Let a policy choose `ε_A` in state family A and `ε_B` in family B, and suppose the two representations require rebuilding the affected partition/view state to switch. A stream alternates A,B,A,B,… with one tuple update per phase. Rebuilding each switch costs up to the theorem's `O(N^(1+mw))` preprocessing scale, so this implementation can spend `Θ(T N^(1+mw))` transition work, versus the fixed-threshold update baseline `O(T N^mw)` when `N` stays within one size band. Thus per-update threshold switching without a proven incremental migration or a bounded switching frequency can lose a factor `Θ(N)`. Hysteresis on degree membership does not itself prove that an arbitrary policy over ε values avoids this sequence. This falsifies the naïve policy, not all possible migration algorithms.

**Other adversaries that any future proof must cover:** a single degree oscillating around a switch boundary; a sudden persistent skew shift followed by reversal; high-degree values moved among several relations; deletions and insert/delete reversals; database size near major-rebalance boundaries; a switch whose new view tree has a much larger intermediate; dual-state peak memory; and enumeration requests during migration. In particular, a favorable static maintenance-width expression alone does not cover the work to transform `M_t` into a valid state for `ε_{t+1}`.

## 7. Gate result and exact blocker

* **Gate 1 — primary algorithm/theorem reconstructed:** PASS (author full-text preprint, all relevant sections/appendices read; publication metadata identity matched; ACM published full-text delta not compared).
* **Gate 2 — genuine limitation:** PARTIAL. The precise uncovered distinction is data-instance/trajectory-dependent online selection of `ε`, not dynamic heavy/light reassignment. Whether that improves any meaningful guarantee over the paper's minimax `ε` is not established.
* **Gate 3 — substantive mechanism beyond prior art:** FAIL. Portfolio, hysteresis, rebalancing and view migration are known components; no new invariant or comparison theorem was isolated.
* **Gate 4 — exact semantics/invariant:** NOT MET for a new policy. The required invariant is stated above, but no update/migration protocol proving it at every committed time was derived.
* **Gate 5 — full cost and space accounting:** FAIL. No bound on migration, dual maintenance, or peak view-state memory is proved.
* **Gate 6 — falsifiable analytical target:** FAIL. A legitimate target would need to specify a causal comparator (fixed minimax threshold, best causal static threshold, or offline dynamic schedule), a fixed query/workload class, and the exact memory/delay constraints. No meaningful improvement target survived this cycle.

The smallest unresolved mathematical question is: for a fixed query `Q`, does a causal policy selecting `ε_t` from current degree statistics achieve strictly lower *total* update-plus-transition work than the best fixed-ε scheme on any nontrivial stream class, under the same peak-space and exact constant-delay constraints? A publishable statement would need to specify that stream class and comparator, prove the migration invariant, and beat the existing minimax maintenance-width bound in a declared sense. This is not enqueued as a successor.

## 8. Future evaluation protocol (not run and not yet warranted)

No empirical comparison is justified until the preceding theorem-level target and exact migration algorithm exist. If they are later supplied, compare (i) the 2026 heavy-light implementation at its query-optimal fixed `ε`, (ii) a causal best-fixed threshold baseline selected only from past data, and (iii) the proposed causal adaptive policy. The offline best fixed and offline switching-cost sequence may be reported only as oracles, never as deployable algorithms. Freeze queries (triangle, 4-cycle, and one structurally distinct query), data scale, multiplicity semantics, and insert/delete streams; include stationary, alternating-boundary, sudden-shift, and shift-reversal skew. Use identical memory caps and exact result semantics. Measure update work and latency, migration/rebuild work, peak memory, output delay during cutover, and exactness against full recomputation. Repeated trials and uncertainty would be required. Falsify the proposed advantage if migration erases saved delta work, peak space exceeds the cap, or enumeration ceases to have its promised delay. No data, implementation, workload generator, benchmark, or model inference was run in this assignment.

## 9. Independent review and disposition

The adversarial review confirms that the earlier C5 wording understated the primary source: **changing skew is already addressed** insofar as it changes degree configurations and heavy/light membership, and changing total size also triggers amortized threshold-base rebalancing. The remaining difference—reoptimizing exponent ε from realized data—is real as a distinction of problem formulation, but not yet a defensible research contribution. The current paper's worst-case maintenance width is already minimized over ε and all degree configurations; a claimed gain must therefore be instance-sensitive and identify a workload comparator, not claim a better worst-case exponent by merely selecting ε online.

**Final class: F — no defensible research contribution in this cycle.** The source audit is a useful correction to the opportunity registry, not a new IVM theorem or algorithm. The dynamic-skew C5 mechanism is down-ranked/closed as currently formulated. This does not prove all distribution-adaptive IVM is solved; it says the proposed portfolio idea has not earned admission. No algorithm-design artifact is created, no task is enqueued, no experiment or benchmark is run, no Paper 3/4 or supervisor state is changed, and no follow-up cycle is launched.
