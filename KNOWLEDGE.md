# Accumulated Knowledge — Edit by topic, not by sprint

## Open Items — Check each sprint, remove when done
- **~~Test energy-entropy hierarchy in a DIFFERENT model~~** DONE (Sprint 104). Tested in J1-J2 chain. Result: **NOT universal.** Hierarchy direction is model-dependent. Potts walking gives O(1) entropy deviation — unique to walking mechanism. J1-J2 gives only O(1%) differences. The Casimir-Re(c) finding is walking-specific, not a general CFT principle.
- **~~Harden chi_F scaling at q=5~~** DONE (Sprint 103, updated Sprint 116). alpha(q) mapped q=2-25. All polynomial/power-law forms ruled out. **Log+loglog alpha(q) = 2.62 ln(q) - 1.77 ln(ln(q)) - 1.26 marginally AIC-best** (dAIC=1.4 over pure log) with 10 data points (Sprint 116). Pure log: 1.86 ln(q) - 0.96.
- **~~Test χ_F in different model~~** DONE (Sprint 105). J1-J2 BKT: invisible (α→0). MG first-order: saturates. Walking super-scaling is unique.
- **~~Understand χ_F mechanism~~** DONE (Sprint 106). α = β_me + 2z_m - 1. Single multiplet dominates. Spectral gap symmetry-forbidden.
- **~~Harden χ_F mechanism~~** DONE (Sprint 107). 5 sizes at q=5, cross-validated. CONFIRMED NOVEL.
- **~~Log corrections to α(q)~~** CORRECTED (Sprint 109). Sprint 108's 1/ln(N) extrapolation was WRONG for q=2,3. Power-law 1/N² corrections recover exact ν: q=2→α_∞=1.00 (exact 1.0), q=3→α_∞=1.40 (exact 7/5). Walking (q≥5) zero corrections confirmed. q=4 BKT genuinely slow (neither model converges at accessible sizes).
- **Hardware validation** — 580s QPU unused for ~90 sprints (BLOCKED: ~/.qiskit/qiskit-ibm.json empty). Strongest prediction: q=2 Ising χ_F at g_c, or Heisenberg chain c_eff on 5-10 qubits.
- **CHANGELOG.md is over budget (511 lines vs 300 trigger).** Compress sprints older than the last ~10 into one-line summaries. (KNOWLEDGE.md itself is fine at ~130 lines — the old "560-line" note was stale, removed S131.)

## Five Entanglement Archetypes
| Archetype | Example | MI pattern | I3 sign | Negativity | Source |
|-----------|---------|-----------|---------|------------|--------|
| Democratic | GHZ, Ising ordered | Uniform high | +1 (redundant) | Flat | Sprint 005 |
| Distributed | W state | Uniform weak | +0.2 (weak redundant) | Growing with cut | Sprint 005 |
| Geometric | Cluster 1D | Nearest-neighbor only | -1 (irreducible) | Explosive, geometry-dependent | Sprint 007 |
| Topological | Toric code | Non-contractible loops | 0 (zero everywhere) | Uniform floor | Sprint 020 |
| Scale-Free | Critical TFIM | Power-law decay | Mixed | Highest rank, steep decay | Sprint 029 |

## Four Levels of Entanglement Description
Each captures orthogonal information. Different phase transitions are visible at different levels.
1. **Scalar** (entropy) — amount of entanglement
2. **Correlation** (MI, I3) — topology of correlations. I3<0 = irreducible multipartite. I3>0 = redundant/classical-like.
3. **Spectral** (eigenvalue distribution of ρ_A) — symmetry content. U(1) gives doublet degeneracies. Z₃ gives triplets.
4. **Hamiltonian** (H_E = -log ρ_A structure) — locality and entanglement temperature.

## ⚠ Model Identity — READ THIS (Audit April 2026)

### TWO MODELS WERE STUDIED — NOT ONE

**Sprints 033-075:** Studied the **Potts-clock hybrid** H = -Jδ(s_i,s_j) - g(X+X†). Z_q symmetry.
**Sprints 076-118:** Switched to the **standard S_q Potts model** H = -Jδ(s_i,s_j) - gΣ_{k=1}^{q-1} X^k. S_q symmetry. All six claimed novel findings (098, 102-118) are on this model.

The switch happened at Sprint 076 (introduced S_q for comparison) and was never reversed. Code audit confirms: all experiment scripts from 076+ use `build_sq_potts` with `for k in range(1, q)` or TeNPy `SqField = ones(q,q) - eye(q)`.

| Model | Coupling | Transverse field | Symmetry | Sprints | q>4 transition |
|-------|----------|-----------------|----------|---------|---------------|
| S_q Potts | δ(s_i,s_j) | Σ_{k=1}^{q-1} X^k | S_q | **076-118** | Weakly 1st-order (walking) |
| Z_q clock | cos(2π(s_i-s_j)/q) | X + X† | Z_q | 034,065,067 | Two BKT |
| Potts-clock hybrid | δ(s_i,s_j) | X + X† | Z_q | **033-075** | Continuous 2nd order |

For q=2,3 all three are equivalent (up to field rescaling at q=2). For q≥4 they differ.

### Implications for novelty claims

The S_q Potts model is the SAME model studied by Gorbenko-Rychkov-Zan, Ma & He, Tang et al., and Jacobsen & Wiese. Therefore:
- Agreement between Casimir energy and Re(c) is **expected** (GRZ predictions are for this model)
- g_c = 1/q is a **known exact result** (Kramers-Wannier self-duality)
- The model is NOT novel — but our **probes** (χ_F spectral decomposition, Casimir vs entropy comparison) may be

### What IS still potentially novel on the S_q model
- **χ_F spectral decomposition** (Sprint 107): selection rule + single-multiplet dominance mechanism
- **χ_F scaling data across q** (Sprints 102-117): systematic measurement, appears to be new data
- **Casimir vs entropy systematic comparison** (Sprint 098): useful quantitative observation

### ⚠ Spectral chi_F: Methodology Status (Sprints 125-126)
Spectral Lehmann sum was missing factor 2 (Sprint 125). Even corrected, spectral method captures only the dominant state — non-dominant states at high eigenvalue indices cause **systematic negative alpha bias of 0.005–0.038** (Sprint 126). Bias grows with system size. **Use exact chi_F (finite-difference) for all exponent claims.** The selection rule is standard Z_q representation theory. The formula alpha = beta_me + 2·z_m − 1 is a tautological identity. *(Sprint 129 audit: exact chi_F uses overlap-squared and /n — per-site, factor-2 — both constant prefactors that cancel in the exponent, verified harmless. Values good to ~5 sig figs, not the 6 decimals stored (dg=1e-4 gives a smooth ~1e-6 low-bias). g_c=1/q is exact self-dual to 1e-15.)*

### ⚠ q=4 chi_F framing CORRECTED (Sprint 129 audit) — read before using the table
We measure the **per-site** chi_F density, whose correct leading exponent at a QCP is **2/nu − d**
(Albuquerque, Alet, Sire, Capponi, PRB 81 064418 (2010), Eq.21). Our own q=3 anchor proves the
convention: nu=5/6 ⇒ 2/nu−d = 7/5 = 1.40 (= our "exact" q=3 value). For 4-state Potts nu=2/3 ⇒
**2/nu−d = 2.0 is the CORRECT answer, not a hypothesis to reject.** Measured ~1.77 is the FINITE-SIZE
value below 2: q=4 has the marginal (dilution, c=1) operator ⇒ slow log-corrected approach to 2;
q=3 has none ⇒ converges to 7/5. At L<=11 (ln N x1.73) the data CANNOT distinguish "1.77 forever"
from "2 with marginal logs"; open-BC DMRG even drifts UP toward 2. The S_q values below are
finite-size **effective** exponents, NOT asymptotes.

### ✔ q=4 reframing HARDENED (Sprint 130) — independent ν + marginal-log signature
Two calibrated, g_c-assumption-free observables from the full χ_F(g,N) curve (calibration on q=2→1/ν=1
and q=3→1/ν=1.2, no marginal op):
- **Data collapse (location scaling, marginal-log-insensitive):** 1/ν(q=4)=1.45 raw → **1.49 after the
  q=2,3 calibration (×0.973) ⇒ ν=2/3 confirmed from our own data.** Excludes 1/ν≤1.2. This confirms the
  literature input the Sprint-129 reframing relied on.
- **Amplitude (self-locating peak-HEIGHT) exponent:** recovers 2/ν−d to ≤1.3% at q=2,3 (method unbiased)
  but a(q=4)=1.75 = **12.7% below 2.0** ⇒ the deficit is *physical*, the marginal log. Albuquerque
  residual 2κ−1−a is ~0 at q=2,3 but **+0.14 at q=4** — the marginal operator made visible.
- Given ν=2/3 (confirmed) + Albuquerque (a proven identity), the amplitude exponent **must →2** asympt.;
  measured ~1.77–1.81 is finite-size. **Peak-SHIFT exponent is unusable for ν** (gives 1.8/2.3/2.5 vs
  true 1.0/1.2/1.5 — peak sits at x*≈−0.2, shift is correction-dominated; logged dead end).
- Methodological nugget: self-locating peak-HEIGHT is the lowest-bias accessible-size estimator of
  2/ν−d (≤1.3% at q=2,3), better than fixed-g_c (overshoots +0.07). Full report: sprints/sprint_130.md.

### chi_F effective exponents (Sprints 127-131, exact chi_F; see Sprint 129 caveat above)

| q | Hybrid alpha | S_q alpha (effective) | # sizes (S_q) | Pairwise drift (S_q) |
|---|-------------|-----------|---------------|---------------------|
| 3 | 1.481+/-0.014 | 1.468+/-0.012 | 6 (n=4-14) | Decreasing (1.57->1.44) |
| **4** | **1.549+/-0.012** | **1.794+/-0.011** | 6 (n=4-11) | Oscillating ~1.79 |
| 5 | 1.352+/-0.043 | **2.094+/-0.002** | 5 (n=4-10) | Increasing (S131 fix) |
| **6** | **1.186+/-0.038** | **2.375+/-0.006** | 6 (n=4-9) | Increasing (2.35->2.40) |
| 7 | 0.971+/-0.058 | **2.636+/-0.018** | 4 (n=4-8) | Increasing (2.58->2.67, S131 fix) |

S_q alpha(q) effective exponents increase with q (walking for q>=5). **q=5 and q=7 RECONCILED (Sprint 131):** canonical = results.db `alpha_exact` (q=5 -> 2.094+/-0.002, q=7 -> 2.636+/-0.018; raw chi_F reproduced CPU-vs-GPU to 4.8e-9). The prior 2.139/2.584 were stale sprint-128 alpha(q)-table transcriptions, reproduced by NO standard fit (full/subset, linear/log-space all give 2.09/2.64); sprint-127.md and CHANGELOG already held the correct values. With the corrected points the effective-exponent curve is **convex in ln q** (local slopes 1.14, 1.34, 1.54, 1.69 monotonically increasing; quadratic adds +0.44(ln q)^2, chi2/dof->0), i.e. super-logarithmic — not the "nearly linear / alpha~1.34 ln q" of sprint 128 (that near-linearity was the artifact). Functional form remains **not load-bearing**: q=3,4 are finite-size *effective* exponents whose asymptotes are 2/nu-d (1.40, 2.0), so the curve mixes the continuous-transition and walking regimes.

**Asymptotic extrapolation (Sprint 128c) — RETRACTED as evidence against logs (Sprint 129).** The ansatz alpha_eff(N)=alpha_inf+c/N^p has NO log term, so it cannot detect log corrections: fed synthetic true-alpha=2-with-Salas-Sokal-logs data it returns alpha_inf=1.60-1.89. Its q=3 "validation" is a non-sequitur (q=3 has no marginal operator). So q=4 alpha_inf=1.771 is NOT evidence that the asymptote is below 2.

**S_q q=4 log correction analysis (Sprint 128d, exact chi_F) — REFRAMED (Sprint 129):** the 4-model AIC comparison is valid *as a description of n<=11* (passes a synthetic recovery test), and at those sizes the data prefer a sub-2 effective exponent:
- Power+1/N^2 alpha=1.760 (AIC=-52) — but 3 params/6 pts, corr(A,alpha)=-0.999, alpha NOT identified
- Free log alpha=1.643 p=-0.31 (AIC=-41); Pure power alpha=1.795 (AIC=-21); Log-alpha=2 p=0.41 (AIC=-11)
BUT: (1) "**Salas-Sokal p=3/2**" is **MISLABELED** — 3/2 is the 2D-classical specific-heat log power (Salas-Sokal Eq.2.34a); their susceptibility log power is 1/8; there is no chi_F log prediction in that paper to reject. (2) An alpha=2 + free-log + 1/N^2 model out-fits pure power (SSR 0.003 vs 0.097), so the alpha=2-with-corrections family is NOT excludable at these sizes. Honest statement: **q=4 per-site chi_F is consistent with the expected leading exponent 2 suppressed by marginal logs; unresolved below L>>11.** The novelty ("no prior chi_F log measurement at q=4") survives only by dropping the Salas-Sokal comparison.

**g_c(hybrid):** q=2->0.250, q=3->0.333, q=4->0.393, q=5->0.438, q=6->0.474, q=7->0.535, q=10->0.684.

**DMRG extension (Sprint 124):** Open-BC chi_F at n=6-20 (8 sizes). Pairwise alpha drifts UPWARD: 1.505->1.523. Power+1/N^2 corrected alpha_open=1.524+/-0.002. Log-corrected alpha=2 still worst fit (R^2=0.9997 vs 0.999999). **But drift direction is upward** -- consistent with eventual convergence to higher value (periodic 1.77 or log-corrected 2.0). Asymptotic regime needs L>>20 (likely L>100). iDMRG overlap method FAILED for S_q Potts (non-abelian symmetry).

### Hybrid model findings — CLOSED (Sprint 128e)
Sprint 065 confirmed hybrid ≠ clock, Sprint 076 confirmed hybrid ≠ S_q Potts. Sprints 119-121: chi_F spectral decomposition confirms continuous transitions for q>=5 and walking->continuous boundary at q_cross=3.58. **Sprint 128e:** Power law wins for q<=4, logarithmic chi_F ~ A*(ln N)^beta wins for q>=6 (dAIC=20 at q=6), marginal at q=5. This is consistent with BKT-class transitions at large q. Thread closed — no further compute needed.

**Key literature (search before claiming novelty):**
- **Albuquerque, Alet, Sire & Capponi (PRB 81, 064418, 2010; arXiv:0912.2689):** chi_F density ~ L^{2/nu-d} at a QCP. THE correct null for our per-site chi_F. q=4 ⇒ L^2.
- **Salas & Sokal (J. Stat. Phys. 88, 567, 1997; hep-lat/9607030):** 2D *classical* 4-state Potts. p=3/2 is the SPECIFIC-HEAT log power (Eq.2.34a); susceptibility log power is 1/8 (Eq.2.34c). NOT a chi_F prediction — do not "reject" it.
- **Gorbenko, Rychkov & Zan (JHEP 2018, SciPost 2018):** Complex CFT for q>4 S_q Potts.
- **Ma & He (PRB 99, 195130, 2019):** Measured c_eff for q=5,6,7 on Hermitian S_q chain.
- **Tang et al. (PRL 133, 076504, 2024):** Non-Hermitian q=5 S_q Potts.
- **Jacobsen & Wiese (PRL 133, 077101, 2024):** All S_q Potts exponents via analytic continuation.
- **Sun, Luo & Chen (arXiv:2006.11361, 2020):** Z_q clock has two BKT transitions for q>4.

**Retracted:** ~~"No CFT predictions for q>4"~~, ~~"Analytic continuation WRONG"~~, ~~"Potts NEVER first-order"~~, ~~"Our model is a novel Potts-clock hybrid" (for sprints 076+)~~, ~~"q=4 alpha=1.77 asymptotic, Salas-Sokal log corrections rejected" (Sprint 129: 2/nu-d=2 is the correct value; 1.77 is finite-size; exp_128c extrapolation is circular)~~ — see archive / sprint_129_audit.md for details.

## Detailed Findings

All detailed findings from sprints 029-115 (walking regime, entanglement spectrum, BW analysis, 2D extension, hybrid model characterization, MI-CV, entropy methods, CFT content, OPE, SREE, χ_F) are in **KNOWLEDGE_ARCHIVE.md**. Read that file when you need:
- Methodology details (how to extract c, x₁, ν, C_sse)
- Past numerical values or data tables
- What's been tried and ruled out
- Hybrid model vs clock vs S_q Potts comparisons
