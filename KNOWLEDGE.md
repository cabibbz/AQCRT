# Accumulated Knowledge — Edit by topic, not by sprint

*(Detailed findings & closed threads: KNOWLEDGE_ARCHIVE.md. Last 10 sprints: CHANGELOG.md.
A 48-agent system audit (2026-06-09) verified the pipeline and HEDGED three interpretive
claims — hedges are inline below; full audit report: sprints/audit_2026-06-09.md.)*

## Open Items — Check each sprint, remove when done
- **Hardware validation** — 580s QPU unused for ~90 sprints (BLOCKED: ~/.qiskit/qiskit-ibm.json
  empty; needs human to restore token). Strongest prediction: q=2 Ising χ_F at g_c on 5-10 qubits.
- **~~Walking crossover via Z_q-conserving DMRG~~ DONE (Sprint 137) — CROSSOVER OBSERVED.**
  Exponential decay term required at q=8 (dAIC +17, Λ_Im=1.59ξ) and q=10 (dAIC +37, Λ_Im=1.71ξ);
  q=6 control needs none. **Λ ∝ ξ_d (exact: 158.9/23.9/10.56 for q=6/8/10)**. See S137 block below.
- **~~Jacobsen-Wiese comparison~~ DONE (Sprint 137):** Re(1/ν_complex) = 1.534/1.563/1.588/
  1.609/1.646 (q=5/6/7/8/10; den Nijs continuation, validated exact on Q≤4). Measured effective
  1/ν matches ONLY at q=5 (1.505, −1.9%); q=6,7 rise PAST it (+5.4%/+11.8%) toward d=2 —
  **"conformal shadow" language is quantitatively licensed only for q=5.**
- **~~S135 rigor gap~~ CLOSED (Sprint 137d):** chi-doubling 48→96 at n=24: q=3 rel 3.1e-8,
  q=4 rel 5.0e-5 — the S135 production values were fully converged.
- **~~q=7 Λ prediction test~~ DONE (Sprint 138) — CONFIRMED, dead center.** Registered
  Λ_Im=79±5 / Λ_Dm=126±7; measured 79±25 / 118±24, decay independently demanded (dAIC +13/+7),
  fixed-at-prediction fit beats pure power with zero free Λ (+14.9/+9.0). Λ_Im≈1.65ξ_d spans
  q=7,8,10 (ξ 4.6x range) with the q=7 point earned blind.
- **~~Interface-tension identity~~ RESOLVED (Sprint 139):** the 0.40 was the crossover-ONSET
  value; the ASYMPTOTIC decay rate (q=10 to L/ξ=3.4) is **σ̃·ξ_d = 1/4 = σ_od·ξ_d/2** —
  naive duality transfer (1/2) excluded dAIC +17(tail)/+135(joint); s≡1/4 AIC-equivalent to
  free. Reading: gap = tunneling amplitude ⇒ Δ ~ (1/L)e^{−σ_od L/2}, σ_od exact (Borgs-Janke
  2σ_od=1/ξ_d). Caveat: velocity/anisotropy factor not independently fixed → next item.
- **~~Velocity v(q=10)~~ DONE (Sprint 140) — BOTH readings refuted; S139 interpretation
  downgraded.** Direct ξ_x(q=10 at g_c) ≲ 4.3 sites (OZ correlator, size-converged) — not
  ξ_d^cl=10.6 (amplitude reading) nor 21 (rescaled duality). σ̃·ξ_x = 0.05-0.10, no special
  value. **σ̃ = σ_od^cl/2 stands as an unexplained numerical identity at ONE q.** New puzzle:
  TWO decoupled lengths at the quantum first-order point (microscopic ξ_x = 2-4 sites vs
  tunneling Λ ≈ 17 sites ∝ classical ξ_d) — classically locked by duality+wetting, quantum-side not.
- **~~q=8 universality check~~ DONE (Sprint 141) — THE CONSTANT RECURS. Law, not numerology.**
  Plateau means: q=8 (L/ξ≥1.3) = 0.256 vs q=10 (L/ξ≥2) = 0.259 — same to 1% across ξ 2.26x;
  joint shared-s tail fit = 0.213±0.029 (1/4 in 1.3σ; 0.40 out 6.4σ; 0.50 out 9.9σ).
  q=8-only fit underpowered (admitted). Whether the shared constant is EXACTLY 1/4 is open;
  q-independence + scale established. **Standing theory puzzle:** quantum tunneling rate =
  half the exact classical Borgs-Janke tension per CLASSICAL ξ_d, mechanism unknown
  (amplitude/naive duality both removed S139/S140; quantum ξ_x decoupled).
- **Theory probe (next):** measure the quantum chain's OWN order-disorder interface free
  energy directly (fixed-BC DMRG energy excess) → compare σ_interface^quantum vs σ̃ vs σ_od^cl.
- **ξ_x(q) mini-survey** (cheap): exp_140a at q=7,8 — is ξ_x ∝ ξ_d^cl with a small coefficient,
  or q-flat? Distinguishes uniform compression vs genuine decoupling.

## Five Entanglement Archetypes
| Archetype | Example | MI pattern | I3 sign | Negativity | Source |
|-----------|---------|-----------|---------|------------|--------|
| Democratic | GHZ, Ising ordered | Uniform high | +1 (redundant) | Flat | Sprint 005 |
| Distributed | W state | Uniform weak | +0.2 (weak redundant) | Growing with cut | Sprint 005 |
| Geometric | Cluster 1D | Nearest-neighbor only | -1 (irreducible) | Explosive, geometry-dependent | Sprint 007 |
| Topological | Toric code | Non-contractible loops | 0 (zero everywhere) | Uniform floor | Sprint 020 |
| Scale-Free | Critical TFIM | Power-law decay | Mixed | Highest rank, steep decay | Sprint 029 |

## Four Levels of Entanglement Description
1. **Scalar** (entropy) — amount. 2. **Correlation** (MI, I3) — topology; I3<0 = irreducible.
3. **Spectral** (eigenvalues of ρ_A) — symmetry content. 4. **Hamiltonian** (H_E) — locality.

## ⚠ Model Identity (Audit April 2026) — TWO MODELS WERE STUDIED
| Model | Coupling | Field | Symmetry | Sprints | q>4 transition |
|-------|----------|-------|----------|---------|----------------|
| S_q Potts | δ(s_i,s_j) | Σ_{k=1}^{q-1} X^k | S_q | **076-now** | Weakly 1st-order (walking) |
| Potts-clock hybrid | δ(s_i,s_j) | X + X† | Z_q | 033-075 | Continuous 2nd order |

S_q Potts (g_c=1/q exact, Kramers-Wannier) is the SAME model as GRZ / Ma-He / Tang / Jacobsen-Wiese
— the model is not novel; our *probes* may be. For q=2,3 all variants coincide. DB model names are
canonical: `sq_potts`, `hybrid`, `hybrid_2d` (migrated 2026-06-09; db_utils canonicalizes on write).

## Standing claims, q=4 χ_F thread (S129-136, audit-hedged; details in ARCHIVE)
- **Convention (proven):** per-site χ_F leading exponent at a QCP is 2/ν−d (Albuquerque PRB 81
  064418); our q=2,3 anchors reproduce their exact nulls 1.0 / 1.4. Golden gate enforces.
- **ν(q=4):** calibrated collapse gives 1/ν = 1.45-1.49 at n≤10 — **consistent with the exact
  den Nijs ν=2/3 and excluding ν≥5/6**; no error bar, and the 2.0 asymptote ultimately rests on
  the exact literature ν. (Hedged from "ν=2/3 CONFIRMED from our own data".)
- **S134 (solid):** fixed-g_c vs on-peak artifact resolved; on-peak κ_eff ascends toward 2.0 for
  both BC, validated against exact nulls at q=2,3. The standard estimator shows NO sub-2 plateau.
- **S135 (hedged):** q=4 on-peak χ_F (DMRG, n≤24) shows a **0.30 deficit vs its null that the
  q=3 control does not** — consistent with the predicted marginal (c=1, dilution) log GIVEN the
  independently-fixed 2.0 asymptote; NOT a model-independent log detection (no-log K=1.70 fits
  equally well; s = −1.3..−1.8 parametrization-dependent).
- **S136 (hedged):** thermal-gap EP estimator Im(g_EP)=√(Δ_min/Δ″) recovers exact 1/ν at q=2,3
  (p=0.95/1.17) — a clean NEW estimator. But it is **NOT independent of χ_F**: both are dominated
  by the same ε multiplet; χ_F^peak·Im(g_EP)² ≈ const (~2%) ties them by construction. The
  product-constancy itself = single-multiplet dominance, the real quantitative result. q=4
  undershoot (8.7% at matched n) is 2-9x the no-marginal-op controls (q2 3.9%, q3 0.9%) —
  consistent with, not uniquely demonstrating, the marginal log. Falsifier at DMRG sizes: slope
  must follow 1.5−c/lnL (pass ~1.44 by L~30), not saturate near 1.40.
- **Walking q=5,6,7 (S137-resolved):** S136's effective 1/ν_eff = 1.51/1.65/1.78. The S137
  Coulomb-gas comparison shows q=5 matches Re(1/ν_complex)=1.534 (genuine shadow; ξ≈2500) while
  q=6,7 already exceed theirs (1.563/1.588) — crossover-contaminated even at L/ξ ~ 0.05-0.15.
- **S139 — asymptotic gap decay σ̃·ξ_d^cl = 1/4 at q=10 (MEASURED; interpretation OPEN per
  S140):** σ_loc·ξ_d^cl flattens at 0.23–0.27; tail s=0.213±0.035; s≡1/4 parsimony-preferred;
  s≡1/2 excluded (+16.8). The "amplitude ⇒ σ_od/2" reading was units-blind (S140 addendum):
  the numerical identity σ̃=0.02367 vs σ_od^cl/2=0.02368 is unexplained, one-q. The S137/138
  Λ∝ξ law = onset regime; asymptotic Λ_∞(Dm)=4ξ_d^cl. unresolved/sprint_139.md.
- **S141 — σ̃·ξ_d^cl ≈ 1/4 is q-INDEPENDENT (q=8 + q=10):** registered P1 passed (plateau
  0.256 vs 0.259, 1% match across ξ 2.26x; L/ξ≈2 window 0.277 ∈ 0.25±0.04); joint shared-s
  = 0.213±0.029 excludes 0.40/0.50 at 6-10σ. The constant's exact value (1/4 vs 0.21-0.25)
  open; its universality established. unresolved/sprint_141.md.
- **S140 — two-length structure at the quantum first-order point:** ξ_x(q=10, disordered
  branch, at g_c) ≲ 4.3 sites (direct OZ correlator, n=48/64 converged; 2.2 at g_c+0.003)
  vs tunneling scale Λ ≈ 17 sites ∝ ξ_d^cl. METHOD: near coexistence use exact charge BLOCKS
  (Fourier basis) — plain ⟨P⟩ filtering fails (Lanczos tower mixing); flat magnon bands make
  ξ=v/Δ unreliable (use the correlator). unresolved/sprint_140.md.
- **S138 — Λ ∝ ξ CONFIRMED by blind prediction (q=7):** the S137 coefficients predicted
  Λ_Im=79±5 BEFORE any q=7 data; measurement returned 79±25 (1.64ξ vs predicted 1.65ξ) with
  the decay term independently demanded at the q=8-calibrated strength. Λ_Dm/Λ_Im = 1.50
  (vs 1.58/1.59). Upgrades S137 to CONFIRMED NOVEL (hardening #1-#3). unresolved/sprint_138.md.
- **S137 — WALKING CROSSOVER OBSERVED (strongest result to date; unresolved/sprint_137.md):**
  Z_q-charge-conserving DMRG (zq_dmrg_utils, ED-validated 3e-4) extends the thermal-gap EP to
  n=28 at q=8,10. Both Im(g_EP)(L)=Δm/c1 (asymmetric avoided-crossing fit) and Δ_min(L) demand
  an exponential factor beyond the shadow power law exactly where L crosses the EXACT ξ_d:
  fits A·L^{−p}e^{−L/Λ} preferred by dAIC +17/+37 (q=8/q=10, Δm series) with **Λ_Im = 1.59ξ /
  1.71ξ and Λ_Dm = 2.51ξ / 2.71ξ — Λ ∝ ξ to ~10% while ξ varies 2.26x**; the q=6 control
  (ξ=159, L/ξ≤0.15) needs NO decay (dAIC≈0; Δm·L flat ~2.4 = CFT-like). Excludes truncation
  artifacts (same chi ladder for control; slopes smooth across chi tiers). The exponential gap
  closing at first-order quantum Potts transitions is known (Campostrini et al. 1410.8662);
  new: the EP observable, the q-resolved shadow→crossover map vs exact ξ_d, the null control,
  and the q=5-only shadow anchor. METHOD NOTES: open-chain crossing wings are asymmetric (fit
  Δ=sqrt(Δm²+(c1δ+c2δ²)²)); 4-param fits need ≥7 points (5-point "exact" fits hide 5-18%
  parameter noise); DB names BC-qualified (im_gEP_open).

## χ_F effective exponents (S127-131; finite-size EFFECTIVE values, fixed-g_c periodic)
| q | S_q α_eff | sizes | note |
|---|-----------|-------|------|
| 3 | 1.468±0.012 | n=4-14 | asymptote 1.40 (exact) |
| 4 | 1.790±0.006 | n=4-12 | asymptote 2.0 + marginal log |
| 5 | 2.094±0.002 | n=4-10 | walking effective |
| 6 | 2.375±0.006 | n=4-9 | walking effective |
| 7 | 2.636±0.018 | n=4-8 | walking effective |

Stat errors only — the fixed-g_c estimator carries a known **+0.05-0.07 systematic** (S130/S134);
α(q) functional-form claims (log vs log+loglog) are NOT robust against it. Hybrid-model values
and g_c(hybrid) table: ARCHIVE.

## Key literature (search before claiming novelty)
- **Albuquerque, Alet, Sire, Capponi** PRB 81 064418 (2010): χ_F density ~ L^{2/ν−d}. THE null.
- **Salas & Sokal** JSP 88 567 (1997): 2D classical 4-state Potts logs; 3/2 is SPECIFIC-HEAT
  power, susceptibility is 1/8 — no χ_F prediction there to reject.
- **Gorbenko, Rychkov, Zan** SciPost 5 050 (2018): complex CFT for q>4; quotes ξ(5)~2500.
- **Jacobsen & Wiese** PRL 133 077101 (2024): all S_q Potts exponents via analytic continuation.
- **Ma & He** PRB 99 195130 (2019): c_eff for q=5,6,7 Hermitian S_q chain.
- **Buffenoir & Wallon** (1993): exact ξ_d(q) at the q>4 transition (values in Open Items).
- **Sun, Luo, Chen** arXiv:2006.11361: Z_q clock has two BKT transitions for q>4.

**Retracted:** see ARCHIVE ("no CFT predictions for q>4", "analytic continuation wrong", S128c
extrapolation, S132/S133 fixed-g_c readings, S108 1/lnN extrapolation, spectral-χ_F exponents).
