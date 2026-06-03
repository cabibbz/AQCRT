# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 136 -- **PIVOT: thermal-gap EXCEPTIONAL-POINT estimator of 1/ν; q=4 marginal log cross-checked OFF χ_F.**
sprints/sprint_136.md (+unpublished/); results/sprint_136a_validate_q2.json, sprint_136b_imEP_q{2..7}.json,
sprint_136_analysis.json. DB: im_gEP / thermal_gap_min / gstar_thermal (q2..7 per n); imEP_exponent (p per q).
- NEW observable (fresh thread, off the χ_F arc): charge-0 thermal gap Δ_ε(g) (P=∏X_i filter) on PERIODIC
  chain; at its minimum g*(L) the 2 charge-0 levels form an avoided crossing ⇒ complex-g coalescence (EP /
  quantum Fisher zero) at **Im(g_EP)=√(Δ_min/Δ_ε″)** (real-axis only). Validated vs true complex-symmetric
  diag H(g*+iy) at q=2 (~2%); GPU eigsh to dim≈2M.
- **Recovers exact 1/ν:** local slope of Im(g_EP)~L^{−1/ν} → q2=1.0 (p=0.95), q3=1.2 (p=1.17). 2nd ν route.
- **q=4: 1/ν_eff climbs to 1.5 FROM BELOW** (slopes 1.336→1.369, p=1.354) + Δ_min·L drifts down — the marginal
  (c=1) operator, the SAME suppression χ_F showed (S129–135), now in an independent observable. Two agree.
- **Walking q=5,6,7 = complex-CFT shadow:** 1/ν_eff = 1.51, 1.65, 1.78 (rises smoothly across q=4, still
  climbing; steeper for larger q as ξ shrinks). sat-fit γ=0 ∀q (no plateau; the walking signal is the
  power-law→faster crossover at L≳ξ, NOT γ>0 — corrected my pre-data guess).

## CRITICAL: standing framework (unchanged)
- ν(q=4)=2/3 CONFIRMED (S130) + Albuquerque 2/ν−d=2 (proven) ⇒ χ_F leading exp **2.0**. Golden gate enforces.
- q=4 finite-size exponents sit BELOW their asymptote because of the marginal (dilution, c=1) operator's
  log. This is now seen in TWO independent observables: χ_F (S135, s≈−1.26) AND the thermal-gap EP (S136,
  1/ν_eff→1.5 from below). Walking (q>4) "looks conformal" at L<ξ (ξ>12 for q=5) — exact diag can't resolve it.

## Active Research Thread
Thermal-gap EP / complex-CFT location (S136). 1/ν_eff(q) mapped q=2..7; q≤4 anchored to exact ν. The
walking SATURATION/crossover (the definitive q>4 signature) is beyond exact diag (L<ξ) -- needs DMRG.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty). ~90+ sprints unused. Strongest sim
prediction for HW: q=2 Ising χ_F (or thermal gap) at g_c on 5-10 qubits. Needs credentials restored.

## Top 3 Next Experiments
1. **Walking saturation via Z_q-conserving DMRG** (the S136 headline-completing step). Implement a
   Z_q-charge MPS site (charges arange(q)); ground = charge-0; first-excited charge-0 (ε) via orthogonal_to;
   thermal gap + curvature at 3 g near g* ⇒ Im(g_EP) to n=20–40 for q=5,6. Look for the power-law→faster
   crossover (slope steepening past the conformal shadow) at L≳ξ. OPEN BC ok (the crossover is bulk physics).
2. **Compare 1/ν_eff(q≥5) to Jacobsen–Wiese (PRL 133 077101, 2024) complex ν.** They give the analytic-
   continuation (complex) Potts exponents; check our shadow 1/ν_eff(5,6,7)=1.51/1.65/1.78 vs Re(1/ν_complex).
3. **CHANGELOG.md compression** (~470 > 300). Compress sprints older than last ~10 to one-liners. OVERDUE.

## Ruled Out / Retracted
- Pre-data guess "walking ⇒ Im(g_EP)→γ>0 plateau" -- WRONG (sat-fit γ=0 ∀q; the finite-L gap EP →0 for both
  continuous and first-order; the walking signal is the SCALING crossover, not a plateau). Header corrected.
- Naive 1/lnL extrapolation of OPEN-BC κ_eff (S135 q3 control overshoots 1.96 vs 1.4). Use proven-null-fixed.
- S132/S133 q=4 χ_F sub-2 readings = fixed-g_c off-peak artifacts (S134). n=13 (q=4, 67M) ED infeasible.
- eigsh WIDE g-scan into the deep-ordered phase STALLS (near-degeneracy). Fix: narrow prediction-window on
  the disordered side (g*→g_c from below); dense-subset (scipy eigh subset_by_index) for dim≤1500.

## Key Tools
exp_136b (thermal-gap Im(g_EP), arg=q): charge-0 filter P=∏X_i, gap-min parabola, Im=√(Δmin/Δ″); dense-subset
≤1500 else GPU eigsh(ncv,maxiter). exp_136a (q=2 validation + complex-g EP cross-check). exp_136_analysis
(power/sat fits, slopes). chif_utils.chi_F_exact. DMRG: exp_135a/b (SqPottsChain, but TRIVIAL legs = no
charge conservation -- next sprint needs Z_q-charge legs). db_utils, fss_utils, hamiltonian_utils. Pre-sprint
BLOCKING gates: experiments/test_golden.py + experiments/db_check.py. python = system Python311.
