# Bounded internal vertices and the unbounded-caterpillar bottleneck

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-BOUNDED-H-CATERPILLAR-007`
**Parent checkpoint:** `a8da720`
**Method:** mathematical proof and primary-source audit only; no experiment

## 1. General parameterized theorem

Let (T) be a finite tree with (h\ge1) non-leaf vertices, one distinct token at every vertex, and a bijection from tokens to destination vertices. For each edge (e), let (C(e)) be the number of token-to-destination paths using (e), and (r(e)=C(e)/2). Since the destination map is a permutation, every cut has equally many tokens leaving and entering, so (C(e)) is even. Define

\[
W(x)=\sum_{e\ni x}r(e),\qquad LB_{\rm hub}=\max\{D,\max_x W(x)\},
\]

with (D) the maximum token distance.

### Diameter

For a tree with at least two vertices, the endpoints of any diameter are leaves. If its length is (d), the (d-1) internal vertices on this path are all non-leaves; hence (d-1\le h), or

\[
\operatorname{diam}(T)\le h+1.
\]

### Incorrect leaves and positions

For a leaf (z), its incident edge is crossed by exactly two token paths if (z) is incorrect (one token leaves and, by bijectivity, one enters), and by zero paths otherwise. Thus (r(e_z)=1) exactly for an incorrect leaf. Summing (W(x)) over non-leaf vertices counts every incorrect leaf once and every internal edge twice, so

\[
\#\{\text{incorrect leaves}\}\le \sum_{x\text{ non-leaf}}W(x)\le hLB_{\rm hub}.
\]

There are only (h) non-leaf positions, therefore if (m) is the number of incorrect positions,

\[
m\le hLB_{\rm hub}+h.
\]

### Constructive path-transposition schedule

Decompose the position-to-destination permutation into directed cycles. A cycle of length (q) is realized by (q-1) endpoint transpositions. To transpose the tokens at endpoints of a tree path of length ℓ, swap along its edges forward and then backward omitting the final edge. This word has (2\ell-1) swaps, exchanges exactly the endpoint tokens, and restores every internal vertex. Emit each edge swap as a separate round; each is a singleton matching, so token identity and matching legality are automatic.

Every logical transposition uses at most (2(h+1)-1=2h+1) swaps. This gives a deterministic polynomial-time schedule (at most (O(nh)) operations). For a nonidentity permutation, the number of logical transpositions is (m-c\le m-1), where (c\ge1) is the number of nontrivial cycles. Also (LB_{\rm hub}\ge1). Thus

\[
R\le(m-1)(2h+1)
 \le (hLB_{\rm hub}+h-1)(2h+1)
 \le (2h-1)(2h+1)LB_{\rm hub}
 = (4h^2-1)LB_{\rm hub}.
\]

The last inequality uses ((h-1)(LB_{\rm hub}-1)\ge0). A slightly looser route uses (m\le h(LB_{\rm hub}+1)\le2hLB_{\rm hub}), giving the requested

\[
R\le2h(2h+1)LB_{\rm hub}.
\]

Since (LB_{\rm hub}\le OPT), both are approximation bounds with the same factors relative to (OPT). For (h=3), the coarse factor is (2\cdot3\cdot7=42), recovering the prior three-center bound; the sharper factor is ((5)(7)=35).

### Degenerate cases

If (h=0), a connected tree has either one vertex or one edge. The one-vertex instance is necessarily the identity and uses zero rounds. On the one-edge tree, identity uses zero rounds; the transposition uses one round and has (D=LB_{\rm hub}=1). For (h\ge1), identity also has (m=D=LB_{\rm hub}=R=0); the nonidentity proof above applies. This avoids dividing by a zero lower bound.

This is an elementary parameterized consequence of path transpositions, not a novel arbitrary-tree approximation: the factor grows quadratically with (h).

## 2. Arbitrarily long caterpillar: one exchange lemma fails; the main question remains open

Let the caterpillar backbone be (v_1,v_2,\ldots,v_t), with arbitrary pendant leaves at its vertices. At an internal spine vertex (v_i), its mandatory hub workload is

\[
W(v_i)=r(v_{i-1}v_i)+r(v_iv_{i+1})+a_i,
\]

where (a_i) is the number of initially incorrect pendant leaves at (v_i); at the endpoints omit the missing spine edge. This exactly lower-bounds rounds spent at that vertex, because each incident edge needs at least (r(e)) swaps and one vertex cannot participate in two swaps in a round. Across each spine cut the two directional token counts agree. These facts account for interval traffic and matching capacity, but do not by themselves order exchanges of specific token identities.

### Falsified local frontier lemma

Consider this candidate lemma for a left-to-right monotone cut sweep:

> Once the prefix left of cut (v_iv_{i+1}) is settled, if an incoming token remains on the right side, it can be prepared for the cut exchange using at most one swap between (v_{i+1}) and one of its pendant leaves.

This is false on a parameterized caterpillar. Take the bare spine (v_1\cdots v_t), add one leaf (x) at (v_1) and one leaf (y) at (v_t), and no leaves at (v_2,\ldots,v_{t-1}). Exchange the tokens at (x,y), leaving every spine token fixed. For cut (v_1v_2), the token destined for (x) is at (y), at distance (t-1) from (v_2); (v_2) has no pendant leaf, so the proposed local preparation swap does not exist. The full endpoint distance is (t+1), already reflected in (D), and this instance is routable in (2(t+1)-1) sequential swaps by the endpoint-transposition word. Therefore this only falsifies one-hop frontier access; it is **not** an unbounded (OPT/LB_{\rm hub}) obstruction and does not disprove all cut-sweep algorithms. A repair must permit remote transport and charge its scheduling against the actual interval demands.

### Adversarial checks of the candidate invariant

| Configuration pattern | What the invariant sees | Review result |
|---|---|---|
| Opposing flows across a spine cut | Equal directional demand (r(e)); both directions consume the boundary vertices' matching capacity. | Feasibility/counting is sound, but the count does not specify which identity must be brought to the boundary. |
| Two adjacent busy hubs | Their shared edge contributes (r(e)) to each endpoint workload; each center can execute at most one incident swap per round. | (W(v_i)) is a valid local lower bound. It gives no exchange order for simultaneous interval demands. |
| Correct/fixed spine tokens | They can lie internally on a path-transposition word and be displaced temporarily. | The endpoint word restores every internal token exactly, but a “never touch a correct center” monotonicity rule is invalid for this generic construction. |
| Cyclic dependencies | On (v_1-v_2-v_3), tokens (A,B,C) with destinations (v_2,v_3,v_1) give (r=1) on both edges, (D=2), (W(v_2)=2); swaps (v_2v_3), then (v_1v_2), finish in two rounds. | This small cycle is resolved; it is not evidence of a lower bound. More generally, cut counts alone do not encode the order of token identities in permutation cycles. |
| Remote endpoint exchange | A token can require crossing many successive cuts while all intermediate spine tokens are initially fixed. | Refutes the local one-swap access lemma only; (D) pays for the long displacement. |

No polynomial algorithm with (R\le cLB_{\rm hub}) for arbitrary-length caterpillars has been proved here, and no family with unbounded (OPT/LB_{\rm hub}) has been constructed. The precise remaining obligation is a **token-preserving frontier exchange lemma** that schedules remote incoming identities through successive cuts with total delay (O(\max\{D,\max_i W(v_i)\})), while each round is a matching; alternatively, a schedule-independent family disproving that bound is needed. The failed one-hop lemma narrows the failed normal form but leaves the global conjecture open.

## 3. Prior-art and novelty boundary

* **Classical matching routing.** Alon, Chung, and Graham define the same matching-round pebble exchange model and prove a worst-case (rt(T)<3n) upper bound for every (n)-vertex tree ([1994 primary paper](https://doi.org/10.1137/S0895480192236628); [author-hosted text](https://mathweb.ucsd.edu/~ronspubs/94_04_routing.pdf)). This is a bound in (n), not the instance-wise (LB_{\rm hub}) guarantee.
* **Sharper general-tree routing number.** Zhang's matching-routing result uses a “caterpillar tree partition” and proves worst-case routing number at most (\frac32n+O(\log n)) on every tree ([1999 primary paper](https://doi.org/10.1137/S0895480197323159)). The partition terminology should not be confused with an instance-sensitive result for graph-theoretic caterpillars.
* **Equivalent terminology and hardness.** Ramras's routing-permutations formulation and later “permutation routing via matching” work study the same operation. Kawahara et al. distinguish the matching-round version from sequential token swapping and give an additive-one path approximation; Aichholzer et al. prove parallel token swapping NP-hard on trees ([JGAA 2019](https://jgaa.info/index.php/jgaa/article/view/paper483); [ESA 2022](https://arxiv.org/abs/2103.06707)).
* **Nearby approximation classes.** Bansal, Günlük, and Shapley prove constant-factor results for cycles, one-junction subdivided stars, and grids; their subdivided-star bound is (4OPT+\min\{OPT,\Delta\}+1), and maximum-distance stretch is degree-dependent ([2025 revised primary preprint](https://arxiv.org/abs/2411.18581)). A general caterpillar can have many branching spine vertices and is not their one-junction class.
* **Sequential objective is distinct.** Sadanandan--Chitturi optimize the number of sequential swaps on double brooms, not matching rounds ([2022](https://doi.org/10.3390/a15070220)).

The (h)-parameterized theorem is an elementary consequence of cycle factorization and path transpositions; it does not improve the known worst-case routing-number bounds in a way that supports a novelty claim. The literature audit found no directly equivalent universal-(c), instance-wise (LB_{\rm hub}) theorem for arbitrary caterpillars, but this bounded search establishes neither novelty nor nonexistence.

## 4. Claim status and next decision

| Claim | Classification |
|---|---|
| Diameter ≤ (h+1); incorrect leaves ≤ (hLB_{\rm hub}); incorrect positions ≤ (hLB_{\rm hub}+h) | **Fully proved** |
| General (R\le2h(2h+1)LB_{\rm hub}) and sharper (R\le(4h^2-1)LB_{\rm hub}) | **Fully proved; deterministic polynomial construction** |
| (h=3) factors 42 and 35 | **Fully proved** |
| One-swap local frontier-access lemma | **Disproved by parameterized caterpillar family** |
| Universal constant-factor (LB_{\rm hub}) approximation on arbitrary caterpillars | **Open; neither established nor refuted** |
| General-tree constant-factor approximation follows from the (h)-bound | **False; factor depends on (h)** |
| Novelty/priority of the elementary (h)-bound | **No claim** |

**Bounded-cycle decision:** retain arbitrary caterpillars as a genuinely unresolved theory opportunity, but do not expand fixed-center examples or run computation. The next useful proof attempt must formulate a nonlocal frontier-exchange invariant that charges each token's travel to (D) and each center's operations to (W), or else produce a schedule-independent asymptotic obstruction.

Paper 3 and Paper 4 remain unchanged. No experiment, computation, supervisor start, or budget renewal occurred.
