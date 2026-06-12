# Sprint 142 — Write-up sprint: the thermal-gap EP / walking-crossover arc (S136–141)

**Date:** 2026-06-12
**Thread:** Consolidation. The arc is experimentally complete: validated estimator (S136) →
crossover + null control (S137) → blind Λ∝ξ prediction (S138) → asymptotic constant (S139) →
velocity test removing explanations (S140) → two-q universality (S141). This sprint produces
the paper-style manuscript + publication figures from the existing data (no new compute).

## Deliverables
1. **unresolved/manuscript_EP_walking_arc.md** — paper-style draft (abstract, intro, model &
   methods, five results sections, discussion centered on the open 1/4 puzzle, methods
   appendix with the reproducibility map to scripts/DB).
2. **unresolved/figures/fig1..fig4** (PNG, matplotlib; generator experiments/exp_142a_figures.py):
   - Fig 1: the crossover — Δm·L vs L/ξ_d^cl for q=6,7,8,10 (+ Im local slopes panel).
   - Fig 2: the blind q=7 prediction — Λ_Im/ξ vs q with the registered prediction band.
   - Fig 3: the universal constant — σ_loc·ξ_d^cl vs L/ξ (q=8, q=10) with 1/4 / 0.40 / 0.50 lines.
   - Fig 4: the two-length structure — C(r) at q=10 g_c (ξ_x ≈ 2–4) vs ξ_d^cl; + 1/ν_eff(q)
     vs Re(1/ν_complex) (the q=5-only shadow anchor).

## Results
Both deliverables produced:
- **unresolved/manuscript_EP_walking_arc.md** — full draft: abstract, intro, estimator+methods
  (incl. the fitting-discipline and validation numbers), six results sections (crossover+null
  control, blind q=7 prediction, asymptotic constant, velocity test/two lengths, q=8
  universality, shadow validity), discussion centered on the open σ̃·ξ_d≈1/4 puzzle with three
  candidate resolutions and the fixed-BC interface-free-energy experiment as the decisive
  probe, limitations stated, and a reproducibility map (claim → script → data) as appendix.
- **unresolved/figures/fig1–4 (png+pdf; exp_142a_figures.py):** Fig 1 revealed a BONUS visual
  result — plotted against L/ξ_d^cl, the q=7/8/10 Δm·L curves nearly COLLAPSE onto a common
  declining trajectory (the Λ∝ξ law as a scaling collapse) while the q=6 control stays flat.
  Fig 3 shows both plateaus oscillating about 1/4 with the excluded 0.40/0.50 lines. Fig 4
  pairs the two-length decoupling (C(r) with ξ_x=4.3 vs the ξ_d^cl=10.56 marker) with the
  q=5-only shadow anchor (CG curve vs measured effective exponents).

No new physics claims; consolidation only. The manuscript is draft v1 — candidate polish
items for a future pass: bootstrap error bars, BC-dependence study, pinning 1/4 vs 0.213.
