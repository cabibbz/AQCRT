# Sprint 130 — Independent ν and the marginal-log signature from χ_F finite-size scaling (hardening the corrected q=4 framework)

**Date:** 2026-06-02
**Thread:** S_q Potts q=4 — is the per-site χ_F leading exponent the expected 2/ν−d = 2 (with marginal
logs), or a true sub-2 value? (Sprint 129 audit reframing.)
**Environment:** CPU-only (CuPy unavailable). Exact diag via `gpu_utils.eigsh` → scipy fallback.
Sizes: q=2 n≤20, q=3 n≤12, q=4 n≤10.

## Motivation
Sprint 129 corrected the headline: the per-site χ_F leading exponent at a QCP is **2/ν−d**
(Albuquerque, Alet, Sire & Capponi, PRB 81 064418). q=3 anchors the convention (ν=5/6 ⇒ 2/ν−d = 7/5 =
1.40 = our "exact" value); q=4 (ν=2/3) ⇒ 2/ν−d = **2.0**, so the measured ~1.77 *at g_c* is a
finite-size value **below** 2, slowed by the q=4 marginal operator. That reframing rests on two
external inputs: **(a)** the Albuquerque scaling relation, and **(b)** ν=2/3 taken from the literature.

**This sprint hardens leg (b) with our own data, via independent observables** (novelty-hardening rule
#2: cross-check the same physics with a different method). Instead of the χ_F *height at fixed g_c*
(the quantity with the log-correction ambiguity), I scan the whole **χ_F(g,N) curve** in the FSS
scaling window and extract four estimators, calibrating each on q=2 (1/ν=1, no marginal op) and q=3
(1/ν=1.2, no marginal op) before applying to q=4:

1. **at-g_c exponent** — χ_F(g_c) ~ N^a, a = 2/ν−d (reproduces the prior method as a self-check)
2. **peak-HEIGHT exponent** — χ_F(g\*) ~ N^a, peak self-located (**needs no g_c assumption**)
3. **peak-SHIFT exponent** — |g\*−g_c| ~ N^{−1/ν} (standard FSS, but a-priori fragile here)
4. **data-collapse 1/ν** — full curve; the **location** scaling, which a marginal log barely touches

Method note (why a scaling-window scan is exponent-clean): the consecutive-overlap χ_F uses grid step
h = Δx·N^{−κ₀}, which scales as the FSS width N^{−1/ν}, so the leading finite-h bias is an
N-independent multiplicative factor → it cancels in every *exponent* (confirmed: q=2 height → 1.013).
We quote only exponents. Curves saved (`results/sprint_130{a,b,c}_fss_q{2,3,4}.json`).

## Predictions (logged before running)
| q | 1/ν | 2/ν−d | height a | collapse 1/ν | role |
|---|-----|-------|----------|--------------|------|
| 2 | 1.0 | 1.0 | →1.0 | →1.0 | calibration (clean) |
| 3 | 1.2 | 1.40 | →1.40 | →1.2 | calibration (clean) |
| 4 | 1.5 | 2.0 | <2, log-biased | →1.5 (log-insensitive) | TEST |

## Experiments
- `exp_130a_fss_q2.py` — q=2 calibration, n=8..20
- `exp_130b_fss_q3.py` — q=3 calibration, n=5..12
- `exp_130c_fss_q4.py` — q=4 test, n=5..10
- `exp_130d_synthesis.py` — calibration-controlled synthesis (no new diag)
- `collapse_utils.py` — curve scan, peak-from-curve, leave-one-size-out collapse cost

## Results

### Raw estimators (each q, all its sizes)
| q | sizes | at-g_c a | **height a** | (target 2/ν−d) | shift 1/ν | **collapse 1/ν** | (target) | 2D (κ, a) | 2κ−1−a |
|---|-------|----------|----------|-----|-----------|--------------|------|-----------|--------|
| 2 | 8–20 | 1.074 | **1.0135±0.0016** | 1.00 | 1.81 | **0.970** | 1.00 | (0.98, 0.97) | −0.01 |
| 3 | 5–12 | 1.467 | **1.4033±0.0021** | 1.40 | 2.25 | **1.170** | 1.20 | (1.18, 1.37) | −0.01 |
| 4 | 5–10 | 1.807 | **1.7467±0.0035** | 2.00 | 2.52 | **1.447** | 1.50 | (1.47, 1.80) | **+0.14** |

All power-law fits R²≥0.9999. Pairwise drift: q=4 height drifts **up** (1.72→1.76 over n=5→10), q=4
at-g_c drifts **down** (1.83→1.80) — converging toward ~1.78 from both sides, still below 2.0.

### Calibration → q=4 (exp_130d)
- **Height estimator is accurate where the answer is known:** a/(2/ν−d) = 1.0135 (q=2), 1.0024 (q=3),
  mean **+0.8%**. So the q=4 height a = 1.747 = **12.7% below 2.0** is a *physical* deficit, not method bias.
- **Collapse recovers 1/ν** with a small, consistent undershoot: 0.970 (q=2), 0.975 (q=3), mean ×0.973.
  q=4 collapse 1/ν = 1.447 → **calibration-corrected 1.487 ≈ 1.50 ⇒ ν=2/3 CONFIRMED.**
- **Apples-to-apples (q=3 vs q=4 both on n=5..10, identical sizes & method):** q=3 height 1.399 (true
  1.40), collapse 1.185 (true 1.20); q=4 height 1.747, collapse 1.446. The method behaves identically;
  the comparison is fair.

### Two independent observables, one consistent story
- **Location scaling (collapse, log-insensitive):** 1/ν(q=4) = 1.49 ≈ 1.5 → **ν=2/3**. This is the
  external input the Sprint-129 reframing borrowed from the literature, now confirmed from our data.
  It cleanly **excludes** the q=3-like value 1/ν=1.2; q=4 is genuinely more strongly divergent.
- **Amplitude scaling (height):** a(q=4) = 1.75 < 2.0. Given ν=2/3 confirmed and Albuquerque's relation
  (a proven QCP identity), a **must** → 2.0 asymptotically, so the observed 1.75–1.81 is necessarily a
  finite-size amplitude exponent.
- **The marginal operator is directly exposed:** the Albuquerque residual 2κ−1−a is ~0 at q=2,3 (pure
  power law) but jumps to **+0.14 at q=4** — the height grows slower than the location scaling implies,
  exactly what a marginal (dilution, c=1) log does.

### Peak-SHIFT: confirmed fragile (logged negative result)
The shift exponent overshoots badly and is stable in its wrongness: 1.81 (q=2, true 1.0), 2.25 (q=3,
true 1.2), 2.52 (q=4). The χ_F peak sits anomalously close to g_c (peak scaling-variable x\* ≈ −0.2),
so the small shift |g\*−g_c| is dominated by subleading corrections at accessible sizes. **The
peak-shift method is unusable for ν here** — do not revisit. (The height and collapse, which do *not*
rely on a small difference, are the robust estimators.)

## Hostile-reviewer checklist
- **Apples to apples?** Yes — calibration and test use the same method/estimators/window; matched-range
  n=5..10 check included (§Calibration). The g_c-free **height** and full-curve **collapse** are the
  headline estimators precisely so the result does not depend on assuming g_c=1/q.
- **Non-trivial data points?** One genuinely-could-have-failed result: the collapse confirming ν=2/3 at
  q=4 (q=2,3 are known calibrations). It *did* confirm it (1/ν=1.49), and excluded 1/ν≤1.2.
- **Literature for THIS observable?** ν=2/3 (den Nijs) and 2/ν−d (Albuquerque) are established; this is a
  cross-check, **not a novelty**. The marginal-log suppression of the q=4 χ_F amplitude is consistent
  with Salas-Sokal-type multiplicative logs (and is *not* claimed as a new χ_F log measurement here).
- **Opposite claim?** None for q=4 specifically — q=4 is the textbook marginal case. (Walking is a q>4
  phenomenon.)
- **Finite-size alternative?** Everything here is finite-size and labelled so. The decisive point is that
  the **location** exponent (1/ν, log-insensitive) is already at its asymptote (1.49≈1.5) while the
  **amplitude** exponent is not — the two diverging only at q=4 is the signature, and is robust to the
  small calibration correction (raw collapse 1.45 → corrected 1.46–1.49 across choices).

## Conclusion
**Not novel — a successful hardening of the Sprint-129 reframing.** Two independent, calibrated
observables now support it from our own data: (i) the χ_F data-collapse gives 1/ν(q=4) = 1.49 ≈ 1.5
⇒ ν=2/3, the literature input the reframing relied on; (ii) the amplitude (height) exponent sits 12.7%
below 2/ν−d while being <1.3% accurate at q=2,3, and the Albuquerque residual jumps to +0.14 only at
q=4 — the marginal log made visible. The at-g_c ~1.77–1.81 is reaffirmed as a finite-size amplitude
exponent; 2/ν−d = 2 is the asymptote. Methodological nugget worth keeping: the **self-locating
peak-height** exponent is the lowest-bias accessible-size estimator of 2/ν−d (≤1.3% at q=2,3), better
than fixed-g_c (overshoots +0.07); the **peak-shift** exponent is unusable for ν.

## Next
- (Unchanged core blocker) The 2-vs-1.77 *asymptote* for the amplitude still needs L≫11; this sprint
  does not measure that directly — it confirms ν=2/3 so the asymptote is *fixed at 2 by Albuquerque*.
- Strongest remaining lever: periodic-BC χ_F at larger L (needs GPU/symmetry reduction) to watch the
  amplitude exponent climb past 1.8 toward 2 — but the logic no longer requires it.
- Reconcile the q=5 inconsistency (2.094 vs 2.139) — bookkeeping, independent of this result.
