# Independent audit: double-star parallel token swapping and research direction selection

**Audit checkpoint:** `c560141`
**Audited claim:** `THEORY-PARALLEL-TOKEN-SWAPPING-DOUBLE-STAR-ALL-PERMUTATIONS-005`
**Method:** independent proof reconstruction and bounded primary-source audit; no computation or experiment.

## 1. Independent theorem statement

Let `T` consist of adjacent vertices `u,v`, leaves `L` adjacent to `u`, and leaves `R` adjacent to `v`. Either leaf set may be empty. Each vertex initially contains a distinct token, and each token has a prescribed destination, with the destination map a bijection of `V(T)`. A round is a matching of tree edges whose endpoint tokens are swapped.

For each token `t`, let `P_t` be its source-to-destination path. Define

\[
D=\max_t |P_t|,\qquad C(e)=|\{t:e\in P_t\}|,\qquad r(e)=C(e)/2,
\]
\[
W(x)=\sum_{e\ni x} r(e),\qquad LB_{\rm hub}=\max\{D,\max_x W(x)\}.
\]

Cut balance under a bijection implies that `C(e)` is even and each direction across `e` has `r(e)` tokens. Any schedule needs at least `r(e)` swaps on `e`, at least `D` rounds for a longest token path, and at least `W(x)` rounds incident to a vertex `x`; hence `LB_hub <= OPT`.

**Theorem.** There is a deterministic `O(n)` algorithm producing a matching-round schedule of length

\[
R\le 2LB_{\rm hub}(T,\pi)\le 2OPT(T,\pi).
\]

This is a theorem for double-stars only.

## 2. Reconstructed algorithm and proof

Partition vertices into `A=L∪{u}` and `B=R∪{v}`. Let `r` be the number of tokens initially in `A` whose destinations lie in `B`. Bijection implies that exactly `r` tokens in `B` target `A`. Let `a` and `b` be the counts of initially misplaced leaves in `L` and `R`.

### Phase I: side correction

Repeat `r` times. If `u` does not currently hold an `A→B` token, exchange `u` with any leaf in `L` that holds one. Make the analogous preparation at `v` if needed. Execute both preparations in one round if both are needed, then swap `u,v` in the next round.

Immediately before iteration `j`, there are exactly `r-j` `A→B` tokens still in `A` and `r-j` `B→A` tokens still in `B`. This holds initially. Each preparation is within a side and changes no side count. If a center lacks an outgoing token while its side count is positive, an outgoing token must be on a leaf, since the center is the only other position in that side. After preparation both centers hold outward tokens; the central swap transfers one token in each direction, and both remaining counts decrease by one. This proves the invariant and rules out a stranded outgoing token.

The two possible preparation edges have form `u-x` and `v-y`, so are vertex-disjoint; the bridge swap is in a separate round. Thus every round is a matching and Phase I takes at most `2r` rounds.

Any selected leaf is holding an outward token and therefore is misplaced at that instant. A leaf selected earlier receives a center token that was not outward—the selection guard says the center lacked an outward token—and is never again an outward-token source. Central swaps do not touch leaves. Thus no initially correct leaf is selected, no prepared leaf is reused, and the number of incorrect leaves afterward is at most `a` on the left and `b` on the right. This argument tracks actual tokens, not abstract branch representatives. It allows center tokens to target the center, a local leaf, or the opposite side; Phase I only establishes the correct side.

When the `r` iterations end, every token is on the same side as its destination. The residual target map on each side is a permutation of that side's star.

### Phase II: star permutations

On a star with center `c`, consider each cycle of the position-to-destination permutation.

* A nontrivial cycle containing the center can be written `(c,z₁,…,z_q)` in directed position-map order. Swaps `(c,z₁),…,(c,z_q)` place every token at its target in `q` swaps.
* A leaf-only cycle `(z₁,…,z_q)`, `q≥2`, is sorted by `(c,z₁),…,(c,z_q),(c,z₁)`. The last swap restores the center token, and the word uses `q+1≤2q` swaps.
* Fixed points, including fixed leaves and a fixed center, are skipped.

These words follow by tracking the token at each position through the listed swaps. Cycles within one star are serialized because they share `c`. The left and right stars have disjoint vertex sets, so their current swaps can run in lockstep; if one side has no swap at a slot, only the other side swaps. If `q_A,q_B` are the post-Phase-I numbers of incorrect leaves, Phase II costs at most `2q_A` and `2q_B` rounds on the two sides, hence at most `2max(a,b)` total rounds.

Each incorrect leaf contributes one to its incident-edge demand; a correct leaf contributes zero. The central edge contributes `r`. Therefore `W(u)=r+a` and `W(v)=r+b`; leaf workloads are at most their center workload. Combining phases,

\[
R\le2r+2\max(a,b)=2\max\{W(u),W(v)\}\le2LB_{\rm hub}\le2OPT.
\]

There are `O(n)` transfers and at most `O(n)` star transpositions. Cycle decomposition and schedule generation are `O(n)`; the output has `O(n)` rounds and swaps. The identity permutation produces no swaps. With no leaves, the unique central exchange, if needed, takes one round and satisfies the bound. This includes the two-vertex tree. All cases preserve individual token identities.

### Adversarial proof checklist

The center is either already outward (no preparation) or, if outward demand remains and it is not outward, an outward leaf exists. An exchange in preparation cannot create a new outward leaf at the selected position, because the center token moved into it was locally destined. No correct leaf is displaced. After a bridge swap the received token is side-correct; it need not be at its final vertex, which is why the star permutation phase is essential. The center-containing and leaf-only cycle words have different lengths, and both are accounted for. Operations are not incorrectly parallelized within one star. Empty sides, center destinations, fixed leaves, and the identity case cause no exception. I found no counterexample or proof gap in the claimed double-star theorem.

## 3. Prior-art and publication-value audit

| Primary source | Exact setting and result | Relation to this theorem |
|---|---|---|
| Roberts, Symvonis & Zhang (WADS 1995), [*Routing on Trees via Matchings*](https://doi.org/10.1007/3-540-60220-8_67) | In the same matching-routing model, gives offline worst-case routing-number bounds: `rt(T)≤2n` for maximum-degree-3 trees; `≤2n+o(n)` for bounded-degree trees; and `≤13n/5` for arbitrary trees. | This is the closest classical tree theorem audited. A genuine double-star can have unbounded center degrees, so the degree-3 theorem covers only bounded tiny instances. The arbitrary-tree theorem applies but depends on `n`, not the given permutation's `LB_hub`; it does not directly imply `R≤2 LB_hub`. |
| Alon, Chung & Graham (1994), [*Routing Permutations on Graphs via Matchings*](https://doi.org/10.1137/S0895480192236628) | Introduces the matching-round routing-number model and proves general worst-case bounds/lower bounds. | Same model and basic workload intuitions, but the statements are about worst-case routing number, not this instance-wise double-star guarantee. |
| Zhang (1999), [*Optimal Bounds for Matching Routing on Trees*](https://doi.org/10.1137/S0895480197323159) | For every `n`-node tree and permutation, gives a worst-case bound `3n/2+O(log n)` rounds via tree partitions. | Broader host class but worst-case-in-size guarantee; incomparable to the instance-relative bound. |
| Aichholzer et al. (ESA 2022), [*Hardness of Token Swapping on Trees*](https://doi.org/10.4230/LIPIcs.ESA.2022.3) | Defines parallel token swapping by matching rounds and proves NP-completeness on trees (also on subdivided stars). | Establishes hardness of exact optimization, not a double-star approximation; it does not invalidate a restricted constructive algorithm. |
| Bansal, Günlük & Shapley (2025 version), [*Parallel Token Swapping for Qubit Routing*](https://arxiv.org/abs/2411.18581) | Gives constant-factor approximation guarantees for cycles, subdivided stars and grids; a subdivided star has one branching junction. Their subdivided-star bound is `R ≤ 4 OPT + min{OPT,h}+1` in their notation. | Genuine double-stars with both centers branching are not one-junction subdivided stars. Degenerate cases overlap. The topology and `OPT`-relative guarantee do not directly imply this `LB_hub`-relative result. |
| Sadanandan & Chitturi (2022), [*Optimal Algorithms for Sorting Permutations with Brooms*](https://doi.org/10.3390/a15070220) | Computes minimum **sequential swap count** on brooms and double brooms. | A different objective: arbitrary serial swaps versus parallel matching-round makespan. It does not imply this theorem. |
| Irving & Rattan (2009), [*Minimal Factorizations of Permutations into Star Transpositions*](https://doi.org/10.1016/j.disc.2008.02.018) | Studies minimal factorizations under the generating set of star transpositions. | Supports the standard local cycle words; those words are not a new mathematical contribution here. |

### Theorem-level resolution of the prior-art question

The double-star host is exactly a tree of diameter at most three (diameter three when both centers have at least one pendant leaf on their side; degenerate cases have smaller diameter). Roberts–Symvonis–Zhang do not state a diameter-three or double-star theorem in the publisher's theorem summary. Their stated structural parameters are order `n` and maximum degree. Thus their maximum-degree-three bound cannot handle general double-stars, while their arbitrary-tree bound is a worst-case `O(n)` statement. Zhang's later `3n/2+O(log n)` theorem is likewise a worst-case bound for every n-vertex tree. Neither is an instance-sensitive theorem in terms of the fixed permutation's `LB_hub`.

This distinction matters even for fixed diameter: a double-star can have arbitrarily many leaves, while a particular permutation can move only two leaf tokens and have `LB_hub=2`; an `O(n)` routing-number bound alone cannot yield the numerical `2 LB_hub` bound. This observation is about what follows from those theorem statements, not a proof that no corollary can be derived after additional instance reduction.

**Direct-implication verdict:** none of the audited classical results directly states or implies `R(DS,π)≤2 LB_hub(DS,π)` for every double-star and permutation. They establish the routing model and coarser host-size worst-case bounds; they do not subsume the load-sensitive guarantee as stated. We also found no theorem specifically for diameter-three trees in the audited primary sources. This is a bounded search conclusion, not a global absence/priority proof.

**Contribution-value verdict:** the current theorem is best described as a correct, apparently unpublished elementary restricted-class corollary/algorithmic guarantee, not a credibly novel standalone algorithmic contribution. Its proof exploits a single central cut and two disjoint star sorting problems; its cycle operations are standard star-transposition factorizations. The gap between “not directly implied by the audited theorem statements” and “publishably original” is substantial, and the current result does not cross it. Do not make a firstness claim or present this theorem alone as a paper-level breakthrough.

The smallest meaningful strengthening worth considering—only if a concrete proof route emerges—is an instance-sensitive constant-factor theorem for a graph class with an unbounded number of interacting hubs, or a sharp exact characterization of the routing number/optimal schedule for all double-stars. Merely changing the constant, restating the two-phase schedule, or adding another fixed number of centers would not be enough. The already-completed candidate screen remains in force: arbitrary-tree approximation lacked a surviving exchange lemma; the happy-leaf characterization lacked a candidate structural theorem; weighted-tree and double-broom extensions were too close to substantial existing results. No new direction is activated and the theory queue remains idle.

## 4. Candidate research directions and admission decision

Scores are qualitative triage, not forecasts or proof of novelty. “Open evidence” below means the cited primary sources leave a boundary visible; it is not a claim that no later result exists.

| Rank | Candidate | Open-boundary evidence and significance | First proof obligation / quick failure test | Decision |
|---:|---|---|---|---|
| 1 | A constant-factor matching-round approximation for arbitrary-tree token swapping relative to path length plus vertex workload | Aichholzer et al. prove exact hardness on trees; Bansal et al. cover selected topologies, not arbitrary trees. The gap is important but broad, and the present campaign has already failed to produce a caterpillar exchange lemma. | State a token-preserving exchange/order lemma controlling both precedence depth and vertex contention; falsify it first on a parameterized caterpillar with overlapping busy hubs. No such surviving lemma currently exists. | **Not admitted.** Too broad after repeated bounded routes without a candidate invariant; no new small counterexample cycle. |
| 2 | Characterize trees for which every token-swap instance has an optimal schedule preserving happy leaves | Biniaz et al. explicitly pose characterization of the happy-leaf property as an open question and give a finite obstruction. This is a precise combinatorial boundary in sequential token swapping, distinct from PTS makespan. | Determine whether the known forbidden subtree is merely necessary or can be extended to a finite/minor-like obstruction characterization; first challenge any proposed closure rule with the published 10-vertex witness. | **Not admitted this cycle.** The paper identifies the question, but no concrete candidate characterization or proof seed has yet been established here. |
| 3 | Improve or parameterize positive-weight token-swapping approximations on trees | Wein & Zhang (2025), [*Settling Weighted Token Swapping up to Algorithmic Barriers*](https://arxiv.org/abs/2507.22450), already gives a tree approximation ratio `1+W/w` for positive weights and barrier results. | A meaningful target would have to improve dependence on the weight ratio or identify a sharper instance lower bound; no specific gap from the paper was isolated. | **Rejected for now.** Existing theorem is substantial and the new parameterized target is not yet specific. |
| 4 | Exact sequential swapping on double brooms or extension to nearby broom classes | Sadanandan & Chitturi already provide optimal sequential algorithms on broom/double-broom structures. | Any extension would need a class not subsumed by their tree family and an exact recurrence not already implied by their algorithm. | **Rejected.** Too close to established restricted-class results; no defensible new lemma identified. |

No candidate currently combines a verified current gap with a theorem-sized first obligation that survives a quick adversarial check. **No successor theory task is admitted.** Leave the theory queue idle rather than create work for its own sake. The two best leads remain arbitrary-tree PTS approximation (high significance, low present specificity) and the happy-leaf characterization question (clear source-stated open boundary, but no candidate structural theorem yet).

## 5. Repository/research-state disposition

The traversal identities remain proved; only the event-level prose was wrong and is corrected in the accounting note with the path `x-m-y` schedule. The fixed-pairing DAG equivalence remains a representation of the known happy-swap-only distance-optimality criterion, not a new routing result. The double-star theorem is independently reconciled as mathematically complete for its declared class; the broader-tree flag is not a gap in that theorem. Historical worker execution outcomes and append-only supervisor events are not rewritten. Paper 3/4, frozen cohorts, and experiment counters are untouched. No experiment or supervisor was started. The theory queue remains with no pending task.
