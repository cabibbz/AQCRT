# Current State -- Rewrite this completely each sprint

## Last Sprint
**Sprint 142 — WRITE-UP SPRINT: the S136-141 arc is now a paper-style draft.**
sprints/sprint_142.md. Deliverables:
- **unresolved/manuscript_EP_walking_arc.md** (v1): abstract → methods (EP estimator,
  Z_q-DMRG, fitting discipline) → six results sections → discussion on the open
  σ̃·ξ_d^cl≈1/4 puzzle (3 candidate resolutions) → limitations → reproducibility appendix.
- **unresolved/figures/fig1-4** (+exp_142a_figures.py). BONUS visual found while plotting:
  against L/ξ_d^cl the q=7/8/10 Δm·L curves nearly COLLAPSE onto one master trajectory
  (the Λ∝ξ law as a scaling collapse); q=6 control flat. Use fig1a as the paper's lead.

## CRITICAL: standing framework
- χ_F null = 2/ν−d (proven, golden-gated); q=4 marginal-log: q4-vs-q3 deficit contrast.
- Walking arc (S136-141, manuscript-complete): shadow exponents valid ONLY at q=5; onset
  Λ_Im≈1.65ξ_d^cl (blind-confirmed); **asymptotic σ̃·ξ_d^cl = 0.24±0.03 q-INDEPENDENT
  (q=8,10) — mechanism unknown**; quantum ξ_x decoupled (2-4 sites).

## Active Research Thread
Arc written up. The mystery constant awaits its theory probe; or pivot to a fresh question.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty; needs human). Log predictions only.

## Top 3 Next Experiments
1. **Theory probe of the 1/4 (the decisive physics next-step):** measure the quantum chain's
   OWN order-disorder interface free energy directly — fixed-BC DMRG: pin left edge
   disordered-favoring / right edge to one Potts color at g_c; interface energy excess
   F_int(n) vs n → σ_int^quantum. Compare against σ̃ = 0.0237 (q=10) and against σ_od^cl.
   Locates WHERE the classical normalization enters. (New harness needed: boundary fields in
   zq_dmrg_utils — moderate effort, ED-validate at small n first.)
2. **Manuscript polish pass:** bootstrap error bars for Λ and s; pin the constant (1/4 vs
   0.213±0.029) by one more q=10 size (n=40, ~4-5h) or theory; BC-dependence spot check.
3. **ξ_x(q) mini-survey** (cheap, feeds #1): exp_140a at q=7,8 → ξ_x ∝ ξ_d^cl or q-flat?

## Ruled Out / Retracted (recent)
- "S139's 1/4 is numerology" (killed S141); amplitude/naive duality readings (S139/S140);
  plain ⟨P⟩ filtering near coexistence; ξ=v/Δ on flat bands; <7-point crossing fits;
  importing exp scripts (no __main__ guards).

## Key Tools
exp_142a_figures.py (figure generator; unresolved/figures/). exp_137a/b harnesses (SPRINT_NO
env). exp_141a/140a/140b/139a analysis pattern library. zq_dmrg_utils. Gates: test_golden 18
+ db_check A/B/D pre+post via loop.sh. python = system Python311; CuPy PINNED 13.6.0.
Novel findings → unresolved/ (incl. the manuscript).
