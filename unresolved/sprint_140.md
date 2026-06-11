# Sprint 140 — The velocity test: which length does the gap-decay rate actually know about?

**Date:** 2026-06-11
**Thread:** Closes the S139 caveat. S139 measured the asymptotic gap decay σ̃·ξ_d^cl = 1/4
(q=10), using the CLASSICAL isotropic ξ_d^cl = 10.56. But the quantum chain (τ-continuum,
anisotropic limit) has its OWN spatial correlation length ξ_x, which need not equal ξ_d^cl in
lattice units. The dimensionless quantum duality statement must use ξ_x.

## Registered hypotheses (BEFORE the data)
Both reproduce S139's σ̃·ξ_d^cl = 1/4; they are distinguished ONLY by the measured ξ_x:
- **H_A (amplitude factor): ξ_x ≈ ξ_d^cl ≈ 10.6 sites.** Then σ̃ = 1/(4ξ_x): the duality
  transfers at the AMPLITUDE level (gap = matrix element; weight ∝ amplitude² carries the
  classical σ_od = 1/(2ξ)).
- **H_B (quantum-ξ duality): ξ_x ≈ 2ξ_d^cl ≈ 21 sites.** Then σ̃ = 1/(2ξ_x): the NAIVE duality
  holds with the proper quantum length — no amplitude factor; S137/138's success with ξ_d^cl
  was a constant-factor-2 alias (Λ_Im = 1.65ξ_d^cl would really be 0.83ξ_x).
Falsifier for both: ξ_x far from both 10.6 and 21 → report the measured dimensionless
σ̃·ξ_x and flag the duality interpretation as open.

## Method
1. **exp_140a (primary): direct ξ_x** from the disordered-branch correlation function at the
   transition coupling g_c = 1/q = 0.1 (exact, self-dual). Z_q-DMRG ground state (charge-0,
   warm init = field-aligned product state → converges onto the disordered branch even amid
   the tower near-degeneracy; verified by the correlation tail) on open chains n = 48, 64;
   C(r) = <Z1_i Z1d_j> between bulk sites (window n/4..3n/4). Fits: pure exponential AND the
   2D Ornstein-Zernike form C ~ e^{−r/ξ}/√r (the correct massive 2D asymptotics). Also g =
   0.103, 0.106 for smoothness/robustness of ξ_x(g→g_c).
2. **exp_140b (cross-check): velocity from the magnon dispersion.** Periodic ED at q=10, n=6
   (dim 1M, GPU): momentum-resolved low spectrum (translation operator T; charge filter P);
   charge-±1 magnon band E(k); fit E(k)² = Δ_d² + 4v²sin²(k/2) → v, Δ_d; ξ_x^ED = v/Δ_d.
   Run at g = 0.105 (clearly disordered side at n=6; v varies smoothly).

## Results

### exp_140a — direct ξ_x (Z_q-DMRG correlator, disordered branch, OZ-corrected)
| g | ξ_OZ (n=48) | ξ_OZ (n=64) | note |
|---|---|---|---|
| 0.100 (= g_c) | 4.32 | 4.33 | local-ξ drift 2.8→3.9 (tower admixture at exact coexistence → treat as UPPER estimate) |
| 0.103 | 2.17 | 2.15 | clean (drift 1.8→2.0) |
| 0.106 | 1.67 | 1.65 | clean |

Size-converged to 1%. **ξ_x(q=10, disordered branch, at the transition) ≲ 4.3 sites**
(2.2 at the nearest clean point).

### exp_140b — dispersion cross-check (charge-resolved periodic ED, n=6, g=0.105)
Charge-1 block built exactly in the Fourier basis (the plain ⟨P⟩-filter approach fails at
g≈g_c — Lanczos mixes the near-degenerate ordered tower across charge sectors; lesson logged).
Ordered-tower intruder identified by field expectation and excluded. Magnon band:
E(k) = 0.707, 0.742, 1.176 at k = 0, π/3, 2π/3 — **nearly flat at small k** (deep first-order
disordered phase ≈ product state at g=0.1), so the relativistic ξ=v/Δ estimator is unreliable
here; it gives ~0.9, consistent in order with (and below) the authoritative correlator value.

### VERDICT: both registered hypotheses REFUTED
- H_A (ξ_x ≈ ξ_d^cl = 10.6): **NO** — measured ≲ 4.3.
- H_B (ξ_x ≈ 2ξ_d^cl = 21.1): **NO** — off by ≥ 5x.
- The dimensionless products with the QUANTUM length: σ̃·ξ_x ≈ 0.0237 × (2.2–4.3) =
  **0.05–0.10** — no distinguished value (not 1/2, not 1/4).

### What this means (the real finding)
1. **The S139 interpretation is DOWNGRADED.** "σ̃ = σ_od/2 because amplitude vs weight" was a
   units-blind reading: it compared the quantum per-site decay rate against the classical
   per-lattice-unit tension as if the two models shared a length normalization. S140 shows
   they do not (ξ_x/ξ_d^cl ≈ 0.2–0.4). The numerical identity σ̃ = σ_od^cl/2 (0.02367 vs
   0.02368 — eerily exact) currently has NO units-consistent derivation and must be treated
   as possibly numerological until the q=8 asymptotic universality check (does
   σ̃(q=8)·ξ_d^cl(8) = 1/4 too?) — now the decisive queued experiment.
2. **What survives untouched:** the cross-q empirical laws — crossover onset Λ_Im =
   (1.65±0.09)·ξ_d^cl(q) (blind-confirmed at q=7) and the q-ordering of all coexistence
   phenomenology by the exact classical ξ_d. These are statements about the quantum-classical
   correspondence of INTERFACE/coexistence physics, not about the quantum chain's own
   correlation lengths.
3. **New sharp puzzle (worth a thread):** at this strongly-first-order transition the quantum
   chain carries (at least) two distinct lengths: a microscopic spin correlation length
   ξ_x ≈ 2–4 sites, and a coexistence/tunneling length Λ ≈ 17 sites ≈ 4–8× ξ_x that tracks
   the CLASSICAL ξ_d(q). In the classical model these are LOCKED by duality+wetting
   (σ_od·ξ_d = 1/2); in the quantum chain they demonstrably decouple. Why the classical ξ_d
   still organizes the quantum tunneling so precisely (10% across 4.6x in ξ) is open.

### Hostile-reviewer checklist
- Registered hypotheses, both falsified — the test was real and the outcome was the
  unanticipated third branch; reported as such rather than rescued.
- ξ_x is measured two ways (correlator: authoritative, size-converged n=48→64; dispersion:
  order-consistent with a flat-band caveat) and at three couplings (smooth, monotone).
- The exact-g_c value carries a stated tower-admixture caveat (drift) — the verdict needs only
  the order of magnitude, which is unambiguous.

**Status: the S136–139 arc's empirical laws stand; the S139 duality INTERPRETATION is retracted
to "open question" pending the q=8 universality check.** Copied to unresolved/.

## Conclusion
The velocity test did its job by failing both ways: the quantum chain's own correlation length
(≲4.3 sites) supports neither the amplitude-factor nor the rescaled-duality reading of
σ̃·ξ_d^cl = 1/4. The S139 number survives as an exact-looking empirical coincidence at one q;
whether it is a law is now a single decisive experiment away (q=8 asymptotic tail → does
σ̃·ξ_d^cl = 1/4 recur?). The deeper finding is the two-length structure of the quantum
first-order point — microscopic ξ_x decoupled from the classical-ξ_d-governed tunneling scale.

## Files
- experiments/exp_140a_xi_correlation.py (+results/sprint_140a_xi_q10.json)
- experiments/exp_140b_magnon_dispersion.py (+results/sprint_140b_dispersion_q10.json)
- DB: xi_x_disordered (n=48,64 at g_c), v_magnon, gap_disordered, xi_x_from_vgap (sprint 140)

## Literature
Buffenoir-Wallon (exact ξ_d^cl); Borgs-Janke (exact σ_od, 2σ_od=1/ξ_d — classical);
CNPV 1410.8662 (quantum first-order gap FSS). The two-length decoupling at the quantum
first-order point did not surface in targeted searches (S137-139 rounds).
