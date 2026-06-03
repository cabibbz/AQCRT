# Sprint 131 — Reconciling the S_q χ_F walking exponents at q=5 and q=7

**Date:** 2026-06-02
**Thread:** Data integrity / α(q) walking curve. STATE Top-Next #1: "Reconcile q=5 alpha (2.094 vs 2.139)."
**Environment:** CPU-only (CuPy/CUDA unavailable; `gpu_utils.eigsh` → scipy fallback). Python 3.11.

## Motivation
The Sprint-129 audit flagged that the S_q q=5 χ_F exponent is recorded inconsistently:
**2.094 ± 0.002** (results.db id 1775, Sprint 127, CHANGELOG) vs **2.139 ± 0.019**
(KNOWLEDGE.md table, sprints/sprint_128.md α(q) refit). One of them is wrong and it has been sitting
in the canonical α(q) table feeding the "walking super-scaling" narrative. A reconciliation sprint is
the responsible move before any further exponent claims (hostile-reviewer "apples-to-apples" rule).

**Scope expanded after reconnaissance:** auditing the *full* α(q) table (DB vs KNOWLEDGE) revealed a
**second** mismatch of the same kind — **q=7: DB 2.636 ± 0.018 vs KNOWLEDGE/sprint128 2.584.** q=3, 4, 6
match the DB exactly. So two of the five S_q effective exponents were stale in the load-bearing table.

## Plan
1. **exp_131a** — reconcile the *fits*: reproduce the canonical `fit_power_law` on the exact χ_F series
   for q=5 (n=4,6,8,9,10) and q=7 (n=4,6,7,8); cross-check against pairwise slopes and the Sprint-128c
   asymptotic extrapolation; hunt for the origin of the stale 2.139/2.584; then **refit α(q)** with the
   corrected values and compare to the Sprint-128 fit.
2. **exp_131b** — verify the *raw data* itself: independently recompute χ_F_exact at CPU-feasible sizes
   (q=5 n=4,6,8; q=7 n=4,6,7) with scipy and confirm the stored (GPU-computed) values reproduce. This
   closes the loop: the discrepancy is purely a fit/transcription artifact, not a data artifact.

## Results

### exp_131a — fit reconciliation + α(q) refit (`results/sprint_131a_q5q7_reconcile.json`)
Reproducing the canonical `fit_power_law` (linear-space NLS) from the raw exact χ_F series confirms the
**DB is correct at every q**, and **KNOWLEDGE.md was stale at exactly two points**:

| q | sizes | refit α | DB | KNOWLEDGE (was) | status |
|---|-------|---------|-----|-----------------|--------|
| 3 | 4–14 | 1.468±0.012 | 1.468 | 1.468 | ok |
| 4 | 4–11 | 1.794±0.007 | 1.794 | 1.794 | ok |
| **5** | 4,6,8,9,10 | **2.094±0.002** | 2.094 | **2.139** | **KB STALE → fix to 2.094** |
| 6 | 4–9 | 2.375±0.006 | 2.375 | 2.375 | ok |
| **7** | 4,6,7,8 | **2.636±0.018** | 2.636 | **2.584** | **KB STALE → fix to 2.636** |

**Cross-checks (q=5):** pairwise slopes are flat — (4,6)=2.104, (6,8)=2.088, (8,9)=2.094, (9,10)=2.100;
Sprint-128c asymptotic extrapolation gave α_inf=2.093; Sprint-103 χ_F_FSS gave 2.091. Three independent
estimates cluster at **2.09**. The stale **2.139 is reproduced by NONE** of the standard fits (full/subset,
linear- or log-space all give 2.09–2.10) → it is a genuine transcription artifact, not a fit choice.

**Cross-checks (q=7):** pairwise slopes *increase* — (4,6)=2.582, (6,7)=2.631, (7,8)=2.670; full fit 2.636.
The stale **2.584 ≈ the small-size (4,6) leg** (also reproduced by a log-space fit that drops n=8) → it is a
small-size-biased value superseded by the full-series fit. Canonical = **2.636**.

**α(q) refit consequence.** The Sprint-128 fit `α(q)=1.337 ln q − 0.023 (χ²/dof=5)` and its headline
"S_q α(q) is very close to logarithmic" were fit to the two wrong points. Refitting q=3–7:
- **Stale table:** linear slope 1.335 (reproduces sprint-128); local slopes dα/d(ln q) = 1.13, 1.55, 1.29,
  1.36 — **non-monotonic/noisy**; quadratic-in-ln q does not improve the fit (χ²/dof flat at 7e-4).
- **Corrected table:** linear slope 1.375; local slopes = **1.14, 1.34, 1.54, 1.69 — monotonically
  increasing**; a quadratic in ln q fits essentially perfectly (+0.44 (ln q)² curvature, χ²/dof→0 vs
  1.8e-3 linear). I.e. the corrected effective-exponent curve is cleanly **convex / super-logarithmic**,
  not "nearly linear." The noisy near-linearity was the artifact.
- **Caveat (apples-to-apples):** q=3,4 are finite-size *effective* exponents whose asymptotes are 2/ν−d
  (q=3→1.40, q=4→2.0; Sprint 129/130), so this curve mixes the continuous-transition and walking regimes.
  The convexity is a clean statement about the *measured* effective exponents at accessible sizes, not a
  claim about asymptotic physics. Functional form of α(q) remains explicitly **not load-bearing**.

### exp_131b — raw-data verification on CPU (`results/sprint_131b_q5q7_recompute.json`)
Independently recomputed χ_F_exact (scipy, CPU) at q=5 n=4,6,8 and q=7 n=4,6,7 and compared to the stored
GPU-computed values. **Max relative difference = 4.8e-9** — the data reproduces exactly. CPU/scipy and
GPU/cupy agree, confirming the discrepancy is purely in the bookkeeping, not the computation.

## Conclusion
**Not novel — a data-integrity fix with a real downstream consequence.** The canonical S_q χ_F walking
exponents are **q=5 → 2.094 ± 0.002** and **q=7 → 2.636 ± 0.018** (matching results.db and verified raw
data); the KNOWLEDGE.md/sprint-128 values 2.139 and 2.584 were stale and are corrected. The fix turns the
α(q) effective-exponent curve from "noisy ≈ logarithmic" into cleanly **convex in ln q** (super-logarithmic,
accelerating with q) — consistent with the walking/super-scaling picture, with the standing caveat that
q≤4 are finite-size effective exponents. The DB needed no change; only KNOWLEDGE.md, STATE.md, and the
sprint-128 table reference were wrong.

## Next
- Remaining STATE bookkeeping item: results.db chi_F factor-2 convention split (choose one canonical
  normalization). Independent of exponents (prefactor cancels), low priority.
- Core physics blocker unchanged: periodic-BC χ_F at L≫11 (needs GPU) to watch the q=4 amplitude
  exponent climb 1.8→2.0. Blocked until CuPy/CUDA is restored.

