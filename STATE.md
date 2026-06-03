# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 135 -- **q=4 on-peak χ_F pushed to n=24 via DMRG; marginal-operator LOG detected in χ_F (q=3 control).**
sprints/sprint_135.md (+unpublished/); results/sprint_135{a,b,_analysis}*.json; DB chi_F_open_peak +
gstar_open (q=4 n=8..24, q=3 n=8..24), kappa_onpeak_nolog_Kinf (q4=1.70, q3=1.40), kappa_onpeak_marglog_s (q4=−1.26).
- Extended S134's **on-peak** peak-height χ_F (correct FSS observable) past the n=12 exact frontier with TeNPy
  DMRG (OPEN BC). Method validated: chi=48 converges χ_F to 1e-6 vs exact (chiconv@n=12); real-dtype ops (~6x);
  central dg=1e-3 warm-started; **forward-diff peak + dg/2 correction**. DMRG ≡ S134 exact on-peak to ≤0.06% (n=8,10,12).
- **q=4 OPEN on-peak κ_eff ASCENDS MONOTONICALLY 0.66→1.49 (n=4..24)** — no plateau/turnover, joins exact seamlessly.
- **q=3 CONTROL (null 1.40) VALIDATES:** no-log surface fit κ=K+d/L recovers K=**1.401** (exact null, R²=1.0);
  fixed-null log coeff s=**+0.003** (zero) — q3 needs no log.
- **q=4 same fits ⇒ LOG present:** no-log κ=K+d/L → K=**1.70** (undershoots 2.0 = the finite-size effective exp);
  fixed-null 2.0+s/lnL+d/L → s=**−1.26** (max|resid|=0.02, consistent w/ proven 2.0). Marginal-op log seen in χ_F:
  present q=4 (s≈−1.2), absent q=3 (s≈0) = the Cardy(1986)/Hamer(1988) 1/lnL gap correction, now in χ_F.

## CRITICAL: standing framework (unchanged)
- ν(q=4)=2/3 CONFIRMED (S130) + Albuquerque 2/ν−d=2 (proven) ⇒ leading exp **2.0**. Golden gate enforces this.
- On-peak peak-height is THE observable (not fixed-g_c). For OPEN BC, κ_eff also carries a **surface 1/L term**
  on top of the marginal log ⇒ naive 1/lnL extrapolation OVERSHOOTS (q3 control → 1.96, not 1.4): NEVER quote an
  open-BC 1/lnL intercept as the asymptote. Reliable: proven-null-fixed fits + the no-log control fit.

## Active Research Thread
q=4 per-site χ_F asymptote. Direction = 2.0 (proven + flow confirmed both BC, S134); marginal-operator log now
DETECTED in χ_F and isolated from the q=3 (no-log) control (S135). **Asymptote still NOT numerically pinned at
L≤24** — the marginal log is intrinsically slow and the open surface term blocks a clean extrapolation.

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty). ~90+ sprints unused. Strongest sim
prediction for HW: q=2 Ising χ_F at g_c on 5-10 qubits. Needs credentials restored.

## Top 3 Next Experiments
1. **The thread is near-closed; consider PIVOTING.** The q=4 χ_F story is now: direction=2.0 (proven+confirmed),
   marginal log detected, asymptote unpinnable at accessible L (slow log + open surface). Pinning would need
   PERIODIC BC past n=12 (no surface term) -- but TeNPy finite-periodic DMRG is poorly supported; or L≫24 open
   (DMRG cost grew steeply: n=24 cold solve ~190s). Low ROI. Recommend declaring the q=4 χ_F thread CLOSED
   (answer 2.0, log measured) and moving to a NEW direction.
2. **If continuing q=4:** second on-peak observable (peak CURVATURE ~L^{2/ν−d}) as an independent cross-check at
   n≤12 exact; cheap. Or try a non-Hermitian / different-model χ_F marginal-log to generalize the S135 finding.
3. **CHANGELOG.md compression** (~465 > 300). Compress sprints older than last ~10 to one-liners. Housekeeping (overdue).

## Ruled Out / Retracted
- **Naive 1/lnL extrapolation of OPEN-BC κ_eff** -- UNRELIABLE (S135 q=3 control overshoots to 1.96 vs true 1.4;
  q=4 gives 2.3-2.5). Free 3-param κ=K+s/lnL+d/L also overshoots. Use proven-null-fixed + no-log-control fits only.
- S133 "open κ_eff non-monotonic", S132 "periodic descends AWAY from 2.0" -- both fixed-g_c off-peak artifacts (S134).
- n=13 (q=4, 67M) exact-diag infeasible (>24GB GPU). Finite-periodic DMRG not pursued (TeNPy support poor).
- DMRG on-peak past ~n=24 (q=4): cold solves ~190s+ at the near-degenerate ordered-side peak; diminishing returns.

## Key Tools
GPU: `from gpu_utils import eigsh`. chif_utils.chi_F_exact (canonical FIXED g). DMRG on-peak: exp_135a (q=4) /
exp_135b (q=3) -- SqPottsChain real-dtype, warm-start, chi=48 svd=1e-8 dg=1e-3, forward-scan + dg/2 correction;
validated vs exact to ≤0.06%. exp_135_analysis (surface-corrected κ_eff fits). exp_134a (exact on-peak n≤12).
db_utils, fss_utils, hamiltonian_utils (`_decode_states`,`_build_field`; open=drop wrap bond). Pre-sprint BLOCKING
gates: experiments/test_golden.py + experiments/db_check.py. python = system Python311 (NOT ~/quantum-env).
