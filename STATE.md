# Current State -- Rewrite this completely each sprint

## Last Sprint
Sprint 131 -- DATA-INTEGRITY FIX (not novel): reconciled the S_q chi_F walking exponents q=5, q=7.
Report: sprints/sprint_131.md. Data: results/sprint_131{a,b}*.json.
- **Canonical: q=5 -> 2.094+/-0.002, q=7 -> 2.636+/-0.018** (= results.db `alpha_exact`; sprint-127.md &
  CHANGELOG were already correct). KNOWLEDGE.md's 2.139 / 2.584 were stale sprint-128 alpha(q)-table
  transcriptions, reproduced by NO standard fit. Raw chi_F recomputed CPU-vs-GPU: max rel diff 4.8e-9.
- Downstream: corrected alpha(q) effective curve is **convex in ln q** (slopes 1.14,1.34,1.54,1.69 monotone
  up), super-log -- not S128's "nearly linear". NOT load-bearing (q=3,4 are finite-size effective exps;
  curve mixes regimes). DB unchanged (already canonical); only KNOWLEDGE.md was wrong.

## CRITICAL: q=4 reframing CONFIRMED (Sprint 130) -- load-bearing, unchanged
- Data collapse: 1/nu(q=4)=1.49 after q=2,3 calibration => **nu=2/3 confirmed.**
- Peak-HEIGHT exp recovers 2/nu-d to <=1.3% at q=2,3; q=4=1.747 (12.7% below 2.0) = physical marginal log.
  nu=2/3 + Albuquerque => amplitude exp **must ->2**; measured ~1.77-1.81 is finite-size.
- Peak-SHIFT exp UNUSABLE for nu (correction-dominated). Dead end, do not revisit.

## CRITICAL: Standing corrections (unchanged)
Use EXACT finite-difference / curve chi_F (spectral has negative-alpha bias, S126). g_c=1/q exact
self-dual. All sprints 076+ use the STANDARD S_q Potts model (not a novel hybrid; Apr 2026 audit).

## Active Research Thread
S_q q=4 per-site chi_F: nu=2/3 => asymptote 2/nu-d=2; finite-size effective ~1.77-1.81 (marginal log).
Remaining piece: watch amplitude exponent climb past 1.8 toward 2 at L>>11 (needs GPU).

## QPU Budget
580s remaining -- BLOCKED (~/.qiskit/qiskit-ibm.json empty).

## Top 3 Next Experiments
1. **(GPU) periodic-BC chi_F q=4 n=12-14** -- watch amplitude exp 1.8->2.0. Core blocker; CPU can't reach
   (q=4 n=12 = 16.7M). BLOCKED until CuPy/CUDA restored.
2. **CHANGELOG.md compression** (511 > 300 trigger) -- compress sprints older than last ~10. Housekeeping.
3. **results.db chi_F factor-2 convention split** -- pick one canonical normalization. Prefactor cancels
   in exponents (independent of alpha claims) => low priority / safe to defer.

## Ruled Out / Retracted
- q=5/q=7 alpha "inconsistency" RESOLVED (S131): 2.094 / 2.636 canonical; 2.139 / 2.584 stale.
- Peak-SHIFT FSS of chi_F: correction-dominated, useless for nu (S130). Dead end.
- ~~q=4 alpha=1.77 asymptotic / Salas-Sokal rejected~~ INVERTED (S129); 2 correct, 1.77 finite-size.
- exp_128c no-log extrapolation as anti-log evidence: circular (S129). Spectral chi_F primary (S126).
  iDMRG overlap for S_q (S124).

## Key Tools
chi_F curve scan/peak/collapse: experiments/collapse_utils.py (S130). Exact chi_F (periodic): q=3
n<=12(CPU)/14(GPU), q=4 n<=10(CPU)/11(GPU), q=5 n<=10(GPU). fss_utils.py, hamiltonian_utils.py,
gpu_utils.py, db_utils.py. IBM QPU 580s (credentials needed).
