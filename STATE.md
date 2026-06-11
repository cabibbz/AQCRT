# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 139 — INTERFACE-TENSION TEST: σ̃·ξ_d = 1/4 (= σ_od/2), naive duality EXCLUDED.**
sprints/sprint_139.md (+unpublished/). Extended q=10 to n=32,36 (L/ξ=3.4; n=36 fit relres
3.8e-4). Joint fit ln Δm = lnA_q − a lnL − (s/ξ_q)L over q=6,7,8,10 (32 pts, ξ lever 15x):
- **s = 1/2 (classical Borgs–Janke duality σ_od·ξ_d=1/2 transferring naively) EXCLUDED:**
  dAIC +135 joint, +16.8 q=10-tail-only; local rate σ_loc·ξ FLATTENS at 0.23–0.27 over
  L/ξ=2.5–3.4 (H_dual demands 0.51–0.55). s=0 (no decay) excluded too (+141).
- **q=10 tail: s = 0.213±0.035; s≡1/4 fits as well as free (dAIC −0.1).** Reading: the gap is
  a tunneling AMPLITUDE ⇒ Δ_min ~ (1/L)·e^{−σ_od L/2} with the EXACT 2σ_od=1/ξ_d ⇒ σ̃ξ=1/4 ✓.
  Caveat flagged: τ-continuum anisotropy/velocity factor not independently fixed (queued).
- Reconciliation: S137/138's Λ_Dm≈2.5–2.7ξ (s≈0.40) is the crossover-ONSET law (what the blind
  q=7 prediction tested — still stands); the ASYMPTOTIC constant is 1/4 (Λ_∞ = 4ξ).
- Arc complete: estimator (S136) → crossover + null control (S137) → blind Λ∝ξ prediction
  (S138) → exact-anchored asymptotic constant (S139).

## CRITICAL: standing framework (audit-hedged wording — keep)
- χ_F null = 2/ν−d (proven, golden-gated); q=4 collapse 1/ν=1.45-1.49 consistent w/ exact 2/3.
- q=4 marginal-log: q4-vs-q3 deficit CONTRAST is the datum; EP & χ_F NOT independent.
- Walking: shadow exponents valid ONLY at q=5 (S137 CG). Crossover onset Λ_Im≈1.65ξ_d
  (CONFIRMED blind, S138); asymptotic gap decay σ̃=1/(4ξ_d)=σ_od/2 (S139, q=10).

## Active Research Thread
Walking/EP arc is COMPLETE and publication-shaped. Strong pivot candidate; or close remaining
loose ends below.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **Velocity v(q=10) measurement** to close the S139 anisotropy caveat: disordered-phase
   dispersion (single charge-1 magnon: E(k) from twisted-BC ED or DMRG momentum states) at the
   transition → dimensionless σ̃ξ/v vs 1/4. Cheap (ED q=10 n≤6 + small DMRG).
2. **Write-up sprint: the S136–S139 arc as a paper draft** in unpublished/ (EP estimator,
   validation, crossover + null control, blind Λ∝ξ prediction, σ_od/2 asymptotics). All data
   and DB rows exist; pure writing + 2-3 summary figures (matplotlib).
3. **σ̃ universality check at q=8:** extend q=8 to n=44,48 (L/ξ≈1.8-2.0; ~3-4h each) to verify
   the σ_loc plateau → 1/4 sets in at the SAME L/ξ as q=10 — tests the scaling form, not just
   the constant. (Optional; q=10 already carries the claim.)

## Ruled Out / Retracted (recent)
- Naive duality transfer σ̃ξ=1/2 (S139); "ξ/Λ≈0.40 is asymptotic" (it is the onset value).
- Shadow language for q≥6 effective exponents; <7-point hyperbola fits; importing exp scripts.

## Key Tools
zq_dmrg_utils (Z_q DMRG; orthogonal_to = constructor kwarg). exp_137a/b harnesses w/ SPRINT_NO
provenance env. exp_139a (joint interface-tension fit). exp_138a (Λ prediction test). exp_137c
(AIC/CG). ep_utils (golden-gated). Gates: test_golden 18 + db_check A/B/D, pre+post via
loop.sh. python = system Python311; CuPy PINNED 13.6.0. Costs: q=10 n=32/36 chi=128 ≈ 3.2h
each (34 solves). JSON accumulate files merge-on-save; same-q parallel runs still discouraged.
