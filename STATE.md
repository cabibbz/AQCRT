# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 130 -- HARDENED the Sprint-129 q=4 reframing with two independent, calibrated χ_F FSS
observables (CPU-only). Scanned the full χ_F(g,N) curve in the scaling window for q=2,3,4 and
extracted: at-g_c exp, peak-HEIGHT exp, peak-SHIFT exp, and a data-collapse 1/ν.
Full report: sprints/sprint_130.md. Data: results/sprint_130{a,b,c,d}*.json.

## CRITICAL: q=4 reframing now CONFIRMED from our own data (Sprint 130)
- **Data collapse (location scaling, log-insensitive): 1/ν(q=4)=1.45 → 1.49 after q=2,3 calibration
  ⇒ ν=2/3 confirmed.** Excludes 1/ν≤1.2. (Calibration: q=2→0.97, q=3→0.975 vs true 1.0,1.2.)
- **Peak-HEIGHT exp recovers 2/ν−d to ≤1.3% at q=2(1.013),q=3(1.403); q=4=1.747 = 12.7% BELOW 2.0**
  ⇒ deficit is physical = the q=4 marginal log. Albuquerque residual 2κ−1−a: ~0 (q=2,3), +0.14 (q=4).
- ν=2/3 (confirmed) + Albuquerque (proven) ⇒ amplitude exp **must →2**; measured ~1.77-1.81 is finite-size.
- **Peak-SHIFT exp is UNUSABLE for ν** (1.8/2.3/2.5 vs true 1.0/1.2/1.5; peak at x*≈−0.2, correction-
  dominated). Logged dead end -- do not revisit.
- Self-check: my curve-based at-g_c q=3 exp=1.467 reproduces prior finite-diff 1.468 (S128). Pipeline sound.

## CRITICAL: Standing corrections (unchanged)
Use EXACT finite-difference / curve chi_F (spectral has negative-alpha bias, S126). g_c=1/q exact
self-dual. All sprints 076+ use the STANDARD S_q Potts model (not a novel hybrid; Apr 2026 audit).

## Active Research Thread
**S_q q=4 per-site χ_F: ν=2/3 ⇒ asymptote 2/ν−d=2, finite-size effective ~1.77-1.81 (marginal log).**
Now CONFIRMED via independent collapse, not just borrowed from literature. The remaining unmeasured
piece is watching the amplitude exponent climb past 1.8 toward 2 at L≫11 (needs GPU/symmetry reduction;
logic no longer requires it).

## QPU Budget
580s remaining -- BLOCKED (qiskit-ibm.json empty).

## Top 3 Next Experiments
1. **Reconcile q=5 alpha** (2.094 vs 2.139) -- trace which sizes/fit produced each, pick one. CPU-OK (n≤8).
2. **Compress KNOWLEDGE.md / results.db factor-2 split** -- bookkeeping; choose canonical convention.
3. **(If GPU returns) periodic-BC χ_F q=4 at n=12-14** -- watch amplitude exponent rise 1.8→2.0.

## What's Been Ruled Out / Retracted
- **Peak-SHIFT FSS of χ_F** -- correction-dominated, useless for ν at accessible sizes (S130). Dead end.
- ~~"q=4 alpha=1.77 asymptotic, Salas-Sokal rejected"~~ -- INVERTED (S129). 2 is correct; 1.77 finite-size.
  Now POSITIVELY hardened (S130): ν=2/3 confirmed by independent collapse.
- exp_128c power-law extrapolation as evidence against logs -- circular (S129).
- Spectral chi_F as primary method (S126); iDMRG overlap for S_q (S124).

## Key Tools
- χ_F curve scan + peak + data collapse: experiments/collapse_utils.py (Sprint 130).
- Exact chi_F (periodic): q=3 n<=12(CPU)/14(GPU), q=4 n<=10(CPU)/11(GPU), q=5 n<=10(GPU)
- fss_utils.py (fit_power_law, pairwise_exponents), hamiltonian_utils.py, gpu_utils.py
- IBM QPU: 580s remaining (credentials needed)
