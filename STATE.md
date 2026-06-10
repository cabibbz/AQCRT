# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 137 — WALKING CROSSOVER OBSERVED (audit-retargeted run).** sprints/sprint_137.md
(+unpublished/). NEW experiments/zq_dmrg_utils.py = Z_q-charge-conserving DMRG (Fourier basis;
charge-0 ground + first-excited via orthogonal_to as CONSTRUCTOR kwarg), ED-validated to 3e-4.
- **Headline:** Im(g_EP)(L) and Δ_min(L) leave the conformal-shadow power law EXPONENTIALLY at
  Λ ∝ ξ: fits y=A·L^{−p}e^{−L/Λ} required at q=8 (dAIC +17/+11; Λ_Im=1.59ξ) and q=10
  (dAIC +37/+31; Λ_Im=1.71ξ, slopes −1.8→−2.64 runaway), NOT at the q=6 control (dAIC≈0,
  Δm·L flat 2.31→2.39). Λ/ξ consistent to ~10% while ξ varies 2.26x. ξ_d exact: 158.9/23.9/10.56.
- **Coulomb-gas verdict (closes audit Q):** Re(1/ν_complex)=1.534/1.563/1.588/1.609/1.646
  (q=5/6/7/8/10; den Nijs continuation, exact on Q≤4). S136 effective 1/ν matches ONLY at q=5
  (1.505); q≥6 rise PAST it (1.648/1.775) — shadow reading dies above q=5; q≥6 ED values are
  crossover phenomenology.
- **S135 rigor closed (audit item):** chi-doubling at n=24 (48→96): q=3 rel 3e-8, q=4 rel 5e-5.

## CRITICAL: standing framework (audit-hedged wording — keep)
- χ_F null = 2/ν−d (proven, golden-gated); q=4 collapse 1/ν=1.45-1.49 consistent w/ exact 2/3.
- q=4 marginal-log: q4-vs-q3 deficit CONTRAST is the datum; EP and χ_F NOT independent
  (χ_F·Im²≈const = single-multiplet dominance). S135 chi=48 values now PROVEN converged (S137d).
- Walking: shadow exponent = complex-CFT Re(1/ν) holds ONLY at q=5; q≥8 now show the real
  crossover (Λ∝ξ). The q=6,7 "1.65/1.78" are neither shadow nor asymptote — crossover-mixed.

## Active Research Thread
Thermal-gap EP across the walking family — S137 found the crossover. Natural next steps below.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **Pin the Λ/ξ coefficient + interface tension:** for L≫ξ, Δ_min ~ e^{−σL} (CNPV 1410.8662);
   extract σ(q) from the q=10 tail (n=24-36, maybe +n=32,36 runs) and test σ = 1/Λ_Dm against
   the known 2D Potts interface tension / Buffenoir-Wallon ξ relation (σξ ~ O(1) check).
2. **q=7 bridge (ξ=48.1):** sizes n=12..40 straddle L/ξ=0.25..0.83 — should show decay ONSET
   (small dAIC, Λ≈1.6ξ≈77 if the S137 scaling holds) — a parameter-free PREDICTION of Λ from ξ.
   Falsifier: dAIC>10 with Λ far from 77, or no onset at all.
3. **EP undershoot correction at q≤4** (marginal-log thread): apply the S137 hyperbola-fit
   methodology (better Δm,c1) to q=4 periodic ED to sharpen the 1/ν_eff→1.5 climb (S136 used
   the parabola; cheap re-analysis of stored scans may suffice).

## Ruled Out / Retracted (recent)
- "Walking = complex-CFT shadow" for q≥6 at ED sizes — measured 1/ν_eff exceeds Re(1/ν_complex);
  only q=5 matches (S137 CG comparison). Shadow language allowed ONLY for q=5.
- Symmetric 2-level crossing form on OPEN chains (20% residuals; wings asymmetric — use
  Δ=sqrt(Δm²+(c1δ+c2δ²)²)). 4-param fits through ~5 points = fake precision (enforce ≥7 pts).
- "ξ>12" budget anchor; q=5,6 crossover hunts at n≤40 (ξ=2512/159 — unreachable; audit).

## Key Tools
zq_dmrg_utils (Z_q-conserving DMRG; max_trunc_err disabled w/ ED-validated accuracy; TeNPy 1.1
orthogonal_to = constructor kwarg). exp_137b (hyperbola-fit EP, arg = q n1 n2...; merge-on-save;
nfit≥7 + relres<5e-3 refinement; DB names BC-qualified: im_gEP_open etc). exp_137c (shadow+decay
AIC analysis + Coulomb-gas continuation). ep_utils (periodic ED EP, golden-gated). Gates:
test_golden (18 checks) + db_check (A/B/D), run pre+post by loop.sh. python = system Python311;
CuPy PINNED 13.6.0. Parallel exp invocations: JSONs merge-on-save but avoid same-q parallelism.
