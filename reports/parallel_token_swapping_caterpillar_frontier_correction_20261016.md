# Caterpillar frontier audit: corrected hypotheses and monotone-event obstruction

**Task:** `THEORY-PARALLEL-TOKEN-SWAPPING-CATERPILLAR-FRONTIER-CORRECTION-008`
**Parent checkpoint:** `8072b07`
**Scope:** mathematical audit; no computation or experiment

## 1. Logical correction: the old proposition had inconsistent preconditions

Let `P` be the vertices strictly to the left of a cut, and let a placement be a bijection from tokens to vertices with a bijective token-to-destination map. Say `P` is settled if every `z in P` holds the unique token whose destination is `z`.

**Proposition.** If `P` is settled, there is no token currently outside `P` whose destination lies in `P`.

**Proof.** If token `x` has destination `z in P`, settledness says that `z` currently holds `x`. Vertex occupancy is unique, so `x` cannot simultaneously be outside `P`. Equivalently, the restriction of the current placement to `P` already contains exactly the tokens whose destinations are in `P`. ∎

Therefore the previous sentence “the prefix left of the cut is settled, while an incoming token destined for that prefix remains on the right” describes an empty state set. Its remote-endpoint example does not satisfy that proposition's hypotheses and is not a valid counterexample to that proposition. The bounded-h theorem and its factor `(4h^2-1) LB_hub` are unaffected.

Three readings must not be conflated:

1. **All vertices in the prefix settled:** incoming tokens destined there are impossible by the proposition.
2. **Earlier cuts processed only partially:** this is consistent, but “processed” must specify which swaps or directional tokens have crossed; it does not imply a settled prefix.
3. **Monotone-routing frontier:** earlier destination blocks are settled, while the current block is deliberately left open. Incoming tokens for that current block may remain on the right. This is the coherent interpretation audited below.

## 2. Corrected one-hop lemma, now with consistent hypotheses

Write a caterpillar as backbone centers `v_1,...,v_t`, with block `B_i={v_i} union L_i`, where `L_i` is the set of pendant leaves attached to `v_i`.

**Candidate F (one-hop access for the current open block).** At stage `i`, all blocks `B_1,...,B_{i-1}` are settled; `B_i` is not required to be settled. If a token whose destination is in `B_i` is at a vertex in `B_{i+2} union ... union B_t`, then that exact token can be prepared to cross the backbone cut `v_i v_{i+1}` using at most one swap between `v_{i+1}` and one of its pendant leaves, before any swap across `v_i v_{i+1}`.

The hypotheses are consistent. Candidate F is false: take the bare backbone `v_1,...,v_t`, attach leaves `x` at `v_1` and `y` at `v_t`, and exchange only the tokens at `x,y`. Set `i=1`. The earlier-block condition is vacuous; `B_1` is open; the token for `x` is at `y`; and `v_2` has no pendant leaf. The specified preparation swap does not exist. This refutes only the exact one-hop access rule. It does not refute a nonlocal algorithm: the token's distance is `t+1`, so the endpoint transposition schedule is `2(t+1)-1`, while `D=t+1` and `W_max=1`.

If instead “processed cut” means all tokens destined in its entire left side have crossed and been placed, it is the settled-prefix case and cannot retain an incoming token to that side. If it means only some cut-crossing quota has been performed, that weaker condition is compatible but needs a quantified residual-flow state; it is not the condition in Candidate F.

## 3. Input-defined identity/interval certificate for monotone routing

For token `x`, let `s(x)` and `d(x)` be its source and destination, and let `b(z)=i` when vertex `z` lies in block `B_i`. Define the projected interval endpoints

`a_x=b(s(x))`, `z_x=b(d(x))`.

For backbone cut `i`, define the identity-resolved directional demands

`F_i^+={x:a_x<=i<z_x}` and `F_i^-={x:z_x<=i<a_x}`.

Bijectivity implies `|F_i^+|=|F_i^-|=r_i`. For each pendant edge `v_i l`, its mandatory demand is one exactly when the token at `l` is not destined for `l`, and zero otherwise. Thus the input supplies every token's route interval, every cut's two identity sets, and every leaf loading/unloading obligation. The vertex workload is exactly

`W(v_i)=r_{i-1}+r_i+q_i`,

where missing endpoint-cut terms are zero and `q_i` is the number of incorrect pendant leaves. This is the mandatory swap load incident to the backbone center, not an ordering theorem.

Make the monotone model precise: each token may cross only edges on its unique source-destination path, and crosses each such edge exactly once. At every edge `e`, a monotone swap must pair one token traversing `e` in each direction. Choose a bijection between the two directional identity sets at every edge. Each paired crossing is one event. Add a precedence arc from each token's event on an edge to its next event along the token's unique path, including its source-leaf and destination-leaf edges when applicable. Call the resulting directed graph `D_pi` for pairing choice `pi`.

**Monotone-event lemma.** For a fixed set of edge pairings `pi`, a legal monotone sequential schedule exists if and only if `D_pi` is acyclic.

**Proof.** Necessity: in a monotone schedule, each token performs its path events in path order, so every precedence arc points forward in time; a directed cycle is impossible. Sufficiency: take any topological ordering. Inductively, before an event, both paired tokens have completed their preceding path events and are at the corresponding endpoints. No other event can move either token: every event involving it is on its prescribed path, and the only next prescribed edge is the event currently being considered. The two tokens therefore occupy opposite endpoints and can be swapped. The induction realizes the whole ordering legally. Each event is a single edge swap; emitting events one per round is a valid matching-round schedule (and any simultaneously ready set of vertex-disjoint events is a matching). ∎

The certificate is input-defined once the edge pairings are specified; its verification is polynomial by constructing `D_pi` and testing acyclicity. Searching over all pairings is not shown polynomial. A topological schedule can have as many rounds as there are events, namely `sum_e r(e)`, so this lemma alone gives no `O(D+W_max)` bound.

## 4. Exact cyclic-dependency obstruction and the role of detours

Take a 3-leaf star with center token `Z` fixed and leaf tokens `A,B,C` destined cyclically: `A:1->2`, `B:2->3`, `C:3->1`. Each leaf edge has one token in each direction, so its pairing is forced. The three event nodes are:

- `E_1`: pair `A` outward with `C` inward on leaf edge 1;
- `E_2`: pair `B` outward with `A` inward on leaf edge 2;
- `E_3`: pair `C` outward with `B` inward on leaf edge 3.

Token-path order forces `E_1<E_2` for `A`, `E_2<E_3` for `B`, and `E_3<E_1` for `C`. Hence `D_pi` is a directed 3-cycle, and no monotone schedule exists. This is a valid instance of the corrected event criterion, unlike the former empty-state counterexample.

Every valid schedule must therefore include at least one extra crossing by a token outside its source-destination path (or repeat a path edge); otherwise it would be monotone and induce the impossible event order. Four swaps suffice: `(center,1),(center,2),(center,3),(center,1)`, leaving `Z` at center and routing `A,B,C` correctly. Three swaps cannot suffice: each of the three leaf edges needs a mandatory crossing swap, so a three-swap schedule would use each edge exactly once and be monotone, contradicting the event cycle. Hence `OPT=4`. Here `D=2`, `W_max=3`, and `LB_hub=3`. This proves a real, bounded detour necessity, not an unbounded ratio.

For general caterpillars, actual events can be classified from the input paths: a **mandatory pair event** pairs opposite-direction path tokens across an edge; an **extra event** has at least one token crossing an edge absent from that token's source-destination path. Correctly placed tokens displaced temporarily appear in the extra-event ledger and must later return. A schedule-state certificate can record token identities, remaining path-event queues, extra crossings, and the set of ready edge events. Each round must select a matching among ready events. This makes identities, leaf load/unload, dependencies, detours, and parallel legality explicit, but it does not bound the number of extra events or the makespan by `D+W_max`.

## 5. Research conclusion and exact open obligation

The former remote-endpoint example was an invalid refutation of its stated proposition because the hypotheses contradicted bijectivity. Under the corrected, nonempty “earlier blocks settled/current block open” hypotheses, it refutes the one-hop access rule.

The identity-resolved interval profile and event-DAG criterion are a precise monotone-routing framework. A forced precedence cycle on the 3-leaf star proves that any successful general construction must account for extra crossings/temporary displacement; raw interval counts and acyclic scheduling alone are insufficient. We have not proved that a minimum cycle-breaking detour augmentation is efficiently computable, schedule-realizable, or bounded by `O(D+W_max)`. Nor have we constructed a family with `OPT/(D+W_max)` unbounded. The universal-constant caterpillar conjecture remains unresolved.

**Next proof obligation:** construct a polynomially computable augmentation of the identity-resolved event DAG by extra crossings such that (i) the augmented event schedule is realizable token-by-token, (ii) every round is a matching, and (iii) the longest schedule is at most `c(D+W_max)` for a universal `c`; or prove a parameterized lower bound that rules out this target. No experiment was run.

Prior model context: the matching-round routing model is classical ([Alon–Chung–Graham](https://doi.org/10.1137/S0895480192236628)). Kawahara et al. explicitly distinguish matching-round routing from sequential token swapping; their polynomial optimum for “star-path” graphs is for the **sequential** objective, not our matching-round objective ([primary paper](https://jgaa.info/index.php/jgaa/article/view/paper483); the definition and algorithm distinguish the models). Star-path graphs are a restricted caterpillar shape, so this is relevant nearby prior art but not a solution to the current bound. Parallel token swapping is NP-hard on general trees ([Aichholzer et al.](https://arxiv.org/abs/2103.06707)), which likewise does not settle the caterpillar subclass or the proposed instance-wise guarantee.
