# Branch-flow dependencies on overlapping hubs

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-BRANCH-FLOW-DEPENDENCY-003`
**Checkpoint:** 2026-10-16
**Scope:** one bounded mathematical proof cycle; no experiment, budget renewal, or Paper 3/4 change.

## 1. Novelty boundary for the fixed-center star formula

The previously recorded formula

\[
  \operatorname{OPT}(K_{1,m},\pi)=m'+q
\]

for a fixed center, `m'` moved leaves, and `q` nontrivial leaf cycles is correct, but it is not a new star-transposition theorem.  On the active support, regard the center as the pivot `1`.  The target permutation has one fixed pivot cycle and `q` nontrivial cycles of lengths `\ell_1,\ldots,\ell_q`, with `\sum_i\ell_i=m'`.  Irving and Rattan's primary theorem states that a permutation with cycle lengths `\ell_1,\ldots,\ell_m` has minimal transitive star-factorization length `n+m-2`; their fixed-point corollary removes irrelevant fixed points.  Substituting `n=m'+1` and `m=q+1` gives

\[
 (m'+1)+(q+1)-2=m'+q.
\]

Their Lemma 2.1 also explains the return transposition for every cycle not containing the pivot.  Pak's 1999 paper is the earlier restricted result for a fixed pivot; Irving--Rattan generalize it to arbitrary target permutations and resolve Pak's stated extension question.  Thus the star proof is preserved as an independent check and a useful prior-art calibration, but its mathematical content is **known prior art**, not a novel theorem.

Primary sources:

* Irving and Rattan, *Minimal Factorizations of Permutations into Star Transpositions*, Discrete Mathematics 309 (2009), arXiv: [math/0610640](https://arxiv.org/abs/math/0610640), Theorem 1.1 and Corollary 1.2.
* Pak, *Reduced decompositions of permutations in terms of star transpositions, generalized Catalan numbers and k-ary trees*, Discrete Mathematics 204 (1999), author source page: [Pak research record](https://www.math.ucla.edu/~pak/papers/research.htm#1999).

This correction does not alter the earlier exact proof or the negative `LB_hub` conclusions.

## 2. Token-level branch-flow object

Let `T=(V,E)` be a finite tree, let the token initially at `x` be named `x`, and let `d:V\to V` be a bijective destination map.  A parallel schedule is a sequence of matchings `M_1,\ldots,M_R`; every edge in `M_t` swaps its endpoint tokens.

For a vertex `v`, let `\mathcal B_v` be the set of components of `T-v`, and adjoin a symbol `0` for `v` itself.  For token `x`, define

\[
 a_v(x)=
 \begin{cases}0&x=v,\\B&x\in B\in\mathcal B_v,\end{cases}\qquad
 b_v(x)=
 \begin{cases}0&d(x)=v,\\B&d(x)\in B\in\mathcal B_v.\end{cases}
\]

The **labelled branch-flow multigraph** `F_v` has one directed arc
`a_v(x)\to b_v(x)` labelled by `x` for every token with `a_v(x)\ne b_v(x)`.  The label is part of the object; two tokens in the same branch are not collapsed.  Because `d` is a bijection, every branch has equal in- and out-degree in `F_v` (and the same balance holds for the `0` symbol).  This is the exact static information about which token must leave one branch and which destination branch it must reach.

For a concrete schedule `\sigma`, an **incident event** is a tuple `(t,e,x,y)` saying that edge `e=vw` is in `M_t` and tokens `x,y` occupy `v,w` immediately before the swap.  The schedule-specific dependency graph `P(\sigma)` has these events as nodes and includes:

1. a precedence edge between consecutive events of the same token;
2. a precedence edge between consecutive events using the same vertex; and
3. an occupancy edge from the event that puts token `x` at a vertex to the event that next removes `x` from that vertex.

The first two relations are visible in a schedule, but the third depends on the actual order and on the token occupying the hub.  A static `F_v` does not determine `P(\sigma)`.  A schedule-independent dependency lower bound therefore has to prove that every possible realization of `F_v` contains a precedence chain, rather than simply counting directed flow cycles.

For a token `x`, a **hub excursion at `v`** is a maximal interval beginning with an incident event that moves `x` from `v` into a component of `T-v` and ending at the next event that returns `x` to `v`; an open interval is allowed at the beginning or end when the source or destination is in a branch.  The number of swaps on edge `e` can be written as the mandatory directional demand `r(e)` plus nonnegative detour slack, but the excursion decomposition is token-labelled and schedule-dependent.  This is the required separation between balanced traffic, hub returns, temporary detours, and actual scheduling cost.

## 3. A rigorous overlapping-hub obstruction

For every integer `h\ge 2`, form `H_h` from the path

\[
 a-u-v-b
\]

by attaching `h-2` additional leaves fixed at `u` and `h-2` additional leaves fixed at `v`.  Thus both `u` and `v` have degree `h`; the added branches carry no active flow and are retained only to make the two adjacent hubs arbitrarily high-degree.  Let the active tokens be `A,U,V,B` initially at `a,u,v,b`, and set

\[
 d(A)=b,\quad d(B)=a,\quad d(U)=v,\quad d(V)=u,
\]

with every added leaf token fixed.

The active cut demands are

\[
 r(au)=1,\qquad r(uv)=2,\qquad r(vb)=1.
\]

Consequently

\[
 D=3,\qquad W(u)=1+2=3,\qquad W(v)=2+1=3,
\]

and no fixed-hub return term applies because the tokens at `u` and `v` are destined for each other.  Therefore the previously established lower bound is

\[
 LB_{\rm hub}(H_h,d)=3.
\]

### Exact four-round schedule

Writing only the active path in the order `(a,u,v,b)`, the matching schedule is

\[
\begin{array}{c|c|c}
\text{round}&\text{matching}&(a,u,v,b)\\ \hline
0&-&(A,U,V,B)\\
1&\{au,vb\}&(U,A,B,V)\\
2&\{uv\}&(U,B,A,V)\\
3&\{au,vb\}&(B,U,V,A)\\
4&\{uv\}&(B,V,U,A).
\end{array}
\]

The final row is exactly the target, and all added leaves are untouched.  Hence `OPT(H_h,d)\le 4`.

### Why three rounds are impossible

Tokens `A` and `B` each have distance three from their destinations.  If a schedule had three rounds, each of them would have to move in every round along its unique path.  Therefore round 1 is forced to contain `au` and `vb`, round 2 is forced to contain `uv`, and round 3 is forced to contain `au` and `vb`.  The state after those forced three rounds is `(B,U,V,A)`, not `(B,V,U,A)`.  A fourth `uv` swap is necessary.  Thus

\[
 \boxed{\operatorname{OPT}(H_h,d)=4>LB_{\rm hub}(H_h,d)=3.}
\]

This is a proof for every `h\ge2`, not a computational observation.  It is a constant-size active obstruction embedded at arbitrarily high-degree adjacent hubs; it does **not** establish an unbounded approximation gap.

## 4. Refutation of the naive dependency-cycle certificate

At `u`, ignore zero-flow inert branches and call the `a`-branch `A_0` and the `v`-side branch `B_0`.  The labelled branch flow is

\[
 A_0\xrightarrow{A}B_0,\quad
 B_0\xrightarrow{B}A_0,\quad
 0\xrightarrow{U}B_0,\quad
 B_0\xrightarrow{V}0.
\]

It is the disjoint union of two directed 2-cycles.  The same is true at `v`.  A tempting extension of the fixed-center star argument is

\[
 LB_{\rm cyc}:=\max_{z\in V}\bigl(W(z)+c_z\bigr),
\]

where `c_z` is the number of token-labelled branch-flow cycles, with one extra incident swap charged per cycle.  On `H_h`, `c_u=c_v=2`, so this certificate demands `LB_{\rm cyc}\ge5`.  The four-round schedule above disproves that claim.  The two local 2-cycles are not two independent return obligations: the same outer-edge/bridge phases jointly realize them, and the branch containing multiple tokens cannot be treated as one abstract token.

This is a concrete falsification of the proposed cycle-count lower bound, not a falsification of every possible dependency certificate.  A restricted statistic that excludes cycles involving the `0` hub symbol, or that charges only schedule-independent precedence chains, is not decided by this example and must be proved separately.

## 5. What remains needed for a constructive theorem

The exact missing exchange-ordering lemma is stronger than edge coloring:

> **Token-preserving exchange-ordering obligation.** Given a tree, a destination permutation, and a chosen set of mandatory directional crossings plus explicitly certified return events, construct in polynomial time a sequence of matchings such that every selected edge swap has the required endpoint token identities, no token is used twice in a round, all tokens preserve their identities, and the final placement is the destination permutation. The length must be bounded by the proposed dependency lower bound times a universal constant.

Edge-demand slots alone do not satisfy the obligation: they specify an edge and a time slot but not which token is at the shared endpoint. The three-round forced prefix of `H_h` is the smallest explicit demonstration: all static shortest-path demands can be scheduled, yet the two hub tokens remain unswapped and require a final bridge event.

The current result therefore establishes only:

* a finite, independently hand-verified counterexample to `W+c` flow-cycle charging;
* an exact `OPT=4` overlapping-hub family with `OPT>LB_hub`;
* the exact proof obligation for a future schedule construction.

It establishes neither a constant-factor approximation algorithm nor an unbounded `OPT/LB_hub` family.  The arbitrary-tree stretch question remains open.

## 6. Claim classification and next action

| Claim | Classification |
|---|---|
| `C(e)=2r(e)` and mandatory-load decomposition | Established in the parent checkpoint; preserved, not re-proved here |
| Fixed-center star `OPT=m'+q` | Fully proved but known prior art via Pak and Irving–Rattan |
| Token-labelled `F_v` and schedule-specific `P(\sigma)` definitions | Fully specified; structural definitions, not a theorem about approximation |
| `OPT(H_h,d)=4` and `LB_hub=3` | Fully proved finite parameterized family; independently checked by forced-distance argument and explicit schedule |
| `LB_cyc=max_v(W(v)+c_v)` | Disproved by `H_h` |
| Any branch-flow cycle count is a valid arbitrary-tree lower bound | Not established; the naive form is false |
| A universal-constant schedule relative to `LB_hub` | Plausible but unproved |
| A polynomial token-preserving exchange-ordering algorithm | Open proof obligation |
| An unbounded separation from `LB_hub` | Not established |

The star formula is closed as a novelty lead.  The branch-flow route is narrowed to proving a schedule-independent precedence-chain certificate or finding a family with a growing number of such chains.  No new experiment is authorized or recommended in this checkpoint.
