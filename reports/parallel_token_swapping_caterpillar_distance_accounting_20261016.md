# Caterpillar DAG augmentation: traversal accounting, known optimality criterion, and closure

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-CATERPILLAR-DISTANCE-ACCOUNTING-009`
**Parent checkpoint:** `24d026d`
**Scope:** one bounded proof and prior-art cycle; no experiments

## 1. Exact extra-traversal accounting

Let `T` be a tree, one distinct token occupy each vertex, and each token have a fixed destination, bijectively. Fix any legal sequential or matching-round schedule. For token `t` and edge `e`, let `N_t(e)` count traversals of `e`. Let `P_t` be the unique path from the source of `t` to its destination, and set

`χ_t(e)=1` if `e in P_t`, otherwise `χ_t(e)=0`.

Deleting `e` gives two components. Each traversal toggles which component contains `t`. The token finishes on the opposite side from its source exactly when `e in P_t`. Therefore

`N_t(e) ≡ χ_t(e) (mod 2)`.

Also `N_t(e) >= χ_t(e)`, so there is a unique nonnegative integer

`b_t(e)=(N_t(e)-χ_t(e))/2`

and

`N_t(e)=1[e in P_t]+2 b_t(e)`.

Let `s(e)` be the total number of swaps on edge `e` in the schedule and let `r(e)=C(e)/2`, where `C(e)=sum_t χ_t(e)`. Each swap on `e` moves exactly two tokens across the cut, hence `sum_t N_t(e)=2s(e)`. Bijectivity balances the cut, giving `C(e)=2r(e)`. Summing the traversal identity yields

`2s(e)=2r(e)+2 sum_t b_t(e)`, hence exactly

`sum_t b_t(e)=s(e)-r(e)`.

Summing over edges, if `L=sum_t dist(source(t),destination(t))=sum_e C(e)` and `S=sum_e s(e)` is the total sequential swap count, then

`S = L/2 + sum_e sum_t b_t(e)`.

This accounting is per token-edge pair, not an integer-valued accounting attached to individual swaps. The quantity `N_t(e)-χ_t(e)=2b_t(e)` counts **excess traversal incidences** for token `t` on edge `e`; the aggregate identity says that the total number of swaps on `e` beyond the baseline `r(e)` is half the total excess traversal incidences. A single swap can contain zero, one, or two excess traversal incidences, so assigning one whole unit of `b` to a swap with only one excess traversal would be wrong. There is generally no canonical event-by-event integer attribution: `b_t(e)` records the total number of extra traversal pairs by a token, not which particular swap should receive them. A traversal may be in the wrong direction or may repeat a direction; parity only guarantees that after one required net crossing, the remaining traversals occur in an even number.

For a hand-checkable example, take the path `x-m-y`, with tokens `X,M,Y` initially at `x,m,y` and destinations `y,m,x`, respectively. Execute swaps `(x,m)`, `(m,y)`, `(x,m)`. The initial total distance is `L=4`, and the schedule uses `S=3` swaps. On edge `xm`, tokens `X` and `Y` each have one required path traversal, while `M` has no required traversal but traverses `xm` twice. Thus `C(xm)=2`, `r(xm)=1`, `s(xm)=2`, `b_M(xm)=1`, and `sum_t b_t(xm)=1=s-r`. There are two excess traversal incidences on `xm`, one in each of the first and third swaps; each such swap also moves one token along its baseline path. They sum to two excess incidences, not two units of `b`. On `my`, both endpoint tokens make their one required traversal in the middle swap, so `C(my)=2`, `r(my)=s(my)=1`, and `sum_t b_t(my)=0`. Overall `S-L/2=1=sum_{e,t}b_t(e)`. This example makes the distinction explicit: the excess-swap count `s-r` is an aggregate edge identity, not a canonical integer charge assigned to each swap.

## 2. Fixed-pairing DAG equivalence and novelty correction

For each tree edge `e`, there are `r(e)` tokens whose original paths cross `e` in each direction. Choose a bijection pairing the two identity sets. Each pair is a proposed swap-event on `e`. Add precedence arcs between consecutive edge-events along each token's original path. For a fixed family of pairings, the resulting directed event graph is acyclic iff those events admit a monotone sequential realization: a topological order puts both paired tokens at the endpoints when each event is executed. Every event is then a legal swap; singleton rounds also satisfy matching legality.

The following existential equivalence is true:

> There is a choice of opposite-direction pairings with acyclic precedence graph iff there is a sequential routing schedule using exactly `L/2` swaps.

**Forward.** A topological realization swaps each path token exactly once across each edge on its original path and never elsewhere. Thus it has `sum_e r(e)=L/2` swaps.

**Reverse.** In any schedule of `L/2` swaps, every swap can reduce the total token-distance potential by at most two, while the total required decrease is `L`. Equality forces every swap to decrease potential by exactly two: both tokens move one step toward their destinations. On a tree these are happy swaps, and each token traverses each edge of its original path once in the correct direction and no other edge. Pair the two tokens at each swap. Their chronological order makes every precedence arc forward, so the event graph is acyclic.

The equivalence is a schedule-level reformulation of a known optimality criterion, not a new theorem. Miltzow et al. prove the `L/2` lower bound (Lemma 2 in *Approximation and Hardness for Token Swapping*, ESA 2016; [primary paper](https://drops.dagstuhl.de/opus/volltexte/2016/6408/pdf/LIPIcs-ESA-2016-66.pdf)). The exact equality characterization—minimum length is `L/2` iff there is a solution using happy swaps only—is stated as Proposition 2 by Bonnet, Miltzow, and Rzążewski in *Complexity of Token Swapping and Its Variants* ([primary full text](https://d-nb.info/1148813438/34), [journal DOI](https://doi.org/10.1007/s00453-017-0387-0)). The DAG simply records token-identity precedence constraints for a fixed pairing of happy swaps.

Akers and Krishnamurthy's 1989 tree method is the classical happy-swap/shove approach ([primary DOI](https://doi.org/10.1109/12.21148)); it does not assert that every instance admits an all-happy schedule. Biniaz et al. review this method and show why fixing happy leaves can obstruct optimality: an optimal tree solution may need to swap a correctly placed leaf token. Those results reinforce the boundary: the DAG characterizes the distance-tight/all-happy subclass, not all optimal schedules or the extra detours they may require ([Biniaz et al., *Token Swapping on Trees*](https://doi.org/10.46298/dmtcs.8383); [arXiv version](https://arxiv.org/abs/1903.06981)).

The equality concerns **total sequential swaps**, not parallel-round makespan. It neither bounds the number of rounds for a given schedule nor supplies a schedule with `O(D+W_max)` rounds.

## 3. Why this DAG-augmentation route does not yet yield a caterpillar theorem

The exact identity reveals the right accounting variable: any augmentation by extra traversals has total extra-swap count

`S-L/2 = sum_e sum_t b_t(e)`.

At vertex `v`, the total number of incident swap operations in a schedule is exactly

`load(v)=sum_{e incident to v} s(e)=W(v)+sum_{e incident to v} sum_t b_t(e)`.

Consequently every matching-round schedule obeys both `R>=D` and `R>=max_v load(v)`. For a planned event system, one must additionally bound its longest precedence chain and explicitly color the time slots so every round is a matching. Bounding only total extra swaps, or even `max_v load(v)`, is insufficient to establish a makespan bound: long precedence chains and resource-order conflicts can serialize events.

No polynomially computable augmentation was found that simultaneously (i) realizes token identities and edge occupancy, (ii) bounds the extra-traversal load at each center, (iii) controls precedence depth, and (iv) yields a legal matching schedule in `c(D+W_max)` rounds for universal `c`. No parameterized family with unbounded `OPT/(D+W_max)` was proved either.

**Exact remaining statement:** find a polynomial construction of additional, token-labeled traversals and a precedence/resource schedule with makespan `O(D+W_max)` on every caterpillar, or prove a family where every legal schedule violates every universal-constant bound. The sum-of-distance identity is necessary bookkeeping, not the missing scheduling theorem.

## 4. Stop decision and alternative research ranking

Close the fixed-pairing DAG-augmentation route for now. Its criterion is equivalent to known distance-optimality and cannot by itself describe schedules that require shoves/detours. Do not spend another cycle on small star/path examples or on unquantified feedback-set variants.

Ranked alternatives (research leads, not admitted tasks):

1. **Caterpillar matching-round block scheduling, without monotone-DAG augmentation.** The unresolved challenge is to order identity-preserving moves on the backbone while bounding both critical-path depth and center contention. This remains only a research lead: no specific exchange lemma currently survives enough scrutiny to admit as a task.
2. **Instance-relative refinement on star-path/subdivided-star trees.** Kawahara et al. give polynomial optimal *sequential* token swapping on star-path graphs, while Bansal, Günlük, and Shapley (2025) give a parallel constant-factor result on all subdivided stars, with `R<=4OPT+min{OPT,h}+1` (hence at most `6OPT` when `OPT>=1`). A star-path is a special subdivided star, so generic star-path matching-round approximation is already covered and is down-ranked. A new lead would need a genuinely stronger benchmark such as `D+W_max` and a proof that is not subsumed by their result. [Bansal et al.](https://arxiv.org/abs/2411.18581).
3. **General-tree parallel routing beyond current lower bounds.** This has broader scope but weaker structural leverage and substantial existing hardness; down-rank until a concrete tree parameter or proof invariant is identified.

No alternative is automatically enqueued. The current ranking is descriptive, not an automatic successor task; do not admit work just to prevent queue idleness. The old worker/execution and event records are not rewritten.
