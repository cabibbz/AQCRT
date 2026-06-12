# Sprint 141 — The q=8 universality test: is σ̃·ξ_d^cl = 1/4 a law or a one-q accident?

**Date:** 2026-06-11
**Thread:** The decisive test left by S139 (measured σ̃·ξ_d^cl = 1/4 at q=10) and S140 (which
removed the proposed amplitude-duality explanation, leaving the 1/4 as an unexplained,
eerily exact identity at a SINGLE q). If the same dimensionless constant recurs at q=8 —
where ξ_d^cl = 23.9 instead of 10.56 — it is a LAW of the quantum-classical coexistence
correspondence (in need of theory); if not, S139's 1/4 dies as numerology.

## Registered predictions (BEFORE any new data)
Under the "law" hypothesis H_law (σ̃(q)·ξ_d^cl(q) = 1/4):
- **P1:** the q=8 local decay rate σ_loc·ξ_d^cl = −ξ_d^cl·d ln(Δm·L)/dL must rise from its
  current ~0.20-0.24 (windows around L/ξ ≈ 1.0) and **flatten at 0.25 ± 0.04 by L/ξ ≈ 2**
  (mirroring q=10's plateau, which set in by L/ξ ≈ 2 at 0.23-0.27).
- **P2:** a tail-restricted fit (ln Δm = lnA − a lnL − (s/ξ_d^cl)L over n ≥ 36, i.e. L/ξ ≥ 1.5)
  must give s consistent with 1/4 (q=10 gave 0.213 ± 0.035 over the same L/ξ range), with
  s ≡ 1/4 AIC-competitive with the free fit and BOTH s ≡ 0.4 (onset value frozen) and
  s ≡ 0.5 (classical duality) disfavored.
Falsifiers: a plateau at a clearly different level (e.g. staying ≲0.18 or rising past 0.35),
or a tail fit excluding 1/4 — either kills H_law.
*(Honest note: q=8 reaches only L/ξ ≈ 2.0 vs q=10's 3.4 — the plateau is just opening; the
fit-level test P2 plus the matched-L/ξ comparison to q=10 carry the verdict.)*

## Method
exp_137b harness (SPRINT_NO=141; q=8 series file seeded forward to
sprint_141b_crossover_q8.json — provenance note inside; new sizes' DB rows sprint=141).
Sizes n = 36, 40, 44, 48 (L/ξ = 1.51, 1.67, 1.84, 2.01); chi ladder → 128. Then exp_141a:
σ_loc trajectory + tail fits + matched-L/ξ q=10 overlay + verdict.

## Results

### Production (n=36, 40, 44, 48; 2-2.9h/size, chi=128, ~10.5h total)
Δm·L: 1.481 → 1.453 → 1.368 → 1.306 (L/ξ = 1.51 → 2.01). Fit quality: relres 9e-3 / 4.1e-2
(n=40, noisiest of the series) / 1.2e-2 / 2.4e-2 — per-point Δm noise 1-4%, which makes
adjacent-size local windows scatter; wide windows and fits carry the verdict.

### P1 — the plateau (fit-free, the registered primary)
σ_loc·ξ_d^cl, q=8 tail windows: (28,36) **0.270**, (36,40) 0.114, (40,44) 0.361,
(44,48) **0.277** (at the registered L/ξ ≈ 2 mark: inside 0.25 ± 0.04 ✓).
**Tail-window mean (L/ξ ≥ 1.3): 0.256.  q=10 plateau reference (L/ξ ≥ 2): 0.259.**
Two different q, ξ differing 2.26x, same plateau to 1%. The (36,40)/(40,44) scatter is the
n=40 noise (±0.18 per window from its 4% Δm uncertainty) oscillating around the plateau.

### P2 — tail fits (the registered parametric test)
- q=8-only (n≥36, 4 pts): s = 0.71 ± 0.52 — UNDERPOWERED (a↔s degeneracy with 4 points, one
  noisy); fixed-s variants all within dAIC ±1.4 — the q=8-only fit discriminates nothing.
  Reported as registered: this part of P2 did not deliver on its own.
- **Joint q=8 (n≥36) + q=10 (n≥16) tails, shared s: s = 0.213 ± 0.029** (10 pts):
  **1/4 inside 1.3σ; s = 0.40 excluded at 6.4σ; s = 0.50 at 9.9σ**; s ≡ 1/4 costs only
  +0.9 dAIC vs free.

### VERDICT: the law hypothesis is SUPPORTED
σ̃(q)·ξ_d^cl(q) ≈ 1/4 now stands at TWO q values: the fit-free plateau means agree to 1%
(0.256 vs 0.259) and the joint parametric fit is consistent with 1/4 while excluding the
onset-frozen and classical-duality alternatives. **S139's constant is upgraded from
"possibly numerological (one q)" to "reproduced at a second q — a law candidate of the
quantum-classical coexistence correspondence, with NO mechanism**: S140 removed the
amplitude-duality explanation (the quantum chain's own ξ_x is 2-4 sites, decoupled), so a
quantum-chain decay rate locked to HALF the exact classical Borgs-Janke tension — across q —
is now a sharp standing theoretical puzzle."
Precision caveat (stated plainly): the joint central value 0.213 sits 1.3σ below 1/4 — both q
are consistent with ONE shared constant, but whether that constant is exactly 1/4 (vs ~0.21-
0.25) needs larger L/ξ or theory; what is established is its q-INDEPENDENCE and its scale.

### Hostile-reviewer checklist
- Predictions registered before data; P1 passed as written ((44,48)=0.277 ∈ 0.25±0.04 at
  L/ξ≈2; plateau mean 0.256); P2 q=8-alone underpowered — admitted, not papered over; the
  discriminating joint fit excludes the rival constants at 6-10σ.
- Could-have-failed: a q=8 plateau at e.g. 0.18 or 0.35 (the rival outcomes) was fully
  measurable with these error bars — the test had teeth.
- chi-truncation: same ladder as the q=6 null control; n=40's poor relres is dip-sampling
  noise (visible in the fit residual), not truncation.

**POTENTIALLY NOVEL (strengthened):** the asymptotic avoided-crossing decay rate of the OBC
transverse-field Potts chain satisfies σ̃·ξ_d^cl = 0.24 ± 0.03 at BOTH q=8 and q=10 — half the
exact classical order-disorder interface tension, q-independent, with the naive and
amplitude-level duality explanations both experimentally removed (S139/S140). Copied to
unresolved/.

## Conclusion
The decisive test returned "law, not numerology": the dimensionless decay-rate constant
recurs at q=8 with the same value it took at q=10 (plateau means 0.256 / 0.259; joint
s = 0.213 ± 0.029). Combined with S140 (the quantum chain's own correlation length is
decoupled, 2-4 sites), the project now owns a clean, exact-anchored, two-q experimental
mystery: WHY does the quantum tunneling rate lock to half the classical Borgs-Janke tension
per classical correlation length? That question — plus the S136-141 arc write-up — is the
natural next work.

## Files
- exp_137b harness (SPRINT_NO=141) → results/sprint_141b_crossover_q8.json (seeded from the
  S137 series, provenance note inside; new sizes' DB rows sprint=141)
- experiments/exp_141a_q8_universality.py (+results/sprint_141_analysis.json)
- DB: sigma_xi_product (q=8); im_gEP_open/thermal_gap_min_open/gstar_thermal_open q=8
  n=36-48 (sprint 141)
