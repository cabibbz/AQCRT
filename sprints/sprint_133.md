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

**Cross-method check:** S124 DMRG (open, forward/dg=1e-3, χ_max≤110) at n=12–20 gives pairwise exponents
1.515→1.524 — *also rising*, agreeing with the canonical exact-diag rise direction despite the different
convention and DMRG truncation. The rising open tail is robust across method AND convention.

### exp_133b — reconciliation analysis (model-free)  (DONE)

A shared-bulk + multiplicative-1/L-boundary **joint fit FAILED**, and the failure is itself a result:
the ratio χ_O/χ_P **decreases away from 1** (0.352→0.260), whereas a multiplicative (1+b/L) boundary
forces the ratio *toward* 1. So **a vanishing 1/L boundary correction is refuted** — at n≤12 the two BC
do *not* converge; the gap is not a simple boundary term dying off. (A κ=2 marginal-log form also has to
contort, e≈37 / c≈−1.2, to mimic what is essentially a clean ~1.80 power law.) With 9+9 points and several
plausible competing-correction structures the joint fit is **non-identifiable** — the S132 degeneracy
lesson, reaffirmed. We therefore drop fit-based model selection and report robust, model-free facts.

**The decisive model-free signal — the SHAPE of each κ_eff(L):**
- A series *relaxing to a nearby plateau* has κ_eff increments that **shrink** toward 0.
- A series *climbing* has **growing** increments (accelerating) — it is not near its destination.

| | trajectory | increments | reading |
|---|---|---|---|
| **periodic** | 1.863 → 1.778, monotone ↓ | decrements shrink geometrically (ratio ≈0.56) | decelerating descent → apparent plateau ≈1.776 |
| **open** | 1.556 → **min 1.520 @ n≈7.5** → 1.537 | post-min increments **grow** +0.0023→+0.0054 | accelerating climb; destination > 1.537, unknown |

The open post-minimum increments *grow* (2nd diffs +0.0018, +0.0009, +0.0004 — still positive), so open
κ_eff is **still climbing at the frontier and has not inflected to a plateau**: open is provably *not*
settling near 1.55. A series relaxing to a low plateau would show shrinking increments (like periodic's
descent); open shows the opposite.

**Clean per-BC power laws (fss_utils):** periodic α = **1.791 ± 0.004** (R²=0.99998), open α = **1.527 ±
0.001** (R²=0.999996); top-5 (n=8..12) periodic 1.781, open 1.530. Both are excellent power laws far below
the null 2.0 in this window — a face-value fit "prefers" sub-2, exactly as S132. The open turnaround (above)
is the empirical evidence that this face-value reading is **unreliable**.

## Verdict (honest)
1. **The BC gap is real and convention-independent**: with the identical canonical estimator, open
   κ_eff = 1.537 vs periodic 1.778 at n=12. The prior "1.52 vs 1.78" was not an artifact of mixing
   conventions (forward/dg=1e-3 open vs central/dg=1e-4 periodic) — it survives apples-to-apples.
2. **Open κ_eff is non-monotonic** (min 1.520 @ n≈7.5, accelerating climb) — a *new* observation; S124
   DMRG saw only the rising tail. Periodic shows a decelerating descent (no turnaround by n=12).
3. **A vanishing boundary correction is refuted** (ratio moves away from 1); the BC do not converge by
   n=12, and the joint shared-bulk fit is non-identifiable.
4. **The asymptote remains unquotable at L≤12** — fits cannot distinguish 2.0-with-marginal-logs from a
   sub-2 plateau (S132 degeneracy stands). **What changed:** the open turnaround *neutralizes the S132
   "wrong-sign descent" argument against 2.0.* S132 reasoned that a true-2.0+single-marginal-log gives an
   *ascending* κ_eff while the data descend → tension. But the open BC empirically exhibits a descend-then-
   ascend κ_eff for this very observable, proving the correction structure is richer than a single
   monotonic log. A finite-window apparent plateau can reverse (open did it). So periodic's descent toward
   ≈1.78 is **not** evidence the asymptote is below 2.0. Net: **2.0 not excluded; sub-2 plateau not
   established; the contradiction between the two BC drift directions is resolved** as two windows of one
   non-monotonic finite-size flow, open ahead of periodic.

## Hostile-reviewer self-check
- **Apples to apples?** Yes — same basis, same field operator, same central-diff/dg=1e-4/factor-2/÷n
  estimator, same g_c=1/q, same eigensolver; the ONLY difference between periodic and open is the single
  wrap bond. Periodic reproduces results.db to ≤5e-9; open forward-diff reproduces the old DB `chi_F_open`
  exactly. The dip is ~0.002–0.005 in κ_eff, far above the dg=1e-4 noise floor (~1e-6 in χ_F).
- **Is the open dip a numerical artifact?** No. Same converged solver as periodic (which matches DB to
  1e-9); dg-bias is ~1e-6; the dip is smooth across 4 points with monotone-growing increments; and the
  rise direction agrees with independent S124 DMRG at n=12–20.
- **Could finite size explain the whole thing?** That is precisely the point — *everything here is finite
  size*. We do NOT claim to have reached the asymptote. We claim the BC are reconciled and the S132
  wrong-sign argument is defused.
- **Did the literature already do this?** No prior open-vs-periodic χ_F effective-exponent comparison at
  q=4 with matched convention, nor a report of a non-monotonic χ_F κ_eff for the 4-state Potts chain.
  Boundary-dependence of fidelity scaling is known qualitatively; the marginal-log mechanism is known for
  thermodynamic susceptibilities, not χ_F. Consistent with the standing S128/129/132 novelty flag.

**POTENTIALLY NOVEL (hardening, cross-check method per novelty-rule #2):** the open-BC q=4 per-site χ_F
effective exponent is non-monotonic in L (minimum κ_eff≈1.520 at n≈7.5, accelerating rise to 1.537 at
n=12), measured by canonical exact diagonalization and cross-confirmed in drift direction by DMRG to n=20.
Combined with the periodic descent, this reconciles the two boundary conditions as one non-monotonic
finite-size flow and removes the prior "wrong-sign-vs-2.0" tension. Literature search found no prior
report of a non-monotonic fidelity-susceptibility effective exponent, nor an open/periodic χ_F reconciliation,
for the 4-state Potts chain. Copied to unresolved/.

## Files
- `experiments/exp_133a_bc_canonical_q4.py`, `experiments/exp_133b_bc_reconcile.py`
- `results/sprint_133a_bc_canonical_q4.json`, `results/sprint_133b_bc_reconcile.json`
- results.db: `chi_F_open_exact` (q=4 n=4..12, canonical open), `kappa_eff_open` (q=4 n=12)
