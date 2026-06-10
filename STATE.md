# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 138 — Λ ∝ ξ PREDICTION CONFIRMED at q=7 (blind/out-of-sample).** sprints/sprint_138.md
(+unpublished/). Registered BEFORE data: Λ_Im = 79±5 (=1.65ξ, from S137's q=8,10 coefficients),
Λ_Dm = 126±7. Measured (n=8..40, ED-validated 1.1e-6, every size ≥7 fit points):
- **Λ_Im = 79 ± 25 (1.64ξ) — dead center; Λ_Dm = 118 ± 24 (0.3σ).** Decay term independently
  demanded: dAIC +13.0 (Δm) / +7.0 (Im); with Λ FIXED at the prediction (zero extra params)
  it still beats pure power by +14.9/+9.0. Matched-window q=8 calibration: +12.5 vs q=7's +13.0.
- Λ_Dm/Λ_Im = 1.50 (q=8: 1.58, q=10: 1.59). All 3 pre-registered falsifiers evaded.
- **The law Λ_Im ≈ 1.65 ξ_d now spans q=7,8,10 (ξ 10.6→48.1, 4.6x) with q=7 earned blind.**
  S137's POTENTIALLY NOVEL upgraded to CONFIRMED (hardening #1,#2,#3 satisfied).

## CRITICAL: standing framework (audit-hedged wording — keep)
- χ_F null = 2/ν−d (proven, golden-gated); q=4 collapse 1/ν=1.45-1.49 consistent w/ exact 2/3.
- q=4 marginal-log: q4-vs-q3 deficit CONTRAST is the datum; EP and χ_F NOT independent
  (χ_F·Im²≈const). S135 chi=48 values PROVEN converged (S137d).
- Walking: shadow exponent = Re(1/ν_complex) holds ONLY at q=5 (S137 CG). q≥7: the real
  crossover, **Λ_Im ≈ 1.65 ξ_d (CONFIRMED S138)**; q=6 ED/DMRG values are crossover-mixed.

## Active Research Thread
Thermal-gap EP walking crossover — law confirmed. Natural continuations below; also consider a
PIVOT (thread is mature; the EP toolkit + Z_q DMRG are reusable for new questions).

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **Interface-tension identity:** for L≫ξ, Δ_min ~ e^{−σL}; test σ vs the exact 2D Potts
   interface tension via σ·ξ ~ O(1): we have 1/Λ_Dm = σ_eff at q=7/8/10 → check σ_eff·ξ_d =
   1/2.46, 1/2.51, 1/2.71 ≈ 0.40, 0.40, 0.37 — already suspiciously constant! Formalize vs
   literature duality relation (σ(q)ξ_d(q) known exactly?) — cheap, analysis-only sprint.
2. **Write-up sprint:** S136-138 form a complete, publishable arc (EP estimator → crossover →
   confirmed Λ∝ξ law + q=5 shadow anchor). Draft a paper-style summary in unpublished/.
3. **q=5 deep-shadow precision:** ξ=2512 ⇒ pure shadow to any reachable L; high-precision
   1/ν_eff(q=5) via the S137 hyperbola method to n≈40 → sharpest test of Re(1/ν_complex)=1.534
   (S136 ED gave 1.505 at n≤9; DMRG can halve the undershoot).

## Ruled Out / Retracted (recent)
- "Shadow" language for q≥6 effective exponents (S137); symmetric crossing fits on open chains;
  <7-point hyperbola fits (fake precision); "ξ>12" anchors (use exact ξ_d table in KNOWLEDGE).
- exp scripts have NO __main__ guard — NEVER import one (it executes; bit the audit twice).

## Key Tools
zq_dmrg_utils (Z_q-conserving DMRG; orthogonal_to = CONSTRUCTOR kwarg in TeNPy 1.1).
exp_137a/b = generic validate/production harnesses, SPRINT_NO env sets provenance (S138 used
this; JSON name + DB sprint follow). exp_138a (prediction-test analysis). exp_137c (AIC/CG).
ep_utils (periodic ED EP, golden-gated). Gates: test_golden 18 checks + db_check A/B/D,
pre+post via loop.sh. python = system Python311; CuPy PINNED 13.6.0. Costs: q=7 n=40 chi=128
size ≈ 110 min (34 solves); full q sweep n=8..40 ≈ 6.5 h.
