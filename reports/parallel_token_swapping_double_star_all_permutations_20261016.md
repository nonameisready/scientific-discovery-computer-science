# Arbitrary permutations on a double-star: a 2-approximation to the hub-load bound

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-DOUBLE-STAR-ALL-PERMUTATIONS-005`
**Evidence class:** hand-verifiable theorem and constructive algorithm; no computational experiment was run.
**Status:** theorem proved for double-stars only. The arbitrary-tree question remains open.

## Model and theorem

Let (T) be a finite tree whose vertices consist of adjacent centers (u,v), a set (L) of leaves adjacent only to (u), and a set (R) of leaves adjacent only to (v). Either leaf set may be empty. There is one distinct token at each vertex. Each token has one prescribed destination, and the destination map is a bijection (V(T)\to V(T)). One round is a matching of edges; every selected edge swaps its endpoint tokens.

For a token (t), let (s(t)) and (d(t)) be its source and destination. Let (P_t) be the unique tree path between them and define

\[
D=\max_t |P_t|,\qquad C(e)=|\{t:e\in P_t\}|,\qquad r(e)=C(e)/2,
\]
\[
W(x)=\sum_{e\ni x}r(e),\qquad
LB_{\rm hub}=\max\{D,\max_{x\in V(T)}W(x)\}.
\]

On a tree with a bijective destination assignment, the two directional token counts across any edge cut are equal, so (C(e)) is even. Any schedule uses edge (e) at least (r(e)) times, and a matching uses at most one edge incident to (x) in a round. Also a token moves at most one edge per round. Consequently (LB_{\rm hub}\le OPT(T,d)).

Put (A=L\cup\{u\}) and (B=R\cup\{v\}). Let (r) be the number of tokens initially in (A) whose destination lies in (B). Bijection implies that the number initially in (B) destined for (A) is also (r). Let

\[
a=|\{x\in L: d(t_x)\ne x\}|,\qquad
b=|\{y\in R: d(t_y)\ne y\}|,
\]

where (t_x,t_y) are the tokens initially on those leaves. Thus (a,b) count initially incorrect leaf positions, not all incorrect vertices. The leaf edge demands are one exactly for these incorrect leaves and zero otherwise; the central edge has demand (r). Hence

\[
W(u)=r+a,\qquad W(v)=r+b.
\]

**Theorem.** Every such double-star instance has a polynomial-time parallel token-swapping schedule with

\[
R\le 2r+2\max(a,b)=2\max\{W(u),W(v)\}\le 2LB_{\rm hub}\le 2OPT.
\]

This is a constructive 2-approximation relative to (OPT) on the double-star class. It is not an approximation theorem for arbitrary trees.

## Algorithm (executable pseudocode)

Represent each token by its destination. A token is `outA` if its destination lies in (B), and `outB` if its destination lies in (A). `swap(x,y)` exchanges the token identities at positions (x,y).

```text
DOUBLE-STAR-SCHEDULE(u, v, L, R, tokenAt, destination):
    A := L union {u}; B := R union {v}
    r := number of tokens in A whose destination is in B
    a := number of x in L with destination(tokenAt[x]) != x
    b := number of y in R with destination(tokenAt[y]) != y

    # Maintain lists of leaves currently holding outA or outB tokens.
    LA := [x in L whose current token destination is in B]
    RB := [y in R whose current token destination is in A]

    # Phase I: correct the side of every token.
    repeat r times:
        P := empty set of edges
        if destination(tokenAt[u]) is not in B:
            x := pop(LA)              # such a leaf exists by the invariant
            add edge (u,x) to P
        if destination(tokenAt[v]) is not in A:
            y := pop(RB)
            add edge (v,y) to P
        output matching P             # its edges are vertex-disjoint
        swap simultaneously on P
        output matching {(u,v)}
        swap(u,v)
        # Update the lists only as needed; a prepared leaf is never outgoing again.

    # Phase II: each side is now an independent star permutation.
    # For each side separately, map each current position z to the destination
    # of its current token and decompose that position map into disjoint cycles.
    # Process cycles sequentially within a star, skipping singleton cycles.
    # Run the left and right star cycle lists in lockstep; their vertex sets
    # are disjoint, so corresponding swaps may occur in the same round.
    for each nontrivial cycle C in the position-to-destination map on {u} union L:
        if C = (u, z1, ..., zq):
            perform swaps (u,z1), ..., (u,zq), one per round
        else:  # C = (z1, ..., zq) contains leaves only; q >= 2
            perform swaps (u,z1), ..., (u,zq), (u,z1), one per round
    do the analogous cycle procedure on {v} union R, in parallel with the left.
```

For implementation, build each outgoing-leaf list once and pop each selected leaf once; after Phase I, recompute the two local position maps and decompose them in linear time. If the lists are maintained explicitly, an outgoing leaf removed from a list is not reinserted. Total preprocessing and schedule-generation time is (O(|V|+R)=O(|V|)); output size is (O(|V|)) rounds and at most (O(|V|)) swaps. The pseudocode describes every round, including empty padding on the shorter side in Phase II.

## Proof

### Phase I invariant and matching legality

Immediately before the (j)-th bridge swap, for (0\le j<r), exactly (r-j) tokens currently in (A) have destinations in (B), and exactly (r-j) tokens currently in (B) have destinations in (A). The equality follows initially from bijectivity and is preserved because the bridge swap will exchange one token of each type. No Phase-I operation other than the bridge edge changes sides.

If (u) does not currently hold an `outA` token, an `outA` token must be on a leaf in (L): there is still at least one such token in (A), and (u) is the only non-leaf position of (A). So the left preparation is possible. The same argument applies at (v). At most one preparation edge is selected at each center; when both are needed, ((u,x)) and ((v,y)) are disjoint. Thus the preparation set is a matching. It is output in its own round, followed by the distinct central edge ((u,v)) in the next round, also a matching.

After preparation, (u) holds a token destined to (B), and (v) a token destined to (A). Swapping ((u,v)) sends both across the cut to their correct sides. The two directional counts each fall by exactly one, proving the invariant inductively until all (r) transfers are complete. In particular, no outgoing token is stranded: when a center lacks one, the positive remaining side count guarantees one on an incident leaf.

At most one preparation round and one bridge round are used per transfer pair, so Phase I takes at most (2r) rounds.

### Initially correct leaves are protected; the error count does not increase

Only preparation swaps touch leaves in Phase I. A leaf selected for preparation is holding an outgoing token, so its resident token is not destined to that leaf; it was therefore initially incorrect if it has not been touched earlier. After the swap it receives the old center token. The preparation rule was used only when that center token was not outgoing, so the selected leaf can never again be an outgoing-leaf source; bridge swaps do not touch leaves. Thus every selected leaf is selected at most once. An initially correct leaf holds its own token, which is not outgoing, and is never selected. No initially correct leaf position changes during Phase I.

For the count after Phase I, a selected leaf was initially incorrect, and its new token may either remain incorrect or happen to be its exact target. All unselected leaves retain their token. Therefore the number (q_A) of incorrect left leaves after Phase I is at most (a); likewise (q_B\le b). This argument allows the center token to change from iteration to iteration and does not identify a branch with a single token.

### Sorting each star, including center and leaf-only cycles

Once Phase I ends, every token lies on the same side (A) or (B) as its destination. The remaining position-to-destination map on each side is a permutation of that side's star vertices.

For a cycle containing the star center, write it in its directed position-map order as ((c,z_1,\dots,z_q)), meaning the token at (c) targets (z_1), the token at (z_i) targets (z_{i+1}), and the token at (z_q) targets (c). Swapping successively ((c,z_1),\dots,(c,z_q)) places each token at its target and leaves the original center token at (z_q), its target. This uses (q) swaps.

For a leaf-only cycle ((z_1,\dots,z_q)), (q\ge2), perform ((c,z_1),\dots,(c,z_q),(c,z_1)). After the first (q) swaps, the original center token is at (z_q), each original leaf token from (z_i) for (i<q) is at (z_{i+1}), and the token originally at (z_q) is at the center. The last swap returns the center token to (c) and places the (z_q)-token at (z_1), completing the cycle. This takes (q+1\le2q) swaps. Singleton cycles, including fixed leaves and a fixed center, are skipped.

Cycles are disjoint in their positions; processing them sequentially within one star is always legal. Every swap in that star uses its center, so no two such swaps are incorrectly claimed to be simultaneous. The left and right star vertex sets are disjoint, hence their current swaps can be paired round-by-round as matchings. The left takes at most (2q_A\le2a) rounds and the right at most (2q_B\le2b), so Phase II takes at most (2\max(a,b)) rounds.

Adding phases and using the definitions gives

\[
R\le2r+2\max(a,b)=2\max(r+a,r+b)
=2\max(W(u),W(v))\le2LB_{\rm hub}\le2OPT.
\]

All operations swap actual token identities; no branch aggregation is used. Each emitted round is a matching. The algorithm terminates at the target permutation.

## Independent adversarial review

The proof was checked against the following edge cases and possible failure modes:

* **Center token already outgoing / center token locally destined:** preparation is skipped in the first case; in the second, an outgoing leaf is forced whenever transfers remain. The center token placed into that leaf during preparation is not outgoing, preventing repeated use of the same leaf.
* **A center's own destination is a leaf or the other center:** side correction only ensures the correct half-tree. Phase II then sorts the exact local permutation, so it does not assume a center token is already home.
* **Initially fixed leaves:** they hold non-outgoing tokens and are untouched in Phase I; fixed points are singleton cycles and skipped in Phase II.
* **Within-side leaf cycles and cycles containing a center:** both have explicit star-transposition words; the leaf-only word restores the center token.
* **Both centers need preparation:** preparation edges are disjoint. The central swap is in a separate round, never concurrent with a preparation edge.
* **Parallel legality in Phase II:** left-star and right-star supports are disjoint; swaps within one star are serialized because they share its center.
* **Degenerate side with no leaves:** the preparation and star-cycle arguments still apply; a side with no leaf has no leaf-only cycle.
* **Potential counterexample search by proof audit:** the tempting failure would be reusing a leaf whose center replacement is still cross-bound. The guard explicitly forbids preparing when the center already has an outgoing token; after a bridge swap the received center token is directed into that center's current side. Thus the suspected re-use is impossible.

No finite search was run. No claim about a non-double-star tree follows from this invariant.

## Extension boundary: why this proof does not immediately cover three hubs

The decomposition used above has exactly one backbone edge. It separates the tree into two regions, and after all tokens cross that cut in their required direction, the residual graph is the disjoint union of exactly two stars. Preparations on opposite sides use disjoint center-leaf edges, while the single backbone exchange is serialized between them.

With three or more adjacent high-degree centers, a middle hub is incident to two backbone cuts. A token destined beyond that hub may have to cross both cuts; preparing it for one cut can occupy the shared center needed for the other, and crossing one cut can change which token is available for the next. Even though the vertex-load lower bound accounts for mandatory traffic at the middle hub, the two-star proof has no longer a single global side-correction phase followed by independent star permutations: cut-correctness states overlap, and the residual backbone remains nontrivial. This identifies the decomposition property that fails in the proof, not a counterexample to a constant-factor extension.

## Prior art and novelty boundary

* Alon, Chung, and Graham introduced matching-round permutation routing and studied worst-case routing number, including trees. This is the same matching-round model, but worst-case routing-number bounds do not imply this instance-sensitive double-star guarantee. [SIAM J. Discrete Math. 7(3), 1994](https://doi.org/10.1137/S0895480192236628).
* Aichholzer et al. established NP-hardness of parallel token swapping even on trees. That warns against inferring optimality from a simple schedule; it does not preclude a polynomial approximation on this restricted subclass. [ESA 2022](https://arxiv.org/abs/2103.06707).
* Bansal, Günlük, and Shapley give a polynomial approximation for subdivided stars, defined by branches joined at one common vertex, and analyze the maximum-distance lower-bound stretch. Genuine double-stars with both adjacent centers branching are outside that one-junction class; degenerate double-stars can overlap it. Their result is adjacent topology-specific prior art, not the same theorem. [arXiv:2411.18581](https://arxiv.org/abs/2411.18581).
* Sadanandan and Chitturi give an optimal **sequential-swap** algorithm for double brooms (two stars linked by a path). Sequential swap count is a different objective from matching rounds; it neither proves nor refutes the present bound. [Algorithms 15(7), 2022](https://doi.org/10.3390/a15070220).
* Irving and Rattan study minimal factorizations into star transpositions. The local cycle words here are elementary instances of that classical star-transposition structure, not themselves a novelty claim. [Discrete Math. 309(6), 2009](https://arxiv.org/abs/math/0610640).

The bounded source audit found no direct statement of this instance-wise (2LB_{\rm hub}) parallel guarantee for arbitrary permutations on a double-star. That is not an exhaustive novelty or priority proof. The theorem is mathematically valid and useful as a restricted constructive guarantee; publication-level originality remains unverified, and the local star decomposition is standard. It does not solve the arbitrary-tree approximation question.

## Claim classification

| Claim | Classification |
|---|---|
| The stated two-phase schedule reaches every target permutation on a double-star | **Fully proved** |
| Every round is a matching and token identities are preserved | **Fully proved** |
| (R\le2LB_{\rm hub}\le2OPT), with polynomial construction | **Fully proved for double-stars** |
| A three-or-more-hub extension or arbitrary-tree constant approximation | **Open / not established** |
| The result is novel relative to all prior work | **Unverified; no priority claim** |
| A counterexample to the proposed double-star construction | **None found; no computation used** |

Paper 3 Target A and Target B are untouched; no historical outcome labels or forecast scores were added. Paper 4, frozen cohorts, experiment counters, and prior negative findings are unchanged.
