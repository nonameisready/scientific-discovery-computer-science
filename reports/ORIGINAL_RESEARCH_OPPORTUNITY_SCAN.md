# Original research opportunity scan (bounded, 2026-10-16)

**Decision: NO-GO for admitting a new theory task this cycle.** The strongest lead is a precise 2025-authored conjecture on distance-profile complexity in graphs of bounded simple treewidth. Its target is significant and remains explicitly conjectural in the latest version we could authenticate, but the only immediate proof obligation found is an unproved guard-family statement essentially as strong as the desired exponent improvement. The standard treewidth proof still loses one factor of `r`; the outerplanar proof's key circular-order monotonicity has no verified extension to simple treewidth 3. No task is added, no worker or experiment is started, and the theory queue remains intentionally idle.

This scan is a bounded source review, not an exhaustive proof that any question is open. “No later resolution found” below means only that the targeted primary-source and exact-title follow-up checks in this cycle found none. Search non-detection is not proof of absence.

## 1. What the previous campaign taught us

The campaign produced real mathematical work, but often stopped short of original, paper-level knowledge:

| Direction | What was actually achieved | Why it did not establish a publication-level breakthrough |
|---|---|---|
| Zero Extension sparsification | Source-matched reconstruction of the Reidl–Wahlström exact metric-sparsifier theorem; several correct feasibility, interface, tree/cactus, and contraction-only statements; failed constructions and scope corrections were preserved. | The label-independent exponent was not improved or ruled out. Several attractive reductions were elementary preprocessing, pairwise distinguishability did not lower-bound arbitrary joint contractions, and an early related 0-Extension claim in later work was retracted. Proof completion on restricted objects did not cross the original representative-set bottleneck. |
| Parallel token swapping on trees | Correct lower bounds, exact identities, a constructive arbitrary-permutation double-star `R ≤ 2 LB_hub` theorem, and fixed-`h` bounds were proved or independently reviewed. | The double-star result is a restricted elementary algorithmic corollary; standard star-transposition structure and routing literature sharply limit novelty. The fixed-`h` theorem has a parameter-dependent factor. No schedule-independent obstruction or identity-preserving exchange lemma solved the unbounded-hub/caterpillar problem. |
| Caterpillars / event DAGs | Extra-traversal identities and a fixed-pairing event-DAG characterization were proved. | The DAG criterion is equivalent to the known distance-optimal/happy-swap-only condition, not a new scheduling theorem. A swap-count bound does not control matching-round makespan; extra traversals remain hard to schedule. |
| Candidate selection | Primary-source checks and negative results became more careful; false scientific-completion claims were distinguished from artifact completion. | The process repeatedly selected nearby variants of the same tree-routing problem, and sometimes optimized for completing a bounded task rather than testing priority early. The novelty audit often came after proof construction. |

The useful separation is: (i) **proof success** means the quantified statement follows; (ii) **rediscovery** means a known theorem or criterion has been re-expressed; (iii) **elementary special case** means a valid restricted result without a new method; (iv) **broader progress** changes an open parameter boundary or settles a meaningful part of a general problem; and (v) **publication-level originality** additionally requires a verified prior-art boundary and a contribution that survives expert comparison. The double-star theorem is proof-successful, but category (iii), with category (v) unverified. The caterpillar DAG equivalence is category (ii). No previous Zero Extension result reached category (iv) for the central exponent question.

Method change: make theorem-level prior-art comparison a gate *before* proof expansion; require the first lemma to be independently meaningful rather than a renaming of the target; pursue at most one new direction; and leave the queue idle when the first honest proof attempt only reproduces a known bound.

## 2. Candidate scan

Scores are qualitative (`high / medium / low`), not probabilities. In “status,” **unresolved-looking** is deliberately weaker than “open.” “Fast falsifier” means the cheapest mathematical test of the proposed first lemma, not evidence that the full problem is easy.

### 1 — Profile complexity for bounded simple treewidth (strongest lead; not admitted)

**Problem.** For each fixed integer `t ≥ 1`, prove or refute that there is a constant `C_t` such that every finite simple undirected graph `G` with simple treewidth `stw(G) ≤ t`, every integer `r ≥ 1`, and every `A ⊆ V(G)` with `|A|=k ≥ 1` satisfy

`pc_r(G,k) ≤ C_t r^t k`,

where `pc_r` counts distinct non-all-infinite vectors `(min(dist(v,a), r+1))_{a∈A}` (the paper encodes values above `r` as `+∞`). Narrow first target: `t=3`, namely `pc_r(G,k)=O(r^3 k)` for `stw(G)≤3`.

**Best authenticated boundary.** Beaudou et al. prove `O_t(r^{t+1}k)` for treewidth at most `t`, with matching-order lower constructions for general treewidth; they prove `O(r^2 k)` for outerplanar graphs and explicitly conjecture `O_t(r^t k)` for bounded simple treewidth. The conjecture holds for `t=1,2`; simple treewidth 2 is exactly outerplanar. The exponent improvement is one full power of `r` and would be asymptotically tight if true. The arXiv history lists v3 on 2025-12-13, while the HTML body identifies the manuscript as dated 2026-08-24; we preserve that version/date discrepancy rather than infer a post-v3 revision. The current full text still states the conjecture. [Primary paper, v3](https://arxiv.org/abs/2501.08895v3), [full text / Conjecture 33](https://arxiv.org/html/2501.08895).

**Why it matters.** It would close a real exponent gap in a graph-structural measure used in metric dimension, locating/dominating problems, and distance-based kernelization. It is not a mere fixed-size extension: the target is a uniform exponent improvement over a broad graph class.

**First proof obligation attempted.** A sufficient structural lemma would give, for each `G,A,r`, at most `C k` vertex sets `S` of size at most 3 such that every vertex `v` with a finite `r`-profile to `A` has one such `S` intersecting every `v`–`a` path of length at most `r`, for every `a∈A`. For a fixed guard `S`, each distance profile to `A` is determined by the at-most-three truncated distances from `v` to `S`: for each `a`, if a path of length at most `r` exists, it meets `S`, and `dist(v,a)=min_{s∈S}(dist(v,s)+dist(s,a))`; otherwise its truncated coordinate is infinite. Thus this guard-family lemma would yield at most `Ck(r+2)^3=O(r^3k)` profiles.

**Proof attempt and exact failure point.** The authenticated general treewidth proof gives an `O(k)` family of guards, but its guards have size up to `2(t+1)`; combined with a `K_{t+2}`-minor-free profile bound this yields `O_t(r^{t+1}k)`, not the desired exponent. The outerplanar improvement instead orders vertices around an outer boundary and uses a monotonicity lemma on BFS layers to count only `O(r^2k)` profiles. No valid analogue of that circular order was found for simple-treewidth-3 graphs. In an LCA-closure decomposition, a component can attach to two marked bags; the direct separator argument then uses both adhesion boundaries, and we found no proof that their joint distance signatures collapse to a single 3-set or have only `O(r^3)` types. This is a precise obstruction to the attempted proof route, **not** a counterexample to the conjecture.

**Fast falsification test.** First seek a simple 3-tree with two-sided LCA corridors and `A` on both sides whose profiles realize `Ω(r^4 k)`; an asymptotic construction would refute the conjecture, while a finite example can only refute the proposed guard lemma. Check also the complete 3-tree base `K4`, simple 3-tree chains, and attachments to distinct unused triangles. No computational search was run.

**Later-work audit / risk.** Exact-conjecture search and the latest accessible v3 source leave the conjecture stated, but no comprehensive forward-citation proof is claimed. Main risk: the general lower construction for treewidth may already embed in simple treewidth `t`, which would contradict the conjecture; the source authors say their lower bound only shows the proposed exponent would be tight if true, but this scan did not reconstruct that construction's simple-treewidth. **Originality risk: medium** (source-authored conjecture is explicit; a short proof via a known structural theorem would be a rediscovery). **Difficulty: high.** **First-lemma feasibility: not passed**—the small-guard family is an equivalent-strength structural bottleneck, not yet a proof strategy. **Falsifier: high quality.**

### 2 — Happy-leaf characterization in sequential tree token swapping (source-stated, but not admitted)

**Problem.** Characterize trees `T` for which, for every bijective token assignment, there exists an optimal sequential swap sequence that never swaps a leaf while that leaf contains its destination token (a “happy leaf”).

**Known results / gap.** Biniaz et al. give a counterexample to the universal happy-leaf conjecture and explicitly ask for a characterization; they note any such tree must avoid their 10-vertex obstruction as a subtree. They also discuss polynomial solvability on trees with the property and the difficulty already present for brooms. [Primary DMTCS paper](https://dmtcs.episciences.org/en/articles/8383), [full text/open questions](https://dmtcs.episciences.org/10817/pdf).

**First lemma / fast falsifier.** Test whether the forbidden 10-vertex subtree is sufficient as well as necessary; the first failure should be a smallest tree without that subtree and a token permutation whose every optimum moves a happy leaf. Exact enumeration could falsify a finite characterization, but no computation is authorized here and finite non-failure would not prove sufficiency.

**Later status / assessment.** A bounded exact-phrase search found no later characterization; that is not exhaustive citation tracing. It is important and explicitly open in the primary source, but overlaps the campaign’s exhausted token-swapping neighborhood, and no structural characterization theorem survived an initial adversarial review. **Originality high; significance high; confidence unresolved medium; proof difficulty very high; first proof strategy weak; rediscovery risk medium. Not admitted.**

### 3 — Metric Dimension on treewidth-two graphs (series-parallel graphs)

**Problem.** Determine whether Metric Dimension is polynomial-time solvable or NP-hard on graphs with `tw(G)≤2` (equivalently, partial 2-trees; for connected 2-connected blocks, series-parallel graphs).

**Known results / gap.** Bonnet–Purohit (IPEC 2019) explicitly say the complexity of the treewidth-two case is open while proving W[1]-hardness parameterized by treewidth and an ETH lower bound. Li–Pilipczuk then prove NP-hardness at treewidth 24, not 2. Bousquet–Deschamps–Parreau (2023) obtain FPT parameterized by treewidth on chordal graphs, a different restriction that does not cover all partial 2-trees. [IPEC 2019 primary paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.IPEC.2019.5), [IPEC 2021 hardness](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.IPEC.2021.24), [2023 chordal result](https://arxiv.org/abs/2303.10646).

**First lemma / fast falsifier.** Try a bounded-state dynamic program over a series-parallel decomposition; adversarially test whether a partial solution can be summarized by boundary distance vectors of unbounded range. For hardness, first seek a reduction preserving treewidth 2; the known width-24 reduction does not transfer by parameter substitution.

**Later status / assessment.** The source-stated gap survives the specific later results checked; no exhaustive update search. High significance but a P-vs-NP-hard boundary is a large and difficult jump, and the obvious DP state has not been bounded. **Originality medium-high; tractability low; gap confidence medium; first proof route low; rediscovery risk medium. Not admitted.**

### 4 — Planar treelength recognition at threshold two

**Problem.** Determine the complexity of deciding whether a planar graph has treelength at most 2 (tree decomposition with every bag having graph-diameter at most 2); alternatively, find a sharp structural characterization enabling a polynomial algorithm or prove hardness.

**Known results / gap.** Dissaux, Ducoffe, and Nisse give a quadratic algorithm for treelength≤2 on series-parallel graphs and a 3/2-approximation for treelength on that class; their paper identifies planar treelength complexity as unknown. Their proof uses an infinite forbidden-isometric-subgraph characterization specific to series-parallel graphs. [Primary 2023 paper](https://doi.org/10.1016/j.dam.2023.07.022).

**First lemma / fast falsifier.** Test whether a minimal planar graph of treelength≥3 must contain a bounded-size isometric obstruction; large isometric cycles and nested separators are immediate adversarial cases. The fastest falsifier is a family of planar graphs with unbounded minimal obstruction size, but finding finite examples alone would not establish complexity.

**Later status / assessment.** A bounded search found no later planar classification; the cited source itself is 2023 and cannot certify status through 2026. It is distinct and potentially important, but no exact reduction/obstruction conjecture was isolated. **Originality medium; significance medium-high; gap confidence medium-low; proof route weak; risk of broad unsolved problem. Not admitted.**

### 5 — Minimum Sum Vertex Cover approximation gap

**Problem.** Improve the polynomial-time approximation factor for Minimum Sum Vertex Cover (MSVC), or improve conditional hardness, closing some portion of the interval between known approximation and UGC-hardness.

**Known bounds.** Bansal, Batra, Farhadi, and Tetali give a `16/9` approximation and matching integrality gap for their natural LP. Stanković (APPROX/RANDOM 2022) proves UGC-hardness below `1.0748` (and `1.0157` for regular graphs). Aute–Panolan give parameterized algorithms under vertex-cover and clique-modulator parameters, not a better general approximation. [Primary 16/9 paper](https://epubs.siam.org/doi/10.1137/21M1434052), [2022 hardness paper](https://drops.dagstuhl.de/doi/10.4230/LIPIcs.APPROX-RANDOM.2022.50), [2024 parameterized paper](https://arxiv.org/abs/2401.05085).

**First lemma / fast falsifier.** Search for a rounding inequality improving the LP's 16/9 guarantee or a stronger integrality gap on a restricted graph family. The fastest falsifier is a small graph for a proposed inequality; however, simply improving a finite instance does not improve the worst-case algorithmic ratio.

**Later status / assessment.** The 16/9 versus 1.0748 gap remains visible in checked primary sources; not an exhaustive 2026 citation audit. Significant approximation problem, but this scan found no concrete rounding invariant or reduction seed. **Originality medium; significance high; unresolved-bound confidence medium; tractability very low; first lemma absent; rediscovery risk high. Not admitted.**

### 6 — Longest Path parameterized multiplicatively above girth (directed graphs)

**Problem.** The directed version asks, given a digraph `G` and `k`, for a directed path of length at least `k·girth(G)`; the open-looking parameterized boundary is whether the XP algorithm can be improved to FPT or whether matching parameterized hardness holds.

**Known results.** Jacob, Włodarczyk, and Zehavi prove Longest Cycle above girth is W[1]-hard, resolving an earlier open question, and Longest Path above girth is in XP. They also prove W[1]-hardness of Hamiltonian Cycle/Path parameterized by directed feedback vertex set. [Primary ESA 2023 paper](https://drops.dagstuhl.de/opus/volltexte/2023/18723/), [arXiv](https://arxiv.org/abs/2308.06145).

**First lemma / fast falsifier.** Analyze whether the XP dynamic program can be compressed to a bounded state on a DFVS modulator; test against the paper's hardness gadgets before attempting FPT. This quick check may instead show the proposed parameter is already subsumed by a reduction.

**Later status / assessment.** The paper resolves the cycle case but does not assert FPT for directed Longest Path above girth. A bounded exact-title search found no later classification. The gap is precise but likely inherits the hard core of directed path problems; not enough proof seed to admit. **Originality medium; importance high; current-gap confidence medium; difficulty very high; immediate strategy weak; rediscovery risk medium. Not admitted.**

### 7 — Planar SSUF cost-preserving rounding after the 2026 counterexample (watchlist, not admitted)

**Problem.** For an acyclic planar single-source unsplittable-flow instance with fractional flow `x`, terminal demands bounded by `d_max`, and arc costs, determine the smallest universal additive capacity-violation coefficient `λ` sufficient to guarantee an unsplittable routing of cost at most `cᵀx` and arc loads at most `x+λd_max`.

**Published boundary and live correction.** Traub, Vargas Koch, and Zenklusen (published 2026-07-22) prove planar cost-preserving rounding with `2d_max` capacity violation and exact `d_max` for the cost-free lower/upper-bound variant; their article says the sharper cost conjecture remained open. A September 2026 Zenodo preprint reports an independently exact-rational-verified seven-vertex counterexample to the exact `λ=1` cost conjecture with a `16/15` violation threshold, and explicitly says the `O(d_max)` question remains. It is not yet a peer-reviewed theorem in the sources checked; treat the counterexample as independently verified finite evidence, not settled publication status. [Published primary paper](https://link.springer.com/article/10.1007/s10107-026-02365-x), [exact verification report](https://zenodo.org/records/22835200).

**First lemma / fast falsifier.** Independently reconstruct the rational instance and solve its small path-assignment separation LP by exact arithmetic; then determine whether a two-terminal planar instance can force any `λ>1`. The smallest proof target is not the already-refuted exact conjecture, but a certified lower bound on the optimal coefficient in the two-terminal case.

**Later status / assessment.** The exact `λ=1` conjecture is apparently refuted by a public independent verification, while the relaxed coefficient is a live and important gap. However, provenance and expert/peer review are unsettled, and the first step would be replication of an external counterexample rather than original theorem discovery. **Originality potential high; significance high; boundary confidence medium; immediate feasibility medium; verification risk high. Not admitted in this theorem-discovery cycle.**

## 3. Qualitative ranking and admission gates

| Rank | Direction | Originality potential | Importance | Gap confidence | Concrete proof route | Bounded result likelihood | Independent verification | Admission |
|---:|---|---|---|---|---|---|---|---|
| 1 | Bounded-simple-treewidth profile complexity, first `stw≤3` | High | High | High that source still states it; medium that no later result exists | Medium-low: an `O(k)` three-vertex guard-family lemma would suffice, but is not established | Low-medium | High | **No-go: Gate 5 not passed** |
| 2 | Happy-leaf characterization | High | High | Medium | Low | Low | Medium | Not admitted; overlaps exhausted campaign and lacks a structural seed |
| 3 | Planar treelength≤2 | Medium-high | Medium-high | Low-medium | Low | Low | Medium | Not admitted; no sharp lemma isolated |
| 4 | Metric Dimension at treewidth 2 | Medium-high | High | Medium | Low | Low | High | Not admitted; the boundary is real but reduction/DP route absent |
| 5 | MSVC approximation gap | Medium | High | Medium | Low | Very low | High | Not admitted; no rounding or hardness idea |
| 6 | Directed Longest Path above girth | Medium | High | Medium | Low | Low | High | Not admitted; cycle result already resolved the neighboring target |
| 7 | Planar SSUF coefficient after 2026 counterexample | High | High | Medium | Medium | Medium | Medium-high | Not admitted; verification/provenance and novelty boundary need independent audit |

The `stw≤3` conjecture passes the source, precision, significance, and bounded-scope checks. It fails the adversarial-feasibility gate **for admission now**, not because a counterexample was found, but because the proposed first lemma is an unproved strengthening whose only derivation attempt stalls exactly at two-sided decomposition corridors. The outerplanar proof technique is not transferable by a known theorem, and the general treewidth proof gives only `r^4 k`. No positive claim is warranted. The remaining directions either lack an equally strong explicit theorem-sized entry point, are in the exhausted token-swapping neighborhood, or have a newer result whose verification status is still unsettled.

**Queue disposition:** no task admitted; no queue/state/experiment counters changed. The theory track remains idle by design. Best next action, if revisited in a future independently scoped cycle, is source-level reconstruction of the Joret–Rambaud lower construction and Beaudou et al.'s guarding-set proof to decide whether the simple-3-tree obstruction is structural or whether the conjecture's proposed exponent conflicts with an existing construction. That audit is a *recommendation*, not a scheduled task.

## 4. Theorem-attempt outcome and independent review

No new theorem was attempted because no candidate passed all admission gates. For the leading candidate, we derived only the following **conditional reduction**: an `O(k)` family of radius-`r` guards each of size at most 3 would imply `pc_r(G,k)=O(r^3k)` by counting at most `(r+2)^3` truncated distance vectors per guard. This implication is a direct counting argument and is not a new result about simple-treewidth graphs. The required guard-family existence is unproved.

Independent adversarial review:

* A guard set must hit every short path to every landmark simultaneously; merely being a separator for one landmark or one chosen shortest path is insufficient.
* For two-sided corridors in an LCA-closure decomposition, the union of two adhesion boundaries may have up to six vertices. Counting all distance vectors to this union loses the desired exponent; no valid correlation bound was found.
* The `O(r^{t+1}k)` treewidth theorem is an established fallback, not evidence of `O(r^t k)` on simple treewidth.
* The 2026 SSUF report is not silently treated as a peer-reviewed theorem; the older journal article's “open” statement is stale relative to the later verification report.
* No citation-search non-detection is converted into an open-problem proof.

**Classification:** F for new mathematical result this cycle; the conditional guard-counting implication is elementary and is not submitted as original. No publication candidate has been established.
