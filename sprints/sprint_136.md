# Sprint 136 — Locating the complex-CFT fixed point of the transverse-field S_q Potts CHAIN via the thermal-gap exceptional point

**Date:** 2026-06-03
**Thread:** NEW DIRECTION (pivot from the q=4 χ_F asymptote thread, declared near-closed in S135).
**Model:** S_q Potts chain, H = −Σδ(s_i,s_{i+1}) − g Σ_{k=1}^{q−1} X^k, PERIODIC BC (exact diag).

## Motivation / the pivot
The q=4 χ_F thread (S129–S135) is mature: direction = 2/ν−d = 2.0 (proven via ν=2/3 + Albuquerque),
marginal-operator log detected and isolated from the q=3 control, asymptote unpinnable at accessible L.
STATE.md recommends pivoting. New question, fresh observable, sidesteps the marginal-log swamp.

**The complex-CFT picture (Gorbenko–Rychkov–Zan).** For the 2D Potts model the critical and tricritical
fixed points collide at q=4 and move off into the complex-coupling plane for q>4, becoming a pair of
**complex CFTs** at complex coupling. RG flows pass near them → "walking" → weakly-first-order transition
with a huge but finite correlation length ξ ~ exp(A/√(q−4)). This is established for the **2D classical**
model (GRZ 1808.04380; Jacobsen–Wiese PRL 133 077101 (2024) lattice realization; classical Fisher-zero
literature: zeros sit at finite imaginary distance for q>4).

**The gap (what's new here).** The analog for the **transverse-field quantum chain** — locating the complex
fixed point's *imaginary transverse-field coupling* directly from finite chains — uses the **exceptional
point (EP)** of the thermal (energy, Z_q-charge-0) gap. The charge-0 gap Δ_ε(g) couples to the energy
operator (the coupling/"temperature" direction); its complex-g zero is the quantum analog of a Fisher zero.

**Sharp, falsifiable prediction.** Define Im(g_EP)(L) = the imaginary distance from the real axis to the
nearest complex-g coalescence of the two lowest charge-0 levels. The local log-log slope
−d ln Im(g_EP)/d ln L is an EFFECTIVE thermal exponent 1/ν_eff(L):
- **Continuous (q≤4):** Im(g_EP) ~ L^{−1/ν}; the local slope SETTLES to the exact 1/ν
  (q=2→1.0, q=3→1.2, q=4→1.5 with marginal-log slow approach from below).
- **Walking (q≥5):** at L≪ξ_q the flow passes near the COMPLEX CFT, so Im(g_EP) looks power-law
  ("conformal shadow") with 1/ν_eff ≈ the complex fixed point's Re(1/ν); for L≫ξ_q it must cross over
  toward the first-order behaviour (gap→tunnelling splitting), so the slope does NOT settle — it keeps
  climbing/steepening. ξ_q shrinks as q grows (more strongly first order), so the steepening sets in earlier.
Falsification: if q=2,3 do NOT recover their exact 1/ν, the method is broken. If q=5,6 settle to a clean
constant exactly like q=2,3 (no excess climb), there is no walking signal at accessible L.
*(NOTE: the finite-L gap EP → 0 for every q — power-law for continuous, eventually exponential for
first-order; the walking signature is the SCALING crossover, not a non-zero plateau. Header corrected
post-data from the original γ_q>0 guess.)*

**Bonus (the project-relevant cross-check):** q=4's 1/ν_eff is an INDEPENDENT observable (not χ_F) for the
marginal-operator log — it must climb toward 1.5 from below, mirroring the S129–S135 χ_F marginal-log story.

## Method
- **Thermal gap:** Δ_ε(g,L) = E₁ − E₀ within the Z_q-charge-0 sector. Charge resolved by P = ∏_i X_i
  (cyclic shift on every site); charge-0 ⇔ ⟨v|P|v⟩ ≈ +1. (Charge machinery validated S061.)
- **EP locator (real-axis, robust):** near the gap minimum g*(L), the two levels form a 2-level avoided
  crossing Δ_ε(g) = √(Δ_min² + v²(g−g*)²) ⇒ the complex zero sits at g* ± i·Δ_min/v, i.e.
  **Im(g_EP) = √(Δ_min / Δ_ε″(g*))** (v² = Δ_min·Δ_ε″). Computed from Δ_min and the curvature at the min.
- **Cross-check:** actually diagonalize the complex-symmetric H(g*+iy) and find the y where the two
  charge-0 eigenvalues coalesce (dense, small n). Must match the real-axis estimate.

---

## Results

### Method validation on q=2 Ising (exp_136a, exact, PERIODIC, n=6,8,10)
The real-axis EP estimate Im(g_EP)=√(Δ_min/Δ_ε″) was cross-checked against an actual
complex-symmetric diagonalization H(g*+iy) (the y where the two charge-0 levels coalesce):

| n | g* | Δ_min | Δ_min·L | Im(g_EP) estimate | Im(g_EP) complex-scan |
|---|------|--------|---------|-------------------|------------------------|
| 6 | 0.4330 | 1.0000 | 6.000 | 0.25002 | 0.2438 |
| 8 | 0.4619 | 0.7654 | 6.123 | 0.19139 | 0.1866 |
| 10| 0.4755 | 0.6180 | 6.180 | 0.15457 | 0.1507 |

Real-axis estimate ≡ true EP to ~2% (the residual is the coarse y-grid, ny=41). g*→g_c=0.5,
Δ_min·L→2π (=2πv·x_ε with v=1, x_ε=1), and Im(g_EP)~L^{−1} (local slopes −0.93,−0.95). **Method validated.**

### Im(g_EP)(L) across q (exp_136b, exact, PERIODIC) — the master result
Self-located charge-0 thermal-gap minimum; Im(g_EP)=√(Δ_min/Δ_ε″); GPU eigsh to dim≈2M.

| q | g_c | n-range | dim_max | EP power-fit p | exact 1/ν | last local slope | R² |
|---|-----|---------|---------|----------------|-----------|------------------|-----|
| 2 | 0.5000 | 6–11 | 2,048 | **0.946** | 1.000 | −0.961 | 0.9999 |
| 3 | 0.3333 | 5–12 | 531k | **1.173** | 1.200 | −1.189 | 1.0000 |
| 4 | 0.2500 | 5–10 | 1.05M | **1.354** | 1.500 | −1.369 | 1.0000 |
| 5 | 0.2000 | 4–9 | 1.95M | 1.505 | — | −1.537 | 0.9999 |
| 6 | 0.1667 | 4–8 | 1.68M | 1.648 | — | −1.686 | 0.9999 |
| 7 | 0.1429 | 4–7 | 823k | 1.775 | — | −1.814 | 0.9999 |

**1. Validation (q=2,3):** the EP estimator's local slope converges from below to the EXACT 1/ν —
q=2 → 1.0 (−0.96 at n=11, still rising), q=3 → 1.2 (−1.189, decelerating onto 1.2). This is a NEW,
g_c-assumption-free, χ_F-independent route to the thermal exponent 1/ν, validated on the two exactly-known
continuous Potts cases. (Δ_min·L is the CFT-constant 2πv·x_ε: q=2→6.28, q=3→4.50.)

**2. q=4 — independent confirmation of the marginal-operator log (project-relevant):** the EP exponent
climbs MONOTONICALLY from below toward 1/ν=1.5 (local slope 1.336→1.350→1.359→1.366→1.369; power-fit
p=1.354), undershooting 1.5 exactly as a marginal (dilution) operator demands. Δ_min·L drifts DOWN
3.681→3.494 (the same marginal-log signature). This reproduces — in a COMPLETELY DIFFERENT observable
(the complex-coupling EP of the thermal gap, vs the fidelity susceptibility) — the central S129–S135
finding that q=4's finite-size exponents sit below their asymptote because of the marginal log. Two
independent observables now agree (novelty-hardening rule #2).

**3. Walking q=5,6,7 — the complex-CFT "conformal shadow":** at L≪ξ_q the flow passes near the complex
CFT, so Im(g_EP) looks power-law with an effective 1/ν_eff that rises smoothly across the q=4 boundary:
1.51 (q5), 1.65 (q6), 1.78 (q7), still CLIMBING with L (slopes do not settle, unlike q=2,3). The climb is
steeper and more persistent for larger q (ξ_q shrinks → the crossover toward the first-order/exponential
regime sets in earlier). This is the quantum-chain echo of the GRZ complex fixed point: the thermal
exponent continues smoothly and analytically through q=4 into the walking regime. Δ_min·L declines
increasingly fast with q (q5: 3.18→2.83, q7: 2.46→2.09) — the gap closing faster than 1/L, the
shadow-CFT precursor of the first-order crossover.

**4. No spurious plateau:** a 3-parameter saturating fit Im(g_EP)=γ+A·L^{−p} returns γ=0 (±1e-3) for
EVERY q — Im(g_EP)→0 at accessible L for all q, as it must (the finite-L gap EP vanishes for both
continuous and first-order; the walking signature is the SCALING crossover, not a non-zero plateau).
So the definitive walking test — Im(g_EP)'s power-law→faster crossover at L≳ξ — is NOT reachable by
exact diag for q=5 (ξ>12 sites, KNOWLEDGE_ARCHIVE). It needs DMRG to L≫12 (charge-0 excited state in a
Z_q-conserving MPS) — the clear next step.

### Hostile-reviewer checklist
- **Apples to apples?** Every q measured with the identical code/BC/estimator/charge filter. ✓
- **Non-trivial data points?** q=2,3 are validation (exact ν). The could-have-failed cases that did NOT:
  q=4 climbing toward 1.5-from-below (marginal log) — independent of χ_F; q=5,6,7 a smooth, monotone
  continuation across the q=4 boundary. 4 non-trivial points (q=4 cross-check + 3 walking).
- **Literature for THIS observable?** Complex CFTs/Fisher zeros for Q>4 Potts are established for the **2D
  classical** model (GRZ 1808.04380; Jacobsen–Wiese PRL 133 077101 (2024); classical Fisher-zero lit). The
  **transverse-field quantum-chain** thermal-gap exceptional-point estimator of 1/ν / the complex-coupling
  location was NOT found. Modest/methodological novelty.
- **Anyone claim the opposite?** No.
- **Finite-size / simpler alternative?** YES, acknowledged: q≥5 values are EFFECTIVE (L<ξ, the conformal
  shadow); we do NOT claim asymptotic walking exponents nor a located complex fixed point. The q≤4
  recover the exact ν, anchoring the method.

**POTENTIALLY NOVEL (modest / methodological):** a thermal-gap exceptional-point estimator of the thermal
exponent 1/ν for the transverse-field S_q Potts chain — Im(g_EP)=√(Δ_min/Δ_ε″) from the charge-0 gap —
validated to recover exact 1/ν at q=2 (1.0) and q=3 (1.2), giving an INDEPENDENT (non-χ_F) confirmation of
the q=4 marginal-operator log (1/ν_eff climbs to 1.5 from below), and mapping a smooth 1/ν_eff(q) across
the q=4 continuous→walking boundary (the complex-CFT conformal shadow). No prior quantum-chain EP
measurement of this was found. Copied to unpublished/.

### What this sprint does and does NOT establish
- **DOES:** introduce + validate (vs exact ν at q=2,3, and vs a true complex-g diagonalization at q=2) a
  new EP/complex-coupling estimator of 1/ν; give an independent observable confirming the q=4 marginal log;
  map 1/ν_eff(q) continuously across q=2..7.
- **Does NOT:** reach the walking saturation/crossover (needs L≫ξ via DMRG); locate the complex fixed point
  in the complex-g plane to thermodynamic precision; claim asymptotic exponents for q≥5.

## Conclusion
A pivot from the q=4 χ_F thread to a fresh observable — the exceptional point of the Z_q-charge-0 thermal
gap in the complex transverse-field plane. The real-axis estimate Im(g_EP)=√(Δ_min/Δ_ε″) is validated
against a true complex-symmetric diagonalization (q=2, ~2%) and recovers the exact thermal exponent 1/ν at
q=2 (1.0) and q=3 (1.2). At q=4 it climbs to 1.5 from below — an independent (non-χ_F) confirmation of the
marginal-operator log that the whole S129–S135 thread established with the fidelity susceptibility. For
q=5,6,7 (walking) it gives a smoothly rising effective 1/ν_eff (1.51, 1.65, 1.78) — the conformal shadow of
the GRZ complex fixed point continued analytically through q=4. The definitive walking crossover
(power-law→faster) sits beyond the exact-diag frontier (ξ>12); reaching it via Z_q-conserving DMRG is the
clean next experiment.

## Files
- experiments/exp_136a_thermal_gap_validate_q2.py (validation + complex cross-check)
- experiments/exp_136b_thermal_gap_imEP.py (production, q=2..7), exp_136_analysis.py
- results/sprint_136a_validate_q2.json, sprint_136b_imEP_q{2..7}.json, sprint_136_analysis.json
- DB: im_gEP, thermal_gap_min, gstar_thermal (q=2..7, per n); imEP_exponent (power-fit p per q)

## Literature (sources)
- V. Gorbenko, S. Rychkov, B. Zan, *Walking, Weak first-order transitions, and Complex CFTs II.
  Two-dimensional Potts model at Q>4*, SciPost Phys. 5, 050 (2018), arXiv:1808.04380.
- J. L. Jacobsen & U. Wiese, *Lattice Realization of Complex CFTs: 2D Potts model with Q>4*,
  PRL 133, 077101 (2024).
- Classical Fisher-zero literature for the Q-state Potts model (zeros at finite imaginary distance for Q>4).
- Albuquerque, Alet, Sire & Capponi, PRB 81, 064418 (2010) — per-site χ_F density ~ L^{2/ν−d} (the
  sister observable; this sprint cross-checks the q=4 marginal log it could not pin).


---

## AUDIT ADDENDUM (2026-06-09) — read before citing this sprint
A 48-agent system audit (sprints/audit_2026-06-09.md) verified the numbers but corrected two framings:
1. **"Two INDEPENDENT observables agree" is near-tautological.** The thermal-gap EP and on-peak
   chi_F are dominated by the SAME single epsilon multiplet: the 2-level identity
   chi_F^peak x Im(g_EP)^2 ~ const holds to ~2% across q and n, so agreement with the S129-135
   chi_F story was expected BY CONSTRUCTION. Correct framing: a second ESTIMATOR of the same
   low-energy eps-gap physics; the product-constancy itself (single-multiplet dominance) is the
   clean quantitative result. Genuine independence requires a non-spectral observable.
2. **q=4 "climbs exactly as a marginal operator demands" overstates discrimination.** 4-6 sizes
   cannot distinguish s/lnL from generic L^-omega drift. Controlled statement: the undershoot at
   matched n is 8.7% (q=4) vs 3.9%/0.9% (q=2/q=3 controls) -- 2-9x larger, CONSISTENT with the
   marginal log. Falsifier at DMRG sizes: slope must follow 1.5 - c/lnL (pass ~1.44 by L~30).
3. Minor: "sat-fit gamma=0 (+-1e-3) for EVERY q" -- gamma is pinned at the fit lower bound and
   the q=2 error is +-0.013; the honest statement is "no detectable plateau".
4. **Planning correction:** "xi>12 for q=5" was only a lower bound. Exact classical values:
   xi_d(5)=2512, xi_d(6)=159, xi_d(7)=48, xi_d(8)=24, xi_d(10)=10.6 -- the q=5,6 DMRG crossover
   hunt proposed in the conclusion is UNREACHABLE at n<=40; retargeted to q=8-10 (Sprint 137).
   Also fixed in code: gap_curve diagonalized twice per g-point; edge-clamped minima now raise.
