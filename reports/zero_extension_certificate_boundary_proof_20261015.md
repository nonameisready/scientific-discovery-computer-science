# Reidl–Wahlström certificate layers: adversarial audit of a proposed deletion

Task: `THEORY-ZEROEXT-CERTIFICATE-BOUNDARY-005`
Review date: 2026-10-15

This is one source-level proof cycle. No experiment or computational search was
run. The original worker artifact at 19:32:48–19:34:23 UTC failed the strict
proof-obligation validation; its false result, raw hash, and event-log entries
are preserved. This independently produced exposition does not rewrite that
execution history.

## 1. Exact source certificate and its role

Use Reidl–Wahlström's notation (S=\{t_1,\ldots,t_r\}), (r=|S|\le s),
with at most (s) metric labels. Define the terminal boundary
\[
E_S=\bigcup_{t\in S}\delta(t).
\]
After the source's edge-to-vertex transformation, (E_S) is the source set of
each gammoid. The preceding rejection test ensures (|E_S|\le 2k); otherwise
no injectively terminal-labeled extension can use at most (k) crossings.
For each original edge (e=uv), the construction also makes a sink-copy
vertex (e'), with incoming arcs from copies of (u) and (v).

The matroid is the direct sum
\[
M=M_1\oplus\cdots\oplus M_s\oplus M_0,
\]
where each (M_i) is a copy of the gammoid rooted at (E_S), of rank
(|E_S|\le2k), and (M_0=U_{|E|,k}), of rank (k). Thus
\[
\operatorname{rank}(M)\le (2s+1)k.
\]
For (e\notin E_S),
\[
Y(e)=\{e'_1,\ldots,e'_s,e_0\},\qquad p=|Y(e)|=s+1,
\]
with one sink-copy in every gammoid and the original edge in (M_0). The
representative-set lemma gives at most
\(\binom{\operatorname{rank}(M)}{p}=O_s(k^{s+1})\) representatives
when (s) is fixed. This is a certificate bound; the graph sparsifier
requires the paper's additional sequential recomputation and contraction of
irrelevant edges.

For a cost-optimal extension \(\lambda\) chosen with minimum crossing count,
write \(C\) for its crossing set and \(V_i=\lambda^{-1}(i)\). The source
uses the common witness coordinates
\[
X_i=\begin{cases}
\delta(V_i)\cup\delta(t_i),&i\le r,\\
\delta(V_i),&r<i\le s,
\end{cases}
\qquad X_0=C\setminus\{e\}.
\tag{1}
\]

* Each of the first (r) **terminal-specific gammoids** certifies pushed
  reachability after excluding the corresponding terminal source side; the
  extra \(\delta(t_i)\) is part of that separator query.
* The other (s-r) **unused-label gammoids** certify reachability from all
  terminals for labels with no prescribed terminal. They cannot generally be
  dropped merely because one particular optimum does not use those labels:
  the certificate must cover every admissible metric/labeling query.
* The **uniform layer** is not just a second counter for \(|C|\le k\). Since
  \(X_0=C\setminus\{e\}\), any candidate \(f\in C\setminus\{e\}\)
  overlaps \(X_0\), while \(e\) is disjoint and \(|X_0|+1=|C|\le k\).
  It makes \(e\) the unique extension among crossing-edge candidates.

In the source proof this uniqueness is combined with the gammoid layers:
if a candidate edge lies in \(C\), the uniform coordinate forces it to be
the requested \(e\); otherwise the label layer whose class contains it
separates its sink-copy from \(E_S\). Conversely, pushing and the gammoid
cut characterization establish that the essential target \(e\) extends in
every layer. This is the exact per-essential-edge exchange step needed to
show all essential edges lie in the selected set.

## 2. Candidate transformation and corrected counterexample

The transformation under test deletes (M_0), on the intuition that the
crossing budget is already controlled elsewhere. A first attempted witness,
the all-terminal triangle (K_3), is **invalid**: every edge belongs to
\(E_S\), while source tuples (Y(e)) are only defined for (e\notin E_S\).
We discard that example rather than treating it as evidence.

The corrected graph (G) is a two-terminal series-parallel multigraph with
terminals (a,b), internal vertices (u,v), three parallel edges from (a
to (u), two parallel edges \(e_1,e_2\) from (u\) to (v), and three
parallel edges from (v) to (b). Set
\[
S=\{a,b\},\quad D=\{A,B\},\quad \tau(a)=A,\ \tau(b)=B,
\quad s=3,\quad k=3,
\]
and let \(\mu\) be the discrete metric \(\mu(A,B)=1\). The metric is
finite, symmetric, positive off-diagonal, and satisfies the triangle
inequality. The source gate is exactly tight:
\(|E_S|=6=2k\), and the two middle edges satisfy \(e_1,e_2\notin E_S\).

Every admissible labeling is a cut. The possible (a)-side sets are
\(\{a\},\{a,u\},\{a,v\},\{a,u,v\}\), with boundary sizes
\(3,2,8,3\). Therefore the unique minimum cut is
\(C=\{e_1,e_2\}\), of cost 2. It is feasible for budget \(k=3\). With
essential-edge threshold (q=2\), every extension of cost at most (q\) and
at most (k\) crossings is this same optimum. Both (e_1,e_2\) are therefore
essential by the source definition.

Fix this single optimum \(\lambda\). The gammoid query tuple
\(X_G=(X_1,\ldots,X_s)\) in (1) is identical whichever of (e_1,e_2\) is
designated as target. By the source's own pushing argument, applied to each
essential edge separately, both sink-copies extend the corresponding
gammoid restrictions in every layer: after pushing from any label, each
essential edge remains crossing in every cost-optimal extension, so its
endpoint is reachable from the prescribed source side while avoiding the
separator. Proposition 4.8 then gives the gammoid extension. The third,
unused label has \(V_3=\varnothing\), so its gammoid query is empty and
does not separate these two candidates.

For the requested target (e_1\), however,
\(X_0=C\setminus\{e_1\}=\{e_2\}\). In (M_0=U_{8,3}\), (e_1\) extends
\(X_0\) and (e_2\) does not, due to overlap. Swapping the requested target
swaps the unique extension. Hence deleting (M_0) destroys the source
proof's **per-essential-edge unique-extension witness**: the gammoid
coordinates alone admit both essential candidates for the same (X_G\).

This is a counterexample to the **specific drop-in deletion**, not a theorem
that every representative family for the reduced gammoid system must omit
an essential edge, and not a lower bound on every possible joint certificate.
It pinpoints the failed proof obligation: after deletion, the source argument
can no longer infer that an arbitrary representative extending (X_G\) is
the requested essential edge. A different representative theorem might
still exist, but none is established here.

## 3. Replacement-certificate check and parameter accounting

On an abstract ground set of (m\le k\) elements, the singleton certificates
\(Y'(e)=\{e\}\) in (U_{m,k}\) have parameter (p=1\). For
\(X=E\setminus\{e\}\), only \(Y'(e)\) extends (X\); therefore every
representative family must keep every singleton. The size is exactly
\(m\le k=O(k)\), with (f(s)=1\) and exponent (c=1\). This is a fully
proved identity bound, not a compression of the graph above (which has eight
edges and (k=3\)), not an executable graph algorithm, and not an exact
terminal-preserving sparsifier. It contributes no improvement to the
Reidl–Wahlström bound.

The proposed removal keeps the number of gammoid layers (s), and the proof
provides no reduction of their combined rank (O(sk)\) or representative
parameter. Thus the source's (O_s(k^{s+1})\) bound is unchanged; no
\(f(s)k^c\) result with universal (c\) is obtained.

## 4. Claim ledger, adversarial review, and novelty verdict

| Claim | Classification | Scope |
|---|---|---|
| Source certificate has (s) gammoid coordinates plus one uniform coordinate, (p=s+1), rank at most ((2s+1)k) | Known prior art; source-reconstructed | Reidl–Wahlström Section 4.3 |
| The parallel-bundle SP graph above has two essential edges outside (E_S), and both extend the same gammoid-only query | Independently checked finite counterexample | Does not imply a lower bound on all representative families |
| Dropping (M_0) preserves the source's per-edge unique-extension argument | Disproved | The two requested targets are no longer distinguished by the common gammoid query |
| Singleton identity certificate on abstract (m\le k) ground sets has size (m) and all (m) are necessary | Fully proved | Trivial certificate fact only |
| The (s) gammoid layers admit a smaller joint certificate | Plausible but unproved | Open; requires a new exchange lemma |
| A general (f(s)k^c) sparsifier bound follows | Not established | No graph construction/algorithm transfer proved |

Adversarial checks: (i) the source family excludes (E_S\), and the corrected
candidate edges meet this condition; (ii) \(|E_S|=2k\) satisfies the source
precheck; (iii) the cut enumeration establishes feasibility and essentiality,
not just pairwise signatures; (iv) the gammoid conclusion is invoked only
for essential edges under the source's pushing lemma and Proposition 4.8;
(v) the uniform coordinate distinguishes the designated edge; and (vi) no
claim is made about arbitrary joint compression, alternate graph
representations, or terminal-preserving sparsifiers.

**Novelty verdict:** no novel theorem or sparsifier improvement. The useful
result is a corrected, feasible obstruction to this particular layer
deletion and an explicit identification of the unique-extension step that
fails. The failed (K_3) attempt is recorded for auditability, not counted
as evidence. Close this transformation; do not generate another elementary
interface variant. A future Zero Extension task is justified only by a
concrete simultaneous-gammoid exchange lemma or a family that lower-bounds
all joint certificates.

## 5. Paper 3 separation

Paper 3 Target A (direct resolution/refutation) and Target B (independently
verifiable evidence growth) remain separate. No historical outcome label,
forecast score, or frozen cutoff was changed.
