# Parallel token swapping on arbitrary trees: congestion-plus-dilation falsification

**Task:** THEORY-PARALLEL-TOKEN-SWAPPING-TREE-APPROX-001
**Checkpoint:** 67632d8
**Date:** 2026-10-16
**Status:** proof-obligation audit completed; no experiment was run and no experiment budget was renewed.

## 1. Scope and model

Let \(T=(V,E)\) be a finite tree. There is one distinct token at each vertex. A permutation \(\pi\) specifies the destination of each token. In one parallel round we choose a matching \(M\subseteq E\), and swap the tokens across every edge in \(M\). Let \(\operatorname{OPT}(T,\pi)\) be the minimum number of rounds.

For each token \(t\), let \(P_t\) be its unique source-to-destination path. Define
\[
D=\max_t |P_t|,\qquad C(e)=|\{t:e\in P_t\}|,\qquad C_{\max}=\max_e C(e).
\]

The candidate schedule claim was a universal statement of the form
\[
\operatorname{OPT}(T,\pi)\le C_{\max}+D+K
\]
for one constant \(K\), for every tree and permutation. The proof below refutes that claim. It does not refute every possible constant-factor bound in terms of a stronger lower bound.

## 2. Parameterized star counterexample

For every integer \(m\ge2\), take the star with center \(c\) and leaves \(\ell_0,\ldots,\ell_{m-1}\). Put the center token at \(c\), with destination \(c\). Put token \(t_i\) at \(\ell_i\), with destination \(\ell_{i+1\bmod m}\).

### Static quantities

The path of every leaf token is
\[
\ell_i-c-\ell_{i+1\bmod m},
\]
so \(D=2\). For every star edge \(e_i=c\ell_i\), exactly two paths use it: the path of \(t_i\), which leaves \(\ell_i\), and the path of \(t_{i-1\bmod m}\), which enters \(\ell_i\). Therefore
\[
C(e_i)=2\quad\text{for every }i,\qquad C_{\max}=2.
\]

### Round lower bound and exact value

All star edges meet at \(c\), so a matching contains at most one star edge. Every edge \(e_i\) must be used at least once: otherwise the two tokens whose source and destination sides differ across \(e_i\) cannot reach their destinations. If there were only \(m\) rounds, every edge would be used exactly once. But the center token starts and ends at \(c\), so it must leave \(c\) and later return across the same edge; that edge would have to be used twice. Hence
\[
\operatorname{OPT}(T,\pi)\ge m+1.
\]

The bound is tight. Use edges in the order
\[
e_0,e_1,\ldots,e_{m-1},e_0.
\]
After the first \(m\) swaps, \(t_{i-1}\) is at \(\ell_i\) for \(1\le i\le m-1\), \(t_{m-1}\) is at \(c\), and the center token is at \(\ell_0\). The final \(e_0\) swap restores the center token and places \(t_{m-1}\) at \(\ell_0\). Thus
\[
\operatorname{OPT}(T,\pi)=m+1.
\]

Consequently, for every fixed \(K\), choosing \(m>K+3\) gives
\[
m+1>2+2+K=C_{\max}+D+K.
\]
The proposed \(C+D+O(1)\) theorem is therefore false on arbitrary trees. This is a parameterized hand-verifiable counterexample, not a numerical search. The obstruction is the return of a correctly placed hub token; static shortest paths do not encode that occupancy dependency.

## 3. The corrected vertex-capacity lower bound

The previously stated \(\operatorname{OPT}\ge\max(C_{\max},D)\) is also false. On a two-vertex tree with the two tokens exchanged, \(C(e)=2\), \(D=1\), and one swap is optimal.

For a vertex \(v\), write
\[
S(v)=\sum_{e\ni v}C(e).
\]
The valid lower bound is
\[
LB_0(T,\pi)=\max\left\{D,\max_{v\in V}\frac{S(v)}2\right\}.
\]
Since the schedule length is integral, the directly usable version is
\[
LB_{\mathrm{int}}(T,\pi)=
\max\left\{D,\max_{v\in V}\left\lceil\frac{S(v)}2\right\rceil\right\}.
\]

### Proof

Fix an edge \(e\). Every one of the \(C(e)\) tokens whose source and target lie on opposite sides of \(e\) must cross \(e\) at least once. One swap on \(e\) moves only two tokens across that edge, so any valid schedule uses \(e\) at least \(C(e)/2\) times. Summing over edges incident with \(v\), the number of swaps incident with \(v\) is at least \(S(v)/2\). A matching contains at most one edge incident with \(v\) in each round, hence the schedule has at least that many rounds. Independently, a token can move by at most one tree edge in a round, giving the \(D\) term. This proves both \(LB_0\le\operatorname{OPT}\) and \(LB_{\mathrm{int}}\le\operatorname{OPT}\).

For the two-vertex exchange, \(D=1\), \(S(v)=2\) at both vertices, and \(LB_{\mathrm{int}}=1=\operatorname{OPT}\). This is the exact correction to \(\max(C_{\max},D)\).

### A useful local strengthening

The star exposes one additional, rigorously provable term. Suppose a vertex \(v\) initially contains the token whose destination is \(v\), and let
\[
F(v)=\{e\ni v:C(e)>0\},\qquad q(v)=|F(v)|.
\]
If \(q(v)>0\), every edge in \(F(v)\) must be used. The fixed token at \(v\) must also cross an incident edge to leave and cross back to return. Those are two uses of one incident edge in addition to the first required use of each of the \(q(v)\) edges. Therefore
\[
\operatorname{OPT}(T,\pi)\ge q(v)+1.
\]
Thus the following is a valid, but still incomplete, strengthening:
\[
LB_{\mathrm{hub}}=
\max\left(LB_{\mathrm{int}},
\max_{v:\,q(v)>0,\,\pi^{-1}(v)=v}(q(v)+1)\right).
\]
On the \(m\)-leaf star, \(LB_{\mathrm{int}}=m\) and the hub term is \(m+1\), which exactly matches the optimum. This does not claim that \(LB_{\mathrm{hub}}\) is the sharp lower bound for all trees.

## 4. Hand-checks of the proposed scheduling invariant

These are mathematical checks, not new computational experiments.

| Tree family | Hand-checked instance | Result | What it tests |
|---|---|---|---|
| Path | Two adjacent tokens exchanged | \(C(e)=2,D=1,LB_{\mathrm{int}}=1,OPT=1\) | Corrects the false \(C_{\max}\) lower bound. |
| Star | The \(m\)-cycle above | \(C_{\max}=2,D=2,LB_{\mathrm{int}}=m,OPT=m+1\) | Hub occupancy defeats \(C+D+O(1)\). |
| Subdivided star | \(m\) branches \(c-x_i-\ell_i\), center fixed, leaf cycle | \(C_{\max}=2,D=4,LB_{\mathrm{int}}\ge m,OPT\ge m+1\) | The same return dependency survives branch subdivision. |
| Double star | Centers \(x,y\), \(p\) local cycle leaves at \(x\), \(q\) at \(y\), bridge unused | \(OPT=\max(p+1,q+1)\) by running the two exact star schedules in parallel | Separate high-degree bottlenecks compose by maximum, not sum. |
| Binary tree | Two disjoint sibling-leaf exchanges, parent tokens fixed | Each cherry needs exactly 3 rounds; both complete in 3 parallel rounds; \(LB_{\mathrm{hub}}=3\) | Temporary displacement is necessary even when bottlenecks are disjoint. |
| Multiple bottlenecks | Double star with both local cycles and optional bridge traffic | Local hub terms remain valid, but bridge traffic creates dependent phases | Shows why a local-load proof must also control token identity and phase ordering. |

The examples support the lower bound and identify the missing invariant. They do not establish a constant-factor algorithm.

## 5. Why the obvious upper-bound proof does not transfer

For store-and-forward packet routing, one may assign a packet to each fixed path and schedule edge transmissions subject to congestion and dilation. Token swapping has a different state constraint: a used edge exchanges two occupied vertices, and the return token is not an empty buffer. A swap can simultaneously advance two path tokens, advance one and displace another, or create a required future repair. The star sequence demonstrates the last case exactly.

The most tempting proof route is therefore invalid:

1. reserve \(C(e)/2\) slots on every edge;
2. color the slots into matchings; and
3. infer a token schedule from the edge coloring.

Steps 1--2 do not preserve token identities or intermediate occupancy. A valid conversion would need an exchange lemma saying that every jointly colored set of edge slots can be ordered into swaps while keeping all tokens on compatible paths. No such lemma was proved here, and the star is a direct warning that path-edge slots alone are insufficient.

A distance-decreasing matching rule has the same gap: in the star, the center token is initially at its destination but must be displaced. Requiring every swap to reduce a local distance cannot be a complete invariant. Allowing such detours restores completeness but leaves their number and dependencies unbounded by \(C_{\max}+D\) as the counterexample shows.

## 6. Upper-bound status and narrow surviving conjecture

This cycle establishes neither a constant-factor algorithm relative to \(LB_{\mathrm{int}}\) or \(LB_{\mathrm{hub}}\), nor an unbounded separation between \(\operatorname{OPT}\) and either lower bound. The correct mathematical status is:

* **Disproved:** \(\operatorname{OPT}\le C_{\max}+D+O(1)\) on arbitrary trees.
* **Disproved:** \(\operatorname{OPT}\ge\max(C_{\max},D)\).
* **Fully proved:** \(LB_{\mathrm{int}}\le\operatorname{OPT}\).
* **Fully proved:** the fixed-hub \(q(v)+1\) strengthening under its explicit fixed-token assumptions.
* **Finite exact family:** the star and double-star values above.
* **Open:** whether a polynomial-time matching schedule is always within a universal constant of a sufficiently strong local-load/dependency lower bound, and whether the user-specified \(LB_0\) itself has bounded stretch.

The narrowest surviving conjecture worth a future mathematical attack is:

> There is a universal constant \(\alpha\) and a polynomial-time algorithm that produces a parallel token-swapping schedule of length at most \(\alpha\,LB_{\mathrm{dep}}(T,\pi)\), where \(LB_{\mathrm{dep}}\) extends \(LB_{\mathrm{hub}}\) by a proved certificate for jointly dependent detours.

This is intentionally not presented as a theorem. The first proof obligation is to define \(LB_{\mathrm{dep}}\) without making it as hard to compute as the original problem, and to prove a token-preserving exchange/ordering lemma. Until that is done, a claim of polynomial constant approximation is unsupported.

## 7. Primary-source boundary and novelty assessment

The primary 2022 tree-hardness paper defines a parallel round as swaps on a matching and proves NP-hardness on trees, even subdivided stars. It explicitly describes the arbitrary-tree approximation question as open at that point:

* Aichholzer et al., Hardness of Token Swapping on Trees, ESA 2022, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2022.3 (definition and tree hardness; see also the full text, especially pp. 3--5).

The later primary source by Bansal, Günlük, and Shapley gives constant-factor algorithms for cycles, subdivided stars, and grids, not arbitrary trees. Its Theorem 3 is a \(4OPT+\min\{OPT,h\}+1\) bound for subdivided stars, and its introduction says that the general topology question remains difficult:

* Bansal, Günlük, Shapley, Parallel Token Swapping for Qubit Routing, arXiv v2 (2025), https://arxiv.org/abs/2411.18581 and https://arxiv.org/html/2411.18581v2.

The 1994 Alon--Chung--Graham routing-via-matchings model is the same matching exchange model used here, but its worst-case routing-number bounds are not an instance-sensitive \(C+D\) theorem:

* https://epubs.siam.org/doi/abs/10.1137/S0895480192236628

Bounds for packet routing with empty buffers cannot be imported without an explicit token-preserving conversion; none is supplied by those results.

Therefore the present result is a genuine correction and a bounded theoretical advance over the queued conjecture, but not a new approximation theorem or a publishable breakthrough. The star lower-bound mechanism is elementary and the general upper-bound question remains open after this audit.

## 8. Provenance and metadata audit of 67632d8

The commit appended direction-selection and reconciliation metadata without rewriting prior research/supervisor_events.jsonl records. The audit found:

1. The state-level renaming of several completed-result IDs from AUDIT-* to EXP-* is consistent with the nine matching IDs in research/experiment_ledger.jsonl; audit-only records remain explicitly AUDIT-*.
2. The historical event log retains the earlier worker/reconciliation events, and its new direction-selection record explicitly says historical_worker_events_rewritten:false.
3. The ledger contains EXP-EDCS-LAZY-REPAIR-INVARIANT-20261015, whereas the state snapshot contains the related result under EXP-NOVEL-EDCS-LAZY-REPAIR-EXPERIMENT-001. This is a pre-existing cross-file alias mismatch, not evidence of a new experiment; it is preserved rather than silently rewritten in this theory task.
4. The state snapshot still reports completed_experiments:9 against a configured maximum of 8. Lifetime counters are immutable and were not changed. This remains an operational reconciliation issue, not a scientific result.
5. last_successful_commit in the snapshot still points to 90277a9, even though 67632d8 is the later direction-selection commit. This checkpoint update records the discrepancy; no event history was rewritten.

## 9. Paper 3 and execution boundary

Paper 3 Target A (direct resolution/refutation) and Target B (evidence growth) remain separate frozen objectives. No historical labels or forecast scores were created. No computational experiment, supervisor start, budget renewal, or Paper 4 claim was made in this cycle.

The single most informative future action would be a separately authorized, non-default mathematical/computational study that constructs and independently checks a smallest tree family with \(LB_{\mathrm{hub}}\) bounded but with a provably larger number of dependency phases, or else proves a token-preserving exchange lemma that rules out such a family. It is **not executed** here.
