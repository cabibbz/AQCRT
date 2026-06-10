# Accumulated Knowledge — Edit by topic, not by sprint

*(Detailed findings & closed threads: KNOWLEDGE_ARCHIVE.md. Last 10 sprints: CHANGELOG.md.
A 48-agent system audit (2026-06-09) verified the pipeline and HEDGED three interpretive
claims — hedges are inline below; full audit report: sprints/audit_2026-06-09.md.)*

## Open Items — Check each sprint, remove when done
- **Hardware validation** — 580s QPU unused for ~90 sprints (BLOCKED: ~/.qiskit/qiskit-ibm.json
  empty; needs human to restore token). Strongest prediction: q=2 Ising χ_F at g_c on 5-10 qubits.
- **Walking crossover via Z_q-conserving DMRG — RETARGETED to q=8-10 (audit).** The L≳ξ
  power-law→faster crossover of Im(g_EP) is the definitive walking test, but EXACT classical
  ξ_d values (Buffenoir-Wallon 1993) are: **ξ(q5)=2512, ξ(q6)=159, ξ(q7)=48, ξ(q8)=24, ξ(q10)=10.6**
  — the old "ξ>12" budget anchor was only a lower bound from n≤12 data. DMRG n=20-40 brackets
  L~ξ ONLY for q≥8. Keep q=5,6 as deep-shadow controls.
- **Jacobsen-Wiese comparison (PRL 133 077101) — run BEFORE more complex-CFT language.**
  PRELIMINARY (audit-verifier Coulomb-gas continuation, redo properly): Re(1/ν_complex) =
  1.534/1.563/1.588 for q=5/6/7 vs our effective 1.51/1.65/1.78 — q=5 matches, q=6,7 rise PAST
  it toward the first-order value d=2. If that holds, q≥6 values are crossover phenomenology,
  not shadow exponents.
- **S135 rigor gap:** chi-doubling DMRG check at n=24 (q=4 and q=3 control, chi 48→96, svd 1e-9);
  production used chi=48 verified only at n=12.

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
- **Walking q=5,6,7 (hedged):** effective 1/ν_eff = 1.51/1.65/1.78, rising smoothly across q=4,
  still climbing at n≤9 — **consistent with the complex-CFT "conformal shadow" interpretation**
  (GRZ), but equally consistent with generic weak-first-order finite-size drift; the method
  undershoots 4-9% at these sizes and q=7 has only 3 slope pairs. The Jacobsen-Wiese comparison
  (Open Item) is the discriminating test. (Hedged from "= complex-CFT shadow".)

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
