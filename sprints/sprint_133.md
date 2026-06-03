# Sprint 133 — Reconcile periodic vs open BC for q=4 χ_F (canonical convention, matched to n=12)

**Date:** 2026-06-02
**Thread:** q=4 S_q Potts per-site χ_F effective exponent — STATE Top-Next #1: "the asymptote blocker."
**Environment:** Windows, Python 3.11.9, NVIDIA TITAN RTX (24 GB), CuPy 13.6.0, numpy 1.26.4.

## Motivation

The standing tension (S129–S132): theory says the q=4 per-site χ_F leading exponent is **2/ν−d = 2.0**
(ν=2/3 confirmed S130 collapse + Albuquerque identity). Measured **periodic** exact-diag effective
exponent is ~1.78 at n≤12 and **drifting DOWN** (away from 2.0). Meanwhile **open-BC DMRG** (S113/S124)
gave a much *lower* exponent ~1.52 **drifting UP**. The two BC disagree in both value and drift
direction. Until reconciled, the L→∞ asymptote is unknowable (STATE Top-Next #1).

**Key problem found this sprint (pre-experiment audit):** the prior open-BC data used a **different
χ_F convention** than the periodic series:
- Periodic (canonical, chif_utils): central diff `(2−F²₊−F²₋)/(dg²·n)`, dg=1e-4 — has a built-in ×2.
- Open (S113/S124 exp_113b): forward diff `(1−F²)/(dg²·n)`, dg=1e-3 — **no ×2**, coarser dg.

So canonical ≈ 2× the old open values, and the "1.78 vs 1.52" comparison was **never apples-to-apples**.
The *exponent* is prefactor-independent in principle, but the forward/dg=1e-3 estimator carries more
systematic error and the comparison was only done to n≤9 (exp_113c). This sprint recomputes open BC
with the **identical canonical estimator** used for the periodic series, to the n=12 GPU frontier.

## Literature check (3 keyword variations)
1. "fidelity susceptibility FSS open vs periodic BC" → open & periodic give **different** fidelity
   scaling in the QC regime (known qualitatively; Albuquerque 0912.2689 already our null ref).
2. "4-state Potts marginal operator log corrections susceptibility" → q=4 dilution field marginal
   (critical+tricritical merge) ⇒ multiplicative logs; Salas-Sokal hep-lat/9607030, Blöte 0707.3317.
   These are for *thermodynamic* susceptibility/specific heat, **not χ_F**.
3. "boundary fidelity susceptibility surface exponent open chain DMRG" → χ_F routinely measured by
   DMRG with open BC; no prior open-vs-periodic χ_F *effective-exponent reconciliation* at q=4.
**Gap:** no literature measures the open-vs-periodic χ_F effective-exponent gap or its boundary-deficit
scaling at q=4 with matched convention. Consistent with the existing S128/129/132 novelty flag.

## Experiments

### exp_133a — open vs periodic canonical χ_F, q=4, n=4..12  (DONE)

**Validation (all pass):** periodic canonical reproduces results.db `chi_F_exact` to ≤5e-9 at n=4,6,8,9,10,11;
open forward-diff (dg=1e-3) reproduces results.db `chi_F_open` exactly (4.169510 @ n=6, 6.432503 @ n=8),
confirming the open Hamiltonian; canonical/forward = 2.03–2.04 (the predicted ≈×2 convention gap).

**Matched canonical per-site χ_F at g_c=1/q** (`chi_F_open_exact` n=4..12 → results.db):

| n | periodic | open | open/periodic |
|---|----------|------|---------------|
| 4 | 12.8393 | 4.5234 | 0.3523 |
| 6 | 27.1380 | 8.4606 | 0.3118 |
| 8 | 45.5278 | 13.1033 | 0.2878 |
| 10 | 67.7842 | 18.4112 | 0.2716 |
| 12 | 93.7476 | 24.3524 | 0.2598 |

**Pairwise local effective exponents** (the headline):

| pair | periodic | open |
|------|----------|------|
| (4,5) | 1.8634 | 1.5559 |
| (5,6) | 1.8243 | 1.5301 |
| (6,7) | 1.8038 | 1.5212 |
| (7,8) | 1.7923 | **1.5199 ← min** |
| (8,9) | 1.7855 | 1.5222 |
| (9,10) | 1.7815 | 1.5263 |
| (10,11) | 1.7792 | 1.5313 |
| (11,12) | 1.7779 | 1.5368 |

**Two clean facts:**
1. **The BC gap is real, not a convention artifact.** With the *identical* canonical estimator the open
   and periodic effective exponents are 1.537 vs 1.778 at n=12 — the old "1.52 vs 1.78" (which compared a
   forward/dg=1e-3 open against a central/dg=1e-4 periodic) survives the apples-to-apples recomputation.
2. **Open κ_eff is NON-MONOTONIC: a clear minimum at n≈7.5 (1.5199) then an *accelerating* rise**
   (increments +0.0023, +0.0041, +0.0050, +0.0055) to 1.5368 at n=12. S124 DMRG only ever saw the rising
   tail (1.505→1.523, n≥6) and read it as "drifts up"; the canonical exact-diag reveals the full
   **dip-and-turnaround**. Periodic, by contrast, decreases monotonically but with geometrically shrinking
   decrements (−0.039,−0.020,−0.012,−0.0068,−0.0040,−0.0023,−0.0013; ratio ≈0.55) toward an apparent
   plateau ≈1.776.

**Why this matters (the reconciliation seed):** the open series is an explicit, independent demonstration
that *a decelerating monotonic drift toward an apparent plateau can be the pre-minimum branch of a
non-monotonic curve.* Open κ_eff "looked like" it was settling near 1.52 for n≤7 (shrinking decrements),
then turned up. So reading periodic's apparent plateau ≈1.776 as the L→∞ asymptote is unsafe by the same
token. The natural reconciled picture: **both BC follow a non-monotonic κ_eff(L) heading to 2.0; open
(stronger finite-size corrections, incl. the 1/L boundary term it has and periodic lacks) has already
passed its minimum at n≈7; periodic (weaker corrections) has its minimum pushed beyond n=12.** exp_133b
tests this quantitatively.
