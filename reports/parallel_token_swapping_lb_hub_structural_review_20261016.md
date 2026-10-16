# Structural lower bounds for parallel token swapping on trees

**Follow-up task:** `THEORY-PARALLEL-TOKEN-SWAPPING-LB-HUB-STRUCTURAL-002`

**Parent checkpoint:** `6c29792` and `reports/parallel_token_swapping_tree_approximation_proof_20261016.md`

**Date:** 2026-10-16
**Status:** bounded mathematical proof cycle; no computation, experiment, supervisor start, or budget renewal.

## 1. Scope and preserved results

The previous checkpoint already established, and this note does not re-prove, the exact fixed-center cyclic star family with `OPT=m+1`, the valid vertex-load lower bound, and the fixed-hub return lemma. The purpose here is narrower:

1. make the cut-crossing quantity exact rather than merely even-looking;
2. separate unavoidable traffic from schedule-dependent detours;
3. compare the star obstruction with the published subdivided-star stretch result;
4. stress-test the central conjecture
   \[
      \operatorname{OPT}(T,\pi)\le \alpha\,LB_{\rm hub}(T,\pi)
   \]
   without claiming either a proof or an unbounded counterexample.

The outcome is a rigorous structural increment, not an approximation theorem.

## 2. Model and notation

Let `T=(V,E)` be a finite tree. There is one distinct token at every vertex. A token initially at `u` has a unique destination `\pi(u)`, where `\pi` is a permutation of `V`. A round is a matching of `T`; every matching edge swaps its two endpoint tokens simultaneously. Let `OPT(T,\pi)` be the minimum number of rounds.

For an edge `e`, deleting `e` gives components `A_e` and `B_e`. Let

\[
 x_e=|\{u\in A_e:\pi(u)\in B_e\}||.
\]

The source-to-destination path of a token is unique. Thus a token path contains `e` exactly when its endpoints lie on opposite sides of the cut.

## 3. Exact parity and directional demand

### Lemma 1 (cut balance and even crossing count)

For every tree edge `e`,

\[
 |\{u\in A_e:\pi(u)\in B_e\}|
 =|\{u\in B_e:\pi(u)\in A_e\}|=x_e.
\]

Consequently,

\[
 C(e)=2x_e,
 \qquad r(e):=C(e)/2=x_e.
\]

#### Proof

There are exactly `|A_e|` tokens initially in `A_e`. Since `\pi` is a bijection, exactly `|A_e|` destinations lie in `A_e`. Tokens starting in `A_e` and ending in `A_e` account for the same number on both sides. Therefore the number leaving `A_e` equals the number entering it. The two numbers are respectively the displayed `A_e\to B_e` and `B_e\to A_e` counts. A token path crosses a tree cut exactly when its endpoints are separated by the cut, so `C(e)` is their sum, `2x_e`. ∎

The quantity `r(e)` is not a rounding convention. It is the exact number of tokens that must cross from one side of `e` to the other, in each direction, in the net source-to-destination flow. This identity uses the one-token-per-vertex permutation assumption; it is not valid without the balanced occupancy condition.

## 4. Mandatory traffic versus detours

Fix a particular valid schedule `\sigma` of `R` rounds. Let `s_\sigma(e)` be the number of rounds in which `e` is selected. Every selected edge swaps exactly one token from `A_e` to `B_e` and one from `B_e` to `A_e`. Lemma 1 therefore gives the exact inequality

\[
 s_\sigma(e)\ge r(e).
\]

Define the nonnegative edge slack

\[
 \Delta_\sigma(e):=s_\sigma(e)-r(e)\ge0.
\]

This is the rigorous schedule-level separation:

* `r(e)` is mandatory net crossing traffic forced by the permutation;
* `\Delta_\sigma(e)` is additional use of `e` beyond that traffic.

The slack is the only part that can safely be called a detour at this level of abstraction. A particular extra swap may be needed to restore an occupied vertex, may move a token temporarily away from its shortest path, or may be part of a different valid routing decomposition. Those causes are not identifiable from `r(e)` alone.

For a vertex `v`, define its actual incident workload and its mandatory load by

\[
 L_\sigma(v):=\sum_{e\ni v}s_\sigma(e),
 \qquad
 W(v):=\sum_{e\ni v}r(e).
\]

Then, exactly,

\[
 L_\sigma(v)=W(v)+\sum_{e\ni v}\Delta_\sigma(e).
\]

Because a matching contains at most one edge incident with `v` per round,

\[
 R\ge L_\sigma(v)\ge W(v).
\]

Together with the path-length bound, this recovers the integer lower bound

\[
 LB_{\rm int}(T,\pi)=
 \max\left\{D,\max_v\left\lceil W(v)\right\rceil\right\}
 \le \operatorname{OPT}(T,\pi).
\]

The fixed-hub `q(v)+1` lemma from the parent checkpoint is precisely a statement that, under its fixed-token assumptions, at least one unit of incident slack is forced. It should not be confused with an assertion that all detours are already represented by `W(v)`.

## 5. The star family exposes a second, cycle-structured slack

The prior checkpoint used one cyclic permutation of all leaves. A useful extension is to keep the same star and fixed center but allow the leaf permutation to have several disjoint nontrivial cycles.

Let `K_{1,m}` have center `c`. The center token is fixed. Let the leaf permutation move exactly `m'` leaves and decompose on those leaves into `q` nontrivial cycles. Fixed leaves, if any, are irrelevant to the target permutation. Every moved leaf edge has `r(e)=1`, so

\[
 D=2,\qquad W(c)=m',\qquad q(c)=m',
 \qquad LB_{\rm hub}=m'+1.
\]

### Proposition 2 (exact fixed-center star formula)

For this family,

\[
 \operatorname{OPT}(K_{1,m},\pi)=m'+q.
\]

#### Proof

All star edges meet at `c`, so one round contains at most one swap. Every schedule is therefore a word of star transpositions `(c,\ell)` whose product is the target leaf permutation and fixes `c`.

For the upper bound, realize each leaf cycle of length `\ell` by the standard star-transposition word that visits its `\ell` leaves and repeats one leaf to return the center token. It has length `\ell+1`. Concatenating the `q` cycle words gives `\sum(\ell_i+1)=m'+q` rounds and fixes the center between blocks.

For the lower bound, consider any word of length `L`, including possible unnecessary swaps on fixed leaves. Multiplying by a transposition changes the total number of permutation cycles by exactly one: it either joins two cycles or splits one cycle. Let `a` be the number of split steps. On the vertex set of the star, the identity has `m+1` cycles and the target has `m-m'+q+1` cycles. Hence the number of join steps minus split steps is `m'-q`, and

\[
 L=m'-q+2a.
\]

Every nontrivial final leaf cycle is disjoint from the center. A star transposition always contains the center, so a nontrivial cycle disjoint from the center can first be created only by a split of a cycle containing the center; one split creates at most one such detached cycle. Thus `a\ge q`, and `L\ge m'-q+2q=m'+q`. The upper and lower bounds agree. ∎

### Consequences

1. The old single-cycle family is the special case `q=1`, and its value `m'+1` is recovered.
2. `LB_hub` is not exact even on stars: it misses `q-1` additional hub excursions.
3. The miss is bounded on this family:
   \[
      \frac{\operatorname{OPT}}{LB_{\rm hub}}
      =\frac{m'+q}{m'+1}\le\frac32,
   \]
   because every nontrivial leaf cycle has length at least two, so `q\le m'/2`.
4. This family is not an unbounded counterexample to the central conjecture. It is a precise obstruction to proving the conjecture from `W(v)` and a single fixed-hub return bit alone.

The natural general-tree analogue would track the balanced directed flow between the components of `T-v` and the number of independent flow cycles. That analogue is not proved here: internal branch rearrangements and multiple tokens per component make the projection no longer a literal star-transposition factorization. Treating a branch-flow cycle count as a valid arbitrary-tree lower bound is therefore an explicit open proof obligation, not a theorem.

## 6. Comparison with known subdivided-star results

Bansal, Günlük, and Shapley prove in Theorem 5(c) that the maximum-distance lower bound has stretch `\Theta(h)` on subdivided stars, and their lower-bound instance is a star with a fixed center token, all other tokens wrong, `d_max=2`, and at least `n` rounds forced by the single center bottleneck. Their Theorem 3 gives a polynomial-time bound `4OPT+min{OPT,h}+1` on subdivided stars.

The present fixed-center star is the same high-degree bottleneck phenomenon in a more explicitly parameterized permutation language. In particular:

* the `C+D` falsification is not a new subdivided-star stretch discovery;
* the fact that `d_max` alone misses the center load is already in the 2025 primary source;
* the new contribution of this cycle is only the exact cut-flow accounting and the multi-cycle formula showing why `q(v)+1` is still not a complete hub certificate.

The exact matching-swap model and tree hardness boundary are also established in Alon–Chung–Graham (1994) and Aichholzer et al. (ESA 2022). Zhang's 1999 theorem gives a worst-case `3n/2+O(log n)` routing bound on trees; it is a bound in terms of the number of vertices, not an instance-sensitive theorem in terms of `LB_hub`.

## 7. Adversarial review of the `LB_hub` conjecture

The review separates four statements that are often conflated:

1. `LB_int\le OPT`: proved.
2. The fixed-hub `q+1` term under its stated fixed-token assumptions: proved.
3. A constant-factor *existential* upper bound `OPT\le\alpha LB_hub`: unresolved.
4. A polynomial-time algorithm achieving that bound: unresolved, and stronger.

The new star formula falsifies a stronger but tempting claim, namely that the fixed-hub term makes the lower bound exact. It does not falsify bounded stretch. No parameterized family with `OPT/LB_hub\to\infty` was established.

The static-slot proof route still fails for a precise reason. Edge slots can be colored into matchings, but they do not specify which token is at the shared endpoint when the slot is used. A valid upper-bound proof needs a token-preserving exchange-ordering lemma. Any proposed lemma must handle at least:

* a center token that is already at its destination but must make a return excursion;
* several disjoint target cycles through the same hub;
* overlapping hubs on a backbone, where one token's arrival changes the legal exchange order at the next hub;
* swaps that are individually distance-increasing but collectively necessary.

The multi-cycle star gives a minimal adversarial test for the first two items. It survives `LB_hub` with only a bounded ratio, so it neither proves nor disproves the arbitrary-tree conjecture.

## 8. Scientific status and next proof obligation

The central conjecture remains open. The most defensible next obligation is:

> Define a branch-flow dependency certificate at a vertex and prove a valid lower bound for the additional incident swaps forced by its flow-cycle structure; then determine whether the resulting certificate admits a token-preserving exchange-ordering theorem on arbitrary trees.

This is narrower than claiming a full approximation algorithm and stronger than repeating the star example. If the branch-flow certificate fails on a feasible overlapping-hub construction, that failure would be a genuine structural barrier. If it succeeds, it would provide a concrete route toward an instance-sensitive upper bound.

No experiment is authorized or needed for this proof obligation. No Paper 3 label, forecast score, or Paper 4 utility claim is changed.

## References

* N. Alon, F. R. K. Chung, and R. L. Graham, “Routing Permutations on Graphs via Matchings,” SIAM J. Discrete Math. 7 (1994), https://doi.org/10.1137/S0895480192236628.
* O. Aichholzer et al., “Hardness of Token Swapping on Trees,” ESA 2022, https://doi.org/10.4230/LIPIcs.ESA.2022.3.
* I. Bansal, O. Günlük, and R. Shapley, “Parallel Token Swapping for Qubit Routing,” arXiv:2411.18581v2 / Discrete Applied Mathematics 377 (2025), https://arxiv.org/html/2411.18581v2.
* L. Zhang, “Optimal Bounds for Matching Routing on Trees,” SIAM J. Discrete Math. 12 (1999), https://doi.org/10.1137/S0895480197323159.
