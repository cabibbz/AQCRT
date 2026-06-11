# Sprint 132 — Restore GPU compute, push q=4 per-site χ_F to the n=12 frontier

**Date:** 2026-06-02
**Thread:** q=4 S_q Potts per-site χ_F effective exponent. STATE Top-Next #1: "(GPU) periodic-BC χ_F
q=4 n=12–14 — watch amplitude exp 1.8→2.0. Core blocker; CPU can't reach (q=4 n=12 = 16.7M).
BLOCKED until CuPy/CUDA restored."
**Environment:** Windows, Python 3.11.9, NVIDIA TITAN RTX (24 GB), driver 591.74 / CUDA 13.1, nvcc 12.6.

## Motivation
The core physics blocker for ~3 sprints has been "CuPy/CUDA unavailable" — every recent sprint fell
back to CPU and could not reach the q=4 n≥12 sizes needed to watch the per-site χ_F amplitude exponent
climb from its finite-size value (~1.79–1.81 at n≤11) toward the predicted asymptote 2/ν−d = 2.0
(ν=2/3, Albuquerque density law). This sprint **restores GPU compute** and uses it to add the first
new data point past the CPU wall.

## Root cause of the GPU outage (fixed before this sprint's experiments)
`import cupy` failed with `numpy.core.multiarray failed to import` — a hard ABI mismatch:
the installed **cupy-cuda12x 14.0.1 requires numpy≥2.0,<2.6**, but the validated CPU research stack
runs **numpy 1.26.4** (scipy 1.15.3, qiskit 2.3.1, tenpy 1.1.0). The hardware/driver/toolkit were all
fine. **Surgical fix:** downgrade only the GPU package to **cupy-cuda12x 13.6.0** (supports numpy
1.22–2.x), pinning numpy==1.26.4 so the entire validated CPU stack is untouched. Zero risk to the
existing 131-sprint CPU codebase/results.

## Results

### exp_132a — GPU pipeline validation (PASS)
`gpu_utils.gpu_status()` → `GPU enabled (CuPy 13.6.0, device NVIDIA TITAN RTX)`. Recomputed the
canonical exact χ_F (chif_utils, dg=1e-4, g_c=1/q) at q=4 n=9,10,11 on GPU and compared to results.db:

| n | dim | χ_F (GPU) | DB ref | rel diff | time |
|---|-----|-----------|--------|----------|------|
| 9 | 262,144 | 56.183728 | 56.183728 | 6.3e-09 | 0.9s |
| 10 | 1,048,576 | 67.784201 | 67.784201 | 3.2e-09 | 3.0s |
| 11 | 4,194,304 | 80.310875 | 80.310875 | 3.7e-09 | 13.5s |

CPU-vs-GPU cross-check at n=9: CPU 56.18372836 vs GPU 56.18372831, **reldiff 7.9e-10**, GPU 9.2× faster.
The restored pipeline is bit-faithful to the CPU gold standard. Pre-sprint golden + db-check gates: PASS.

### exp_132b — the frontier point: q=4 n=12 (dim 16,777,216), GPU
Memory-frugal build (H_coup/H_field once, 3 ground states sequentially, GPU pool freed between solves).
Build 31.3s + 3 solves ≈ 28.5s = **59.9s total** (well under the 300s wall). GPU peak well within 24 GB.

**χ_F(q=4, n=12) = 93.747642** (overlaps 0.9999943774 / 0.9999943729). Recorded to results.db
(sprint=132, sq q=4 n=12, finite_diff). The point sits cleanly on the trend (unit-step increments
10.66, 11.60, 12.53, **13.44** with smooth, slightly-decreasing second differences 0.944, 0.927, 0.910).

Full periodic-BC series (n = 4,6,8,9,10,11,12):
`12.8393, 27.1380, 45.5278, 56.1837, 67.7842, 80.3109, 93.7476`

- **Power-law fit n=4..12:** α = **1.7900 ± 0.0056** (R²=0.9999748). (n=4..11 only: 1.7945 ± 0.0069.)
- **Pairwise local exponents — MONOTONICALLY DECREASING:**
  (4,6)=1.8458, (6,8)=1.7985, (8,9)=1.7855, (9,10)=1.7815, (10,11)=1.7792, **(11,12)=1.7779**.
- Top-3 local exponent: n=9,10,11 → **1.7803**; n=10,11,12 → **1.7785** (it went **DOWN −0.0018**, not up).

**The amplitude exponent did NOT climb toward 2.0. The local exponent is converging *downward* to
≈1.777** — the opposite of the "marginal-log → 2.0" prediction that has been load-bearing since S129/130.

### exp_132c — marginal-log falsification (model-independent + model comparison)
**Probe 1 (sign-of-trend, the decisive, non-circular one).** For any form χ = A·Nᵃ·L(N) with L slowly
varying, α_loc(N) = a + d ln L/d ln N. A marginally-**irrelevant** operator gives d ln L/d ln N ~ −c/ln N → 0⁻
(flattening), so if a=2 the local exponent must **climb** toward 2. Measured correction-slope
d ln L₂ := α_loc − 2: **−0.154, −0.202, −0.214, −0.218, −0.221, −0.222** — it is **NOT flattening to 0**
(as a marginally-irrelevant correction on a leading power 2 would require); over the accessible window
its magnitude is *growing/saturating* at ≈0.222. (We deliberately do NOT read an asymptote off the
1/ln N extrapolation: the exp_132e q=3 control shows that fit fabricates a spurious deficit even where
the truth is zero — see below. The claim is the *sign of the trend*, not a limit value.)

**Probe 2 (log-space model fits, AIC, with n=12).**

| model | k | SSR(log) | AIC | α_loc(12) | α_loc(10³) | params |
|-------|---|----------|-----|-----------|------------|--------|
| pure power | 2 | 1.9e-04 | −69.5 | 1.808 | 1.808 | a=1.808 |
| **power + 1/N** | 3 | **2.6e-06** | **−97.5** | 1.767 | 1.722 | a=**1.721**, c=−0.525 |
| leading-2 marg-log A·N²(1+b lnN)⁻ʳ | 3 | 2.0e-04 | −67.3 | 1.809 | **1.817↑** | b=0.010, r=20.1 |
| free power × (lnN)ᵖ | 3 | 3.1e-06 | −96.4 | 1.766 | 1.681 | a=1.633, p=0.33 |
| leading-2 × (lnN)ᵖ | 2 | 8.3e-04 | −59.3 | 1.856 | **1.948↑** | p=−0.36 |

AIC-best = **power+1/N, a=1.721**. Both leading-2 forms fit *worse than even 2-parameter pure power*,
and both predict an **increasing** α_loc (→2) — the opposite of the observed decrease.

### exp_132d — synthetic-recovery (closes the Sprint-129 circularity)
S129 proved a no-log χ(N) extrapolation is circular (fed true-2.0-with-logs data it returns ~1.77).
The local-exponent-trend diagnostic does NOT share that flaw, proven by recovery on known truths
generated on our exact sizes:

| pair | REAL α_loc | T_A2 (truth=2.0×marg-log) | T_pow (truth=1.721) |
|------|-----------|---------------------------|---------------------|
| (4,6) | 1.8458 | 1.7733 | 1.8425 |
| (11,12) | 1.7779 | **1.8532** | 1.7692 |
| monotonic | **decreasing** | **increasing** | decreasing |

T_A2 (leading power 2.0 × marginal-irrelevant log), **even forced through the real n=4 and n=12 χ_F
endpoints**, yields an **increasing** local-exponent sequence (1.773→1.853). The REAL data decrease
(1.846→1.778). RMS local-exp distance to the data: **0.0050** (genuine power) vs **0.0599** (a=2+log)
— a 12× discrimination. **The diagnostic correctly separates the two truths, and the data fall
unambiguously on the a<2 side.**

### exp_132e — q=3 null-convergence control (and a self-correction)
The strongest objection: "q=4's 1.78<2.0 is ordinary finite-size undershoot." Control: run the SAME
diagnostic on q=3, which has **no marginal operator** and an exact null 2/ν−d=1.40, so it MUST converge
to its null. Result (q=3 sizes n=4..14):

| q | null | α_loc trajectory | |gap to null| | relative to null |
|---|------|------------------|----------------|------------------|
| 3 | 1.40 | 1.568→1.496→1.465→1.448→**1.437** | 0.168→**0.037** (shrinking) | descends **ONTO** it |
| 4 | 2.00 | 1.846→…→**1.778** | 0.154→**0.222** (growing) | descends **AWAY** from it |

Both local exponents decrease, but **relative to their null they move oppositely**: q=3's null sits below
the data and the data descend onto it (no reversal needed); q=4's null sits above the data and the data
descend *away* from it — reaching 2.0 would require a future **reversal**, of which there is no sign.
**Self-correction this produced:** the 1/ln N gap-extrapolation returns g_∞=−0.18 for q=3 — but q=3's
TRUE deficit is 0. So that extrapolation *manufactures* a ~0.18 spurious deficit (the Sprint-129
circularity, live). We therefore **decline to quote any asymptotic q=4 exponent** and rest the result
purely on the extrapolation-free **trend direction**. (This walks back the draft "leading power ≈1.78"
phrasing; the honest claim is weaker and safer.)

## Interpretation — what changed, and what did NOT
At n≤11 (Sprint 129) the honest verdict was "the data cannot distinguish '1.78 forever' from '2 with
marginal logs'." **The n=12 frontier point breaks that symmetry by revealing the *sign* of the trend:**
the periodic-BC, fixed-g_c, per-site χ_F local exponent decreases monotonically with geometrically
shrinking decrements, moving *away* from its null 2.0 (|gap| grows 0.154→0.222), while the q=3 control
descends *onto* its null — the wrong sign for any single marginally-irrelevant (or additive 1/lnL)
correction on a leading power 2. The simplest "climbs to 2.0" story is now the **less** parsimonious
reading (it requires a reversal with no sign of one).

**This does NOT overturn the theory.** ν=2/3 (S130 data collapse, robust) + the Albuquerque density law
(2/ν−d=2, a proven identity) still predict a leading exponent of 2. So the n=12 result is a **sharpened
tension**, not a refutation:
1. The asymptote is still not directly readable — S129's circularity bars that, and a non-monotone
   multi-term correction with a turnaround at L≫12 cannot be excluded by data alone (there is no sign
   of one). At L=12, 1/ln L = 0.40 — still far from asymptopia; higher-order (ln L)⁻¹ terms are real.
2. **Cross-BC tension (must reconcile next):** open-BC DMRG (S124, n=6–20) drifts *UPWARD* (1.505→1.523),
   the opposite direction, and lands far below periodic (≈1.52 vs ≈1.78). Large BC-dependent finite-size
   effects ⇒ neither setup has reached the bulk asymptote. Periodic exact-diag is the cleaner bulk probe.

## Hostile-reviewer self-audit
- **Apples to apples?** Yes — all points are the *same* canonical estimator (per-site, factor-2,
  dg=1e-4, g_c=1/q exact self-dual), periodic BC, exact ground states, n=4..12. The only new ingredient
  is GPU at n≥9 (validated bit-faithful to CPU, reldiff 8e-10).
- **How many non-trivial data points?** The n=12 point is genuinely new (past the CPU wall). The trend
  rests on 6 pairwise slopes spanning L=4–12; the decrease is monotone and ~20× above the χ_F noise
  floor (~1e-4 in α_loc from the smooth dg-bias).
- **What does the literature predict for THIS observable?** No prior χ_F measurement at the q=4 quantum
  Potts point exists. Salas-Sokal (1997) treat the *2D classical* model's specific heat/susceptibility
  logs, not χ_F. Albuquerque (2010) give the general L^{2/ν−d} law, not the q=4 marginal case. Bethe-
  ansatz gaps scale as x + d/lnL (confirms the 1/lnL correction form I used).
- **Has anyone claimed the OPPOSITE?** Our own open-BC DMRG (S124) drifts upward — addressed above as a
  BC artifact; the periodic exact result is the cleaner bulk comparison.
- **Could finite-size effects explain it?** Partly — they certainly explain the gap between periodic and
  open BC. But the *sign* of the periodic trend (decreasing, converging below 2) is exactly the feature
  a single marginal-log on a=2 cannot produce; explaining it away needs an unobserved turnaround.

## POTENTIALLY NOVEL (hardening of an already-flagged thread)
**Result:** For the q=4 (4-state) quantum Potts chain, periodic BC, the per-site fidelity-susceptibility
density at the self-dual point g_c=1/q has an effective exponent that **decreases monotonically to
≈1.78 over L=4..12** and whose finite-size trend is the **wrong sign** for a marginally-irrelevant
log correction approaching the Albuquerque value 2/ν−d=2. A leading-power-2 marginal-log model — even
endpoint-matched — predicts an *increasing* local exponent; the data decrease.
**Scope:** holds for periodic BC, exact diag, L≤12; the true L→∞ asymptote is **deliberately not
quoted** (the q=3 control calibrates such extrapolations as unreliable) and remains in tension with the
theoretical 2 (ν=2/3 + Albuquerque). The robust claim is the *trend direction*, hardened by (i) a
synthetic-recovery proof the diagnostic is non-circular and (ii) a q=3 null-convergence control showing
q=3 descends onto its null while q=4 descends away from its.
**Extends:** the χ_F-q=4 "no prior log measurement" novelty (S128/129) with the first sub-CPU-wall data
point and a non-circular trend diagnostic. Copied to `unresolved/sprint_132.md`.

## Files
- experiments/exp_132a_gpu_validation.py, exp_132b_q4_n12_frontier.py,
  exp_132c_marginal_log_falsification.py, exp_132d_synthetic_recovery.py, exp_132e_q3_control.py
- results/sprint_132{a,b,c,d,e}*.json
- results.db: sq q=4 n=12 χ_F_exact=93.747642; alpha_exact (n=4..12)=1.7900±0.0056 (sprint 132)
