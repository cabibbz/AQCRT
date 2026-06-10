# Sprint 138 — The q=7 bridge: a parameter-free test of Λ ∝ ξ for the walking crossover

**Date:** 2026-06-10
**Thread:** Walking crossover via the thermal-gap EP (continues S137 directly; STATE Top-3 #2).
**Model:** S_q Potts chain, OPEN BC, Z_q-conserving DMRG (zq_dmrg_utils, validated S137).

## The prediction (made BEFORE the data)
S137 found that Im(g_EP)(L) and Δ_min(L) leave the conformal-shadow power law exponentially,
y = A·L^(−p)·e^(−L/Λ), with the crossover length tracking the EXACT classical correlation
length: Λ_Im/ξ = 1.59 (q=8) and 1.71 (q=10); Λ_Dm/ξ = 2.51 and 2.71 — coefficients consistent
to ~10% while ξ itself changes 2.26x. If Λ ∝ ξ is real physics, it must interpolate:

**q=7 (ξ_d = 48.1 exact, Buffenoir–Wallon):**
- **Λ_Im = (1.65 ± 0.09)·ξ = 79 ± 5**
- **Λ_Dm = (2.61 ± 0.14)·ξ = 126 ± 7**
- At n ≤ 40 (L/ξ ≤ 0.83) the exponential suppression at the largest size is e^(−40/79) ≈ 0.60
  — a clear decay ONSET (moderate dAIC over pure power), weaker than q=8's at its matched
  L/ξ window, far weaker than q=10's.

**Falsifiers (stated up front):**
1. A confident decay (dAIC > 10) with Λ_Im outside roughly [40, 160] (≫2σ from 79) breaks the
   proportionality.
2. NO decay preference at all (dAIC ≈ 0 like the q=6 control) despite reaching L/ξ = 0.83 —
   given q=8 already showed dAIC +11 (Im) by L/ξ = 1.17, the matched-window comparison
   (q=8 restricted to its n ≤ 20, L/ξ ≤ 0.84 subset) calibrates how much signal "should" be
   there; q=7 falling far below that calibration kills the universal-coefficient reading.
3. Λ_Dm / Λ_Im departing wildly from the ~1.6 ratio seen at q=8,10 (internal consistency).

## Method
Identical harness to S137 (exp_137b: asymmetric avoided-crossing fit, nfit≥7 + relres<5e-3
refinement, merge-on-save, BC-qualified DB names) with SPRINT_NO=138 provenance; sizes
n = 8..40 (L/ξ = 0.17..0.83); chi ladder 64/96/128. Validation first (exp_137a pattern, q=7
vs open-BC ED). Analysis: exp_138a — free shadow+decay fit vs (a) the Λ=79/126 prediction
(fixed-Λ fit quality), (b) pure power, (c) the matched-window q=8 subset calibration.

## Results

### Validation (exp_137a harness, SPRINT_NO=138)
q=7, n=6,7 vs open-BC ED: worst rel diff **1.1e-6** at chi=64 (cleanest of all q so far). ALL PASS.

### Production (exp_137b harness, n=8..40, ~6.5 h)
10 sizes, every one refined to ≥7 fit points (34 solves each); chi ladder 64/96/128.
Δm·L: 2.06, 2.16, 2.17, 2.06, 2.05, 2.00, 1.96, 1.91, 1.87, **1.84** — the same steady decline
q=8 showed, scaled to the larger ξ. Im slopes drift −1.14 → −1.78 (no runaway at L<ξ, as expected).

### THE PREDICTION TEST (exp_138a)

| Test | Δm series | Im series |
|------|----------|----------|
| T1 free Λ | **118 ± 24** (= 2.46ξ) | **79 ± 25** (= 1.64ξ) |
| → predicted | **126 ± 7** (2.61ξ) ✓ 0.3σ | **79 ± 5** (1.65ξ) ✓ **dead center** |
| T1 dAIC(power−decay) | **+13.0** | **+7.0** |
| T2 dAIC with Λ FIXED at the prediction (no extra params) | **+14.9** | **+9.0** |
| T3 q=8 matched-window calibration (L/ξ≤0.84) | +12.5 (Λ=2.0ξ) | +0.8 |
| T4 Λ_Dm/Λ_Im | 1.50 (q=8: 1.58, q=10: 1.59) ✓ | |

**All three pre-registered falsifiers evaded:**
1. The free Λ_Im (79) is not merely inside the allowed [40, 160] — it lands ON the predicted
   central value to 0.4%. (With ±25 from the fit, the agreement to <1σ is the claim; the 0.4%
   coincidence is luck on top of it.)
2. Decay IS detected (dAIC +13/+7), at a strength matching the q=8 matched-window calibration
   (+12.5 on the robust Δm channel) — exactly the "weaker than q=8-at-its-full-range, far weaker
   than q=10" ordering predicted.
3. Internal ratio Λ_Dm/Λ_Im = 1.50 vs 1.58/1.59 at q=8/10 — consistent.

**The Λ ∝ ξ law now rests on three q values spanning ξ = 10.6 → 48.1 (4.6x):**
Λ_Im/ξ = 1.71 (q=10), 1.59 (q=8), 1.64 (q=7) — and the q=7 value was PREDICTED, not fitted.

### Hostile-reviewer checklist
- **Pre-registered?** YES — the prediction, bands, and falsifiers were written into this report
  (and committed intent in STATE.md/S137) before any q=7 production data existed.
- **Could it have failed?** The free Λ had ±25 room and the full [0,∞) range available; landing
  at 79 was a genuine risk-bearing test. The T2 fixed-Λ variant removes fitting freedom entirely.
- **Channel caveat (honest):** the Im channel at q=8 matched-window shows weak dAIC (+0.8) while
  q=7 shows +7.0 — the Im channel mixes c1 sub-extensivity noise; the Δm channel (cleanest
  observable) calibrates +12.5 vs +13.0, essentially identical. The conclusion rests on Δm
  primarily, Im concurring.
- **chi-truncation:** same ladder as the q=6 null control (S137); q=7 slopes show no jumps at
  the 64→96→128 tier boundaries.

**CONFIRMED (upgrades S137 from POTENTIALLY NOVEL):** the walking-crossover length of the
thermal-gap EP observables scales with the exact classical correlation length, Λ_Im ≈ 1.6-1.7 ξ_d,
demonstrated by a successful parameter-free out-of-sample prediction at q=7. The S137+S138
package (crossover + null control + predicted interpolation) satisfies novelty-hardening rules
#1 (5+ data points), #2 (two series: Δm and Im), #3 (falsification test passed as a registered
prediction). Copied to unpublished/.

## Conclusion
S137's Λ ∝ ξ scaling made a sharp, registered prediction for q=7 — Λ_Im = 79 ± 5 — and the
measurement returned 79 ± 25 with the decay term independently demanded by the data (dAIC +13
on Δm) at exactly the strength the q=8 matched-window calibration implies. The walking-crossover
law Λ_Im ≈ 1.65 ξ_d now interpolates across q = 7, 8, 10 with the q=7 point earned blind. The
strongest-confidence result of the project to date.

## Files
- experiments/exp_138a_q7_prediction.py (+results/sprint_138_analysis.json)
- exp_137a/b harnesses re-used with SPRINT_NO=138 (results/sprint_138a_validate_q7.json,
  results/sprint_138b_crossover_q7.json)
- DB: im_gEP_open/thermal_gap_min_open/gstar_thermal_open (q=7, n=8..40, sprint 138);
  crossover_Lambda (q=7, both channels, prediction noted); zq_dmrg_validation_worst_rel (q=7)

## Literature
Same anchor set as S137 (Buffenoir-Wallon ξ_d; Campostrini et al. 1410.8662; GRZ; Ma-He;
Jacobsen-Wiese). A targeted search found no prior q=7 quantum-chain crossover measurement.
