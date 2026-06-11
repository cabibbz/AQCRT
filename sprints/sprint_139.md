# Sprint 139 — Interface-tension test: does the quantum-chain crossover rate obey the exact 2D Potts duality σ_od = 1/(2ξ_d)?

**Date:** 2026-06-10
**Thread:** Walking crossover (S136→137→138). The S138 bonus observation: ξ/Λ_Dm = 0.41, 0.40,
0.37 at q=7, 8, 10 — nearly constant. This sprint asks WHAT that constant is.

## Exact theory anchor (literature)
For the 2D classical Potts model at the first-order transition (q>4), duality + complete
wetting give the EXACT order-disorder interface tension (Borgs–Janke 1992):
    **2 σ_od(q) = 1/ξ_d(q)**,  verified by MC at q=10 (2σ_od = 0.094701 = 1/10.56).
For the QUANTUM chain at its first-order transition with OPEN BC, the avoided-crossing gap
between the disordered state and the symmetric ordered combination should close through a
single order-disorder interface sweeping the chain: Δ_min ~ (prefactor) · e^{−σ L} with
σ = σ_od in the asymptotic regime L ≫ ξ (cf. Campostrini–Nespolo–Pelissetto–Vicari 1410.8662
for the BC-dependence of first-order quantum Potts gap scaling).

## Registered hypotheses (BEFORE the new data/fits)
- **H_dual:  σ_∞ · ξ_d = 1/2** — the classical duality transfers to the OBC quantum chain
  (single interface). Our onset values (0.37-0.41) then must FLOW UPWARD with L as the
  power-law prefactor's −(a/L) correction dies away.
- **H_2int:  σ_∞ · ξ_d = 1** — two-interface mechanism (would require the local rate to keep
  rising well past 0.5/ξ).
- **H_onset: σ · ξ ≈ 0.40 asymptotically** — the shadow-decay Λ is itself asymptotic and the
  classical duality does NOT transfer (e.g., genuinely different quantum kink tension).
Discriminators: (i) local decay rate σ_loc(L) = −d ln(Δm·L)/dL for q=10 extended to n=36
(L/ξ = 3.4); under H_dual, σ_loc·ξ must rise from ~0.27 (at L/ξ≈2.5) toward 0.5 with the
characteristic (a+1)·ξ/L correction shape; (ii) a JOINT fit across q = 6,7,8,10 of
ln Δm = ln A_q − a·ln L − (s/ξ_q)·L with SHARED a and s — H_dual says s = 1/2 with one
universal prefactor exponent; AIC-compare s free / s≡0.5 / s≡0.
*(Honest flag: at L/ξ ≤ 3.4 the prefactor exponent a and s partially trade off in a single-q
fit; the multi-q joint structure with ξ varying 15x (incl. the q=6 near-null lever) is what
breaks the degeneracy.)*

## Method
1. Extend the q=10 tail: n = 32, 36 (L/ξ = 3.03, 3.41) with the validated exp_137b harness
   (SPRINT_NO=139; the q=10 series file copied forward to sprint_139b_crossover_q10.json so
   the window planner keeps its priors — top-level provenance documented in the file; the new
   sizes' DB rows carry sprint=139).
2. exp_139a: joint multi-q fit + windowed σ_loc trajectories + AIC verdict.

## Results

### Tail extension (q=10, n=32, 36; L/ξ = 3.03, 3.41)
Heaviest points of the project (3.2 h each, chi=128): Δm = 0.029559 (relres 5.4e-3) and
0.023810 (relres **3.8e-4** — the cleanest large-size fit yet). Δm·L: 1.033 → 0.946 → 0.857.
Im slopes extend the S137 runaway: −2.64, −2.59, **−2.91**.

### The verdict (exp_139a; 32 points, q=6,7,8,10, ξ lever 15x)

| Fit | s = σ·ξ_d | dAIC vs s-free |
|-----|----------|----------------|
| Joint V4 (per-q prefactor, shared s) | 0.284 ± 0.012 | — |
| **V2: s ≡ 1/2 (H_dual, naive duality transfer)** | — | **+135 (joint), +16.8 (q=10 tail-only) — EXCLUDED** |
| V3: s ≡ 0 (pure shadow, no decay) | — | +141 — EXCLUDED |
| q=10 tail-only (n≥16), s free | **0.213 ± 0.035** | — |
| **q=10 tail-only, s ≡ 1/4** | — | **−0.1 — fits as well as free; preferred by parsimony** |

q=10 local decay rate σ_loc·ξ = −ξ·d ln(Δm·L)/dL: rises 0.13 → 0.27 through the crossover and
**FLATTENS at 0.23–0.27 over L/ξ = 2.5–3.4** — where H_dual demands 0.51–0.55 (factor ~2 above
the data, far outside noise). Windowed picture: σ_eff·ξ flows from ~0.40 (crossover onset, the
S137/138 Λ fits) down to ~1/4 asymptotically.

### Interpretation (with the honest caveat)
**The asymptotic gap-decay rate of the OBC quantum Potts chain at its first-order transition is
HALF the exact classical order–disorder interface tension:**
    σ̃ = σ_od / 2 = 1/(4 ξ_d),   i.e.   Δ_min ~ (1/L)·e^{−σ_od L / 2}
(prefactor exponent a ≈ 0.9–1.0 across q). The factor 2 has a natural origin: the gap is a
tunneling matrix ELEMENT (amplitude) between the disordered state and the symmetric ordered
combination, while the classical interface free energy σ_od suppresses the configuration
WEIGHT ∝ |amplitude|² — hence e^{−σ_od L/2} in the amplitude. With Borgs–Janke's exact
2σ_od = 1/ξ_d this predicts σ̃·ξ_d = 1/4, and the tail measurement (0.213±0.035 free;
s≡1/4 AIC-equivalent) agrees.
**Caveat (flagged, not resolved):** the quantum chain is the extreme-anisotropy (τ-continuum)
limit of the classical model; the dimensionless comparison σ̃·ξ_d implicitly uses lattice
units J=1 and the velocity factor v(q=10) is not independently fixed here. The amplitude-factor
reading is the most economical; pinning it requires an independent v measurement (queued).

### Reconciliation with S137/138
The Λ ∝ ξ law (Λ_Dm ≈ 2.5–2.7ξ ⇒ s_onset ≈ 0.37–0.40) describes the crossover ONSET window
(L/ξ ≲ 1.5–2) where the shadow power and the developing exponential mix — that is exactly what
the blind q=7 prediction tested, and it stands. S139 refines the ASYMPTOTIC constant:
Λ_∞(Dm) = 4ξ (σ̃ξ = 1/4). Both are now measured, with the flow between them visible in the
windowed fits.

### Hostile-reviewer checklist
- **Exact anchor:** 2σ_od = 1/ξ_d is exact (duality + complete wetting, Borgs–Janke 1992;
  MC-verified at q=10: 2σ_od = 0.094701 = 1/10.56). Our ξ_d values are the exact ones.
- **Could-have-failed:** s = 1/2 was the registered default (H_dual); the data overruled it at
  dAIC +17/+135 — the test had teeth. The flat local-rate plateau (9 windows) is not a fit
  artifact: it is visible in raw ln(Δm·L) differences.
- **Truncation/method:** n=36 fit relres 3.8e-4; q=6 null control shares the chi ladder (no
  spurious decay); Δm series smooth across chi tiers.
- **Alternative (slow approach to 1/2):** would require σ_loc to keep rising past 0.3 by
  L/ξ=3.4 — it does not (0.26 at the last window). A crossover-function conspiracy that holds
  σ_loc at 1/4 over a full decade of suppression before doubling is not excluded logically but
  has no mechanism; the amplitude factor-2 does.

**POTENTIALLY NOVEL (sharp, exact-anchored):** first measurement of the asymptotic gap-decay
rate of the transverse-field Potts chain at its first-order transition, σ̃·ξ_d = 1/4 =
σ_od·ξ_d/2 (q=10, L/ξ ≤ 3.4), i.e. the quantum avoided-crossing gap decays with HALF the exact
classical order–disorder interface tension — consistent with amplitude-level interface
suppression. No prior quantum-chain measurement of this constant found (CNPV 1410.8662
established the exponential closing; the σ_od/2 identification vs the exact Borgs–Janke value
appears new). Copied to unresolved/.

## Conclusion
The S138 bonus observation is resolved: the near-constant ξ/Λ_Dm ≈ 0.40 was the crossover-onset
value; the asymptotic decay rate settles at σ̃ = 1/(4ξ_d) — half the exact classical interface
tension, the natural amplitude-vs-weight factor. The naive duality transfer (σ̃ξ = 1/2) is
excluded at dAIC +17 (tail-only) / +135 (joint). The walking-crossover arc (S136→139) now has:
a validated estimator, the observed crossover with a null control, a blind-prediction-confirmed
Λ ∝ ξ onset law, and an exact-theory-anchored asymptotic constant.

## Files
- experiments/exp_139a_interface_tension.py (+results/sprint_139_analysis.json)
- results/sprint_139b_crossover_q10.json (S137 series + n=32,36; top-level note documents the
  seeding; new sizes' DB rows sprint=139)
- DB: sigma_xi_product (global, q=0/n=0 sentinel documented in notes); im_gEP_open/
  thermal_gap_min_open/gstar_thermal_open q=10 n=32,36 (sprint 139)

## Literature
- Borgs & Janke (1992): explicit/exact 2D Potts interface tension; 2σ_od = 1/ξ_d via duality +
  complete wetting (MC-verified at q=10: 2σ_od = 0.094701).
- Buffenoir & Wallon (1993): exact ξ_d(q) at the transition.
- Campostrini, Nespolo, Pelissetto, Vicari (1410.8662): FSS at first-order quantum Potts
  transitions (exponential gap closing, BC dependence).
