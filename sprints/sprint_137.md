# Sprint 137 — Z_q-conserving DMRG: hunting the walking CROSSOVER of Im(g_EP) at q=8,10 (where L~ξ is reachable)

**Date:** 2026-06-09
**Thread:** Walking crossover via the thermal-gap EP (continues S136), RETARGETED by the
2026-06-09 system audit: exact classical ξ_d = 2512 (q5), 159 (q6), 48 (q7), **24 (q8), 10.6 (q10)**
(Buffenoir–Wallon 1993) — the originally planned q=5,6 hunt at n=20–40 was unreachable (L≪ξ);
q=8–10 brackets L~ξ inside DMRG range.
**Model:** S_q Potts chain, H = −Σδ(s_i,s_{i+1}) − g Σ_{k=1}^{q−1} X_i^k, OPEN BC (DMRG; the
crossover is bulk physics), g_c = 1/q exact (self-dual).

## The question
S136 validated Im(g_EP)=√(Δ_min/Δ″) (charge-0 thermal-gap exceptional point) as a 1/ν estimator
(exact at q=2,3) and mapped a smoothly rising effective 1/ν_eff(q) at exact-diag sizes — but at
L≪ξ everything "looks conformal". The DEFINITIVE walking/weak-first-order signature is the
**crossover of Im(g_EP)(L) from power-law to faster (gap → exponentially small avoided
crossing) at L ≳ ξ**. At q=8 (ξ≈24) and q=10 (ξ≈10.6), DMRG to n≈32 genuinely crosses ξ.

**Sharp predictions:**
1. q=10 (ξ≈10.6): local slope −d ln Im/d ln L should STEEPEN visibly beyond n≈10–16 and keep
   steepening (approach exponential) — the first direct observation of the crossover in this
   observable.
2. q=8 (ξ≈24): the same steepening should set in later (n≳24), weaker at our sizes.
3. q=6 control (ξ≈159): NO steepening anywhere in range (pure conformal-shadow drift) — if q=6
   steepens like q=10, the "crossover" is an artifact (e.g. χ-truncation), not physics.
4. Audit follow-ups carried in this sprint: (a) PROPER Coulomb-gas/Jacobsen–Wiese comparison of
   Re(1/ν_complex)(q) vs measured 1/ν_eff(q); (b) S135 χ-doubling rigor check (n=24, χ 48→96).

**Falsifiers:** if the DMRG gap at L>ξ for q=10 stays on the small-L power law, the
weak-first-order picture for the quantum chain (or the EP estimator's sensitivity to it) is wrong.
If q=6 shows the same steepening as q=10 at matched n, the signal is numerical, not physical.

## Method
- **Z_q-charge-conserving MPS site** (NEW, experiments/zq_dmrg_utils.py): Fourier (charge) basis
  |m⟩, m=0..q−1. Field Σ_k X^k is DIAGONAL: −g(qδ_{m,0}−1). Coupling δ(s_i,s_j) =
  (1/q)[I + Σ_{k=1}^{q-1} Zk_i Zkd_j] with Zk = charge-raise-by-k (real permutation matrices ⇒
  real dtype). Global charge = Σm_i mod q; ground + first-excited computed INSIDE charge-0
  (initial product state of charge 0; excited via orthogonal_to=[psi0]).
- Thermal gap Δ_ε(g) at 5 coarse + 3 fine g near the predicted minimum (windows extrapolated
  size-to-size, exp_136b pattern, edge hits fail loudly); Im(g_EP)=√(Δ_min/Δ″) from the 3-point
  parabola.
- **Validation:** DMRG vs open-BC exact diag (charge-0 filter ⟨v|P|v⟩>0.9) at small n per q.

## Results
*(filled in as experiments complete)*
