# Parallel token swapping on a three-center caterpillar

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-THREE-CENTER-CATERPILLAR-006`
**Parent checkpoint:** `8892219`
**Evidence class:** mathematical proof with bounded primary-source audit; no computation
**Status:** proved for the stated three-center class; no arbitrary-tree claim

## Result

Let (T) consist of a backbone (u-v-w), with any number (including zero) of pendant leaves attached to each of (u,v,w), and no other vertices. Let every vertex contain one distinct token and let the destination assignment be any permutation of (V(T)). Define

\[
C(e)=\#\{\text{token source--destination paths using }e\},\qquad
r(e)=C(e)/2,
\]
\[
W(x)=\sum_{e\ni x}r(e),\qquad
LB_{\rm hub}(T,\pi)=\max\{D,\max_x W(x)\},
\]
where (D) is the maximum token distance. The parity of (C(e)) follows from the bijection: across every cut, the number of tokens leaving equals the number entering.

There is a deterministic (O(n))-time algorithm that outputs a legal matching-round schedule using

\[
R\le 42\,LB_{\rm hub}(T,\pi)\le42\,OPT(T,\pi).
\]

The constant is deliberately loose. This proves a polynomial-time constant-factor approximation on this three-center caterpillar class, which strictly contains the two-center double-stars. It does **not** establish the same bound for arbitrary trees or for caterpillars with an unbounded backbone.

## Constructive algorithm

Treat the current configuration as a permutation of positions: σ(x) is the destination of the token currently at vertex (x). Decompose σ into disjoint directed cycles. For each cycle ((z_1,z_2,\ldots,z_q)), where the token at (z_i) is destined to (z_{i+1}) and the token at (z_q) is destined to (z_1), perform the following logical endpoint transpositions in order:

```text
for each nontrivial cycle (z1,z2,...,zq):
    for i = 2,...,q:
        path = the unique vertex path z1,...,zi
        swap on path edges forward, then backward without the last edge:
            (z1z2), (z2z3), ..., (z_{i-1}zi),
            (z_{i-2}z_{i-1}), ..., (z1z2)
        emit each edge swap as its own round
```

For a path of length ℓ, this word has (2\ell-1) swaps. It exchanges the endpoint tokens and restores every internal vertex to its previous token. Thus each word implements exactly the logical transposition ((z_1,z_i)), even if the path passes through other cycle positions or previously processed vertices. The ordered transpositions ((z_1,z_2),(z_1,z_3),\ldots,(z_1,z_q)) realize the directed cycle exactly. Cycles have disjoint supports; path-interior tokens are restored after each logical transposition, so one cycle's execution does not corrupt another.

The graph has diameter at most four, so ℓ≤4 and every logical transposition takes at most seven edge swaps. There are ∑(q−1)≤m logical transpositions, where (m) is the number of nonfixed positions of σ. The emitted sequence therefore has at most (7m) swaps. Serializing one edge swap per round is always legal: every round is a singleton matching. Token identities are never merged or abstracted.

This handles center destinations, leaf-only cycles, mixed cycles, and cycles meeting several backbone cuts uniformly. The middle vertex participates in at most one swap per round, indeed every vertex does, because only one swap is emitted in each round.

## Approximation bound

Let (a,b,c) be the numbers of initially incorrect pendant-leaf positions attached to (u,v,w), respectively. Let (r_1=r(uv)) and (r_2=r(vw)). A pendant edge has (r(e)=1) exactly when its leaf is incorrect, and zero otherwise. Hence

\[
W(u)=r_1+a,\qquad W(v)=r_1+r_2+b,\qquad W(w)=r_2+c.
\]

Each (W(x)\le LB_{\rm hub}), so

\[
a+b+c\le W(u)+W(v)+W(w)
=2r_1+2r_2+a+b+c\le3LB_{\rm hub}.
\]

The only non-leaf positions are (u,v,w). Thus at most three further positions can be nonfixed, and

\[
m\le a+b+c+3\le3LB_{\rm hub}+3.
\]

If the permutation is nonidentity, (D\ge1) and therefore (LB_{\rm hub}\ge1). Consequently

\[
R\le7m\le21LB_{\rm hub}+21\le42LB_{\rm hub}.
\]

For the identity permutation (R=LB_{\rm hub}=0). Finally, (LB_{\rm hub}\le OPT): a token needs at least its path length (D) rounds, and each edge (e) must be swapped at least (r(e)) times; since (x) participates in at most one swap per round, at least ∑_{e incident x}r(e)=W(x) rounds are necessary.

The cycle decomposition is (O(n)). For this fixed three-center topology, store each vertex's center/leaf owner; the path between any two vertices is then emitted by a constant-size case distinction over their owners and whether an endpoint is a center. Thus each path word is generated in O(1), and the total construction is O(n). The output also has O(n) rounds because (m\le n) and every word has at most seven swaps.

## Exact failure of the direct two-cut preparation rule

The double-star proof's local preparation rule assumes that if a cut-center lacks an outgoing token, an outgoing token is available at an incident pendant leaf. This is false at the first cut of a three-center tree.

Take the path (u-v-w) and add leaves (x) at (u), (y) at (w); attach no leaf to (v). Initially swap the tokens at (x,y), while tokens at (u,v,w) are already destined for their own vertices. For cut (uv), the token at (y) must cross from the (v,w,y) side to the (u,x) side, but the token at center (v) is destined to (v), and (v) has no pendant leaf. The double-star preparation move at (v) is unavailable. This falsifies that *local preparation invariant*; it does not falsify a more general cut schedule or any constant-factor algorithm. The constructive theorem above bypasses the cut-correction normal form.

## Extension boundary

The endpoint-transposition word is valid on every tree. For a tree of diameter Δ it takes at most (2\Delta-1) swaps per logical transposition. This gives an existential constructive cost (O(\Delta m)), but it is not a constant-factor bound against (LB_{\rm hub}) when Δ or the number of nonfixed internal vertices grows. In particular, it does not prove an arbitrary-length caterpillar theorem. The three-center proof uses both the constant diameter (Δ≤4) and the fact that only three non-leaf positions can contribute the additive (+3). A longer-backbone result needs a sharper ordering/routing argument that charges internal backbone movement to edge loads without multiplying by diameter.

## Targeted prior-art and novelty audit

The matching-round model is classical under the name **routing permutations via matchings**. Alon, Chung, and Graham formulate precisely the same operation—swap pebbles on a selected matching—and study the worst-case routing number on graph classes including trees ([1994 paper](https://doi.org/10.1137/S0895480192236628); [author-hosted full text](https://fanchung.ucsd.edu/ron/papers/94_04_routing.pdf)). Their worst-case routing-number results are not the instance-sensitive (R\le42LB_{\rm hub}) statement proved here.

For the earlier double-star theorem, this audit checked that same classical routing-number line, equivalent “permutation routing via matching” terminology, parallel-token-swapping definitions, subdivided-star approximation, and double-broom sorting. No directly equivalent all-permutation double-star guarantee in matching rounds was identified in the checked primary sources. The instance-sensitive `2 LB_hub` guarantee is distinct from worst-case `rt(T)`, but this targeted search is not a proof of priority or global absence.

Ramras's graph-routing formulation and the parallel-network framework of Baumslag--Annexstein are equivalent terminology/background, not an identified three-center theorem ([Ramras 1993](https://doi.org/10.1002/net.3230230420); [Baumslag--Annexstein 1991](https://doi.org/10.1007/BF01200063)). Kawahara et al. explicitly define a parallel swap as a matching and study routing complexity; their positive path approximation and hardness results do not state this restricted diameter-four instance bound ([JGAA 2019](https://jgaa.info/index.php/jgaa/article/view/paper483)). Aichholzer et al. prove the parallel problem NP-hard on general trees, which is consistent with a fixed three-center subclass theorem ([2022 paper](https://arxiv.org/abs/2103.06707)).

Bansal, Günlük, and Shapley give constant-factor algorithms for parallel token swapping on cycles, **subdivided stars**, and grids ([2025 revised preprint](https://arxiv.org/abs/2411.18581)). A subdivided star has one branch junction; it is not the general three-center caterpillar here, though the classes overlap on degenerate inputs. Sadanandan--Chitturi's double-broom result minimizes **sequential swaps**, not matching rounds, so it cannot be treated as an equivalent parallel theorem ([2022](https://doi.org/10.3390/a15070220)).

This was a targeted source check, not an exhaustive priority search. No directly matching theorem was found in the checked sources. **No firstness or publication-level novelty claim is made.** The algorithmic proof is established; its originality remains unverified, and its coarse cycle/path-transposition ingredients are elementary.

## Structured claim classification and adversarial review

| Claim | Status |
|---|---|
| (R\le42LB_{\rm hub}\le42OPT) for all permutations on the stated three-center class | **Fully proved** |
| O(n)-time deterministic algorithm; each emitted round is a matching | **Fully proved** |
| Direct double-star-style local preparation at cut (uv) works for all inputs | **Disproved** by the stated five-vertex configuration |
| Failure of that preparation rule implies no constant approximation exists | **False inference; not claimed** |
| Same bound for arbitrary trees / unbounded-backbone caterpillars | **Open; not established** |
| The theorem is novel or first | **Unverified; no priority claim** |

Adversarial checks: the cycle word orientation was checked token-by-token; the path word has the correct (2\ell-1) parity and restores all internal positions; routes may intersect prior cycles without affecting them because each endpoint-swap macro restores its interior; no matching claim is made for multiple swaps in one round (single swaps are emitted); (LB=0) is handled separately; all no-leaf and fixed-position cases are covered by empty cycle/leaf sets.

No experiment, computation, supervisor start, budget renewal, Paper 3 edit, or Paper 4 edit occurred. Existing uncommitted supervisor/checkpoint and Paper 3 files were left untouched.
