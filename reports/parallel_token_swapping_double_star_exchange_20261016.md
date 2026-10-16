# A token-preserving exchange schedule on an active double-star family

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-DOUBLE-STAR-EXCHANGE-004`
**Parent checkpoint:** `d2a9829` and `reports/parallel_token_swapping_branch_flow_dependency_20261016.md`
**Scope:** bounded mathematical proof cycle; no experiments, computation, Paper 3/4 changes, or budget renewal.

## 1. Correction to the preceding obstruction

The family (H_h) in the previous note has an active core consisting only of the path (a-u-v-b). Increasing (h) adds leaves whose tokens stay fixed. Thus its active token count, active branch count, path demands, and optimum remain constant. It disproves the proposed cycle-count certificate, but it is not an asymptotically growing active-flow obstruction. The construction below replaces inert degree padding with a number of genuinely moving branches that grows with the parameter.

## 2. Model and parameterized instance

For each integer (m\ge 1), let (T_m) be the double-star with adjacent centers (u,v), left leaves (x_1,\ldots,x_m) adjacent to (u), and right leaves (y_1,\ldots,y_m) adjacent to (v). There are (2m+2) vertices and all are active. A token is named by its initial vertex. The destination permutation is

\[
 x_i\leftrightarrow y_i\quad(1\le i\le m),\qquad u\leftrightarrow v.
\]

A round is a matching of tree edges; each selected edge swaps its two tokens. (D) is the maximum source-to-destination distance, (C(e)) counts token paths using (e), (r(e)=C(e)/2), and (W(z)=\sum_{e\ni z}r(e)). Here (LB_{\rm hub}=\max\{D,\max_z W(z)\}); the optional fixed-hub return term is inapplicable because each center token is destined to the other center.

## 3. Exact traffic and lower-bound arithmetic

For each pendant edge, exactly the leaf token and one incoming token cross its cut:

\[
C(ux_i)=C(vy_i)=2,\qquad r(ux_i)=r(vy_i)=1.
\]

Across the central cut, every (x_i)-token and (y_i)-token crosses in opposite directions, and the two center tokens cross in opposite directions as well:

\[
C(uv)=2m+2,\qquad r(uv)=m+1.
\]

Each leaf-pair token travels three edges; center tokens travel one, so (D=3). Therefore

\[
W(u)=W(v)=m+(m+1)=2m+1,\quad W(x_i)=W(y_i)=1,
\]
\[
\boxed{LB_{\rm hub}(T_m,\pi_m)=2m+1.}
\]

These are mandatory-demand lower bounds: every schedule has at least (m+1) uses of (uv), at least one use of each pendant edge, and at least (2m+1) rounds incident to each center. They do not by themselves account for token identities or give an upper schedule.

## 4. Exchange-ordering lemma and proof

### Lemma (paired cross-hub swaps with center exchange)

For every (m\ge1), the permutation above has a legal parallel token-swapping schedule of (3m+1) rounds. The schedule is constructible in (O(m)) time and has

\[
\operatorname{OPT}(T_m,\pi_m)\le 3m+1<\tfrac32(2m+1)=\tfrac32 LB_{\rm hub}(T_m,\pi_m).
\]

#### Construction

For (i=1,\ldots,m), execute the following three rounds in order:

1. swap (ux_i) and (vy_i);
2. swap (uv);
3. swap (ux_i) and (vy_i).

After all (m) blocks, swap (uv) once more.

#### Token-identity verification

Immediately before block (i), induction gives tokens (U,V) at (u,v), and tokens (X_i,Y_i) at (x_i,y_i), where each token is the one initially named by its position. Other leaf pairs already processed have their targets; unprocessed pairs are untouched. The local state transitions are

\[
\begin{array}{c|cccc}
 &x_i&u&v&y_i\\\hline
\text{before block}&X_i&U&V&Y_i\\
\text{after round 1}&U&X_i&Y_i&V\\
\text{after round 2}&U&Y_i&X_i&V\\
\text{after round 3}&Y_i&U&V&X_i
\end{array}
\]

Thus the leaf tokens are exchanged, while both center tokens are restored to their original centers. This proves the induction invariant and prevents a multi-token branch from being treated as an abstract token. At the end, the final (uv) swap exchanges (U,V) and leaves every leaf target untouched.

#### Matching and complexity verification

Rounds 1 and 3 of each block use two distinct pendant edges, hence a matching. Round 2 and the final round each use only (uv). The blocks are sequential, so every round is a matching and every edge operation has its specified endpoint tokens. The construction emits (3m+1) rounds and takes (O(m)) time and output space.

Each pendant edge is used twice although its mandatory demand is one; (uv) is used exactly (m+1=r(uv)) times. Hence the schedule's edge-use slack is exactly one on every pendant edge and zero on the backbone. Its round count exceeds the hub lower bound by (m), giving the displayed strict (3/2) upper bound on the ratio. This is an upper bound on OPT/LB, not a proof that OPT is (3m+1) or that the ratio tends to (3/2).

## 5. What this establishes—and does not

This is a parameterized, token-preserving exchange-ordering lemma on a meaningful interacting-hub family: the number of active tokens and pendant branches grows with (m), and (m+1) units of directional flow cross the shared backbone. It supplies an explicit feasible schedule whose identities and matching constraints are checked round by round. It also shows that growing active flow in this family does not by itself create an unbounded (OPT/LB_{\rm hub}) gap.

It does **not** prove any of the following:

* that the displayed schedule is optimal for (m\ge2);
* a lower bound stronger than (LB_{\rm hub}) for every schedule;
* a constant-factor algorithm for arbitrary double-stars with arbitrary permutations;
* a constant-factor algorithm or existential bound for arbitrary trees;
* a novel approximation theorem.

The only all-schedule lower bound used is the already established (LB_{\rm hub}=2m+1). We have not proved that every valid schedule must serialize the pair exchanges in this exact order, nor that it must incur the displayed (m) rounds of overhead. This avoids turning one convenient construction's dependency pattern into a purported universal dependency certificate.

## 6. Independent adversarial review

* **Center exchange counted correctly:** the central cut contains (2m+2) crossing token paths, not (2m); hence (r(uv)=m+1).
* **No false fixed-center charge:** neither center token is fixed, so the fixed-hub return lemma is not invoked.
* **Endpoint identities:** each three-round block starts and ends with the same center-token placement; the final central swap alone realizes the center transposition.
* **Simultaneous swaps:** the two pendant swaps in a round are edge-disjoint. The bridge swap is never scheduled in the same round as either incident pendant edge.
* **Lower-bound scope:** (LB_{\rm hub}) is a universal lower bound; no optimality inference is made from the constructed schedule.
* **Active versus padded size:** all (2m+2) tokens move, and the active degree at each hub is (m+1); there are no inert padding leaves.

## 7. Prior-art boundary

Aichholzer et al. prove NP-hardness of parallel token swapping on trees (including subdivided stars); this is a complexity result, not an approximation algorithm for the present family ([ESA 2022 primary paper](https://doi.org/10.4230/LIPIcs.ESA.2022.3)). Bansal, Günlük, and Shapley give constant-factor algorithms for selected topologies including cycles, subdivided stars, and grids ([primary preprint](https://arxiv.org/abs/2411.18581)); those results motivate a careful topology-specific boundary but do not turn this elementary paired-swap construction into a new general theorem. Classical matching-routing results of Alon, Chung, and Graham concern the broader routing model and do not prove this instance-sensitive (LB_{\rm hub}) guarantee ([primary paper](https://doi.org/10.1137/S0895480192236628)).

The novelty verdict is deliberately conservative: this is an independently checked explicit schedule for a growing family, with a clear (3/2) upper ratio against a known lower bound. The gadget is elementary, and no publication-level novelty is claimed. A broader double-star permutation theorem would need a separate proof and a source-level audit.

## 8. Claim ledger and next task

| Claim | Status |
|---|---|
| Previous (H_h) has only a four-vertex active core | Fully checked correction |
| (C,r,D,W,LB_{\rm hub}) values for (T_m) | Fully proved from cut counts |
| The (3m+1)-round schedule reaches the exact target | Fully proved by token-state induction |
| Every round is a matching; construction time is (O(m)) | Fully proved |
| (OPT/LB_{\rm hub}<3/2) on this family | Fully proved as an upper bound |
| Schedule is optimal or all schedules incur its synchronization overhead | Not established |
| Arbitrary-tree constant-factor approximation | Open; unchanged |
| Novelty beyond an elementary family-specific schedule | Not claimed |

**Next focused question:** for *arbitrary* destination permutations on a double-star (not just paired opposite-leaf swaps plus center exchange), is there a polynomial-time token-preserving schedule with a universal constant bound relative to (LB_{\rm hub})? First seek a normal form handling within-side leaf cycles and mixed center/leaf cycles; explicitly keep it as a restricted-class question, not a general-tree approximation claim. No experiment or budget authorization is requested.

## References

* O. Aichholzer et al., “Hardness of Token Swapping on Trees,” ESA 2022, https://doi.org/10.4230/LIPIcs.ESA.2022.3.
* I. Bansal, O. Günlük, R. Shapley, “Parallel Token Swapping for Qubit Routing,” https://arxiv.org/abs/2411.18581.
* N. Alon, F. R. K. Chung, R. L. Graham, “Routing Permutations on Graphs via Matchings,” SIAM J. Discrete Math. 7 (1994), https://doi.org/10.1137/S0895480192236628.
